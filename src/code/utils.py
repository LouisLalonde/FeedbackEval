import json
import random
import re
import importlib

api_key = ""
FEEDBACK_TYPES = ["test_feedback", "compiler_feedback", "human_feedback", "simple_feedback"]
MODELS = {
    "GPT": "gpt-4o-2024-11-20",
    "Claude": "claude-3-5-sonnet-20241022",
    "Gemini": "gemini-1.5-pro",
    "GLM": "glm-4-plus",
    "Qwen": "qwen2.5-72b-instruct"
}


class DataLoader:
    def __init__(self, file_path, sample_size=-1):
        self.file_path = file_path
        self.sample_size = sample_size
        self.data = self._load_data()

    def _load_data(self):
        if "HumanEval" in self.file_path:
            return self._load_human_eval()
        elif "CoderEval" in self.file_path:
            return self._load_coder_eval()
        else:
            raise ValueError("Invalid file path")

    def _load_human_eval(self):
        data_list = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                json_data = json.loads(line.strip())
                data_list.append(json_data)
        if self.sample_size == -1:
            return data_list
        return random.sample(data_list, self.sample_size)

    def _load_coder_eval(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if self.sample_size == -1:
            return data['RECORDS']
        return random.sample(data['RECORDS'], self.sample_size)


def read_jsonl(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_data = json.loads(line.strip())
            data_list.append(json_data)
    return data_list


def write_jsonl(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            json_line = json.dumps(item, ensure_ascii=False)
            file.write(json_line + '\n')


def gen_solution(model_name, model_version, prompt):
    try:
        model_class = getattr(importlib.import_module(f"src.model.{model_name}"), model_name)
        llm = model_class(api_key, model_version, prompt)
        generate_result = llm.generation()

        match = re.search(r"```python\s*(.*?)\s*```", generate_result, re.DOTALL)
        if match:
            solution = match.group(1).strip()
            return solution
        else:
            raise ValueError("No Python code block found in the generated result.")

    except Exception as e:
        print(f"Error during code generation: {e}")
