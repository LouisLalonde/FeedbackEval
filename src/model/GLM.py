from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from src.code.utils import base_url


class GLM:
    def __init__(
            self,
            api_key: str,
            model_name: str,
            content: str
    ):
        self.client = OpenAI(
            api_key="",
            base_url=base_url,
        )
        self.model_name = model_name
        self.content = content

    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
    def generation(self, temperature=0.3):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": self.content
                }
            ],
            temperature=temperature
        )
        if response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            raise ValueError("Empty response from API")
