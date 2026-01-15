#!/usr/bin/env python3
"""
Quick demo of the automated evaluation system.
Runs a single simple scenario to show how it works.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_scenario_evaluation import ScenarioEvaluator
from scripts.evaluate_scenarios import get_scenario_by_id

def main():
    print("=" * 60)
    print("AUTOMATED EVALUATION DEMO")
    print("=" * 60)
    print("\nThis will run CASE_01 (basic greeting) to demonstrate")
    print("the automated evaluation system.\n")
    
    input("Press Enter to start...")
    
    # Create evaluator
    evaluator = ScenarioEvaluator(
        project_path=".",
        provider="openai",
        model="gpt-4o-mini",
        interval=0  # No wait for single scenario
    )
    
    # Get the first scenario (simple greeting)
    scenario = get_scenario_by_id("CASE_01")
    
    # Run evaluation
    results = evaluator.run_evaluation([scenario], save_report=True)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print("\nKey features demonstrated:")
    print("✓ Automated query execution")
    print("✓ LLM-based metric evaluation")
    print("✓ Automatic scoring (0-100)")
    print("✓ Rating classification (Excellent/Good/etc.)")
    print("✓ JSON report generation")
    print("\nNo manual input required - fully automated!")

if __name__ == "__main__":
    main()
