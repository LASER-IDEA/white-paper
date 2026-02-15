"""
Main Experiment Runner for LAEV-Baseline Comparison
IEEE VIS 2026 - Production Experiment Framework
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from data.test_queries import get_all_queries, get_query_statistics, TaskType
from data.dataset_loader import get_dataset
from baselines.nl4dv_baseline import NL4DVBaseline, DirectLLMBaseline


class ExperimentRunner:
    """
    Runs comparison experiments between LAEV-Agents and baselines
    """
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        # Load dataset
        print("Loading LAEV dataset...")
        self.dataset = get_dataset()
        
        # Initialize systems
        self.systems = {}
        
        print(f"Experiment output: {self.output_dir}")
    
    def init_nl4dv_baseline(self) -> bool:
        """Initialize NL4DV baseline"""
        print("\nInitializing NL4DV Baseline...")
        try:
            # Load real dataset first
            df = self.dataset.get_nl4dv_format()
            baseline = NL4DVBaseline()
            if baseline.load_dataframe(df, label="lae_flights"):
                self.systems["nl4dv"] = baseline
                print("✓ NL4DV baseline ready")
                return True
            else:
                print("✗ Failed to load dataset into NL4DV")
                return False
        except Exception as e:
            print(f"✗ NL4DV initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def init_direct_llm_baseline(self, provider: str = "deepseek") -> bool:
        """Initialize Direct LLM baseline"""
        print(f"\nInitializing Direct LLM Baseline ({provider})...")
        try:
            baseline = DirectLLMBaseline(llm_provider=provider)
            self.systems[f"direct_llm_{provider}"] = baseline
            print("✓ Direct LLM baseline ready")
            return True
        except Exception as e:
            print(f"✗ Direct LLM initialization failed: {e}")
            return False
    
    def init_laev_agents(self, use_full: bool = False) -> bool:
        """Initialize LAEV-Agents system"""
        print("\nInitializing LAEV-Agents...")
        try:
            from agents.orchestrator import LAEVOrchestrator
            
            # Try to get knowledge base if available
            kb = None
            try:
                from knowledge_base import initialize_knowledge_base
                kb = initialize_knowledge_base()
            except:
                print("  (Knowledge base not available, will use schema only)")
            
            orchestrator = LAEVOrchestrator(
                llm_provider="deepseek",
                use_full_agents=use_full,
                knowledge_base=kb
            )
            self.systems["laev_agents"] = orchestrator
            print("✓ LAEV-Agents ready")
            return True
        except Exception as e:
            print(f"✗ LAEV-Agents initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_comparison(self, queries: List[Any] = None, save_interval: int = 5) -> Dict[str, Any]:
        """
        Run comparison experiment
        
        Args:
            queries: List of queries to test (default: all test queries)
            save_interval: Save results every N queries
        """
        if queries is None:
            queries = get_all_queries()
        
        results = {
            "experiment_info": {
                "timestamp": datetime.now().isoformat(),
                "total_queries": len(queries),
                "systems_tested": list(self.systems.keys())
            },
            "query_results": []
        }
        
        print(f"\n{'='*80}")
        print(f"Running Comparison Experiment")
        print(f"Queries: {len(queries)}")
        print(f"Systems: {list(self.systems.keys())}")
        print(f"{'='*80}\n")
        
        for i, query_obj in enumerate(queries):
            print(f"\n[{i+1}/{len(queries)}] Query: {query_obj.query_en}")
            print(f"  Task: {query_obj.task_type.value}, Complexity: {query_obj.complexity.value}")
            
            query_result = {
                "query_id": query_obj.id,
                "query_en": query_obj.query_en,
                "query_zh": query_obj.query_zh,
                "task_type": query_obj.task_type.value,
                "complexity": query_obj.complexity.value,
                "system_results": {}
            }
            
            # Run each system
            for system_name, system in self.systems.items():
                print(f"  → Testing {system_name}...", end=" ")
                
                try:
                    start_time = time.time()
                    
                    if system_name == "nl4dv":
                        result = system.process_query(query_obj.query_en)
                    elif system_name.startswith("direct_llm"):
                        schema = self.dataset.get_domain_metadata().get("attribute_semantics", {})
                        result = system.process_query(query_obj.query_en, schema)
                    elif system_name == "laev_agents":
                        result = system.process(query_obj.query_en)
                    else:
                        result = {"success": False, "error": "Unknown system"}
                    
                    result["execution_time"] = time.time() - start_time
                    query_result["system_results"][system_name] = result
                    
                    status = "✓" if result.get("success") else "✗"
                    print(f"{status} ({result.get('execution_time', 0):.2f}s)")
                    
                except Exception as e:
                    print(f"✗ Error: {e}")
                    query_result["system_results"][system_name] = {
                        "success": False,
                        "error": str(e)
                    }
            
            results["query_results"].append(query_result)
            
            # Periodic save
            if (i + 1) % save_interval == 0:
                self._save_intermediate(results, i + 1)
        
        return results
    
    def _save_intermediate(self, results: Dict, completed: int):
        """Save intermediate results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"experiment_partial_{completed}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"  [Saved intermediate results: {filename.name}]")
    
    def save_results(self, results: Dict, filename: str = None):
        """Save final results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"experiment_final_{timestamp}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✓ Results saved to: {filepath}")
        return filepath
    
    def generate_report(self, results: Dict) -> str:
        """Generate human-readable report"""
        report_lines = [
            "=" * 80,
            "LAEV Experiment Results Report",
            "=" * 80,
            f"Generated: {results['experiment_info']['timestamp']}",
            f"Total Queries: {results['experiment_info']['total_queries']}",
            f"Systems: {', '.join(results['experiment_info']['systems_tested'])}",
            "",
            "-" * 80,
            "Summary Statistics",
            "-" * 80,
        ]
        
        # Calculate per-system statistics
        system_stats = {}
        for system_name in results['experiment_info']['systems_tested']:
            successes = 0
            total_time = 0
            count = 0
            
            for qr in results['query_results']:
                if system_name in qr['system_results']:
                    sr = qr['system_results'][system_name]
                    count += 1
                    if sr.get('success'):
                        successes += 1
                    total_time += sr.get('execution_time', 0)
            
            system_stats[system_name] = {
                "success_rate": successes / count if count > 0 else 0,
                "avg_time": total_time / count if count > 0 else 0,
                "total": count
            }
        
        for system_name, stats in system_stats.items():
            report_lines.append(f"\n{system_name}:")
            report_lines.append(f"  Success Rate: {stats['success_rate']:.1%} ({stats['total']} queries)")
            report_lines.append(f"  Avg Execution Time: {stats['avg_time']:.2f}s")
        
        # Per-task-type breakdown
        report_lines.extend([
            "",
            "-" * 80,
            "Performance by Task Type",
            "-" * 80,
        ])
        
        task_types = set(qr['task_type'] for qr in results['query_results'])
        for task_type in sorted(task_types):
            report_lines.append(f"\n{task_type}:")
            task_queries = [qr for qr in results['query_results'] if qr['task_type'] == task_type]
            
            for system_name in results['experiment_info']['systems_tested']:
                successes = sum(
                    1 for qr in task_queries
                    if qr['system_results'].get(system_name, {}).get('success')
                )
                report_lines.append(f"  {system_name}: {successes}/{len(task_queries)} ({successes/len(task_queries):.1%})")
        
        report_lines.append("\n" + "=" * 80)
        
        report = "\n".join(report_lines)
        return report


def main():
    parser = argparse.ArgumentParser(description="Run LAEV-Baseline Comparison Experiment")
    parser.add_argument("--systems", nargs="+", choices=["nl4dv", "direct_llm", "laev", "all"],
                       default=["all"], help="Systems to test")
    parser.add_argument("--queries", type=int, default=None, help="Number of queries to test (default: all)")
    parser.add_argument("--output", type=str, default="results", help="Output directory")
    parser.add_argument("--full-agents", action="store_true", help="Use full agent implementation")
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = ExperimentRunner(output_dir=args.output)
    
    # Initialize requested systems
    systems_to_init = args.systems
    if "all" in systems_to_init:
        systems_to_init = ["nl4dv", "direct_llm", "laev"]
    
    init_success = []
    if "nl4dv" in systems_to_init:
        init_success.append(runner.init_nl4dv_baseline())
    if "direct_llm" in systems_to_init:
        init_success.append(runner.init_direct_llm_baseline())
    if "laev" in systems_to_init:
        init_success.append(runner.init_laev_agents(use_full=args.full_agents))
    
    if not any(init_success):
        print("\n✗ No systems initialized successfully. Cannot run experiment.")
        sys.exit(1)
    
    # Get queries
    queries = get_all_queries()
    if args.queries:
        queries = queries[:args.queries]
    
    # Run experiment
    results = runner.run_comparison(queries)
    
    # Save results
    result_file = runner.save_results(results)
    
    # Generate and save report
    report = runner.generate_report(results)
    report_file = result_file.with_suffix('.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n✓ Report saved to: {report_file}")


if __name__ == "__main__":
    main()
