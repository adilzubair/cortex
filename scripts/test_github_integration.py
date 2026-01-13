#!/usr/bin/env python3
"""
Test script to verify GitHub repository integration.
This script tests the GitHub cloning and indexing functionality.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.loaders.github import load_github_repo
from ingestion.pipeline import ingest_and_index

def test_github_loader():
    """Test the GitHub loader with a small public repo."""
    print("=" * 60)
    print("Testing GitHub Repository Loader")
    print("=" * 60)
    
    # Use a small, well-known repo for testing
    test_repo = "https://github.com/octocat/Hello-World.git"
    
    print(f"\n1. Testing load_github_repo() with: {test_repo}")
    try:
        docs, clone_path = load_github_repo(test_repo)
        print(f"   ✓ Successfully cloned to: {clone_path}")
        print(f"   ✓ Loaded {len(docs)} documents")
        
        # Verify the path exists
        if os.path.exists(clone_path):
            print(f"   ✓ Clone path exists and is persistent")
        else:
            print(f"   ✗ ERROR: Clone path does not exist!")
            return False
            
        # Check expected location
        expected_path = Path.home() / ".cortex" / "repos" / "Hello-World"
        if Path(clone_path) == expected_path:
            print(f"   ✓ Cloned to expected location")
        else:
            print(f"   ⚠ Warning: Unexpected clone location")
            print(f"     Expected: {expected_path}")
            print(f"     Got: {clone_path}")
        
        # Check metadata
        if docs:
            sample_doc = docs[0]
            print(f"\n2. Checking document metadata:")
            print(f"   - source: {sample_doc.metadata.get('source')}")
            print(f"   - repo: {sample_doc.metadata.get('repo')}")
            print(f"   - repo_url: {sample_doc.metadata.get('repo_url')}")
            
        return True
        
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_integration():
    """Test the full pipeline with GitHub URL."""
    print("\n" + "=" * 60)
    print("Testing Pipeline Integration")
    print("=" * 60)
    
    test_repo = "https://github.com/octocat/Hello-World.git"
    
    print(f"\n3. Testing ingest_and_index() with GitHub URL")
    try:
        num_indexed, project_path = ingest_and_index(test_repo, "github")
        print(f"   ✓ Indexed {num_indexed} files")
        print(f"   ✓ Project path: {project_path}")
        
        # Verify .cortex directory was created
        cortex_dir = os.path.join(project_path, ".cortex")
        if os.path.exists(cortex_dir):
            print(f"   ✓ .cortex directory created at: {cortex_dir}")
        else:
            print(f"   ✗ ERROR: .cortex directory not found!")
            return False
            
        return True
        
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🧪 GitHub Integration Test Suite\n")
    
    results = []
    
    # Test 1: GitHub loader
    results.append(("GitHub Loader", test_github_loader()))
    
    # Test 2: Pipeline integration
    results.append(("Pipeline Integration", test_pipeline_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("🎉 All tests passed!" if all_passed else "❌ Some tests failed"))
    
    sys.exit(0 if all_passed else 1)
