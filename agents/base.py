from llm.base import BaseLLM

class BaseAgent:
    def __init__(self, llm: BaseLLM, system_prompt: str):
        self.llm = llm
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def run(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        response = self.llm.chat(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        self.history = [{"role": "system", "content": self.system_prompt}]