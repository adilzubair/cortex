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
    EDGE_CASES = "Edge Cases"
    PERFORMANCE = "Performance & Efficiency"


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
    
    TestScenario(
        case_id="CASE_19",
        category=ScenarioCategory.MULTI_STEP,
        description="Guided implementation with clarifications",
        user_query=[
            "I want to add caching to search results",
            "Use an in-memory LRU cache",
            "Cache search_code results for 5 minutes",
            "Add cache invalidation when files are re-indexed"
        ],
        expected_behavior="Agent should guide through each step, maintain context, and build upon previous steps to create a complete caching solution",
        success_criteria=[
            "Maintains context across all steps",
            "Implements LRU cache (using functools.lru_cache or custom)",
            "Adds caching to search_code in agents/tools.py",
            "Implements time-based expiration (5 min)",
            "Adds cache clearing in StateManager or ingestion pipeline",
            "Provides coherent final implementation"
        ],
        evaluation_metrics=["Memory & Context", "User Experience", "Accuracy"]
    ),
    
    TestScenario(
        case_id="CASE_20",
        category=ScenarioCategory.MULTI_STEP,
        description="Iterative refinement",
        user_query=[
            "Create a new tool for finding file dependencies",
            "Actually, add support for Python imports only",
            "Also detect circular dependencies",
            "Add a warning when circular deps are found"
        ],
        expected_behavior="Agent should iteratively refine the implementation, incorporating each new requirement without starting over",
        success_criteria=[
            "Creates initial dependency finder tool",
            "Refines to focus on Python imports (using ast module)",
            "Adds circular dependency detection logic",
            "Incorporates warning/logging for circular deps",
            "Maintains code quality throughout iterations",
            "Doesn't lose previous requirements"
        ],
        evaluation_metrics=["Memory & Context", "Accuracy", "User Experience", "Robustness"]
    ),
    
    # ========================================================================
    # Case 21-23: Error Handling & Robustness
    # ========================================================================
    TestScenario(
        case_id="CASE_21",
        category=ScenarioCategory.ERROR_HANDLING,
        description="Handling ambiguous requests",
        user_query="Fix the bug in the indexing code",
        expected_behavior="Agent should ask clarifying questions about which bug, what symptoms are observed, or which part of indexing (pipeline, state management, loaders, etc.)",
        success_criteria=[
            "Recognizes ambiguity",
            "Asks specific clarifying questions about the bug symptoms",
            "Mentions different indexing components (pipeline, StateManager, loaders)",
            "Doesn't make unfounded assumptions",
            "Guides user to provide needed information"
        ],
        evaluation_metrics=["User Experience", "Language Understanding", "Robustness"]
    ),
    
    TestScenario(
        case_id="CASE_22",
        category=ScenarioCategory.ERROR_HANDLING,
        description="Handling non-existent code references",
        user_query="Update the VectorDatabase class",
        expected_behavior="If class doesn't exist (Cortex uses Chroma, not a custom VectorDatabase class), agent should inform user and ask if they want to create it or meant something else like the vectorstore module",
        success_criteria=[
            "Searches for VectorDatabase class",
            "Informs user it doesn't exist in the codebase",
            "Offers alternatives (mentions Chroma usage, vectorstore module, or creating new class)",
            "Doesn't hallucinate code that doesn't exist"
        ],
        evaluation_metrics=["Accuracy", "Robustness", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_23",
        category=ScenarioCategory.ERROR_HANDLING,
        description="Handling conflicting requirements",
        user_query="Make the search_code function both synchronous and asynchronous",
        expected_behavior="Agent should explain the conflict and suggest alternatives (async wrapper, two versions, or using async throughout)",
        success_criteria=[
            "Identifies the conflict between sync and async",
            "Explains why having both in one function is problematic",
            "Suggests viable alternatives (async wrapper, separate functions, refactor to async)",
            "Asks user to choose approach"
        ],
        evaluation_metrics=["Language Understanding", "User Experience", "Robustness"]
    ),
    
    # ========================================================================
    # Case 24-26: Edge Cases
    # ========================================================================
    TestScenario(
        case_id="CASE_24",
        category=ScenarioCategory.EDGE_CASES,
        description="Very large codebase navigation",
        user_query="Find all tool definitions in the codebase",
        expected_behavior="Agent should handle potentially large result sets efficiently, finding all @tool decorated functions in agents/tools.py and subagents",
        success_criteria=[
            "Searches for tool definitions (using @tool decorator or 'def' in tools.py)",
            "Handles result set gracefully (lists all tools or summarizes)",
            "Provides organized output (grouped by file or category)",
            "Doesn't timeout or crash",
            "Mentions tools like search_code, read_file, grep_code, list_files, etc."
        ],
        evaluation_metrics=["Robustness", "Speed", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_25",
        category=ScenarioCategory.EDGE_CASES,
        description="Code with multiple languages",
        user_query="Find all file loading logic in the project (Python loaders and shell scripts)",
        expected_behavior="Agent should search across Python files in ingestion/loaders/ and any shell scripts like install_models.sh",
        success_criteria=[
            "Searches across multiple file types (.py and .sh)",
            "Identifies Python loaders (folder.py, github.py, etc.)",
            "Finds shell scripts if relevant",
            "Organizes results by type/language",
            "Provides comprehensive coverage"
        ],
        evaluation_metrics=["Accuracy", "Language Understanding", "Robustness"]
    ),
    
    TestScenario(
        case_id="CASE_26",
        category=ScenarioCategory.EDGE_CASES,
        description="Handling special characters and keywords",
        user_query="Find code using the '__init__' method or 'class' keyword",
        expected_behavior="Agent should properly handle Python special methods and keywords in searches, finding class definitions and __init__ methods",
        success_criteria=[
            "Handles special characters (__) correctly",
            "Distinguishes between 'class' keyword and class names",
            "Returns accurate results for __init__ methods",
            "Doesn't error on edge cases",
            "Finds multiple class definitions in the codebase"
        ],
        evaluation_metrics=["Robustness", "Accuracy"]
    ),
    
    # ========================================================================
    # Case 27-29: Performance & Efficiency
    # ========================================================================
    TestScenario(
        case_id="CASE_27",
        category=ScenarioCategory.PERFORMANCE,
        description="Parallel tool execution",
        user_query="Show me the Orchestrator class, the StateManager class, and all available tools",
        expected_behavior="Agent should execute independent searches in parallel to minimize latency",
        success_criteria=[
            "Identifies three independent operations",
            "Executes searches in parallel (if agent supports it)",
            "Finds Orchestrator in agents/orchestrator.py",
            "Finds StateManager in indexing/state.py",
            "Lists tools from agents/tools.py",
            "Completes faster than sequential execution would"
        ],
        evaluation_metrics=["Speed", "User Experience"]
    ),
    
    TestScenario(
        case_id="CASE_28",
        category=ScenarioCategory.PERFORMANCE,
        description="Efficient tool selection",
        user_query="Find the exact string 'TODO: refactor'",
        expected_behavior="Agent should use grep_code for exact string match rather than semantic search_code",
        success_criteria=[
            "Chooses grep_code over search_code for exact match",
            "Uses appropriate pattern matching",
            "Completes quickly",
            "Returns accurate results",
            "Doesn't use unnecessarily expensive semantic search"
        ],
        evaluation_metrics=["Speed", "Cost Efficiency", "Accuracy"]
    ),
    
    TestScenario(
        case_id="CASE_29",
        category=ScenarioCategory.PERFORMANCE,
        description="Cost-effective operation",
        user_query="List all Python files in the agents directory",
        expected_behavior="Agent should use list_files rather than expensive search operations",
        success_criteria=[
            "Uses list_files with agents/ directory path",
            "Avoids unnecessary LLM calls or vector searches",
            "Filters for .py files",
            "Completes efficiently",
            "Provides accurate listing of agent files"
        ],
        evaluation_metrics=["Cost Efficiency", "Speed", "Accuracy"]
    ),
    
    # ========================================================================
    # Case 30: Combined Complexity
    # ========================================================================
    TestScenario(
        case_id="CASE_30",
        category=ScenarioCategory.COMPLEX_REASONING,
        description="End-to-end complex task",
        user_query="I need to add support for a new embedding model (sentence-transformers). Find the current embedding configuration, update it to support multiple models, add a config option to choose between them, and update the documentation",
        expected_behavior="Agent should break down the task, find current Ollama embedding usage, implement model switching logic, add configuration, and update README",
        success_criteria=[
            "Breaks down into logical steps",
            "Finds current embedding implementation (embeddings/ or core/config.py)",
            "Identifies OllamaEmbeddings usage",
            "Implements model factory or switching logic",
            "Adds configuration option (in config.py or .env)",
            "Updates README.md with new embedding model option",
            "Provides comprehensive summary",
            "Maintains context throughout",
            "Asks clarifying questions as needed (e.g., which sentence-transformers model)"
        ],
        evaluation_metrics=["Accuracy", "Memory & Context", "User Experience", "Language Understanding", "Robustness", "Speed"]
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
