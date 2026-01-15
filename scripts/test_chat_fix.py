#!/usr/bin/env python3
"""
Quick test to verify the chat fix works.
This script will test if the orchestrator can respond to a simple query.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import Orchestrator

def test_chat_response():
    """Test that the orchestrator can respond to a simple query"""
    print("Testing Cortex chat with gpt-4o-mini...")
    print("-" * 50)
    
    try:
        # Initialize orchestrator
        orchestrator = Orchestrator(
            project_path=".",
            provider="openai",
            model_name="gpt-4o-mini"
        )
        
        # Test query
        query = "what is this codebase about"
        print(f"\nQuery: {query}")
        print("\nWaiting for response...")
        
        # Get response (with timeout awareness)
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Response took too long (>30s)")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            response = orchestrator.ask(query)
            signal.alarm(0)  # Cancel alarm
            
            print("\n" + "=" * 50)
            print("RESPONSE:")
            print("=" * 50)
            print(response[:500])  # Show first 500 chars
            if len(response) > 500:
                print(f"\n... (truncated, full response is {len(response)} chars)")
            
            print("\n" + "=" * 50)
            print("✅ SUCCESS! Chat is working properly.")
            print("=" * 50)
            return True
            
        except TimeoutError as e:
            signal.alarm(0)
            print(f"\n❌ FAILED: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_response()
    sys.exit(0 if success else 1)
