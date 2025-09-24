import json
import random
import re
import importlib
import logging
import os
from datetime import datetime

api_key = ""
base_url = ""
FEEDBACK_TYPES = ["test_feedback", "compiler_feedback", "llm_skilled_feedback", "llm_expert_feedback", "minimal_feedback", "mixed_feedback"]
MODELS = {
    "GPT": "gpt-4o-2024-11-20",
    "Claude": "claude-3-5-sonnet-20241022",
    "Deepseek": "deepseek-r1-250528",
    "GLM": "glm-4-plus",
    "Qwen": "qwen2.5-72b-instruct"
}


def setup_logging(dataset, module_name, version=None, feedback=None, function=None):
    """General logging setup function.

    Args:
        dataset: Dataset name
        module_name: Module name (evaluate/feedback)
        version: Model version (optional, for evaluate)
        feedback: Feedback type (optional, for evaluate)
        function: Function name (optional, for evaluate)
    """
    # Determine log directory based on module name
    if module_name == 'feedback':
        log_dir = f"logs/{dataset}/feedback"
    else:  # evaluate or other modules
        log_dir = f"logs/{dataset}/{function}/{version}/{feedback}"
    
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/{timestamp}.log"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
        ],
        force=True
    )

    logger = logging.getLogger(module_name)
    return logger


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


def get_model_response(model_name, model_version, prompt):
    try:
        model_class = getattr(
            importlib.import_module(f"src.model.{model_name}"), model_name
        )
        llm = model_class(model_version, prompt)
        generate_result = llm.generation()
        return generate_result

    except Exception as e:
        print(f"Error during code generation: {e}")

def extract_repaired_code(generated_text):
    try:
        match = re.search(r"<repaired_code>(.*?)</repaired_code>", generated_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("No code found between <repaired_code> tags in the generated result.")
    except Exception as e:
        print(f"Error extracting repaired code: {e}")