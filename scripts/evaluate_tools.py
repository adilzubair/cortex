import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from agents.orchestrator import Orchestrator

load_dotenv()

console = Console()

# Define test cases that target specific tools
TOOL_TEST_CASES = [
    {
        "tool": "list_files",
        "query": "Show me the directory structure of the 'ingestion' folder. Use the list_files tool."
    },
    {
        "tool": "read_file",
        "query": "Read the main.py file and tell me the version of the project if listed."
    },
    {
        "tool": "search_code",
        "query": "Search for 'read_file_robust' and explain where it is used."
    },
    {
        "tool": "get_symbol_info",
        "query": "Find the class definition and signature for 'Orchestrator' in the agents module."
    },
    {
        "tool": "find_references",
        "query": "Find where 'load_github_repo' is called in this codebase."
    },
    {
        "tool": "get_file_outline",
        "query": "Give me an outline of classes and functions in 'agents/tools.py'."
    },
    {
        "tool": "grep_code",
        "query": "Use a regex search to find all occurrences of 'provider' in .py files."
    },
    {
        "tool": "multi-step",
        "query": "Find the definition of 'get_global_repos_dir' and then read the file where it is defined to see the implementation."
    }
]

def run_tool_evaluation(project_path: str = ".", provider: str = "openai", model: str = "gpt-4o", interval: int = 15):
    project_path = os.path.abspath(project_path)
    console.print(Panel(f"[bold blue]Starting Tool Performance Evaluation[/bold blue]\n[bold]Project:[/bold] {project_path}\n[bold]Model:[/bold] {provider}/{model}\n[bold]Wait Interval:[/bold] {interval}s", title="Cortex Tool Evaluator"))
    
    orchestrator = Orchestrator(project_path=project_path, provider=provider, model_name=model)
    results = []
    
    summary_table = Table(title="Tool Evaluation Summary")
    summary_table.add_column("Target Tool", style="cyan")
    summary_table.add_column("Query", style="white")
    summary_table.add_column("Time (s)", style="magenta")
    summary_table.add_column("Status", style="bold")

    for i, test in enumerate(TOOL_TEST_CASES):
        if i > 0:
            console.print(f"\n[dim]Waiting {interval} seconds before next request to avoid rate limits...[/dim]")
            time.sleep(interval)

        console.print(f"\n[bold green][{i+1}/{len(TOOL_TEST_CASES)}] Testing Tool: {test['tool']}[/bold green]")
        console.print(f"[italic]Query: {test['query']}[/italic]")
        
        start_time = time.time()
        with console.status("[yellow]Agent is executing tool-based query...[/yellow]"):
            try:
                response = orchestrator.ask(test["query"])
                duration = time.time() - start_time
                
                results.append({
                    "target_tool": test["tool"],
                    "query": test["query"],
                    "response": response,
                    "duration": duration,
                    "status": "success"
                })
                
                summary_table.add_row(test["tool"], test["query"][:40] + "...", f"{duration:.2f}", "[green]PASS[/green]")
                console.print("\n[bold]Agent Response Summary:[/bold]")
                # Just show the first few lines of the response to keep the console clean
                preview = "\n".join(response.split("\n")[:10])
                if len(response.split("\n")) > 10:
                    preview += "\n..."
                console.print(Markdown(preview))
                
            except Exception as e:
                duration = time.time() - start_time
                results.append({
                    "target_tool": test["tool"],
                    "query": test["query"],
                    "error": str(e),
                    "duration": duration,
                    "status": "error"
                })
                summary_table.add_row(test["tool"], test["query"][:40] + "...", f"{duration:.2f}", "[red]FAIL[/red]")
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")

    console.print("\n")
    console.print(summary_table)
    
    # Save results to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"tool_evaluation_report_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    
    console.print(f"\n[bold green]Tool evaluation complete![/bold green] Results saved to [bold underline]{report_file}[/bold underline]")

if __name__ == "__main__":
    # Default interval of 15 seconds to be safe with OpenAI tier 1 limits
    run_tool_evaluation(interval=15)
