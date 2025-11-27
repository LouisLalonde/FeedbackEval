from src.model.GPT import GPT
import logging
import argparse
from tqdm import tqdm
from feedback import run_test, run_pylint
import os
from collections import defaultdict
from utils import (
    FEEDBACK_TYPES,
    read_jsonl,
    write_jsonl,
    get_model_response,
    extract_repaired_code,
    setup_logging,
)
from template import build_gpt_prompt, build_gpt_gt_prompt, build_repair_prompt


def single_round_fix_code(
    file_path,
    model_name,
    model_version,
    feedback,
    dataset,
    use_docstring,
    use_context,
    use_persona,
    use_cot,
    use_few_shot,
    use_instructions,
    use_es_shot,
    use_sa,
    use_sg_icl,
    use_sbp,
    use_rr,
):
    print(f"Evaluating file: {file_path}")
    fixed_list = []
    ques_list = read_jsonl(file_path)

    for ques in tqdm(ques_list, total=len(ques_list), desc="Fixing code"):
        fixed_results = []
        list_results = ques["false_results"]
        for result in list_results:
            if feedback == "mixed_feedback":
                raise NotImplementedError("Mixed feedback is not supported.")
            else:
                actual_feedback = result[feedback]
            prompt = build_repair_prompt(
                solution=result["generate_code"],
                feedback=actual_feedback,
                docstring=ques.get("docstring", None) if use_docstring else None,
                context=ques.get("oracle_context", None) if use_context else None,
                current_task=ques,  
                dataset=dataset,  
                is_persona=use_persona,
                is_cot=use_cot,
                is_few_shot=use_few_shot,
                is_instructions=use_instructions,
                is_es_shot=use_es_shot,
                is_sa=use_sa,
                is_sg_icl=use_sg_icl,
                is_sbp=use_sbp,
                is_rr=use_rr,
            )
            logger.info(
                f"Model：{model_name}，Feedback：{feedback}，Task：{ques['_id']}，prompt: \n{prompt}\n"
            )
            response = get_model_response(model_name, model_version, prompt)
            fixed_code = extract_repaired_code(response)
            logger.info(
                f"Model：{model_name}，Feedback：{feedback}，Task：{ques['_id']}，response: \n{response}\n"
            )
            fixed_results.append(
                {
                    "source": result["source"],
                    "false_code": result["generate_code"],
                    "fixed_code": fixed_code,
                }
            )

        if dataset == "HumanEval":
            fixed_list.append(
                {
                    "_id": ques["_id"],
                    "fixed_results": fixed_results,
                    "test": ques["test"],
                    "correct_code": ques["correct_code"],
                }
            )
        elif dataset == "CoderEval":
            fixed_list.append(
                {
                    "_id": ques["_id"],
                    "fixed_results": fixed_results,
                    "level": ques["level"],
                    "oracle_context": ques["oracle_context"],
                    "docstring": ques["docstring"],
                    "correct_code": ques["correct_code"],
                }
            )
        else:
            raise ValueError(f"Invalid dataset: {dataset}")

    
    if all([use_docstring, use_context, use_persona, use_instructions]) and not any(
        [use_cot, use_few_shot, use_sa, use_sg_icl, use_sbp, use_rr, use_es_shot]
    ):
        save_dir = os.path.join("..", "..", "results", model_name, dataset, f"single")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{model_version}_{feedback}.jsonl")
    else:
        save_dir = os.path.join("..", "..", "results", "rq4-prompt")
        os.makedirs(save_dir, exist_ok=True)
        config_suffix = (
            f"doc_{int(use_docstring)}_ctx_{int(use_context)}_"
            f"per_{int(use_persona)}_cot_{int(use_cot)}_shot_"
            f"{int(use_few_shot)}_ins_{int(use_instructions)}_sa_{int(use_sa)}_sg_{int(use_sg_icl)}"
            f"_sbp_{int(use_sbp)}_rr_{int(use_rr)}_es_{int(use_es_shot)}"
        )
        print(config_suffix)
        save_path = os.path.join(
            save_dir, f"{model_version}_{feedback}_{config_suffix}.jsonl"
        )
    write_jsonl(save_path, fixed_list)
    print(f"File saved to: {save_path}")

def pass_rate_single_round(input_path, dataset):
    num_accept, num_tot = 0, 0
    print(f"Calculating score for {input_path}")
    eval_data = read_jsonl(input_path)

    for data in tqdm(eval_data, total=len(eval_data), desc="Calculating score"):
        for result in data["fixed_results"]:
            fixed_code = result["fixed_code"]
            if fixed_code:
                num_tot += 1
                if "isTrue" in result:
                    num_accept += result["isTrue"]
                else:
                    exit_code, test_feedback = run_test(
                        dataset,
                        fixed_code,
                        data.get("_id", None),
                        data.get("test", None),
                    )
                    result["isTrue"] = exit_code in (0, 5)
                    if exit_code not in (0, 5):
                        result["test_feedback"] = test_feedback
                    num_accept += result["isTrue"]

    write_jsonl(input_path, eval_data)
    print(f"Score: {num_accept / num_tot * 100:.2f}, {num_accept}/{num_tot}")


def pass_rate_multi_round(input_path):
    pass_rate_per_round = defaultdict(int)
    total = 0
    print(f"Evaluating file:{input_path}")
    eval_data = read_jsonl(input_path)

    for ques in eval_data:
        for result in ques["repair_results"]:
            if all(record["generate_code"] for record in result["repair_history"]):
                total += 1
            for record in result["repair_history"]:
                if record["round"] not in pass_rate_per_round:
                    pass_rate_per_round[record["round"]] = 0
                if record["isTrue"]:
                    pass_rate_per_round[record["round"]] += 1

    sorted_rounds = sorted(pass_rate_per_round.keys())
    cumulative_passed = 0

    for round_num in sorted_rounds:
        cumulative_passed += pass_rate_per_round[round_num]
        pass_rate = cumulative_passed / total if total > 0 else 0
        print(
            f"Round {round_num}: Pass rate = {pass_rate:.2%}, {cumulative_passed}/{total}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, help="CoderEval or HumanEval")
    parser.add_argument("--model", type=str, required=True, help="Model name")
    parser.add_argument("--version", type=str, required=True, help="Model version")
    parser.add_argument(
        "--feedback",
        type=str,
        required=True,
        choices=FEEDBACK_TYPES,
        help="Type of feedback",
    )
    parser.add_argument(
        "--function",
        type=str,
        required=True,
        choices=["single_fix", "single_score", "multi_fix", "multi_score"],
        help="Function to run",
    )
    parser.add_argument(
        "--no_docstring", action="store_false", help="Whether to use docstring"
    )
    parser.add_argument(
        "--no_context", action="store_false", help="Whether to use context"
    )
    parser.add_argument(
        "--no_persona", action="store_false", help="Whether to use persona"
    )
    parser.add_argument(
        "--is_cot", action="store_true", help="Whether to use chain of thought"
    )
    parser.add_argument(
        "--is_few_shot", action="store_true", help="Whether to use few-shot"
    )
    parser.add_argument(
        "--no_instructions", action="store_false", help="Whether to use instructions"
    )
    parser.add_argument("--is_es_shot", action="store_true", help="Whether to use ES-Shot")
    parser.add_argument("--is_sa", action="store_true", help="Whether to use SA")
    parser.add_argument(
        "--is_sg_icl", action="store_true", help="Whether to use SG-ICL"
    )
    parser.add_argument("--is_sbp", action="store_true", help="Whether to use SBP")
    parser.add_argument("--is_rr", action="store_true", help="Whether to use RR")
    args = parser.parse_args()

    global logger
    logger = setup_logging(
        args.dataset, "evaluate", args.version, args.feedback, args.function
    )

    if args.function == "single_fix":
        input_path = os.path.abspath(os.path.join(
            "../../dataset", args.dataset, f"{args.dataset}_feedback_test.jsonl"
        ))
        single_round_fix_code(
            input_path,
            args.model,
            args.version,
            args.feedback,
            args.dataset,
            args.no_docstring,
            args.no_context,
            args.no_persona,
            args.is_cot,
            args.is_few_shot,
            args.no_instructions,
            args.is_es_shot,
            args.is_sa,
            args.is_sg_icl,
            args.is_sbp,
            args.is_rr,
        )
    elif args.function == "single_score":
        input_path = os.path.abspath(os.path.join(
            "../../results",
            args.model,
            args.dataset,
            "single",
            f"{args.version}_{args.feedback}.jsonl",
        ))
        pass_rate_single_round(input_path, args.dataset)
    elif args.function == "multi_fix":
        raise NotImplementedError("Multi-fix function is not supported.")
    elif args.function == "multi_score":
        raise NotImplementedError("Multi-score function is not supported.")


if __name__ == "__main__":
    main()
