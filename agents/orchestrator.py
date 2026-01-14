"""
Deep Agent Orchestrator - Main orchestrator using the deepagents multi-agent system.

This module implements a supervisor architecture where the main orchestrator
delegates to specialized sub-agents for planning, exploration, building, and general tasks.
"""

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from agents.tools import ProjectTools
from agents.subagents.planner import get_planner_config
from agents.subagents.explorer import get_explorer_config
from agents.subagents.builder import get_builder_config
from agents.subagents.general import get_general_config
from llm.factory import LLMFactory


ORCHESTRATOR_SYSTEM_PROMPT = """
You are Cortex, an AI coding assistant. You EXECUTE tools to answer questions - you NEVER explain how tools work.

CRITICAL RULES:
1. Your FIRST response to ANY code question MUST be tool calls. DO NOT write text first.
2. NEVER say "I will use" or "You can use" - just USE the tools silently.
3. NEVER explain what tools do or how to use them. The user doesn't care.
4. NEVER give generic advice. Give SPECIFIC answers based on ACTUAL code you found.
5. When asked about a codebase, IMMEDIATELY call list_files(".") and search_code.

WRONG RESPONSE (never do this):
"To understand this codebase, I would use the list_files tool to see the structure..."

CORRECT RESPONSE:
[Call list_files(".")] → [Call search_code("main entry")] → [Read key files] → 
"This is a CLI tool built with Typer. The entry point is `main.py:120` which defines..."

SUB-AGENTS (use via `task` tool):
- explorer: For code questions, searching, understanding
- builder: For writing/modifying code
- planner: For multi-step task breakdown
- general: For quick answers

For "explain this codebase": 
1. Call list_files(".") immediately
2. Read main.py and key files  
3. Summarize WHAT YOU FOUND, not how you found it

REMEMBER: Act, don't explain. Execute tools first, then summarize findings.
"""


class Orchestrator:
    """
    Deep Agent Orchestrator that coordinates specialized sub-agents.
    
    Uses LangChain's deepagents library to implement a supervisor pattern
    where the main orchestrator delegates to specialized sub-agents for
    different types of tasks.
    """
    
    def __init__(self, project_path: str = ".", provider: str = "openai", model_name: str = None):
        """
        Initialize the orchestrator with sub-agents.
        
        Args:
            project_path: Path to the project to work with
            provider: LLM provider ('openai' or 'ollama')
            model_name: Specific model name to use
        """
        self.llm = LLMFactory.get_llm(provider, model_name)
        self.memory = InMemorySaver()
        self.project_tools = ProjectTools(project_path, llm=self.llm)
        
        # Get categorized tools
        all_tools = self.project_tools.get_tools()
        exploration_tools = self.project_tools.get_exploration_tools()
        builder_tools = self.project_tools.get_builder_tools()
        
        # Configure sub-agents
        self.subagents = [
            get_planner_config(),
            get_explorer_config(exploration_tools),
            get_builder_config(builder_tools),
            get_general_config(exploration_tools),
        ]
        
        # Create the deep agent with sub-agents
        self.agent = create_deep_agent(
            model=self.llm,
            tools=all_tools,  # Orchestrator has access to all tools
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            subagents=self.subagents,
            checkpointer=self.memory,
        )

    def ask(self, query: str, thread_id: str = "default"):
        """
        Ask the orchestrator a question or request.
        
        The orchestrator will analyze the request and delegate to
        the appropriate sub-agent(s) as needed.
        
        Args:
            query: The user's question or request
            thread_id: Conversation thread ID for memory
            
        Returns:
            The response from the orchestrator
        """
        inputs = {"messages": [HumanMessage(content=query)]}
        config = {"configurable": {"thread_id": thread_id}}
        
        response = self.agent.invoke(inputs, config=config)
        
        # The response is typically a list of messages, the last one being the answer
        return response["messages"][-1].content
