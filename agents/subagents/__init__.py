"""
Subagent configurations for the Cortex deep agent system.

Each subagent is specialized for a different type of task:
- planner: Task breakdown and planning
- explorer: Codebase exploration and analysis
- builder: Code writing and execution
- general: Miscellaneous tasks
"""

from agents.subagents.planner import get_planner_config
from agents.subagents.explorer import get_explorer_config
from agents.subagents.builder import get_builder_config
from agents.subagents.general import get_general_config

__all__ = [
    "get_planner_config",
    "get_explorer_config", 
    "get_builder_config",
    "get_general_config",
]
