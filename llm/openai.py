import os
import requests
from .base import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self, model="gpt-4o", api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.url = "https://api.openai.com/v1/chat/completions"

    def chat(self, messages: list[dict]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to OpenAI: {str(e)}"