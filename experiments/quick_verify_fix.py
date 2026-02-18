"""
Quick verification of COLOR_SCHEME fix on previously failed queries
验证之前失败的3个查询在修复后是否能正常工作
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))

from data.test_queries import get_all_queries
from data.dataset_loader import get_dataset
from agents import LAEVOrchestrator
import json

# 之前失败的3个查询
FAILED_QUERIES = ["DIST-05", "CORR-05", "ANOM-04"]

def get_query_by_id(query_id):
    """通过ID获取查询"""
    all_queries = get_all_queries()
    for q in all_queries:
        if q.id == query_id:
            return {
                "id": q.id,
                "query": q.query_en,  # 使用英文查询
                "task_type": q.task_type.value,
                "complexity": q.complexity.value
            }
    return None

def test_fixed_queries():
    """测试修复后的查询"""
    print("="*70)
    print("COLOR_SCHEME Fix Verification - Testing Previously Failed Queries")
    print("="*70)
    
    print("\nLoading dataset...")
    dataset = get_dataset()
    
    print("Initializing LAEV-Agents...")
    orchestrator = LAEVOrchestrator(use_full_agents=False, max_iterations=3)
    
    results = []
    
    for query_id in FAILED_QUERIES:
        print(f"\n{'='*70}")
        print(f"Testing {query_id}...")
        print('='*70)
        
        # 获取查询
        query_data = get_query_by_id(query_id)
        if not query_data:
            print(f"  ⚠️ Query {query_id} not found")
            continue
        
        query = query_data["query"]
        print(f"Query: {query}")
        print(f"Task: {query_data['task_type']}, Complexity: {query_data['complexity']}")
        
        # 运行系统
        try:
            start_time = time.time()
            result = orchestrator.process(query)
            elapsed = time.time() - start_time
            
            success = result.get("success", False)
            
            print(f"\n  Result:")
            print(f"    Success: {'✓ YES' if success else '✗ NO'}")
            print(f"    Time: {elapsed:.1f}s")
            print(f"    Iterations: {result.get('iterations', 0)}")
            
            if not success:
                print(f"    Error: {result.get('error', 'Unknown')}")
            
            results.append({
                "query_id": query_id,
                "query": query,
                "success": success,
                "time": elapsed,
                "iterations": result.get("iterations", 0)
            })
            
        except Exception as e:
            print(f"  ✗ Exception: {str(e)[:100]}")
            import traceback
            traceback.print_exc()
            results.append({
                "query_id": query_id,
                "query": query,
                "success": False,
                "error": str(e)
            })
    
    # 汇总
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for r in results if r["success"])
    failed = total - passed
    
    print(f"\nTotal tested: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    
    if passed == total:
        print("\n🎉 ALL PREVIOUSLY FAILED QUERIES NOW PASS!")
        print("   COLOR_SCHEME fix is working correctly!")
        print("   Expected new success rate: 32/32 = 100%")
    else:
        print(f"\n⚠️ {failed} queries still failing")
        for r in results:
            if not r["success"]:
                print(f"   - {r['query_id']}: {r.get('error', 'Failed')}")
    
    # 保存结果
    output_file = Path(__file__).parent / "results" / "color_scheme_fix_verification.json"
    with open(output_file, "w") as f:
        json.dump({
            "tested_queries": FAILED_QUERIES,
            "results": results,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "fix_working": passed == total
            }
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    import time
    success = test_fixed_queries()
    sys.exit(0 if success else 1)
