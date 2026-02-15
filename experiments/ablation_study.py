"""
Ablation Study for LAEV-Agents
Tests the contribution of each component
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from data.test_queries import get_all_queries, get_queries_by_task
from data.dataset_loader import get_dataset
from baselines.nl4dv_baseline import DirectLLMBaseline


@dataclass
class AblationResult:
    """Result of an ablation experiment"""
    system_name: str
    query_id: str
    query: str
    success: bool
    execution_time: float
    error: str = None
    iterations: int = 1


class AblationStudy:
    """
    Ablation study to evaluate contribution of each component:
    
    1. LAEV-Full: Complete system with all components
    2. LAEV-NoGraphRAG: Remove GraphRAG, keep Vector RAG only
    3. LAEV-NoRAG: Remove all RAG, use only LLM
    4. LAEV-SingleAgent: Single-pass, no iteration
    5. Direct-LLM: Direct LLM prompting (baseline)
    """
    
    SYSTEM_VARIANTS = [
        ("LAEV-Full", "Full system with all components"),
        ("LAEV-NoGraphRAG", "Without GraphRAG (Vector RAG only)"),
        ("LAEV-NoRAG", "Without any RAG (LLM only)"),
        ("LAEV-SinglePass", "Single pass, no iteration"),
        ("Direct-LLM", "Direct LLM prompting"),
    ]
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        print("Loading dataset...")
        self.dataset = get_dataset()
        
        # Load extracted entities for GraphRAG
        self.entity_file = self.output_dir / "extracted_entities.json"
        
    def init_system(self, variant: str):
        """Initialize a specific system variant"""
        if variant == "Direct-LLM":
            return DirectLLMBaseline()
        
        # For LAEV variants
        from agents.orchestrator import LAEVOrchestrator
        
        if variant == "LAEV-Full":
            return LAEVOrchestrator(
                use_full_agents=False,
                max_iterations=3,
                knowledge_base=None  # Will use schema + GraphRAG
            )
        
        elif variant == "LAEV-NoGraphRAG":
            # Create orchestrator but disable GraphRAG in retriever
            # This requires modifying the retriever to skip graph search
            orchestrator = LAEVOrchestrator(
                use_full_agents=False,
                max_iterations=3
            )
            # Disable graph store
            if hasattr(orchestrator.agents.get('retriever'), 'graph_store'):
                orchestrator.agents['retriever'].graph_store = None
            return orchestrator
        
        elif variant == "LAEV-NoRAG":
            # Disable both vector and graph RAG
            orchestrator = LAEVOrchestrator(
                use_full_agents=False,
                max_iterations=3,
                knowledge_base=None
            )
            # Disable all retrieval
            if hasattr(orchestrator.agents.get('retriever'), 'graph_store'):
                orchestrator.agents['retriever'].graph_store = None
            return orchestrator
        
        elif variant == "LAEV-SinglePass":
            return LAEVOrchestrator(
                use_full_agents=False,
                max_iterations=1
            )
        
        else:
            raise ValueError(f"Unknown variant: {variant}")
    
    def run_query(self, system, query: str, system_name: str) -> AblationResult:
        """Run a single query on a system"""
        start_time = time.time()
        
        try:
            if system_name == "Direct-LLM":
                schema = self.dataset.get_domain_metadata().get("attribute_semantics", {})
                result = system.process_query(query, schema)
                return AblationResult(
                    system_name=system_name,
                    query_id="",
                    query=query,
                    success=result.get("success", False),
                    execution_time=time.time() - start_time,
                    error=result.get("error")
                )
            else:
                # LAEV orchestrator
                result = system.process(query)
                return AblationResult(
                    system_name=system_name,
                    query_id="",
                    query=query,
                    success=result.get("success", False),
                    execution_time=time.time() - start_time,
                    error=result.get("error"),
                    iterations=result.get("iterations", 1)
                )
        except Exception as e:
            return AblationResult(
                system_name=system_name,
                query_id="",
                query=query,
                success=False,
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    def run_ablation(self, queries: List = None, variants: List[str] = None):
        """Run ablation study on all variants"""
        if queries is None:
            # Use a subset of queries for ablation
            queries = get_all_queries()[:10]  # First 10 queries
        
        if variants is None:
            variants = [v[0] for v in self.SYSTEM_VARIANTS]
        
        print("\n" + "="*70)
        print("ABLATION STUDY")
        print("="*70)
        print(f"Queries: {len(queries)}")
        print(f"Variants: {', '.join(variants)}")
        print("="*70 + "\n")
        
        results = []
        
        for variant in variants:
            print(f"\nTesting: {variant}")
            print("-"*70)
            
            try:
                system = self.init_system(variant)
                print(f"  ✓ System initialized")
            except Exception as e:
                print(f"  ✗ Failed to initialize: {e}")
                continue
            
            for i, query_obj in enumerate(queries):
                print(f"  [{i+1}/{len(queries)}] {query_obj.id}: {query_obj.query_en[:40]}...", end=" ")
                
                result = self.run_query(system, query_obj.query_en, variant)
                result.query_id = query_obj.id
                results.append(result)
                
                status = "✓" if result.success else "✗"
                print(f"{status} ({result.execution_time:.1f}s)")
        
        return results
    
    def analyze_results(self, results: List[AblationResult]) -> Dict[str, Any]:
        """Analyze ablation results"""
        from collections import defaultdict
        
        # Group by system
        by_system = defaultdict(list)
        for r in results:
            by_system[r.system_name].append(r)
        
        analysis = {}
        
        for system_name, system_results in by_system.items():
            total = len(system_results)
            successes = sum(1 for r in system_results if r.success)
            avg_time = sum(r.execution_time for r in system_results) / total if total > 0 else 0
            
            analysis[system_name] = {
                "total_queries": total,
                "successes": successes,
                "success_rate": successes / total if total > 0 else 0,
                "avg_execution_time": round(avg_time, 2),
                "failures": [r.query_id for r in system_results if not r.success]
            }
            
            # Add iteration stats for LAEV systems
            if system_name.startswith("LAEV"):
                avg_iters = sum(r.iterations for r in system_results) / total if total > 0 else 0
                analysis[system_name]["avg_iterations"] = round(avg_iters, 2)
        
        return analysis
    
    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate ablation study report"""
        lines = [
            "="*70,
            "ABLATION STUDY REPORT",
            "="*70,
            "",
            "This study evaluates the contribution of each component",
            "by comparing different system variants.",
            "",
            "-"*70,
            "Results by System Variant",
            "-"*70,
            ""
        ]
        
        for system_name, stats in analysis.items():
            lines.append(f"\n{system_name}:")
            lines.append(f"  Success Rate: {stats['success_rate']:.1%} ({stats['successes']}/{stats['total_queries']})")
            lines.append(f"  Avg Time: {stats['avg_execution_time']:.2f}s")
            
            if 'avg_iterations' in stats:
                lines.append(f"  Avg Iterations: {stats['avg_iterations']}")
            
            if stats['failures']:
                lines.append(f"  Failures: {', '.join(stats['failures'][:5])}")
        
        # Calculate component contributions
        lines.extend([
            "",
            "-"*70,
            "Component Contribution Analysis",
            "-"*70,
            ""
        ])
        
        if "LAEV-Full" in analysis and "Direct-LLM" in analysis:
            full_rate = analysis["LAEV-Full"]["success_rate"]
            direct_rate = analysis["Direct-LLM"]["success_rate"]
            improvement = full_rate - direct_rate
            lines.append(f"Full System vs Direct LLM: {improvement:+.1%} improvement")
        
        if "LAEV-Full" in analysis and "LAEV-NoGraphRAG" in analysis:
            full_rate = analysis["LAEV-Full"]["success_rate"]
            no_graph_rate = analysis["LAEV-NoGraphRAG"]["success_rate"]
            graph_contrib = full_rate - no_graph_rate
            lines.append(f"GraphRAG Contribution: {graph_contrib:+.1%}")
        
        if "LAEV-Full" in analysis and "LAEV-SinglePass" in analysis:
            full_rate = analysis["LAEV-Full"]["success_rate"]
            single_rate = analysis["LAEV-SinglePass"]["success_rate"]
            iteration_contrib = full_rate - single_rate
            lines.append(f"Multi-Agent Iteration Contribution: {iteration_contrib:+.1%}")
        
        lines.extend([
            "",
            "="*70
        ])
        
        return "\n".join(lines)
    
    def save_results(self, results: List[AblationResult], analysis: Dict[str, Any]):
        """Save results to files"""
        # Save raw results
        results_data = [
            {
                "system": r.system_name,
                "query_id": r.query_id,
                "query": r.query,
                "success": r.success,
                "execution_time": r.execution_time,
                "error": r.error,
                "iterations": r.iterations
            }
            for r in results
        ]
        
        results_file = self.output_dir / "ablation_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        # Save analysis
        analysis_file = self.output_dir / "ablation_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to:")
        print(f"  - {results_file}")
        print(f"  - {analysis_file}")
    
    def run(self):
        """Run complete ablation study"""
        # Run experiments
        results = self.run_ablation()
        
        # Analyze
        analysis = self.analyze_results(results)
        
        # Save
        self.save_results(results, analysis)
        
        # Report
        report = self.generate_report(analysis)
        print("\n" + report)
        
        # Save report
        report_file = self.output_dir / "ablation_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {report_file}")


def main():
    """Main entry point"""
    study = AblationStudy()
    study.run()


if __name__ == "__main__":
    main()
