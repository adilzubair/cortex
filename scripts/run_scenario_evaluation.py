"""
AI Code Assistant Agent - Scenario Evaluation Runner

This script runs the comprehensive evaluation scenarios defined in evaluate_scenarios.py
and generates detailed reports with metrics analysis.

Usage:
    # Run all scenarios
    python scripts/run_scenario_evaluation.py
    
    # Run specific category
    python scripts/run_scenario_evaluation.py --category "Code Search"
    
    # Run specific scenario
    python scripts/run_scenario_evaluation.py --case-id CASE_01
    
    # Custom interval between requests
    python scripts/run_scenario_evaluation.py --interval 10
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# Add parent directory to path to import from project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import Orchestrator
from scripts.evaluate_scenarios import (
    EVALUATION_SCENARIOS,
    EVALUATION_METRICS,
    ScenarioCategory,
    TestScenario,
    get_scenarios_by_category,
    get_scenario_by_id
)

load_dotenv()
console = Console()


class ScenarioEvaluator:
    """Evaluates AI code assistant against defined scenarios"""
    
    def __init__(
        self,
        project_path: str = ".",
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        interval: int = 15
    ):
        self.project_path = os.path.abspath(project_path)
        self.provider = provider
        self.model = model
        self.interval = interval
        self.orchestrator = Orchestrator(
            project_path=self.project_path,
            provider=provider,
            model_name=model
        )
        self.results = []
        
    def evaluate_scenario(self, scenario: TestScenario) -> Dict[str, Any]:
        """Evaluate a single scenario"""
        console.print(f"\n[bold cyan]═══ {scenario.case_id}: {scenario.description} ═══[/bold cyan]")
        console.print(f"[dim]Category: {scenario.category.value}[/dim]")
        
        # Handle multi-turn conversations
        if isinstance(scenario.user_query, list):
            return self._evaluate_multi_turn(scenario)
        else:
            return self._evaluate_single_turn(scenario)
    
    def _evaluate_single_turn(self, scenario: TestScenario) -> Dict[str, Any]:
        """Evaluate single-turn scenario"""
        console.print(f"\n[yellow]User Query:[/yellow] {scenario.user_query}")
        
        start_time = time.time()
        total_cost = 0.0
        
        try:
            with console.status("[bold green]Agent processing...[/bold green]"):
                response = self.orchestrator.ask(scenario.user_query)
                duration = time.time() - start_time
                
            console.print("\n[bold]Agent Response:[/bold]")
            # Show preview of response
            preview = response[:500] + "..." if len(response) > 500 else response
            console.print(Markdown(preview))
            
            # Manual evaluation prompts
            console.print("\n[bold magenta]═══ Manual Evaluation ═══[/bold magenta]")
            console.print(f"[dim]Expected: {scenario.expected_behavior}[/dim]")
            console.print(f"[dim]Success Criteria: {', '.join(scenario.success_criteria)}[/dim]")
            
            # Collect metrics
            metrics = self._collect_metrics(scenario, duration, response)
            
            result = {
                "case_id": scenario.case_id,
                "category": scenario.category.value,
                "description": scenario.description,
                "query": scenario.user_query,
                "response": response,
                "duration": duration,
                "cost": total_cost,
                "metrics": metrics,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            
            return {
                "case_id": scenario.case_id,
                "category": scenario.category.value,
                "description": scenario.description,
                "query": scenario.user_query,
                "error": str(e),
                "duration": duration,
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
    
    def _evaluate_multi_turn(self, scenario: TestScenario) -> Dict[str, Any]:
        """Evaluate multi-turn conversation scenario"""
        console.print(f"\n[yellow]Multi-turn conversation ({len(scenario.user_query)} turns)[/yellow]")
        
        total_duration = 0.0
        total_cost = 0.0
        turns = []
        
        try:
            for i, query in enumerate(scenario.user_query, 1):
                console.print(f"\n[cyan]Turn {i}:[/cyan] {query}")
                
                start_time = time.time()
                with console.status(f"[bold green]Agent processing turn {i}...[/bold green]"):
                    response = self.orchestrator.ask(query)
                    duration = time.time() - start_time
                    total_duration += duration
                
                preview = response[:300] + "..." if len(response) > 300 else response
                console.print(f"[dim]{preview}[/dim]")
                
                turns.append({
                    "turn": i,
                    "query": query,
                    "response": response,
                    "duration": duration
                })
                
                # Small delay between turns
                if i < len(scenario.user_query):
                    time.sleep(2)
            
            # Manual evaluation
            console.print("\n[bold magenta]═══ Manual Evaluation ═══[/bold magenta]")
            console.print(f"[dim]Expected: {scenario.expected_behavior}[/dim]")
            console.print(f"[dim]Success Criteria: {', '.join(scenario.success_criteria)}[/dim]")
            
            # Collect metrics based on full conversation
            full_response = "\n\n".join([t["response"] for t in turns])
            metrics = self._collect_metrics(scenario, total_duration, full_response)
            
            return {
                "case_id": scenario.case_id,
                "category": scenario.category.value,
                "description": scenario.description,
                "turns": turns,
                "total_duration": total_duration,
                "cost": total_cost,
                "metrics": metrics,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            
            return {
                "case_id": scenario.case_id,
                "category": scenario.category.value,
                "description": scenario.description,
                "turns": turns,
                "error": str(e),
                "total_duration": total_duration,
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
    
    def _collect_metrics(self, scenario: TestScenario, duration: float, response: str) -> Dict[str, Any]:
        """Collect evaluation metrics using automated LLM-based scoring"""
        metrics = {}
        
        console.print("\n[bold]Automated Evaluation:[/bold]")
        
        for metric_name in scenario.evaluation_metrics:
            if metric_name == "Speed":
                # Auto-calculate speed rating
                rating = self._rate_speed(duration)
                metrics[metric_name] = {
                    "value": duration,
                    "rating": rating,
                    "auto": True
                }
                console.print(f"  {metric_name}: {duration:.2f}s → [bold]{rating}[/bold]")
            
            elif metric_name == "Cost Efficiency":
                # Estimate based on response length and duration
                estimated_cost = self._estimate_cost(response, duration)
                rating = self._rate_cost(estimated_cost)
                metrics[metric_name] = {
                    "value": estimated_cost,
                    "rating": rating,
                    "auto": True
                }
                console.print(f"  {metric_name}: ${estimated_cost:.4f} → [bold]{rating}[/bold]")
            
            else:
                # Automated LLM-based scoring
                with console.status(f"[yellow]Evaluating {metric_name}...[/yellow]"):
                    score = self._auto_evaluate_metric(metric_name, scenario, response)
                    rating = self._rate_percentage(metric_name, score)
                    metrics[metric_name] = {
                        "value": score,
                        "rating": rating,
                        "auto": True
                    }
                    console.print(f"  {metric_name}: {score}/100 → [bold]{rating}[/bold]")
        
        return metrics
    
    def _auto_evaluate_metric(self, metric_name: str, scenario: TestScenario, response: str) -> float:
        """Use LLM to automatically evaluate a metric"""
        evaluation_prompt = f"""You are an expert evaluator of AI code assistants. Evaluate the following response based on the metric: {metric_name}.

Scenario: {scenario.description}
User Query: {scenario.user_query if isinstance(scenario.user_query, str) else ' -> '.join(scenario.user_query)}

Expected Behavior: {scenario.expected_behavior}

Success Criteria:
{chr(10).join(f'- {criterion}' for criterion in scenario.success_criteria)}

Agent Response:
{response[:2000]}  # Limit to avoid token limits

Metric to Evaluate: {metric_name}

Evaluation Guidelines for {metric_name}:
"""
        
        # Add metric-specific guidelines
        if metric_name == "Accuracy":
            evaluation_prompt += """
- Did the agent provide correct information?
- Did it use appropriate tools?
- Did it find the right code/files?
- Were there any factual errors?
"""
        elif metric_name == "Robustness":
            evaluation_prompt += """
- Did the agent handle edge cases properly?
- Did it provide fallback strategies?
- Did it avoid errors or crashes?
- Did it handle ambiguity well?
"""
        elif metric_name == "User Experience":
            evaluation_prompt += """
- Was the response clear and well-formatted?
- Did it provide helpful context?
- Was the communication professional?
- Did it guide the user effectively?
"""
        elif metric_name == "Memory & Context":
            evaluation_prompt += """
- Did the agent maintain context across turns?
- Did it reference previous information correctly?
- Did it avoid redundant searches?
- Did it remember earlier decisions?
"""
        elif metric_name == "Language Understanding":
            evaluation_prompt += """
- Did the agent understand the user's intent?
- Did it interpret technical terms correctly?
- Did it handle ambiguous language well?
- Did it ask clarifying questions when needed?
"""
        
        evaluation_prompt += """
Provide a score from 0-100 where:
- 90-100: Excellent - Best possible performance
- 80-89: Good - High quality with minor issues
- 70-79: Satisfactory - Acceptable but room for improvement
- 60-69: Needs Improvement - Below expectations
- 0-59: Poor - Unsatisfactory performance

Respond with ONLY a JSON object in this exact format:
{
    "score": <number between 0-100>,
    "reasoning": "<brief explanation of the score>"
}
"""
        
        try:
            # Use the orchestrator's LLM to evaluate
            eval_response = self.orchestrator.ask(evaluation_prompt)
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{[^}]+\}', eval_response)
            if json_match:
                eval_data = json.loads(json_match.group())
                score = float(eval_data.get("score", 50))
                # Store reasoning for later analysis
                return max(0, min(100, score))  # Clamp to 0-100
            else:
                console.print(f"[yellow]Warning: Could not parse evaluation for {metric_name}, using default 50[/yellow]")
                return 50.0
                
        except Exception as e:
            console.print(f"[red]Error evaluating {metric_name}: {e}[/red]")
            return 50.0  # Default to middle score on error
    
    def _estimate_cost(self, response: str, duration: float) -> float:
        """Estimate API cost based on response characteristics"""
        # Rough estimation: ~$0.01 per 1000 tokens for gpt-4o-mini
        # Average ~4 chars per token
        estimated_tokens = (len(response) + 1000) / 4  # +1000 for prompt
        cost_per_token = 0.00001  # Approximate for gpt-4o-mini
        return estimated_tokens * cost_per_token
    
    def _rate_cost(self, cost: float) -> str:
        """Rate cost efficiency"""
        if cost < 0.01:
            return "Excellent"
        elif cost < 0.02:
            return "Good"
        elif cost < 0.05:
            return "Satisfactory"
        elif cost < 0.10:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _rate_speed(self, duration: float) -> str:
        """Rate speed based on duration"""
        if duration < 4:
            return "Excellent"
        elif duration < 5:
            return "Good"
        elif duration < 6:
            return "Satisfactory"
        elif duration < 7:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _rate_percentage(self, metric_name: str, value: float) -> str:
        """Rate percentage-based metrics"""
        if value >= 90:
            return "Excellent"
        elif value >= 80:
            return "Good"
        elif value >= 70:
            return "Satisfactory"
        elif value >= 60:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def run_evaluation(
        self,
        scenarios: List[TestScenario],
        save_report: bool = True
    ) -> List[Dict[str, Any]]:
        """Run evaluation on multiple scenarios"""
        console.print(Panel(
            f"[bold blue]AI Code Assistant Scenario Evaluation[/bold blue]\n"
            f"[bold]Project:[/bold] {self.project_path}\n"
            f"[bold]Model:[/bold] {self.provider}/{self.model}\n"
            f"[bold]Scenarios:[/bold] {len(scenarios)}\n"
            f"[bold]Interval:[/bold] {self.interval}s",
            title="Cortex Scenario Evaluator"
        ))
        
        results = []
        
        # Generate report filename at start for incremental saving
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"scenario_evaluation_report_{timestamp}.json" if save_report else None
        
        for i, scenario in enumerate(scenarios):
            if i > 0:
                console.print(f"\n[dim]⏳ Waiting {self.interval}s before next scenario...[/dim]")
                time.sleep(self.interval)
            
            console.print(f"\n[bold green]━━━ Scenario {i+1}/{len(scenarios)} ━━━[/bold green]")
            result = self.evaluate_scenario(scenario)
            results.append(result)
            
            # Save incrementally after each scenario
            if save_report:
                self._save_report(results, report_file)
                console.print(f"[dim]💾 Progress saved to {report_file}[/dim]")
        
        # Generate summary
        self._print_summary(results)
        
        # Final save confirmation
        if save_report:
            console.print(f"\n[bold green]✓ Evaluation complete![/bold green]")
            console.print(f"[bold]Report saved to:[/bold] [underline]{report_file}[/underline]")
        
        return results
    
    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print evaluation summary"""
        console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]         EVALUATION SUMMARY            [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        # Summary table
        table = Table(title="Results Overview")
        table.add_column("Case ID", style="cyan")
        table.add_column("Category", style="white")
        table.add_column("Duration", style="magenta")
        table.add_column("Status", style="bold")
        
        total_duration = 0.0
        success_count = 0
        error_count = 0
        
        for result in results:
            duration = result.get("duration") or result.get("total_duration", 0)
            total_duration += duration
            
            status = result["status"]
            if status == "completed":
                success_count += 1
                status_display = "[green]✓ PASS[/green]"
            else:
                error_count += 1
                status_display = "[red]✗ FAIL[/red]"
            
            table.add_row(
                result["case_id"],
                result["category"],
                f"{duration:.2f}s",
                status_display
            )
        
        console.print(table)
        
        # Statistics
        console.print(f"\n[bold]Statistics:[/bold]")
        console.print(f"  Total Scenarios: {len(results)}")
        console.print(f"  Successful: [green]{success_count}[/green]")
        console.print(f"  Failed: [red]{error_count}[/red]")
        console.print(f"  Success Rate: {(success_count/len(results)*100):.1f}%")
        console.print(f"  Total Duration: {total_duration:.2f}s")
        console.print(f"  Average Duration: {(total_duration/len(results)):.2f}s")
    
    def _save_report(self, results: List[Dict[str, Any]], report_file: str = None) -> str:
        """Save evaluation report to file"""
        if report_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"scenario_evaluation_report_{timestamp}.json"
        
        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "project_path": self.project_path,
                "provider": self.provider,
                "model": self.model,
                "total_scenarios": len(results),
                "successful": len([r for r in results if r["status"] == "completed"]),
                "failed": len([r for r in results if r["status"] == "error"])
            },
            "results": results
        }
        
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run AI Code Assistant Scenario Evaluation"
    )
    parser.add_argument(
        "--project-path",
        default=".",
        help="Path to project to evaluate (default: current directory)"
    )
    parser.add_argument(
        "--provider",
        default="openai",
        help="LLM provider (default: openai)"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model name (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Seconds to wait between scenarios (default: 15)"
    )
    parser.add_argument(
        "--category",
        choices=[c.value for c in ScenarioCategory],
        help="Run only scenarios from specific category"
    )
    parser.add_argument(
        "--case-id",
        help="Run only specific scenario by case ID (e.g., CASE_01)"
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List all available scenarios and exit"
    )
    
    args = parser.parse_args()
    
    # List scenarios if requested
    if args.list_scenarios:
        console.print("[bold cyan]Available Scenarios:[/bold cyan]\n")
        for category in ScenarioCategory:
            scenarios = get_scenarios_by_category(category)
            console.print(f"[bold]{category.value}[/bold] ({len(scenarios)} scenarios)")
            for scenario in scenarios:
                console.print(f"  • {scenario.case_id}: {scenario.description}")
        return
    
    # Select scenarios to run
    if args.case_id:
        scenario = get_scenario_by_id(args.case_id)
        if not scenario:
            console.print(f"[red]Error: Scenario {args.case_id} not found[/red]")
            return
        scenarios = [scenario]
    elif args.category:
        # Find matching category
        category = next(c for c in ScenarioCategory if c.value == args.category)
        scenarios = get_scenarios_by_category(category)
        if not scenarios:
            console.print(f"[red]Error: No scenarios found for category {args.category}[/red]")
            return
    else:
        scenarios = EVALUATION_SCENARIOS
    
    # Run evaluation
    evaluator = ScenarioEvaluator(
        project_path=args.project_path,
        provider=args.provider,
        model=args.model,
        interval=args.interval
    )
    
    evaluator.run_evaluation(scenarios)


if __name__ == "__main__":
    main()
