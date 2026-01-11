from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass
