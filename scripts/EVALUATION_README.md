# AI Code Assistant Evaluation Guide

This guide explains how to run comprehensive evaluations of your AI code assistant agent.

## 📁 Files

- **`evaluate_scenarios.py`** - Defines 30 test scenarios across 10 categories
- **`run_scenario_evaluation.py`** - Main evaluation runner script
- **`evaluate_agent.py`** - Legacy agent evaluation (basic queries)
- **`evaluate_tools.py`** - Tool-specific evaluation

## 🚀 Quick Start

### 1. List All Available Scenarios

```bash
uv run python scripts/run_scenario_evaluation.py --list-scenarios
```

This shows all 30 scenarios organized by category.

### 2. Run All Scenarios

```bash
uv run python scripts/run_scenario_evaluation.py
```

**Note:** This will take a while! With 30 scenarios and 15s interval = ~7.5 minutes minimum.

### 3. Run Specific Category

```bash
# Run only Code Search scenarios
uv run python scripts/run_scenario_evaluation.py --category "Code Search & Navigation"

# Run only General Inquiries
uv run python scripts/run_scenario_evaluation.py --category "General Inquiries"
```

### 4. Run Single Scenario

```bash
# Test a specific case
uv run python scripts/run_scenario_evaluation.py --case-id CASE_01
```

### 5. Custom Configuration

```bash
# Use different model
uv run python scripts/run_scenario_evaluation.py --model gpt-4o --interval 20

# Evaluate different project
uv run python scripts/run_scenario_evaluation.py --project-path /path/to/other/project
```

## 📊 Evaluation Process

For each scenario, the script will:

1. **Display the scenario** - Shows case ID, category, and user query
2. **Execute the query** - Sends it to your AI agent
3. **Show the response** - Displays agent's answer (preview)
4. **Automated evaluation** - Uses LLM to automatically score the response:
   - **Accuracy** - Correctness of information and tool usage
   - **Robustness** - Error handling and edge cases
   - **User Experience** - Clarity and helpfulness
   - **Memory & Context** - Context retention (for multi-turn)
   - **Language Understanding** - Intent comprehension
   - **Speed** - Auto-calculated from response time
   - **Cost Efficiency** - Estimated from token usage

5. **Generate report** - Saves detailed JSON report with scores and ratings

### How Automated Evaluation Works

The script uses a **separate LLM call** to evaluate each metric:
- Sends the scenario, expected behavior, success criteria, and agent response to the LLM
- Asks the LLM to score 0-100 based on metric-specific guidelines
- Automatically converts scores to ratings (Excellent/Good/Satisfactory/etc.)
- No manual input required - fully automated!


## 📈 Evaluation Metrics

### Rating Scale

| Score | Rating | Description |
|-------|--------|-------------|
| 90-100% | Excellent | Best performance |
| 80-89% | Good | High quality |
| 70-79% | Satisfactory | Acceptable |
| 60-69% | Needs Improvement | Below expectations |
| <60% | Poor | Unsatisfactory |

### Speed Ratings

| Duration | Rating |
|----------|--------|
| <5s | Excellent |
| 5-8s | Good |
| 8-10s | Satisfactory |
| 10-12s | Needs Improvement |
| >12s | Poor |

## 📝 Scenario Categories

1. **General Inquiries** (2 scenarios) - Basic interactions
2. **Code Search & Navigation** (3 scenarios) - Finding code
3. **Cross-Tool Inquiries** (3 scenarios) - Multi-tool usage
4. **Code Modification** (3 scenarios) - Editing code
5. **Context & Memory Retention** (3 scenarios) - Multi-turn conversations
6. **Complex Reasoning** (3 scenarios) - Advanced analysis
7. **Multi-Step Operations** (3 scenarios) - Complex workflows
8. **Error Handling & Robustness** (3 scenarios) - Edge cases
9. **Edge Cases** (3 scenarios) - Unusual situations
10. **Performance & Efficiency** (4 scenarios) - Speed and cost

## 📄 Report Output

After evaluation, you'll get a JSON report like:

```json
{
  "metadata": {
    "timestamp": "2026-01-15T15:30:00",
    "project_path": "/Users/...",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "total_scenarios": 30,
    "successful": 28,
    "failed": 2
  },
  "results": [
    {
      "case_id": "CASE_01",
      "category": "General Inquiries",
      "query": "Hello! Can you help me?",
      "response": "...",
      "duration": 2.5,
      "metrics": {
        "Accuracy": {"value": 95, "rating": "Excellent"},
        "Speed": {"value": 2.5, "rating": "Excellent", "auto": true}
      }
    }
  ]
}
```

## 💡 Tips

### Start Small
Begin with a single category to understand the process:
```bash
uv run python scripts/run_scenario_evaluation.py --category "General Inquiries"
```

### Adjust Interval
If you hit rate limits, increase the interval:
```bash
uv run python scripts/run_scenario_evaluation.py --interval 30
```

### Focus on Priorities
Run scenarios most relevant to your use case first:
- Code search issues? → Run "Code Search & Navigation"
- Memory problems? → Run "Context & Memory Retention"
- Performance concerns? → Run "Performance & Efficiency"

### Batch Evaluation
For comprehensive testing, run in batches:
```bash
# Day 1: Basic functionality
uv run python scripts/run_scenario_evaluation.py --category "General Inquiries"
uv run python scripts/run_scenario_evaluation.py --category "Code Search & Navigation"

# Day 2: Advanced features
uv run python scripts/run_scenario_evaluation.py --category "Complex Reasoning"
uv run python scripts/run_scenario_evaluation.py --category "Multi-Step Operations"
```

## 🔍 Example Session

```bash
$ uv run python scripts/run_scenario_evaluation.py --case-id CASE_03

╭─────────────────────────────────────────╮
│ AI Code Assistant Scenario Evaluation  │
│ Project: /Users/muhamedadil/gitea/cortex│
│ Model: openai/gpt-4o-mini              │
│ Scenarios: 1                            │
│ Interval: 15s                           │
╰─────────────────────────────────────────╯

━━━ Scenario 1/1 ━━━

═══ CASE_03: Find specific function or class ═══
Category: Code Search & Navigation

User Query: Where is the function that handles user authentication?

Agent Response:
The authentication handling is located in...
[response preview]

Automated Evaluation:
  Speed: 3.2s → Excellent
  Accuracy: 85/100 → Good
  Robustness: 90/100 → Excellent
  Cost Efficiency: $0.0087 → Excellent

✓ Evaluation complete!
Report saved to: scenario_evaluation_report_20260115_153010.json
```


## 🎯 Next Steps

1. **Run initial evaluation** - Start with a few scenarios
2. **Analyze results** - Review the JSON report
3. **Identify weaknesses** - Look for low scores
4. **Improve agent** - Update prompts, tools, or logic
5. **Re-evaluate** - Run scenarios again to measure improvement

## 📚 Additional Resources

- See `evaluate_scenarios.py` for scenario definitions
- Modify scenarios to match your specific use cases
- Add new scenarios by extending `EVALUATION_SCENARIOS` list
