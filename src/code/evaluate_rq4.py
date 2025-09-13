import os
from evaluate import pass_rate_single_round


def evaluate_rq4_prompt_files(dataset):
    """
    评估 rq4-prompt 目录下所有文件的得分

    Args:
        dataset (str): 数据集名称，如 "HumanEval" 或 "CoderEval"
    """
    # rq4-prompt 目录路径
    rq4_prompt_dir = "results/rq4-prompt"

    # 检查目录是否存在
    if not os.path.exists(rq4_prompt_dir):
        print(f"目录 {rq4_prompt_dir} 不存在")
        return

    # 遍历目录中的所有 .jsonl 文件
    for filename in os.listdir(rq4_prompt_dir):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(rq4_prompt_dir, filename)
            print(f"\n开始评估文件: {filename}")
            try:
                # 调用 pass_rate_single_round 函数评估得分
                pass_rate_single_round(file_path, dataset)
            except Exception as e:
                print(f"评估文件 {filename} 时出错: {e}")


if __name__ == "__main__":
    # 请根据实际情况设置数据集名称
    dataset_name = "CoderEval"  # 或 "CoderEval"
    evaluate_rq4_prompt_files(dataset_name)
