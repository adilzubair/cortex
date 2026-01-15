"""
Planner Sub-agent - Specialized for task breakdown and planning.

This sub-agent focuses on breaking down complex tasks into actionable steps.
"""

PLANNER_SYSTEM_PROMPT = """
You are a task planner. Break down complex requests into clear steps.

USE write_todos to create actionable plans. Execute it immediately.

For each task in the plan:
- Be specific (include file paths)
- Define what "done" looks like
- Order by dependencies

Don't explain planning - just create the plan using write_todos.
"""


def get_planner_config(provider: str = "openai"):
    """
    Returns the configuration dictionary for the planner sub-agent.
    Uses the built-in write_todos tool from deepagents.
    """
    return {
        "name": "planner",
        "description": "Creates implementation plans and breaks down complex tasks into steps. Use when the task has multiple parts.",
        "system_prompt": PLANNER_SYSTEM_PROMPT,
        "tools": [],  # Uses built-in write_todos from deepagents
    }
