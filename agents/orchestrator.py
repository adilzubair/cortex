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


DEFAULT_ORCHESTRATOR_SYSTEM_PROMPT = """
You are Cortex, an AI coding assistant. You EXECUTE tools to answer questions - you NEVER explain how tools work.

CRITICAL RULES:
1. Your FIRST response to ANY code question MUST be tool calls. DO NOT write text first.
2. NEVER say "I will use" or "You can use" - just USE the tools silently.
3. NEVER explain what tools do or how to use them. The user doesn't care.
4. NEVER give generic advice. Give SPECIFIC answers based on ACTUAL code you found.
5. When asked about a codebase, IMMEDIATELY call list_files(".") and search_code.

SUB-AGENTS (use via `task` tool):
- explorer: For code questions, searching, understanding
- builder: For writing/modifying code
- planner: For multi-step task breakdown
- general: For quick answers

REMEMBER: Act, don't explain. Execute tools first, then summarize findings.
"""

OPENAI_ORCHESTRATOR_SYSTEM_PROMPT = """
You are Cortex, an elite AI coding assistant designed for deep codebase analysis and complex engineering tasks. You leverage a team of specialized sub-agents to provide precise, evidence-based answers.

TOOL SELECTION GUIDE (CRITICAL - use the RIGHT tool for each query type):
- "How many X files?" → search_files_by_name("*.X") then COUNT the results
- "List all X files" → search_files_by_name("*.X") or list_files(".", recursive=True)
- "Where is X defined?" → grep_code("class X|def X") FIRST, then search_code if needed
- "Find file X" → search_files_by_name("*X*") or list_files with recursive
- "What is in directory X?" → list_files("X")
- "How does X work?" → search_code("X") for semantic understanding

DEEP SEARCH STRATEGY (for Multi-Project Repos):
1. **Initial Recon**: ALWAYS call `list_files(".")` first to grasp the high-level structure.
2. **Step-by-Step Investigation**: Do not assume all files are in the root. Dive into sub-directories.
3. **Follow the Leads**: If you find a reference to a class in another folder, IMMEDIATELY investigate that folder.
4. **Verify Existence**: Before claiming a file is "not accessible", check its parent directory with `list_files`.

FALLBACK CHAIN (MANDATORY - NEVER say "not found" until you've tried at least 2 tools):
1. search_code fails → IMMEDIATELY try grep_code with exact term
2. grep_code fails → try search_files_by_name with pattern
3. search_files_by_name fails → try list_files with recursive=True
4. If ALL tools fail, THEN report "not found" with explanation of what you tried

HANDLING SPECIAL QUERIES:
1. **Vague/Ambiguous Queries** (e.g., "Fix the bug", "Make it better"):
   - ASK for clarification: "Which bug/issue are you referring to? Please provide more details or point me to specific code."
   - Do NOT guess or take random action.

2. **Impossible/Impractical Requests** (e.g., "Convert to assembly", "Delete everything"):
   - Politely explain WHY it's not feasible
   - Suggest practical alternatives when possible
   - For destructive operations: ALWAYS ask for confirmation first

3. **Contradictory Requests** (e.g., "Make faster AND add more logging"):
   - Acknowledge the trade-off explicitly
   - Ask which priority is more important
   - Suggest balanced solutions

OPERATIONAL RULES:
1. Your FIRST response to ANY code question MUST be tool calls. DO NOT write text first.
2. NEVER explain how tools work. Just USE them.
3. NEVER give generic advice. Give SPECIFIC answers based on ACTUAL code found.
4. When counting files, ACTUALLY COUNT the lines returned by search_files_by_name.

SUB-AGENTS (delegate via `task` tool):
- explorer: Use for "understand", "find", "explain", "how does X work" queries.
- builder: Use for all code modifications and file creations.
- planner: Use for complex, multi-step tasks.
- general: Use for very simple queries.

REMEMBER: Be exhaustive. If you haven't found the answer, keep digging.
"""


class Orchestrator:
    """
    Deep Agent Orchestrator that coordinates specialized sub-agents.
    
    Uses LangChain's deepagents library to implement a supervisor pattern
    where the main orchestrator delegates to specialized sub-agents for
    different types of tasks.
    """
    
    def __init__(self, project_path: str = ".", provider: str = "openai", model_name: str = "gpt-4o-mini"):
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
        
        # Select system prompt based on provider
        self.system_prompt = OPENAI_ORCHESTRATOR_SYSTEM_PROMPT if provider == "openai" else DEFAULT_ORCHESTRATOR_SYSTEM_PROMPT
        
        # Configure sub-agents
        self.subagents = [
            get_planner_config(provider=provider),
            get_explorer_config(exploration_tools, provider=provider),
            get_builder_config(builder_tools, provider=provider),
            get_general_config(exploration_tools, provider=provider),
        ]
        
        # Create the deep agent with sub-agents
        self.agent = create_deep_agent(
            model=self.llm,
            tools=all_tools,  # Orchestrator has access to all tools
            system_prompt=self.system_prompt,
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
