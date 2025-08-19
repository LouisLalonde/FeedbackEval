from src.code.utils import write_jsonl
from utils import read_jsonl
import json
data_list = read_jsonl("D:\pythonProjects\Feedback\dataset\HumanEval\HumanEval_feedback.jsonl")
gt_list = read_jsonl("D:\pythonProjects\Feedback\input\HumanEval.jsonl")
gt_dict = {gt["task_id"]: gt for gt in gt_list}
for data in data_list:
    gt = gt_dict[data["task_id"]]
    data["correct_code"] = f"{gt['prompt']}\n{gt['canonical_solution']}"

write_jsonl("D:\pythonProjects\Feedback\dataset\HumanEval\HumanEval_feedback.jsonl", data_list)