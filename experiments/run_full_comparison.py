"""
Full Comparison Experiment - 32 Queries, 3 Systems
IEEE VIS 2026 - Complete baseline comparison
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "nl4dv"))

from data.test_queries import get_all_queries
from data.dataset_loader import get_dataset
from baselines.nl4dv_baseline import NL4DVBaseline, DirectLLMBaseline
from agents import LAEVOrchestrator


class FullComparisonExperiment:
    """Run complete comparison across all systems"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent / "results"
        self.output_dir.mkdir(exist_ok=True)
        
        print("Loading dataset...")
        self.dataset = get_dataset()
        
        # Results storage
        self.results = {
            "experiment_info": {
                "timestamp": datetime.now().isoformat(),
                "total_queries": 0,
                "systems": ["nl4dv", "direct_llm", "laev_agents"]
            },
            "query_results": []
        }
    
    def init_nl4dv(self):
        """Initialize NL4DV baseline"""
        print("\nInitializing NL4DV...")
        try:
            baseline = NL4DVBaseline()
            df = self.dataset.get_nl4dv_format()
            if baseline.load_dataframe(df, "lae_full"):
                print("  ✓ NL4DV ready")
                return baseline
        except Exception as e:
            print(f"  ✗ NL4DV failed: {e}")
        return None
    
    def init_direct_llm(self):
        """Initialize Direct LLM baseline"""
        print("\nInitializing Direct LLM...")
        try:
            baseline = DirectLLMBaseline()
            print("  ✓ Direct LLM ready")
            return baseline
        except Exception as e:
            print(f"  ✗ Direct LLM failed: {e}")
        return None
    
    def init_laev(self):
        """Initialize LAEV-Agents"""
        print("\nInitializing LAEV-Agents...")
        try:
            orchestrator = LAEVOrchestrator(
                use_full_agents=False,
                max_iterations=3
            )
            print("  ✓ LAEV-Agents ready")
            return orchestrator
        except Exception as e:
            print(f"  ✗ LAEV-Agents failed: {e}")
            import traceback
            traceback.print_exc()
        return None
    
    def run_system(self, system, system_name: str, query: str, query_id: str) -> Dict:
        """Run single query on a system"""
        start_time = time.time()
        
        try:
            if system_name == "nl4dv":
                result = system.process_query(query)
                return {
                    "success": result.get("success", False),
                    "execution_time": time.time() - start_time,
                    "chart_type": result.get("chart_type"),
                    "error": result.get("error")
                }
            
            elif system_name == "direct_llm":
                schema = self.dataset.get_domain_metadata().get("attribute_semantics", {})
                result = system.process_query(query, schema)
                return {
                    "success": result.get("success", False),
                    "execution_time": time.time() - start_time,
                    "generated_code": result.get("generated_code", "")[:500] if result.get("generated_code") else None,
                    "error": result.get("error")
                }
            
            elif system_name == "laev_agents":
                result = system.process(query)
                return {
                    "success": result.get("success", False),
                    "execution_time": time.time() - start_time,
                    "iterations": result.get("iterations", 1),
                    "chart_code": result.get("chart_code", "")[:500] if result.get("chart_code") else None,
                    "error": result.get("error")
                }
        
        except Exception as e:
            return {
                "success": False,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def run_experiment(self):
        """Run full experiment"""
        queries = get_all_queries()
        print(f"\nTotal queries to test: {len(queries)}")
        
        # Initialize systems
        systems = {
            "nl4dv": self.init_nl4dv(),
            "direct_llm": self.init_direct_llm(),
            "laev_agents": self.init_laev()
        }
        
        # Filter out failed systems
        active_systems = {k: v for k, v in systems.items() if v is not None}
        print(f"\nActive systems: {list(active_systems.keys())}")
        
        # Run experiments
        print("\n" + "="*70)
        print("RUNNING EXPERIMENTS")
        print("="*70)
        
        for i, query_obj in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] {query_obj.id}: {query_obj.query_en}")
            print(f"    Task: {query_obj.task_type.value}, Complexity: {query_obj.complexity.value}")
            
            query_result = {
                "query_id": query_obj.id,
                "query_en": query_obj.query_en,
                "query_zh": query_obj.query_zh,
                "task_type": query_obj.task_type.value,
                "complexity": query_obj.complexity.value,
                "system_results": {}
            }
            
            for system_name, system in active_systems.items():
                print(f"    → {system_name}...", end=" ", flush=True)
                result = self.run_system(system, system_name, query_obj.query_en, query_obj.id)
                query_result["system_results"][system_name] = result
                
                status = "✓" if result["success"] else "✗"
                print(f"{status} ({result['execution_time']:.1f}s)")
            
            self.results["query_results"].append(query_result)
            
            # Save intermediate results every 5 queries
            if i % 5 == 0:
                self.save_intermediate(i)
        
        self.results["experiment_info"]["total_queries"] = len(queries)
        
        return self.results
    
    def save_intermediate(self, completed: int):
        """Save intermediate results"""
        filename = self.output_dir / f"full_comparison_partial_{completed}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        print(f"    [Saved checkpoint: {filename.name}]")
    
    def analyze_results(self) -> Dict[str, Any]:
        """Analyze and summarize results"""
        analysis = {
            "summary": {},
            "by_task": {},
            "by_complexity": {}
        }
        
        # Overall stats per system
        systems = self.results["experiment_info"]["systems"]
        for system_name in systems:
            system_results = [
                qr["system_results"].get(system_name, {})
                for qr in self.results["query_results"]
            ]
            
            successes = sum(1 for r in system_results if r.get("success"))
            total = len(system_results)
            avg_time = sum(r.get("execution_time", 0) for r in system_results) / total if total > 0 else 0
            
            analysis["summary"][system_name] = {
                "total": total,
                "successes": successes,
                "success_rate": successes / total if total > 0 else 0,
                "avg_execution_time": round(avg_time, 2)
            }
            
            # Add iteration stats for LAEV
            if system_name == "laev_agents":
                avg_iters = sum(r.get("iterations", 1) for r in system_results) / total if total > 0 else 0
                analysis["summary"][system_name]["avg_iterations"] = round(avg_iters, 2)
        
        # By task type
        task_types = set(qr["task_type"] for qr in self.results["query_results"])
        for task_type in task_types:
            task_queries = [qr for qr in self.results["query_results"] if qr["task_type"] == task_type]
            analysis["by_task"][task_type] = {}
            
            for system_name in systems:
                successes = sum(
                    1 for qr in task_queries
                    if qr["system_results"].get(system_name, {}).get("success")
                )
                analysis["by_task"][task_type][system_name] = {
                    "successes": successes,
                    "total": len(task_queries),
                    "rate": successes / len(task_queries) if task_queries else 0
                }
        
        return analysis
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable report"""
        lines = [
            "="*70,
            "FULL COMPARISON EXPERIMENT REPORT",
            "="*70,
            f"Generated: {self.results['experiment_info']['timestamp']}",
            f"Total Queries: {self.results['experiment_info']['total_queries']}",
            "",
            "-"*70,
            "OVERALL RESULTS",
            "-"*70,
            ""
        ]
        
        for system_name, stats in analysis["summary"].items():
            lines.append(f"\n{system_name.upper()}:")
            lines.append(f"  Success Rate: {stats['successes']}/{stats['total']} ({stats['success_rate']:.1%})")
            lines.append(f"  Avg Time: {stats['avg_execution_time']:.2f}s")
            if "avg_iterations" in stats:
                lines.append(f"  Avg Iterations: {stats['avg_iterations']}")
        
        # By task type
        lines.extend([
            "",
            "-"*70,
            "RESULTS BY TASK TYPE",
            "-"*70,
            ""
        ])
        
        for task_type, systems in analysis["by_task"].items():
            lines.append(f"\n{task_type}:")
            for system_name, stats in systems.items():
                lines.append(f"  {system_name}: {stats['successes']}/{stats['total']} ({stats['rate']:.1%})")
        
        # Comparison
        lines.extend([
            "",
            "-"*70,
            "COMPARISON ANALYSIS",
            "-"*70,
            ""
        ])
        
        summary = analysis["summary"]
        if "laev_agents" in summary and "direct_llm" in summary:
            laev_rate = summary["laev_agents"]["success_rate"]
            direct_rate = summary["direct_llm"]["success_rate"]
            improvement = laev_rate - direct_rate
            lines.append(f"LAEV vs Direct LLM: {improvement:+.1%}")
        
        if "nl4dv" in summary:
            nl4dv_rate = summary["nl4dv"]["success_rate"]
            lines.append(f"NL4DV Success Rate: {nl4dv_rate:.1%}")
        
        lines.extend([
            "",
            "="*70
        ])
        
        return "\n".join(lines)
    
    def save_results(self, analysis: Dict):
        """Save all results"""
        # Main results
        results_file = self.output_dir / "full_comparison_final.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        
        # Analysis
        analysis_file = self.output_dir / "full_comparison_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Results saved:")
        print(f"  - {results_file}")
        print(f"  - {analysis_file}")
    
    def run(self):
        """Execute full experiment workflow"""
        print("="*70)
        print("FULL COMPARISON EXPERIMENT")
        print("="*70)
        
        # Run experiments
        self.run_experiment()
        
        # Analyze
        print("\n" + "="*70)
        print("ANALYZING RESULTS")
        print("="*70)
        analysis = self.analyze_results()
        
        # Save
        self.save_results(analysis)
        
        # Report
        report = self.generate_report(analysis)
        print("\n" + report)
        
        # Save report
        report_file = self.output_dir / "full_comparison_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ Report saved: {report_file}")


def main():
    experiment = FullComparisonExperiment()
    experiment.run()


if __name__ == "__main__":
    main()
