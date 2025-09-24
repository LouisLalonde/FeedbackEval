import sys
import os
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from src.code.utils import api_key, base_url

class Deepseek:
    def __init__(self, model_name: str, content: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model_name = model_name
        self.content = content

    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
    def generation(self, temperature=0.3):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": self.content}],
            temperature=temperature,
        )
        if response.choices[0].message.content:
            output = response.choices[0].message.content
            return output
        else:
            raise ValueError("Empty response from API")


if __name__ == "__main__":
    gpt = Deepseek(
        model_name="deepseek-r1-250528",
        content="Hello, how are you?",
    )
    response = gpt.generation()
    print(response)
