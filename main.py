import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from ingestion.pipeline import ingest_and_index
from ingestion.watcher import start_watching, start_background_watcher
from agents.orchestrator import Orchestrator
import os
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(help="Cortex: Your Local AI-Powered Codebase Assistant")
console = Console()

@app.command()
def index(
    path: str = typer.Argument(".", help="Path to the folder or git repo to index"),
    source_type: str = typer.Option("folder", "--type", "-t", help="Type of source: 'folder' or 'github'")
):
    """
    Index a codebase for retrieval.
    """
    console.print(Panel(f"[bold blue]Indexing Source:[/bold blue] {path} ({source_type})", title="Cortex Ingestion"))
    
    with console.status("[bold green]Working on indexing...[/bold green]"):
        num_indexed = ingest_and_index(path, source_type)
    
    console.print(f"\n[bold green]Success![/bold green] Indexed {num_indexed} files.")

@app.command()
def watch(
    path: str = typer.Argument(".", help="Path to the folder to watch for changes")
):
    """
    Automatically re-index files as they change.
    """
    console.print(Panel(f"[bold blue]Watching Path:[/bold blue] {path}", title="Cortex Watcher"))
    try:
        start_watching(path)
    except KeyboardInterrupt:
        console.print("\n[bold red]Stopping watcher...[/bold red]")

@app.command()
def ask(
    query: str = typer.Argument(..., help="The question you want to ask about your codebase"),
    provider: str = typer.Option("ollama", "--provider", "-p", help="LLM Provider: 'ollama' or 'openai'"),
    model: str = typer.Option(None, "--model", "-m", help="Specific model name")
):
    """
    Ask a single question about the indexed codebase.
    """
    watcher = start_background_watcher(".")
    try:
        console.print(Panel(f"[bold blue]Query:[/bold blue] {query}", title="Cortex Search"))
        
        orchestrator = Orchestrator(provider=provider, model_name=model)
        
        with console.status("[bold yellow]Agent is thinking and searching...[/bold yellow]"):
            response = orchestrator.ask(query)
        
        console.print("\n[bold green]Cortex Agent:[/bold green]")
        console.print(Markdown(response))
    finally:
        watcher.stop()
        watcher.join()

@app.command()
def chat(
    provider: str = typer.Option("ollama", "--provider", "-p", help="LLM Provider: 'ollama' or 'openai'"),
    model: str = typer.Option(None, "--model", "-m", help="Specific model name")
):
    """
    Start an interactive chat session with your codebase.
    """
    watcher = start_background_watcher(".")
    try:
        console.print(Panel("[bold magenta]Welcome to Cortex Chat![/bold magenta]\nType 'exit' or 'quit' to end the session.", title="Cortex Interactive"))
        
        orchestrator = Orchestrator(provider=provider, model_name=model)
        thread_id = "session_" + os.urandom(4).hex()
        
        while True:
            try:
                query = console.input("\n[bold cyan]You :[/bold cyan] ")
            except EOFError:
                break
                
            if query.lower() in ["exit", "quit"]:
                console.print("[bold red]Goodbye![/bold red]")
                break
                
            with console.status("[bold yellow]Searching & Thinking...[/bold yellow]"):
                response = orchestrator.ask(query, thread_id=thread_id)
                
            console.print(f"\n[bold green]Cortex :[/bold green]")
            console.print(Markdown(response))
    finally:
        watcher.stop()
        watcher.join()

if __name__ == "__main__":
    app()
