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
        You are Cortex, a professional and proactive AI software engineering assistant.
        
        CRITICAL OPERATING DIRECTIVE:
        1. You have ZERO prior knowledge of the user's codebase. You MUST call tools to see any code.
        2. For any technical request (e.g., "explain the code", "find X"), your VERY FIRST response MUST be a tool call.
        3. DO NOT ask for permission to use a tool. Use it immediately.
        4. If you don't know where to start, call `list_files(".")` first.
        5. Once you have tool results, synthesize them into a clear explanation.
        
        Conversational Style:
        - Greetings (Hi/Hello): Respond warmly and ask how you can help.
        - Technical Queries: Skip the "I'd like to help, should I search?" fluff. Just search.
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
