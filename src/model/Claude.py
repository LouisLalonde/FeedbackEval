import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tenacity import retry, wait_random_exponential, stop_after_attempt
from src.code.utils import api_key
from anthropic import Anthropic


class Claude:
    def __init__(
            self,
            model_name: str,
            content: str
    ):
        self.client = Anthropic(
            api_key=api_key
        )
        self.model_name = model_name
        self.content = content

    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
    def generation(self, temperature=0.3, max_tokens=1024):
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": self.content
                }
            ],
            temperature=temperature
        )
        # The response structure may differ depending on SDK version
        # Try to access the content safely
        try:
            return response.content[0].text
        except (AttributeError, IndexError, KeyError):
            raise ValueError("Empty or unexpected response from API")


if __name__ == "__main__":
    gpt = Claude(
        model_name="claude-3-5-sonnet-20241022",
        content="Hello, how are you?",
    )
    response = gpt.generation()
    print(response)
