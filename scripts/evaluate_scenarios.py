"""
AI Code Assistant Agent - Evaluation Scenarios

This module defines comprehensive test scenarios for evaluating an AI code assistant agent
across multiple dimensions: accuracy, speed, robustness, user experience, memory/context,
language understanding, and cost efficiency.

Evaluation Criteria:
- 90-100%: Excellent
- 80-89%: Good  
- 70-79%: Satisfactory
- 60-69%: Needs Improvement
- Below 60%: Poor
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ScenarioCategory(Enum):
    """Categories of test scenarios"""
    GENERAL_INQUIRIES = "General Inquiries"
    CODE_SEARCH = "Code Search & Navigation"
    CODE_MODIFICATION = "Code Modification"
    CROSS_TOOL = "Cross-Tool Inquiries"
    CONTEXT_RETENTION = "Context & Memory"
    COMPLEX_REASONING = "Complex Reasoning"
    ERROR_HANDLING = "Error Handling & Robustness"
    MULTI_STEP = "Multi-Step Operations"


@dataclass
class TestScenario:
    """Represents a single test scenario"""
    case_id: str
    category: ScenarioCategory
    description: str
    user_query: str
    expected_behavior: str
    success_criteria: List[str]
    evaluation_metrics: List[str]
    
    
# ============================================================================
# TEST SCENARIOS
# ============================================================================

EVALUATION_SCENARIOS = [
    
    # ========================================================================
    # Case 1-2: General Inquiries
    # ========================================================================
    TestScenario(
        case_id="CASE_01",
        category=ScenarioCategory.GENERAL_INQUIRIES,
        description="Greeting and basic interaction",
        user_query="Hello! Can you help me understand this codebase?",
        expected_behavior="Agent should respond politely, confirm availability to help, and ask for clarification on what the user needs",
        success_criteria=[
            "Responds with greeting",
            "Confirms readiness to assist",
            "Asks clarifying questions if needed"
        ],
        evaluation_metrics=["Accuracy", "User Experience", "Language Understanding"]
    ),
    
    TestScenario(
        case_id="CASE_02",
        category=ScenarioCategory.GENERAL_INQUIRIES,
        description="Project overview and capabilities",
        user_query="What is Cortex? What are its main features?",
        expected_behavior="Agent should read README or search for project info, explaining that Cortex is an AI-powered local codebase assistant with RAG, multi-project support, incremental indexing, and LSP integration",
        success_criteria=[
            "Uses appropriate tools (read_file for README, list_files, search_code)",
            "Identifies Cortex as an AI code assistant",
            "Mentions key features like RAG, multi-project support, incremental indexing",
            "References the .cortex directory structure"
        ],
        evaluation_metrics=["Accuracy", "Speed", "Language Understanding", "Robustness"]
    ),
    
    # ========================================================================
    # Case 3-5: Code Search & Navigation
    # ========================================================================
    TestScenario(
        case_id="CASE_03",
        category=ScenarioCategory.CODE_SEARCH,
        description="Find specific function or class",
        user_query="Where is the search_code function defined?",
        expected_behavior="Agent should use search_code or grep_code to locate the search_code function in agents/tools.py and provide file path with line numbers",
        success_criteria=[
            "Uses search_code or grep_code appropriately",
            "Returns correct file path (agents/tools.py)",
            "Provides line numbers and context about the function's purpose"
        ],
        evaluation_metrics=["Accuracy", "Speed", "Robustness"]
    ),
    
    TestScenario(
        case_id="CASE_04",
        category=ScenarioCategory.CODE_SEARCH,
        description="Semantic code search",
        user_query="Show me code that handles file hashing and change detection",
        expected_behavior="Agent should use semantic search to find StateManager class and file hashing logic in indexing/state.py, even if exact terms don't match",
        success_criteria=[
            "Uses semantic search (search_code)",
            "Finds StateManager class or related hashing code",
            "Shows code snippets with context about SHA-256 hashing"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "Robustness"]
    ),
    
    TestScenario(
        case_id="CASE_05",
        category=ScenarioCategory.CODE_SEARCH,
        description="Fallback strategy when primary tool fails",
        user_query="Find the Orchestrator class",
        expected_behavior="If search_code fails, agent should fallback to grep_code for exact match or list_files to explore agents/ directory",
        success_criteria=[
            "Attempts primary tool first",
            "Falls back to alternative tools if needed",
            "Successfully locates Orchestrator in agents/orchestrator.py",
            "Explains the search strategy used"
        ],
        evaluation_metrics=["Robustness", "User Experience", "Accuracy"]
    ),
    
    # ========================================================================
    # Case 6-8: Cross-Tool Inquiries
    # ========================================================================
    TestScenario(
        case_id="CASE_06",
        category=ScenarioCategory.CROSS_TOOL,
        description="Multiple tool invocation in single request",
        user_query="What's the project structure and where is the main entry point?",
        expected_behavior="Agent should use list_files for structure AND search/grep for main.py or __main__ in parallel or sequence",
        success_criteria=[
            "Uses multiple tools (list_files, search_code/grep_code)",
            "Identifies main.py as the entry point",
            "Shows directory structure with agents/, ingestion/, core/, etc.",
            "Executes tools efficiently (parallel if possible)"
        ],
        evaluation_metrics=["Speed", "Accuracy", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_07",
        category=ScenarioCategory.CROSS_TOOL,
        description="Search and explain workflow",
        user_query="Find the tool definitions and explain how they work",
        expected_behavior="Agent should search for tool definitions in agents/tools.py, read the file, and explain the ProjectTools class and individual tools",
        success_criteria=[
            "Searches for tool definitions",
            "Finds ProjectTools class in agents/tools.py",
            "Reads and shows tool functions like search_code, read_file, grep_code",
            "Explains how tools are used by the agent"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_08",
        category=ScenarioCategory.CROSS_TOOL,
        description="Complex analysis requiring multiple tools",
        user_query="How does the ingestion pipeline work from file loading to indexing?",
        expected_behavior="Agent should trace the ingestion flow using multiple searches and file reads, explaining the pipeline from loaders to vector store",
        success_criteria=[
            "Uses multiple tools systematically",
            "Finds ingestion/pipeline.py and related loaders",
            "Traces the flow from file loading to chunking to embedding to storage",
            "Provides step-by-step breakdown with code references"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "Speed", "User Experience"]
    ),
    
    # ========================================================================
    # Case 9-11: Code Modification
    # ========================================================================
    TestScenario(
        case_id="CASE_09",
        category=ScenarioCategory.CODE_MODIFICATION,
        description="Simple code addition",
        user_query="Add a logging statement to the search_code function",
        expected_behavior="Agent should locate search_code in agents/tools.py, read it, and add appropriate logging with correct syntax",
        success_criteria=[
            "Locates search_code function in agents/tools.py",
            "Adds logging in appropriate location (e.g., before query execution)",
            "Uses correct Python logging syntax",
            "Preserves existing functionality"
        ],
        evaluation_metrics=["Accuracy", "Robustness", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_10",
        category=ScenarioCategory.CODE_MODIFICATION,
        description="Refactoring request",
        user_query="Refactor the file hashing logic in StateManager into a separate helper function",
        expected_behavior="Agent should identify hashing code in StateManager, create new helper function, update references, and ensure no breaking changes",
        success_criteria=[
            "Identifies file hashing logic in indexing/state.py",
            "Creates well-structured helper function for SHA-256 hashing",
            "Updates all references in StateManager",
            "Maintains backward compatibility",
            "Follows code style conventions"
        ],
        evaluation_metrics=["Accuracy", "Robustness", "User Experience", "Language Understanding"]
    ),
    
    TestScenario(
        case_id="CASE_11",
        category=ScenarioCategory.CODE_MODIFICATION,
        description="Multi-file modification",
        user_query="Add error handling to all vector store operations across the codebase",
        expected_behavior="Agent should find all Chroma/vector store operations, add consistent error handling, and update multiple files",
        success_criteria=[
            "Identifies all vector store operations (in vectorstore/, agents/tools.py)",
            "Applies consistent try-except error handling pattern",
            "Updates multiple files correctly",
            "Doesn't introduce bugs",
            "Provides summary of changes"
        ],
        evaluation_metrics=["Accuracy", "Robustness", "Speed", "User Experience"]
    ),
    
    # ========================================================================
    # Case 12-14: Context & Memory Retention
    # ========================================================================
    TestScenario(
        case_id="CASE_12",
        category=ScenarioCategory.CONTEXT_RETENTION,
        description="Multi-turn conversation with context",
        user_query=[
            "Find the StateManager class",
            "What methods does it have?",
            "Add a method to clear the cache"
        ],
        expected_behavior="Agent should maintain context across turns, remembering the StateManager location in indexing/state.py and its structure",
        success_criteria=[
            "Remembers StateManager location from turn 1",
            "Doesn't re-search in subsequent turns",
            "Lists methods like compute_hash, is_file_modified, etc.",
            "Correctly adds new method based on existing structure",
            "Maintains conversation context"
        ],
        evaluation_metrics=["Memory & Context", "User Experience", "Speed"]
    ),
    
    TestScenario(
        case_id="CASE_13",
        category=ScenarioCategory.CONTEXT_RETENTION,
        description="Reference to previous operations",
        user_query=[
            "Show me the Orchestrator class",
            "Now add a method to reset the conversation history"
        ],
        expected_behavior="Agent should remember the Orchestrator class location and modify it without re-searching",
        success_criteria=[
            "References Orchestrator from agents/orchestrator.py from previous turn",
            "Doesn't ask for clarification unnecessarily",
            "Applies modification to correct location",
            "Understands context about conversation/memory management"
        ],
        evaluation_metrics=["Memory & Context", "User Experience", "Accuracy"]
    ),
    
    TestScenario(
        case_id="CASE_14",
        category=ScenarioCategory.CONTEXT_RETENTION,
        description="Long conversation with multiple topics",
        user_query=[
            "Find the vector store configuration",
            "What tools are available in ProjectTools?",
            "Update the embedding model we discussed earlier to use a different dimension"
        ],
        expected_behavior="Agent should maintain context even after topic switches and correctly reference the vector store configuration from turn 1",
        success_criteria=[
            "Maintains context across topic switches",
            "Correctly identifies 'earlier discussion' refers to vector store config",
            "Applies change to correct location (core/config.py or vectorstore/)",
            "Doesn't confuse tools discussion with vector store config"
        ],
        evaluation_metrics=["Memory & Context", "Language Understanding", "User Experience"]
    ),
    
    # ========================================================================
    # Case 15-17: Complex Reasoning
    # ========================================================================
    TestScenario(
        case_id="CASE_15",
        category=ScenarioCategory.COMPLEX_REASONING,
        description="Architectural decision making",
        user_query="Should I use ChromaDB or FAISS for the vector store? What does Cortex currently use and why?",
        expected_behavior="Agent should analyze existing vector store implementation, explain that Cortex uses ChromaDB, provide pros/cons, and make recommendation based on codebase conventions",
        success_criteria=[
            "Searches for vector store implementation in vectorstore/ directory",
            "Identifies ChromaDB is currently used",
            "Provides pros/cons of ChromaDB vs FAISS",
            "Makes recommendation aligned with existing codebase",
            "Explains reasoning clearly"
        ],
        evaluation_metrics=["Language Understanding", "Accuracy", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_16",
        category=ScenarioCategory.COMPLEX_REASONING,
        description="Bug diagnosis and fix",
        user_query="The indexing is failing intermittently. Can you investigate and fix it?",
        expected_behavior="Agent should search for indexing code, analyze StateManager and ingestion pipeline, identify potential issues like file locking or hash collisions, and propose fixes",
        success_criteria=[
            "Systematically investigates indexing flow in ingestion/pipeline.py",
            "Examines StateManager for potential race conditions",
            "Identifies potential root causes (file watching, concurrent access, etc.)",
            "Proposes specific fixes with code",
            "Explains the diagnosis process"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "Robustness", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_17",
        category=ScenarioCategory.COMPLEX_REASONING,
        description="Performance optimization",
        user_query="The search_code tool is slow. Find bottlenecks and suggest optimizations",
        expected_behavior="Agent should analyze search_code implementation, identify inefficient vector similarity searches or embedding operations, and suggest specific optimizations",
        success_criteria=[
            "Analyzes search_code in agents/tools.py",
            "Identifies specific bottlenecks (vector store queries, embedding generation, etc.)",
            "Suggests concrete optimizations (caching, batch processing, index tuning)",
            "Provides code examples for improvements"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "User Experience"]
    ),
    
    # ========================================================================
    # Case 18-20: Multi-Step Operations
    # ========================================================================
    TestScenario(
        case_id="CASE_18",
        category=ScenarioCategory.MULTI_STEP,
        description="Complete feature implementation",
        user_query="Add support for indexing JavaScript files with proper chunking",
        expected_behavior="Agent should break down into steps: update file loaders, add JS chunking strategy, update ingestion pipeline, test with sample JS file",
        success_criteria=[
            "Breaks down into logical steps",
            "Updates ingestion/loaders/ to handle .js files",
            "Adds appropriate chunking logic for JavaScript",
            "Updates file type filters in ingestion pipeline",
            "Provides implementation summary",
            "Asks for clarification on JS-specific requirements if needed"
        ],
        evaluation_metrics=["Accuracy", "User Experience", "Language Understanding", "Robustness"]
    ),
]


# ============================================================================
# EVALUATION METRICS DEFINITIONS
# ============================================================================

EVALUATION_METRICS = {
    "Accuracy": {
        "description": "Correctness of responses and code modifications",
        "excellent": (90, 100),
        "good": (80, 89),
        "satisfactory": (70, 79),
        "needs_improvement": (60, 69),
        "poor": (0, 59)
    },
    "Speed": {
        "description": "Response time and latency",
        "excellent": (0, 4),  # seconds
        "good": (4, 5),
        "satisfactory": (5, 6),
        "needs_improvement": (6, 7),
        "poor": (7, float('inf'))
    },
    "Robustness": {
        "description": "Handling edge cases, errors, and unexpected inputs",
        "excellent": (90, 100),
        "good": (80, 89),
        "satisfactory": (70, 79),
        "needs_improvement": (60, 69),
        "poor": (0, 59)
    },
    "User Experience": {
        "description": "Clarity, helpfulness, and communication quality",
        "excellent": (90, 100),
        "good": (80, 89),
        "satisfactory": (70, 79),
        "needs_improvement": (60, 69),
        "poor": (0, 59)
    },
    "Memory & Context": {
        "description": "Retention of conversation context and previous operations",
        "excellent": (90, 100),
        "good": (80, 89),
        "satisfactory": (70, 79),
        "needs_improvement": (60, 69),
        "poor": (0, 59)
    },
    "Language Understanding": {
        "description": "Comprehension of natural language queries and intent",
        "excellent": (90, 100),
        "good": (80, 89),
        "satisfactory": (70, 79),
        "needs_improvement": (60, 69),
        "poor": (0, 59)
    },
    "Cost Efficiency": {
        "description": "Resource usage and API costs",
        "excellent": (0, 0.01),  # USD
        "good": (0.01, 0.02),
        "satisfactory": (0.02, 0.05),
        "needs_improvement": (0.05, 0.10),
        "poor": (0.10, float('inf'))
    }
}


def get_scenarios_by_category(category: ScenarioCategory) -> List[TestScenario]:
    """Get all scenarios for a specific category"""
    return [s for s in EVALUATION_SCENARIOS if s.category == category]


def get_scenario_by_id(case_id: str) -> TestScenario:
    """Get a specific scenario by its ID"""
    for scenario in EVALUATION_SCENARIOS:
        if scenario.case_id == case_id:
            return scenario
    return None


if __name__ == "__main__":
    print(f"Total Test Scenarios: {len(EVALUATION_SCENARIOS)}")
    print("\nScenarios by Category:")
    for category in ScenarioCategory:
        scenarios = get_scenarios_by_category(category)
        print(f"  {category.value}: {len(scenarios)} scenarios")
