from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from agents.tools import tools
from llm.factory import LLMFactory

class Orchestrator:
    def __init__(self, provider: str = "ollama", model_name: str = None):
        self.llm = LLMFactory.get_llm(provider, model_name)
        self.memory = InMemorySaver()
        
        self.system_prompt = """
        You are Cortex, a helpful and expert AI assistant specialized in code intelligence.
        
        Guidelines:
        1. Always use your tools to provide accurate answers about the codebase.
        2. Respond naturally and politely to greetings.
        3. When asked about a file or folder, start with `read_file` or `list_files`.
        4. If you are looking for specific logic or code snippets, use `search_code()`.
        5. If you don't find the requested information, be honest and suggest alternatives.
        6. Synthesize code snippets into clear explanations.
        """
        
        # In this version of LangChain, create_agent handles the loop
        # We add more explicit instructions for local models like Qwen
        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=self.system_prompt,
            checkpointer=self.memory,
            debug= True
        )

    def ask(self, query: str, thread_id: str = "default"):
        # The agent expects a 'messages' list
        inputs = {"messages": [HumanMessage(content=query)]}
        config = {"configurable": {"thread_id": thread_id}}
        
        response = self.agent.invoke(inputs, config=config)
        
        # The response is typically a list of messages, the last one being the answer
        return response["messages"][-1].content
