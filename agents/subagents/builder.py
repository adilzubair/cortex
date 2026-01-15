"""
Builder Sub-agent - Specialized for code writing and execution.

This sub-agent focuses on creating and modifying code files.
"""

BUILDER_SYSTEM_PROMPT = """
You write and modify code. Execute tools immediately.

WORKFLOW:
1. read_file to understand existing code
2. write_file to create/modify
3. run_command to test

RULES:
- Match existing code style
- Add type hints and docstrings
- Test after changes
- Report what was created/modified

Don't explain - just write the code and report results.
"""


def get_builder_config(builder_tools: list, provider: str = "openai"):
    """
    Returns the configuration dictionary for the builder sub-agent.
    
    Args:
        builder_tools: List of builder tools (write_file, run_command, etc.)
    """
    return {
        "name": "builder",
        "description": "Writes and modifies code. Use for 'add feature', 'fix bug', 'create file' requests.",
        "system_prompt": BUILDER_SYSTEM_PROMPT,
        "tools": builder_tools,
    }
