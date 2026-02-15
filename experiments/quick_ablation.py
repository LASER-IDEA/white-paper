"""
Quick Ablation Study - Tests 3 key variants
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from data.test_queries import get_queries_by_task, TaskType
from data.dataset_loader import get_dataset
from agents import LAEVOrchestrator
from baselines.nl4dv_baseline import DirectLLMBaseline


def test_system(system, query, is_direct_llm=False):
    """Test a single query"""
    start = time.time()
    try:
        if is_direct_llm:
            dataset = get_dataset()
            schema = dataset.get_domain_metadata().get("attribute_semantics", {})
            result = system.process_query(query, schema)
            return {
                "success": result.get("success", False),
                "time": time.time() - start,
                "iterations": 1
            }
        else:
            result = system.process(query)
            return {
                "success": result.get("success", False),
                "time": time.time() - start,
                "iterations": result.get("iterations", 1)
            }
    except Exception as e:
        return {
            "success": False,
            "time": time.time() - start,
            "error": str(e),
            "iterations": 0
        }


def main():
    print("="*70)
    print("QUICK ABLATION STUDY")
    print("="*70)
    
    # Test queries (3 per task type)
    test_queries = []
    for task in [TaskType.TREND_ANALYSIS, TaskType.COMPARISON, TaskType.DISTRIBUTION]:
        queries = get_queries_by_task(task)[:2]  # First 2 per task
        test_queries.extend(queries)
    
    print(f"\nTesting {len(test_queries)} queries...")
    for q in test_queries:
        print(f"  - {q.id}: {q.query_en}")
    
    results = {}
    
    # 1. Direct LLM
    print("\n" + "-"*70)
    print("1. Direct LLM Baseline")
    print("-"*70)
    direct = DirectLLMBaseline()
    results["Direct-LLM"] = []
    for q in test_queries:
        print(f"  {q.id}...", end=" ", flush=True)
        r = test_system(direct, q.query_en, is_direct_llm=True)
        results["Direct-LLM"].append(r)
        status = "✓" if r["success"] else "✗"
        print(f"{status} ({r['time']:.1f}s)")
    
    # 2. LAEV Single Pass
    print("\n" + "-"*70)
    print("2. LAEV Single Pass (1 iteration)")
    print("-"*70)
    laev_single = LAEVOrchestrator(use_full_agents=False, max_iterations=1)
    results["LAEV-SinglePass"] = []
    for q in test_queries:
        print(f"  {q.id}...", end=" ", flush=True)
        r = test_system(laev_single, q.query_en)
        results["LAEV-SinglePass"].append(r)
        status = "✓" if r["success"] else "✗"
        print(f"{status} ({r['time']:.1f}s, {r['iterations']} iter)")
    
    # 3. LAEV Full (Multi-iteration)
    print("\n" + "-"*70)
    print("3. LAEV Full (up to 3 iterations)")
    print("-"*70)
    laev_full = LAEVOrchestrator(use_full_agents=False, max_iterations=3)
    results["LAEV-Full"] = []
    for q in test_queries:
        print(f"  {q.id}...", end=" ", flush=True)
        r = test_system(laev_full, q.query_en)
        results["LAEV-Full"].append(r)
        status = "✓" if r["success"] else "✗"
        print(f"{status} ({r['time']:.1f}s, {r['iterations']} iter)")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for system_name, system_results in results.items():
        total = len(system_results)
        successes = sum(1 for r in system_results if r["success"])
        avg_time = sum(r["time"] for r in system_results) / total
        avg_iter = sum(r["iterations"] for r in system_results) / total
        
        print(f"\n{system_name}:")
        print(f"  Success Rate: {successes}/{total} ({successes/total:.1%})")
        print(f"  Avg Time: {avg_time:.1f}s")
        print(f"  Avg Iterations: {avg_iter:.1f}")
    
    # Calculate improvements
    print("\n" + "-"*70)
    print("IMPROVEMENTS")
    print("-"*70)
    
    direct_rate = sum(1 for r in results["Direct-LLM"] if r["success"]) / len(results["Direct-LLM"])
    single_rate = sum(1 for r in results["LAEV-SinglePass"] if r["success"]) / len(results["LAEV-SinglePass"])
    full_rate = sum(1 for r in results["LAEV-Full"] if r["success"]) / len(results["LAEV-Full"])
    
    print(f"\nMulti-Agent vs Direct LLM: {full_rate - direct_rate:+.1%}")
    print(f"Iteration Benefit: {full_rate - single_rate:+.1%}")
    
    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "quick_ablation.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_dir / 'quick_ablation.json'}")
    print("="*70)


if __name__ == "__main__":
    main()
