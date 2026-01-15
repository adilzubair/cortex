"""
General Sub-agent - Versatile assistant for miscellaneous tasks.

This sub-agent handles tasks that don't fit neatly into planning,
exploration, or building categories.
"""

GENERAL_SYSTEM_PROMPT = """
You are a helpful coding assistant. You USE tools to find answers - never explain tools.

CRITICAL: For any code question, call tools FIRST. No text before tool calls.

RULES:
- NEVER say "You can use search_code" - just call search_code
- NEVER give generic programming advice - find SPECIFIC code
- Always base answers on actual code you found
- Be concise and direct

After tool calls, provide a focused answer based on what you found.
"""


def get_general_config(general_tools: list, provider: str = "openai"):
    """
    Returns the configuration dictionary for the general sub-agent.
    
    Args:
        general_tools: List of general tools (typically exploration tools)
    """
    return {
        "name": "general",
        "description": "Handles general questions and quick tasks that don't need deep exploration or code changes.",
        "system_prompt": GENERAL_SYSTEM_PROMPT,
        "tools": general_tools,
    }
