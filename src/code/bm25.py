import os
import json
import re
from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# 全局变量用于缓存数据和BM25实例
_test_missing_data = None
_bm25_instance = None


def preprocess_text(text):
    """预处理文本，用于BM25匹配"""
    if not text:
        return []

    # 转换为小写并移除特殊字符
    text = re.sub(r"[^\w\s]", " ", text.lower())

    try:
        # 使用NLTK进行分词
        tokens = word_tokenize(text)
        # 移除停用词
        stop_words = set(stopwords.words("english"))
        tokens = [
            token for token in tokens if token not in stop_words and len(token) > 1
        ]
        return tokens
    except:
        # 如果NLTK数据不可用，使用简单的空格分割
        return text.split()


def load_test_missing_data(dataset):
    """加载test_missing数据并初始化BM25"""
    global _test_missing_data, _bm25_instance

    if _test_missing_data is not None:
        return _test_missing_data, _bm25_instance

    # 构建数据文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(
        project_root, "dataset", dataset, f"{dataset}_feedback_test_missing.jsonl"
    )

    if not os.path.exists(data_path):
        return [], None

    # 读取数据
    data = []
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except:
                continue

    if not data:
        return [], None

    # 构建用于BM25的文档集合
    documents = []
    for item in data:
        # 合并docstring和oracle_context作为搜索内容
        doc_text = ""
        if item["false_results"]:
            false_result = item["false_results"][0]
            doc_text += false_result.get("generate_code", "")

        documents.append(preprocess_text(doc_text))

    # 初始化BM25
    bm25 = BM25Okapi(documents) if documents else None

    _test_missing_data = data
    _bm25_instance = bm25

    return data, bm25


def find_best_example(current_task, dataset="CoderEval"):
    """使用BM25找到最相似的示例"""
    data, bm25 = load_test_missing_data(dataset)

    if not data or bm25 is None:
        return None

    # 构建当前任务的查询文本
    query_text = ""
    if current_task["false_results"]:
        false_result = current_task["false_results"][0]
        query_text += false_result.get("generate_code", "")

    if not query_text.strip():
        return None

    # 预处理查询文本
    query_tokens = preprocess_text(query_text)
    if not query_tokens:
        return None

    # 使用BM25计算相似度分数
    scores = bm25.get_scores(query_tokens)
    best_idx = scores.argmax()

    # 返回最相似的示例
    best_example = data[best_idx]

    # 选择第一个false_result作为示例
    if best_example.get("false_results"):
        false_result = best_example["false_results"][0]
        return {
            "erroneous_code": false_result.get("generate_code", ""),
            "feedback": false_result.get("test_feedback", ""),
            "fixed_code": best_example.get("correct_code", ""),
        }

    return None

