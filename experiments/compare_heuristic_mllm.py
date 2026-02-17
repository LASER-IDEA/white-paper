"""
对比 Heuristic vs MLLM 评估结果
验证 Heuristic 方法的有效性
"""

import sys
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))

from visual_evaluator_mllm import MLLMVisualEvaluator, compare_heuristic_vs_mllm
from agents.visual_evaluator import VisualQualityEvaluator
from data.test_queries import get_all_queries


def load_existing_results(results_file: str = "experiments/results/full_comparison_final.json"):
    """加载已有实验结果"""
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    # 提取成功的 LAEV 结果
    successful_charts = []
    for item in data.get('query_results', []):
        query_id = item.get('query_id')
        query = item.get('query_en', item.get('query', ''))
        
        laev_result = item.get('system_results', {}).get('laev_agents', {})
        if laev_result.get('success') and laev_result.get('generated_code'):
            successful_charts.append({
                'query_id': query_id,
                'query': query,
                'code': laev_result['generated_code'],
                'html': laev_result.get('html_content', '')
            })
    
    return successful_charts


def compute_correlation(heuristic_scores, mllm_scores):
    """计算两种评估方法的相关性"""
    from scipy.stats import pearsonr, spearmanr
    
    # Pearson 相关系数
    pearson_r, pearson_p = pearsonr(heuristic_scores, mllm_scores)
    
    # Spearman 相关系数
    spearman_r, spearman_p = spearmanr(heuristic_scores, mllm_scores)
    
    # Mean Absolute Error
    mae = np.mean(np.abs(np.array(heuristic_scores) - np.array(mllm_scores)))
    
    return {
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_r': spearman_r,
        'spearman_p': spearman_p,
        'mae': mae
    }


def main():
    print("="*70)
    print("Heuristic vs MLLM Evaluation Comparison")
    print("="*70)
    
    # 初始化评估器
    print("\nInitializing MLLM evaluator...")
    mllm_evaluator = MLLMVisualEvaluator()
    heuristic_evaluator = VisualQualityEvaluator()
    
    # 加载已有结果
    print("\nLoading existing experiment results...")
    charts = load_existing_results()
    print(f"Found {len(charts)} successful charts to evaluate")
    
    # 限制评估数量 (可选，用于快速测试)
    max_samples = 20  # 可以调整为 32 或更多
    charts = charts[:max_samples]
    print(f"Evaluating first {len(charts)} charts...")
    
    # 存储结果
    results = []
    
    # 评估每个图表
    print("\nRunning evaluation...")
    for chart in tqdm(charts, desc="Evaluating"):
        try:
            # Heuristic 评估
            h_result = heuristic_evaluator.evaluate(chart['code'], chart['query'])
            
            # MLLM 评估 (需要 HTML 内容)
            if chart.get('html'):
                m_result = mllm_evaluator.evaluate(chart['html'], chart['query'])
                
                results.append({
                    'query_id': chart['query_id'],
                    'query': chart['query'],
                    'heuristic': {
                        'readability': h_result.get('readability', 0),
                        'aesthetics': h_result.get('aesthetics', 0),
                        'data_encoding': h_result.get('data_encoding', 0),
                        'appropriateness': h_result.get('appropriateness', 0),
                        'overall': h_result.get('overall_score', 0)
                    },
                    'mllm': {
                        'readability': m_result.get('readability', 0),
                        'aesthetics': m_result.get('aesthetics', 0),
                        'data_encoding': m_result.get('data_encoding', 0),
                        'appropriateness': m_result.get('appropriateness', 0),
                        'overall': m_result.get('overall_score', 0)
                    }
                })
        except Exception as e:
            print(f"\nError evaluating {chart['query_id']}: {e}")
            continue
    
    print(f"\nSuccessfully evaluated {len(results)} charts")
    
    # 计算相关性
    print("\n" + "="*70)
    print("CORRELATION ANALYSIS")
    print("="*70)
    
    dimensions = ['readability', 'aesthetics', 'data_encoding', 'appropriateness', 'overall']
    
    for dim in dimensions:
        h_scores = [r['heuristic'][dim] for r in results]
        m_scores = [r['mllm'][dim] for r in results]
        
        corr = compute_correlation(h_scores, m_scores)
        
        print(f"\n{dim.upper()}:")
        print(f"  Pearson r:  {corr['pearson_r']:.3f} (p={corr['pearson_p']:.3f})")
        print(f"  Spearman r: {corr['spearman_r']:.3f} (p={corr['spearman_p']:.3f})")
        print(f"  MAE:        {corr['mae']:.3f}")
    
    # 保存结果
    output = {
        'total_evaluated': len(results),
        'results': results,
        'correlation_summary': {
            dim: compute_correlation(
                [r['heuristic'][dim] for r in results],
                [r['mllm'][dim] for r in results]
            ) for dim in dimensions
        }
    }
    
    output_file = Path(__file__).parent / "results" / "heuristic_mllm_comparison.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # 结论
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    overall_corr = compute_correlation(
        [r['heuristic']['overall'] for r in results],
        [r['mllm']['overall'] for r in results]
    )
    
    if overall_corr['pearson_r'] > 0.7:
        print(f"✓ Heuristic and MLLM evaluations are highly correlated (r={overall_corr['pearson_r']:.3f})")
        print("  → Heuristic method is validated and can be used for fast evaluation")
    elif overall_corr['pearson_r'] > 0.5:
        print(f"⚠ Moderate correlation (r={overall_corr['pearson_r']:.3f})")
        print("  → Consider using MLLM for critical evaluations")
    else:
        print(f"✗ Low correlation (r={overall_corr['pearson_r']:.3f})")
        print("  → MLLM evaluation is recommended for accuracy")


if __name__ == "__main__":
    main()
