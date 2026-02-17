"""
User Study Data Analysis Script
IEEE VIS 2026 - LAEV-Agents User Study

Usage:
    python analysis_script.py --input data/user_study_data.json --output results/
"""

import json
import argparse
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11


def load_data(filepath):
    """Load user study data from JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def calculate_sus(sus_scores):
    """
    Calculate SUS score from individual item scores.
    
    sus_scores: list of 10 integers (1-5)
    Odd items (1,3,5,7,9): score = response - 1
    Even items (2,4,6,8,10): score = 5 - response
    Total = sum of all item scores * 2.5
    """
    if len(sus_scores) != 10:
        return None
    
    total = 0
    for i, score in enumerate(sus_scores, 1):
        if i % 2 == 1:  # Odd items
            total += score - 1
        else:  # Even items
            total += 5 - score
    
    return total * 2.5


def descriptive_statistics(data):
    """Calculate descriptive statistics for all metrics"""
    
    # Extract SUS scores
    nl4dv_sus = [p['results']['nl4dv']['sus_score'] for p in data]
    laev_sus = [p['results']['laev']['sus_score'] for p in data]
    
    # Extract task completion rates
    nl4dv_success = []
    laev_success = []
    
    for p in data:
        nl4dv_tasks = p['results']['nl4dv'].get('tasks', [])
        laev_tasks = p['results']['laev'].get('tasks', [])
        
        nl4dv_success.extend([t['success'] for t in nl4dv_tasks])
        laev_success.extend([t['success'] for t in laev_tasks])
    
    # Extract completion times (only successful tasks)
    nl4dv_times = []
    laev_times = []
    
    for p in data:
        nl4dv_tasks = p['results']['nl4dv'].get('tasks', [])
        laev_tasks = p['results']['laev'].get('tasks', [])
        
        nl4dv_times.extend([t['time'] for t in nl4dv_tasks if t['success']])
        laev_times.extend([t['time'] for t in laev_tasks if t['success']])
    
    stats_dict = {
        'sus': {
            'nl4dv': {
                'n': len(nl4dv_sus),
                'mean': np.mean(nl4dv_sus),
                'std': np.std(nl4dv_sus, ddof=1),
                'median': np.median(nl4dv_sus),
                'min': np.min(nl4dv_sus),
                'max': np.max(nl4dv_sus)
            },
            'laev': {
                'n': len(laev_sus),
                'mean': np.mean(laev_sus),
                'std': np.std(laev_sus, ddof=1),
                'median': np.median(laev_sus),
                'min': np.min(laev_sus),
                'max': np.max(laev_sus)
            }
        },
        'completion_rate': {
            'nl4dv': np.mean(nl4dv_success) * 100,
            'laev': np.mean(laev_success) * 100
        },
        'completion_time': {
            'nl4dv': {
                'n': len(nl4dv_times),
                'mean': np.mean(nl4dv_times),
                'std': np.std(nl4dv_times, ddof=1),
                'median': np.median(nl4dv_times)
            },
            'laev': {
                'n': len(laev_times),
                'mean': np.mean(laev_times),
                'std': np.std(laev_times, ddof=1),
                'median': np.median(laev_times)
            }
        }
    }
    
    return stats_dict


def hypothesis_testing(data):
    """Perform statistical hypothesis testing"""
    
    # Extract SUS scores
    nl4dv_sus = [p['results']['nl4dv']['sus_score'] for p in data]
    laev_sus = [p['results']['laev']['sus_score'] for p in data]
    
    # H1: Paired t-test for SUS scores
    t_stat, p_value = stats.ttest_rel(laev_sus, nl4dv_sus)
    
    # Effect size (Cohen's d)
    mean_diff = np.mean(laev_sus) - np.mean(nl4dv_sus)
    pooled_std = np.sqrt((np.var(laev_sus, ddof=1) + np.var(nl4dv_sus, ddof=1)) / 2)
    cohens_d = mean_diff / pooled_std
    
    # Interpret Cohen's d
    if abs(cohens_d) < 0.2:
        effect_size = "negligible"
    elif abs(cohens_d) < 0.5:
        effect_size = "small"
    elif abs(cohens_d) < 0.8:
        effect_size = "medium"
    else:
        effect_size = "large"
    
    results = {
        'sus_comparison': {
            'test': 'Paired t-test',
            't_statistic': t_stat,
            'df': len(data) - 1,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'mean_difference': mean_diff,
            'cohens_d': cohens_d,
            'effect_size': effect_size
        }
    }
    
    return results


def create_visualizations(data, output_dir):
    """Create visualization figures for the paper"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract data
    nl4dv_sus = [p['results']['nl4dv']['sus_score'] for p in data]
    laev_sus = [p['results']['laev']['sus_score'] for p in data]
    
    # Figure 1: SUS Score Comparison (Box Plot)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sus_data = pd.DataFrame({
        'NL4DV': nl4dv_sus,
        'LAEV-Agents': laev_sus
    })
    
    sus_data.boxplot(ax=ax)
    ax.set_ylabel('SUS Score')
    ax.set_title('System Usability Scale (SUS) Comparison')
    ax.axhline(y=68, color='r', linestyle='--', alpha=0.5, label='Acceptability Threshold (68)')
    ax.axhline(y=80, color='g', linestyle='--', alpha=0.5, label='Excellent Threshold (80)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'sus_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 2: Paired SUS Scores
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = range(len(data))
    ax.plot(x, nl4dv_sus, 'o-', label='NL4DV', alpha=0.7)
    ax.plot(x, laev_sus, 's-', label='LAEV-Agents', alpha=0.7)
    
    for i, (n, l) in enumerate(zip(nl4dv_sus, laev_sus)):
        ax.plot([i, i], [n, l], 'k--', alpha=0.3)
    
    ax.set_xlabel('Participant')
    ax.set_ylabel('SUS Score')
    ax.set_title('Individual SUS Score Changes')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'sus_paired.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualizations saved to {output_dir}")


def generate_report(data, stats_results, test_results, output_dir):
    """Generate analysis report"""
    
    output_dir = Path(output_dir)
    report = []
    
    report.append("="*70)
    report.append("USER STUDY ANALYSIS REPORT")
    report.append("="*70)
    report.append("")
    
    # Sample size
    report.append(f"Sample Size: N={len(data)}")
    report.append("")
    
    # Descriptive Statistics
    report.append("-"*70)
    report.append("DESCRIPTIVE STATISTICS")
    report.append("-"*70)
    report.append("")
    
    sus_stats = stats_results['sus']
    report.append("SUS Scores:")
    report.append(f"  NL4DV:  M={sus_stats['nl4dv']['mean']:.1f}, SD={sus_stats['nl4dv']['std']:.1f}, "
                  f"Median={sus_stats['nl4dv']['median']:.1f}")
    report.append(f"  LAEV:   M={sus_stats['laev']['mean']:.1f}, SD={sus_stats['laev']['std']:.1f}, "
                  f"Median={sus_stats['laev']['median']:.1f}")
    report.append("")
    
    cr_stats = stats_results['completion_rate']
    report.append(f"Task Completion Rate:")
    report.append(f"  NL4DV: {cr_stats['nl4dv']:.1f}%")
    report.append(f"  LAEV:  {cr_stats['laev']:.1f}%")
    report.append("")
    
    # Hypothesis Testing
    report.append("-"*70)
    report.append("HYPOTHESIS TESTING")
    report.append("-"*70)
    report.append("")
    
    sus_test = test_results['sus_comparison']
    report.append("H1: SUS Score Comparison (Paired t-test)")
    report.append(f"  t({sus_test['df']}) = {sus_test['t_statistic']:.2f}, p = {sus_test['p_value']:.4f}")
    report.append(f"  Mean Difference: {sus_test['mean_difference']:.2f}")
    report.append(f"  Cohen's d: {sus_test['cohens_d']:.2f} ({sus_test['effect_size']})")
    report.append(f"  Significant: {'Yes' if sus_test['significant'] else 'No'} (α = 0.05)")
    report.append("")
    
    # Interpretation
    report.append("-"*70)
    report.append("INTERPRETATION")
    report.append("-"*70)
    report.append("")
    
    if sus_test['significant']:
        if sus_test['mean_difference'] > 0:
            report.append("✓ LAEV-Agents has significantly higher SUS scores than NL4DV")
        else:
            report.append("✗ NL4DV has significantly higher SUS scores than LAEV-Agents")
    else:
        report.append("○ No significant difference in SUS scores between systems")
    
    report.append("")
    report.append("="*70)
    
    # Save report
    report_text = "\n".join(report)
    with open(output_dir / 'analysis_report.txt', 'w') as f:
        f.write(report_text)
    
    print(report_text)
    
    return report_text


def main():
    parser = argparse.ArgumentParser(description='Analyze user study data')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file')
    parser.add_argument('--output', '-o', default='results', help='Output directory')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    data = load_data(args.input)
    print(f"Loaded {len(data)} participant records")
    
    # Calculate statistics
    print("\nCalculating descriptive statistics...")
    stats_results = descriptive_statistics(data)
    
    # Hypothesis testing
    print("Running hypothesis tests...")
    test_results = hypothesis_testing(data)
    
    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(data, args.output)
    
    # Generate report
    print("\nGenerating report...")
    generate_report(data, stats_results, test_results, args.output)
    
    print(f"\n✓ Analysis complete. Results saved to {args.output}")


if __name__ == '__main__':
    main()
