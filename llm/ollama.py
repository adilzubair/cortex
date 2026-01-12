import requests
from .base import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model="qwen2.5-coder:7b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = f"{base_url}/api/chat"

    def chat(self, messages: list[dict]) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"