from agents.orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

def test_agent():
    print("Initializing Orchestrator...")
    # Use 'ollama' or 'openai' depending on your setup
    orchestrator = Orchestrator(provider="ollama")
    
    query = "Explain how the incremental indexing works in this project."
    print(f"\nUser: {query}")
    
    print("\n--- Agent Execution ---")
    response = orchestrator.ask(query)
    
    print("\n--- Final Response ---")
    print(response)

if __name__ == "__main__":
    test_agent()
