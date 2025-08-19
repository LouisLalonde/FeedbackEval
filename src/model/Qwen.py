from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt


class Qwen:
    def __init__(
            self,
            api_key: str,
            model_name: str,
            content: str
    ):
        self.client = OpenAI(
            api_key="sk-wTgnnvK6VypulivVXfhGULEQUd9gziz4mvAQaWL8jtjdCiOH",
            base_url="https://api.agicto.cn/v1",
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

if __name__ == "__main__":
    gpt = Qwen(
        api_key="sk-wTgnnvK6VypulivVXfhGULEQUd9gziz4mvAQaWL8jtjdCiOH",
        model_name="qwen2.5-72b-instruct",
        content="Hello, how are you?",
    )
    response = gpt.generation()
    print(response)