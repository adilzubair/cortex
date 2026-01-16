import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from typing import Union

class LLMFactory:
    @staticmethod
    def get_llm(provider: str = "ollama", model_name: str = None) -> Union[ChatOpenAI, ChatOllama]:
        if provider == "openai":
            return ChatOpenAI(
                model=model_name or "gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0  # Critical for consistent tool calling
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model_name or "ministral-3:3b",
                base_url="http://localhost:11434",
                temperature=0
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
