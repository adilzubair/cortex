from agents.tools import get_symbol_info, find_references
import os

def test_lsp_tools():
    print("--- Testing LSP Tools (Jedi) ---")
    
    # Test 1: Find definition of StateManager
    print("\n[TEST 1] Finding definition of 'StateManager'...")
    def_result = get_symbol_info("StateManager")
    print(def_result)
    
    # Test 2: Find references of StateManager
    print("\n[TEST 2] Finding references of 'StateManager'...")
    ref_result = find_references("StateManager")
    print(ref_result)
    
    # Test 3: Find definition of ingest_and_index
    print("\n[TEST 3] Finding definition of 'ingest_and_index'...")
    print(get_symbol_info("ingest_and_index"))

if __name__ == "__main__":
    test_lsp_tools()
