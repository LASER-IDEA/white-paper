"""
Ablation Study - Measure contribution of each component
Tests 5 system variants
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "nl4dv"))

from data.test_queries import get_all_queries
from data.dataset_loader import get_dataset
from baselines.nl4dv_baseline import DirectLLMBaseline
from agents import LAEVOrchestrator


def test_system(system, system_name, query, dataset):
    """Test a single query"""
    start = time.time()
    try:
        if system_name == "Direct-LLM":
            schema = dataset.get_domain_metadata().get("attribute_semantics", {})
            r = system.process_query(query, schema)
        else:
            r = system.process(query)
        return {
            "success": r.get("success", False),
            "time": time.time() - start,
            "iterations": r.get("iterations", 1) if system_name.startswith("LAEV") else 1
        }
    except Exception as e:
        return {"success": False, "time": time.time() - start, "error": str(e), "iterations": 0}


def main():
    print("="*70)
    print("ABLATION STUDY")
    print("="*70)
    
    # Test subset of queries (10 representative queries)
    all_queries = get_all_queries()
    test_queries = [
        all_queries[0],   # TREND-01
        all_queries[2],   # TREND-03 (complex)
        all_queries[3],   # COMP-01
        all_queries[5],   # COMP-03 (complex)
        all_queries[9],   # DIST-01
        all_queries[11],  # DIST-03 (complex)
        all_queries[13],  # CORR-02 (medium)
        all_queries[16],  # EXPL-02
        all_queries[20],  # ANOM-01
        all_queries[29],  # SUMM-01
    ]
    
    print(f"\nTesting {len(test_queries)} queries across 5 system variants")
    print("-"*70)
    
    dataset = get_dataset()
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Initialize systems
    print("\nInitializing systems...")
    
    # V1: Direct LLM (baseline)
    direct = DirectLLMBaseline()
    print("  ✓ V1: Direct LLM")
    
    # V2: LAEV-NoRAG (only LLM, no RAG at all)
    laev_norag = LAEVOrchestrator(use_full_agents=False, max_iterations=1)
    # Disable RAG by setting knowledge_base to None and graph_store to None
    if hasattr(laev_norag.agents.get('retriever'), 'knowledge_base'):
        laev_norag.agents['retriever'].knowledge_base = None
    if hasattr(laev_norag.agents.get('retriever'), 'graph_store'):
        laev_norag.agents['retriever'].graph_store = None
    print("  ✓ V2: LAEV-NoRAG")
    
    # V3: LAEV-VectorRAG (vector only, no GraphRAG)
    laev_vector = LAEVOrchestrator(use_full_agents=False, max_iterations=1)
    # Keep knowledge_base but disable graph
    if hasattr(laev_vector.agents.get('retriever'), 'graph_store'):
        laev_vector.agents['retriever'].graph_store = None
    print("  ✓ V3: LAEV-VectorRAG")
    
    # V4: LAEV-FullRAG (vector + GraphRAG, single pass)
    laev_fullrag = LAEVOrchestrator(use_full_agents=False, max_iterations=1)
    print("  ✓ V4: LAEV-FullRAG (single pass)")
    
    # V5: LAEV-Full (vector + GraphRAG + multi-iteration)
    laev_full = LAEVOrchestrator(use_full_agents=False, max_iterations=3)
    print("  ✓ V5: LAEV-Full (multi-iteration)")
    
    systems = {
        "V1-Direct-LLM": direct,
        "V2-NoRAG": laev_norag,
        "V3-VectorRAG": laev_vector,
        "V4-FullRAG-Single": laev_fullrag,
        "V5-Full-Multi": laev_full
    }
    
    # Run experiments
    results = {name: [] for name in systems.keys()}
    
    print("\n" + "="*70)
    print("RUNNING EXPERIMENTS")
    print("="*70)
    
    for i, q in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] {q.id}: {q.query_en[:45]}...")
        
        for sys_name, system in systems.items():
            print(f"  {sys_name:20s}...", end=" ", flush=True)
            r = test_system(system, sys_name, q.query_en, dataset)
            results[sys_name].append(r)
            status = "✓" if r["success"] else "✗"
            print(f"{status} ({r['time']:.1f}s)")
    
    # Analysis
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    summary = {}
    for sys_name, sys_results in results.items():
        total = len(sys_results)
        successes = sum(1 for r in sys_results if r["success"])
        avg_time = sum(r["time"] for r in sys_results) / total
        avg_iter = sum(r["iterations"] for r in sys_results) / total
        
        summary[sys_name] = {
            "success_rate": successes / total,
            "avg_time": avg_time,
            "avg_iterations": avg_iter,
            "successes": successes,
            "total": total
        }
        
        print(f"\n{sys_name}:")
        print(f"  Success Rate: {successes}/{total} ({successes/total*100:.1f}%)")
        print(f"  Avg Time: {avg_time:.1f}s")
        if "LAEV" in sys_name:
            print(f"  Avg Iterations: {avg_iter:.1f}")
    
    # Component contribution analysis
    print("\n" + "-"*70)
    print("COMPONENT CONTRIBUTION ANALYSIS")
    print("-"*70)
    
    baseline = summary["V1-Direct-LLM"]["success_rate"]
    
    print(f"\nBaseline (Direct LLM): {baseline*100:.1f}%")
    
    # RAG contribution
    norag = summary["V2-NoRAG"]["success_rate"]
    vectorrag = summary["V3-VectorRAG"]["success_rate"]
    fullrag = summary["V4-FullRAG-Single"]["success_rate"]
    fullmulti = summary["V5-Full-Multi"]["success_rate"]
    
    print(f"\nIncremental Improvements:")
    print(f"  + Multi-Agent Pipeline: {(norag-baseline)*100:+.1f}%")
    print(f"  + Vector RAG: {(vectorrag-norag)*100:+.1f}%")
    print(f"  + GraphRAG: {(fullrag-vectorrag)*100:+.1f}%")
    print(f"  + Multi-Iteration: {(fullmulti-fullrag)*100:+.1f}%")
    print(f"  = Total Improvement: {(fullmulti-baseline)*100:+.1f}%")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "queries": [{"id": q.id, "text": q.query_en} for q in test_queries],
        "raw_results": results,
        "summary": summary
    }
    
    output_file = results_dir / "ablation_study_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to: {output_file}")
    print("="*70)


if __name__ == "__main__":
    main()
