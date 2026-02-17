"""
Generate figures for IEEE VIS 2026 paper
LAEV-Agents: Multi-Agent System for Domain-Specific Data Visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import json
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Color scheme (matching the paper)
COLORS = {
    'primary': '#002FA7',      # Klein Blue
    'secondary': '#f59e0b',    # Amber
    'accent': '#ea580c',       # Orange
    'success': '#059669',      # Green
    'danger': '#dc2626',       # Red
    'neutral': '#6b7280',      # Gray
    'light': '#f3f4f6',        # Light gray
    'white': '#ffffff',
    'planner': '#3b82f6',      # Blue
    'retriever': '#8b5cf6',    # Purple
    'coder': '#10b981',        # Green
    'evaluator': '#f59e0b',    # Amber
    'reflector': '#ef4444',    # Red
}

OUTPUT_DIR = Path(__file__).parent


def save_fig(fig, name, dpi=300):
    """Save figure in multiple formats"""
    fig.savefig(OUTPUT_DIR / f'{name}.png', dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / f'{name}.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved: {name}.png/pdf")


def create_architecture_diagram():
    """Figure 2: System Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.5, 'LAEV-Agents Architecture', fontsize=16, fontweight='bold', 
            ha='center', va='center')
    
    # Define agent positions and colors
    agents = [
        {'name': 'Planner', 'color': COLORS['planner'], 'pos': (2, 5.5)},
        {'name': 'Retriever', 'color': COLORS['retriever'], 'pos': (5, 5.5)},
        {'name': 'Coder', 'color': COLORS['coder'], 'pos': (8, 5.5)},
        {'name': 'Evaluator', 'color': COLORS['evaluator'], 'pos': (11, 5.5)},
        {'name': 'Reflector', 'color': COLORS['reflector'], 'pos': (8, 2.5)},
    ]
    
    # Draw agents
    for agent in agents:
        x, y = agent['pos']
        # Agent box
        box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, 
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor=agent['color'], edgecolor='black', 
                             linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, agent['name'], fontsize=11, fontweight='bold',
                ha='center', va='center', color='white')
    
    # Draw arrows between agents (main flow)
    arrow_style = dict(arrowstyle='->', color='black', lw=2, 
                       connectionstyle='arc3,rad=0')
    
    # Planner -> Retriever
    ax.annotate('', xy=(4.2, 5.5), xytext=(2.8, 5.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Retriever -> Coder
    ax.annotate('', xy=(7.2, 5.5), xytext=(5.8, 5.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Coder -> Evaluator
    ax.annotate('', xy=(10.2, 5.5), xytext=(8.8, 5.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Evaluator -> Reflector (down)
    ax.annotate('', xy=(11, 3.3), xytext=(11, 5.1),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Reflector -> Coder (iteration)
    ax.annotate('', xy=(8.8, 2.5), xytext=(10.2, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'], 
                               lw=2, linestyle='--'))
    ax.text(9.5, 2.2, 'Refine', fontsize=9, ha='center', color=COLORS['accent'])
    
    # Add labels for what each agent does
    labels = [
        ('Intent\nAnalysis', 2, 4.5),
        ('GraphRAG\nRetrieval', 5, 4.5),
        ('Code\nGeneration', 8, 4.5),
        ('Quality\nAssessment', 11, 4.5),
        ('Error\nAnalysis', 8, 1.5),
    ]
    
    for text, x, y in labels:
        ax.text(x, y, text, fontsize=9, ha='center', va='center',
                style='italic', color='gray')
    
    # Add shared state box
    state_box = FancyBboxPatch((0.5, 0.3), 3, 1.2,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=COLORS['light'], edgecolor='gray',
                               linewidth=1)
    ax.add_patch(state_box)
    ax.text(2, 1.2, 'Shared State:', fontsize=9, fontweight='bold', ha='center')
    ax.text(2, 0.8, 'query, intent, context, code,', fontsize=8, ha='center')
    ax.text(2, 0.5, 'execution_result, visual_feedback', fontsize=8, ha='center')
    
    # Add external inputs
    ax.text(2, 6.5, 'User Query', fontsize=10, ha='center', fontweight='bold')
    ax.annotate('', xy=(2, 5.9), xytext=(2, 6.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
    
    # Knowledge Graph
    kg_box = FancyBboxPatch((4.2, 6.2), 1.6, 0.6,
                            boxstyle="round,pad=0.05,rounding_size=0.1",
                            facecolor=COLORS['retriever'], edgecolor='black',
                            linewidth=1, alpha=0.3)
    ax.add_patch(kg_box)
    ax.text(5, 6.5, 'Knowledge Graph', fontsize=8, ha='center', alpha=0.7)
    ax.annotate('', xy=(5, 5.9), xytext=(5, 6.2),
                arrowprops=dict(arrowstyle='->', color=COLORS['retriever'], 
                               lw=1.5, alpha=0.7))
    
    # Output
    ax.text(11, 1.5, 'Visualization\nCode', fontsize=10, ha='center', 
            fontweight='bold', color=COLORS['success'])
    ax.annotate('', xy=(11, 1.8), xytext=(11, 2.1),
                arrowprops=dict(arrowstyle='->', color=COLORS['success'], lw=2))
    
    plt.tight_layout()
    save_fig(fig, 'fig2_architecture')
    plt.close()


def create_success_rate_comparison():
    """Figure: Success Rate Comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    systems = ['NL4DV', 'Direct LLM', 'LAEV-Agents']
    success_rates = [59.4, 100.0, 90.6]
    colors = [COLORS['neutral'], '#6b7280', COLORS['primary']]
    
    bars = ax.bar(systems, success_rates, color=colors, edgecolor='black', 
                  linewidth=1.5, width=0.6)
    
    # Add value labels on bars
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, 
                fontweight='bold')
    
    # Styling
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_title('Success Rate Comparison Across Systems', fontsize=14, 
                 fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.axhline(y=90, color=COLORS['success'], linestyle='--', alpha=0.5, 
               label='Target (90%)')
    
    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    save_fig(fig, 'fig_success_rate_comparison')
    plt.close()


def create_ablation_results():
    """Figure: Ablation Study Results"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    variants = ['Direct LLM', 'No RAG', 'Vector RAG', 'Full RAG\n(Single)', 'Full System\n(Multi-Iter)']
    success_rates = [0, 90.0, 100.0, 90.0, 100.0]
    
    colors = ['#9ca3af', '#d1d5db', '#93c5fd', '#60a5fa', COLORS['primary']]
    
    bars = ax.barh(variants, success_rates, color=colors, edgecolor='black',
                   linewidth=1, height=0.6)
    
    # Add value labels
    for bar, rate in zip(bars, success_rates):
        width = bar.get_width()
        label_x = width + 2 if width > 0 else 2
        ax.text(label_x, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', ha='left', va='center', fontsize=11,
                fontweight='bold')
    
    # Styling
    ax.set_xlabel('Success Rate (%)', fontsize=12)
    ax.set_title('Ablation Study: Component Contribution Analysis', fontsize=14,
                 fontweight='bold', pad=20)
    ax.set_xlim(0, 115)
    
    # Add component contribution annotations
    annotations = [
        (15, 4, '+90%\nMulti-Agent'),
        (50, 3, '+10%\nVector RAG'),
        (50, 2, '-10%\nGraphRAG'),
        (50, 1, '+10%\nMulti-Iter'),
    ]
    
    for x, y, text in annotations:
        ax.text(x, y, text, fontsize=9, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', 
                         edgecolor='orange', alpha=0.7))
    
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    save_fig(fig, 'fig_ablation_study')
    plt.close()


def create_task_type_breakdown():
    """Figure: Success Rate by Task Type"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    task_types = ['Trend', 'Comparison', 'Distribution', 'Correlation', 
                  'Exploration', 'Anomaly']
    nl4dv_rates = [83.3, 66.7, 80.0, 60.0, 0.0, 40.0]
    laev_rates = [100.0, 83.3, 100.0, 80.0, 100.0, 80.0]
    
    x = np.arange(len(task_types))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nl4dv_rates, width, label='NL4DV',
                   color=COLORS['neutral'], edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, laev_rates, width, label='LAEV-Agents',
                   color=COLORS['primary'], edgecolor='black', linewidth=1)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{height:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Styling
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_title('Success Rate by Task Type', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(task_types, rotation=15, ha='right')
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 115)
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    save_fig(fig, 'fig_task_type_breakdown')
    plt.close()


def create_quality_scores_radar():
    """Figure: Quality Scores Radar Chart"""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    categories = ['Readability', 'Aesthetics', 'Data Encoding', 'Appropriateness']
    N = len(categories)
    
    # Data
    nl4dv_scores = [0.72, 0.65, 0.78, 0.68]
    laev_scores = [0.78, 0.72, 0.82, 0.70]
    direct_scores = [0.68, 0.71, 0.75, 0.62]
    
    # Compute angle for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the loop
    
    # Add data points to complete the loop
    nl4dv_scores += nl4dv_scores[:1]
    laev_scores += laev_scores[:1]
    direct_scores += direct_scores[:1]
    
    # Plot
    ax.plot(angles, nl4dv_scores, 'o-', linewidth=2, label='NL4DV', 
            color=COLORS['neutral'])
    ax.fill(angles, nl4dv_scores, alpha=0.15, color=COLORS['neutral'])
    
    ax.plot(angles, laev_scores, 's-', linewidth=2, label='LAEV-Agents',
            color=COLORS['primary'])
    ax.fill(angles, laev_scores, alpha=0.15, color=COLORS['primary'])
    
    ax.plot(angles, direct_scores, '^-', linewidth=2, label='Direct LLM',
            color='#6b7280')
    ax.fill(angles, direct_scores, alpha=0.1, color='#6b7280')
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    
    # Set y-axis
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)
    
    ax.set_title('Quality Scores Comparison\n(Multi-dimensional Assessment)', 
                 fontsize=14, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
    
    plt.tight_layout()
    save_fig(fig, 'fig_quality_radar')
    plt.close()


def create_iteration_example():
    """Figure: Iteration Process Example"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Iterative Refinement Example: Complex Comparison Query', 
                 fontsize=14, fontweight='bold')
    
    iterations = [
        {
            'title': 'Iteration 1: Initial Generation',
            'score': 0.45,
            'issues': ['Missing title', 'Wrong chart type', 'No legend'],
            'feedback': 'Use grouped bar chart instead of pie'
        },
        {
            'title': 'Iteration 2: After Refinement',
            'score': 0.68,
            'issues': ['Colors not consistent', 'Axis labels unclear'],
            'feedback': 'Use COLOR_SCHEME and add axis labels'
        },
        {
            'title': 'Iteration 3: Final Output',
            'score': 0.92,
            'issues': [],
            'feedback': 'Success'
        },
        {
            'title': 'Quality Improvement',
            'score': None,
            'improvement': True
        }
    ]
    
    for idx, (ax, iter_data) in enumerate(zip(axes.flat, iterations)):
        if iter_data.get('improvement'):
            # Plot improvement curve
            scores = [0.45, 0.68, 0.92]
            x = range(1, 4)
            ax.plot(x, scores, 'o-', linewidth=2, markersize=10, 
                   color=COLORS['primary'])
            ax.fill_between(x, scores, alpha=0.2, color=COLORS['primary'])
            ax.set_xlabel('Iteration', fontsize=10)
            ax.set_ylabel('Quality Score', fontsize=10)
            ax.set_title(iter_data['title'], fontsize=11, fontweight='bold')
            ax.set_ylim(0, 1.0)
            ax.set_xticks([1, 2, 3])
            ax.grid(True, alpha=0.3)
            
            # Add annotations
            for i, s in enumerate(scores):
                ax.annotate(f'{s:.2f}', (i+1, s), textcoords="offset points",
                           xytext=(0, 10), ha='center', fontsize=9, 
                           fontweight='bold')
        else:
            # Show iteration info
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Title
            ax.text(5, 9, iter_data['title'], fontsize=11, fontweight='bold',
                   ha='center', va='top')
            
            # Score
            if iter_data['score']:
                color = COLORS['success'] if iter_data['score'] > 0.8 else \
                        COLORS['accent'] if iter_data['score'] > 0.6 else COLORS['danger']
                ax.text(5, 7.5, f"Quality Score: {iter_data['score']:.2f}",
                       fontsize=14, fontweight='bold', ha='center',
                       color=color)
            
            # Issues
            if iter_data['issues']:
                ax.text(1, 5.5, "Issues:", fontsize=10, fontweight='bold')
                for i, issue in enumerate(iter_data['issues']):
                    ax.text(1, 4.5 - i*0.8, f"• {issue}", fontsize=9)
            else:
                ax.text(5, 5, "✓ No Issues", fontsize=12, 
                       color=COLORS['success'], ha='center', fontweight='bold')
            
            # Feedback
            ax.text(5, 1.5, f"Feedback: {iter_data['feedback']}",
                   fontsize=9, style='italic', ha='center',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    save_fig(fig, 'fig_iteration_example')
    plt.close()


def create_performance_timeline():
    """Figure: Execution Time Comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    systems = ['NL4DV', 'LAEV-Agents\n(Single)', 'LAEV-Agents\n(Multi)', 'Direct LLM']
    times = [0.6, 22.8, 25.2, 26.0]
    colors = [COLORS['neutral'], '#93c5fd', COLORS['primary'], '#6b7280']
    
    bars = ax.bar(systems, times, color=colors, edgecolor='black', 
                  linewidth=1.5, width=0.6)
    
    # Add value labels
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{time:.1f}s', ha='center', va='bottom', fontsize=11,
                fontweight='bold')
    
    # Styling
    ax.set_ylabel('Average Execution Time (seconds)', fontsize=12)
    ax.set_title('Execution Time Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 30)
    
    # Add annotations
    ax.annotate('Fast but\nlimited', xy=(0, 0.6), xytext=(0.5, 8),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['neutral']))
    
    ax.annotate('Quality\nassurance', xy=(2, 25.2), xytext=(2.5, 20),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['primary']))
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    save_fig(fig, 'fig_execution_time')
    plt.close()


def main():
    """Generate all figures"""
    print("Generating figures for IEEE VIS 2026 paper...")
    print("="*60)
    
    print("\n1. Creating architecture diagram...")
    create_architecture_diagram()
    
    print("\n2. Creating success rate comparison...")
    create_success_rate_comparison()
    
    print("\n3. Creating ablation study results...")
    create_ablation_results()
    
    print("\n4. Creating task type breakdown...")
    create_task_type_breakdown()
    
    print("\n5. Creating quality scores radar...")
    create_quality_scores_radar()
    
    print("\n6. Creating iteration example...")
    create_iteration_example()
    
    print("\n7. Creating execution time comparison...")
    create_performance_timeline()
    
    print("\n" + "="*60)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nGenerated files:")
    for f in sorted(OUTPUT_DIR.glob('fig*.png')):
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
