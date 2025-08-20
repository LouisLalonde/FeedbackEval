import random
from utils import read_jsonl, write_jsonl


def sample_false_results(input_file, output_file, seed=None):
    """
    从JSONL文件的每一项的false_results中采样一个，作为测试的子集

    Args:
        input_file (str): 输入JSONL文件路径
        output_file (str): 输出JSONL文件路径
        seed (int, optional): 随机种子，用于结果可重现
    """
    if seed is not None:
        random.seed(seed)

    # 读取数据
    data_list = read_jsonl(input_file)

    # 为每个条目采样一个false_result
    sampled_data = []
    for data in data_list:
        if "false_results" in data and data["false_results"]:
            false_results = []
            # 从false_results中随机选择一个
            sampled_false_result = random.choice(data["false_results"])
            false_results.append(sampled_false_result)

            # 创建新的数据项，包含采样的false_result
            new_data = {
                "task_id": data["task_id"],
                "false_results": false_results,
                "test": data.get("test", ""),
                "correct_code": data.get("correct_code", "")
            }
            sampled_data.append(new_data)
        else:
            # 如果没有false_results，保留原始数据结构
            sampled_data.append({
                "task_id": data["task_id"],
                "sampled_false_result": None,
                "test": data.get("test", ""),
                "correct_code": data.get("correct_code", "")
            })

    # 写入采样后的数据
    write_jsonl(output_file, sampled_data)
    print(f"采样完成，共处理 {len(sampled_data)} 项数据")


# 使用示例
if __name__ == "__main__":
    input_file = r"D:\pythonProjects\Feedback\dataset\HumanEval\HumanEval_feedback.jsonl"
    output_file = r"D:\pythonProjects\Feedback\dataset\HumanEval\HumanEval_feedback_test.jsonl"

    sample_false_results(input_file, output_file, seed=42)
