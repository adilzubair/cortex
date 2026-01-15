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

TEST_CASES = [
    {
        "category": "Architecture",
        "query": "Explain the overall architecture of the Cortex project. How do the ingestion, indexing, and agent layers interact?"
    },
    {
        "category": "Architecture",
        "query": "Where are the GitHub repositories cloned to, and how is this configured?"
    },
    {
        "category": "Specific Logic",
        "query": "How does the `read_file_robust` function handle different file encodings? List the encodings it tries."
    },
    {
        "category": "Specific Logic",
        "query": "What is the purpose of the `StateManager` class in the indexing module?"
    },
    {
        "category": "Dependency/Integration",
        "query": "Which LLM providers are supported by Cortex, and where is the factory logic for creating these providers located?"
    },
    {
        "category": "Technical Debt/Refactoring",
        "query": "Looking at `main.py`, what are the different command groups available to the user?"
    }
]

def run_evaluation(project_path: str = ".", provider: str = "openai", model: str = "gpt-4o"):
    project_path = os.path.abspath(project_path)
    console.print(Panel(f"[bold blue]Starting Agent Evaluation[/bold blue]\n[bold]Project:[/bold] {project_path}\n[bold]Model:[/bold] {provider}/{model}", title="Cortex Evaluator"))
    
    orchestrator = Orchestrator(project_path=project_path, provider=provider, model_name=model)
    results = []
    
    table = Table(title="Evaluation Results")
    table.add_column("Category", style="cyan")
    table.add_column("Query", style="white")
    table.add_column("Time (s)", style="magenta")
    
    for i, test in enumerate(TEST_CASES):
        console.print(f"\n[bold green][{i+1}/{len(TEST_CASES)}] Testing Category: {test['category']}[/bold green]")
        console.print(f"[italic]Query: {test['query']}[/italic]")
        
        start_time = time.time()
        with console.status("[yellow]Agent is thinking...[/yellow]"):
            try:
                response = orchestrator.ask(test["query"])
                duration = time.time() - start_time
                
                results.append({
                    "category": test["category"],
                    "query": test["query"],
                    "response": response,
                    "duration": duration,
                    "status": "success"
                })
                
                table.add_row(test["category"], test["query"][:50] + "...", f"{duration:.2f}")
                console.print("\n[bold]Agent Response:[/bold]")
                console.print(Markdown(response))
                
            except Exception as e:
                duration = time.time() - start_time
                results.append({
                    "category": test["category"],
                    "query": test["query"],
                    "error": str(e),
                    "duration": duration,
                    "status": "error"
                })
                table.add_row(test["category"], test["query"][:50] + "...", "FAILED", style="red")
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")

    console.print("\n")
    console.print(table)
    
    # Save results to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"evaluation_report_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    
    console.print(f"\n[bold green]Evaluation complete![/bold green] Full report saved to [bold underline]{report_file}[/bold underline]")

if __name__ == "__main__":
    # Default to current project and OpenAI gpt-4o as it's the default in main.py for chat
    # Users can modify these defaults or we could add Typer CLI here too
    run_evaluation()
