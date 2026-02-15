"""
Continue full comparison experiment from checkpoint
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "nl4dv"))

from data.test_queries import get_all_queries
from data.dataset_loader import get_dataset
from baselines.nl4dv_baseline import NL4DVBaseline, DirectLLMBaseline
from agents import LAEVOrchestrator


def main():
    print("="*70)
    print("CONTINUE FULL COMPARISON EXPERIMENT")
    print("="*70)
    
    # Load checkpoint
    results_dir = Path(__file__).parent / "results"
    checkpoint_file = results_dir / "full_comparison_partial_20.json"
    
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)
        completed_ids = {qr["query_id"] for qr in data["query_results"]}
        print(f"\nLoaded checkpoint: {len(data['query_results'])} queries completed")
    else:
        data = {
            "experiment_info": {"timestamp": "", "total_queries": 32, "systems": ["nl4dv", "direct_llm", "laev_agents"]},
            "query_results": []
        }
        completed_ids = set()
        print("\nStarting fresh experiment")
    
    # Get remaining queries
    all_queries = get_all_queries()
    remaining = [q for q in all_queries if q.id not in completed_ids]
    
    print(f"Total queries: {len(all_queries)}")
    print(f"Completed: {len(completed_ids)}")
    print(f"Remaining: {len(remaining)}")
    
    if not remaining:
        print("\n✓ All queries already completed!")
        return
    
    # Initialize systems
    print("\n" + "-"*70)
    print("Initializing systems...")
    print("-"*70)
    
    dataset = get_dataset()
    
    # NL4DV
    try:
        nl4dv = NL4DVBaseline()
        nl4dv.load_dataframe(dataset.get_nl4dv_format(), "lae")
        print("✓ NL4DV ready")
    except Exception as e:
        print(f"✗ NL4DV failed: {e}")
        nl4dv = None
    
    # Direct LLM
    try:
        direct = DirectLLMBaseline()
        print("✓ Direct LLM ready")
    except Exception as e:
        print(f"✗ Direct LLM failed: {e}")
        direct = None
    
    # LAEV-Agents
    try:
        laev = LAEVOrchestrator(use_full_agents=False, max_iterations=1)
        print("✓ LAEV-Agents ready")
    except Exception as e:
        print(f"✗ LAEV-Agents failed: {e}")
        laev = None
    
    systems = {"nl4dv": nl4dv, "direct_llm": direct, "laev_agents": laev}
    active = {k: v for k, v in systems.items() if v is not None}
    
    print(f"\nActive systems: {list(active.keys())}")
    
    # Run remaining queries
    print("\n" + "="*70)
    print("RUNNING REMAINING QUERIES")
    print("="*70)
    
    for i, query_obj in enumerate(remaining, 1):
        print(f"\n[{i}/{len(remaining)}] {query_obj.id}: {query_obj.query_en[:50]}...")
        
        query_result = {
            "query_id": query_obj.id,
            "query_en": query_obj.query_en,
            "query_zh": query_obj.query_zh,
            "task_type": query_obj.task_type.value,
            "complexity": query_obj.complexity.value,
            "system_results": {}
        }
        
        # Test each system
        for sys_name, system in active.items():
            print(f"  → {sys_name}...", end=" ", flush=True)
            start = time.time()
            
            try:
                if sys_name == "nl4dv":
                    r = system.process_query(query_obj.query_en)
                elif sys_name == "direct_llm":
                    schema = dataset.get_domain_metadata().get("attribute_semantics", {})
                    r = system.process_query(query_obj.query_en, schema)
                else:  # laev
                    r = system.process(query_obj.query_en)
                
                result = {
                    "success": r.get("success", False),
                    "execution_time": time.time() - start,
                    "error": r.get("error")
                }
                
                if sys_name == "laev_agents":
                    result["iterations"] = r.get("iterations", 1)
                    if r.get("visual_feedback"):
                        result["visual_score"] = r["visual_feedback"].get("overall_score")
                
            except Exception as e:
                result = {
                    "success": False,
                    "execution_time": time.time() - start,
                    "error": str(e)
                }
            
            query_result["system_results"][sys_name] = result
            status = "✓" if result["success"] else "✗"
            print(f"{status} ({result['execution_time']:.1f}s)")
        
        data["query_results"].append(query_result)
        
        # Save checkpoint every 2 queries
        if i % 2 == 0:
            checkpoint_file = results_dir / f"full_comparison_partial_{len(data['query_results'])}.json"
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"  [Saved checkpoint: {checkpoint_file.name}]")
    
    # Final save
    final_file = results_dir / "full_comparison_final.json"
    with open(final_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE!")
    print("="*70)
    print(f"Total queries: {len(data['query_results'])}")
    print(f"Final results: {final_file}")
    
    # Quick summary
    print("\nQuick Summary:")
    for sys_name in active.keys():
        successes = sum(1 for qr in data["query_results"] if qr["system_results"].get(sys_name, {}).get("success"))
        total = len(data["query_results"])
        print(f"  {sys_name:15s}: {successes}/{total} ({successes/total*100:.1f}%)")


if __name__ == "__main__":
    main()
