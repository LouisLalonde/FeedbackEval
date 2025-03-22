from src.model.GPT import GPT
import re
from utils import DataLoader, write_jsonl, api_key
from tqdm import tqdm
from template import build_mutant_prompt


def generate_false_results(llm, attempts=3):
    """Generate false results using the LLM."""
    false_results = []
    for _ in range(attempts):
        result = llm.generation()
        try:
            match = re.search(r'```python\n(.*?)```', result, re.DOTALL)
            extracted_code = match.group(1).strip()
            false_results.append({
                "source": "llm-based",
                "generate_code": extracted_code
            })
        except Exception as e:
            print(f"error:{e}")
            continue
    return false_results


class Generator:
    def __init__(self, file_path, sample_size=-1):
        self.file_path = file_path
        self.sample_size = sample_size
        self.original_data = DataLoader(self.file_path, self.sample_size).data

    def generate_mutants(self):
        output_path = ""
        mut_list = []

        if "HumanEval" in self.file_path:
            for data in tqdm(self.original_data, total=len(self.original_data), desc="Generating Mutants"):
                ori_code = f"{data['prompt']}\n{data['canonical_solution']}"
                output_path = f"../../output/human_eval/llm_mutants.jsonl"
                prompt = build_mutant_prompt(ori_code)
                llm = GPT(api_key, "gpt-4o-mini", prompt)
                false_results = generate_false_results(llm)
                mut_list.append({
                    "task_id": data["task_id"],
                    "false_results": false_results,
                    "test": f"{data['test']}\ncheck({data['entry_point']})"
                })
        elif "CoderEval" in self.file_path:
            for data in tqdm(self.original_data, total=len(self.original_data), desc="Generating Mutants"):
                ori_code = data['code']
                output_path = f"../../output/coder_eval/llm_mutants.jsonl"
                prompt = build_mutant_prompt(ori_code)
                llm = GPT(api_key, "gpt-4o-mini", prompt)
                false_results = generate_false_results(llm)
                mut_list.append({
                    "_id": data["_id"],
                    "false_results": false_results
                })
        else:
            raise ValueError("Invalid file path.")

        write_jsonl(output_path, mut_list)


if __name__ == "__main__":
    # generator = Generator(f'../input/CoderEval4Python.json')
    generator = Generator(f'../../input/HumanEval.jsonl')
    generator.generate_mutants()
