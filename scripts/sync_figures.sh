#!/bin/bash
# Synchronize figures from paper_figures/ to paper/figures/

echo "========================================"
echo "Synchronizing Figures"
echo "========================================"

# Copy updated fig3 (success rate comparison) with both names
cp paper_figures/fig3_performance_metrics.png paper/figures/fig3_performance_metrics.png
cp paper_figures/fig3_performance_metrics.pdf paper/figures/fig3_performance_metrics.pdf

# Also update fig_success_rate_comparison (what LaTeX currently references)
cp paper_figures/fig3_performance_metrics.png paper/figures/fig_success_rate_comparison.png
cp paper_figures/fig3_performance_metrics.pdf paper/figures/fig_success_rate_comparison.pdf

echo "✅ fig3_performance_metrics -> fig_success_rate_comparison"

# Copy other figures that might be referenced
cp paper_figures/fig2_system_architecture.png paper/figures/fig2_architecture.png
cp paper_figures/fig2_system_architecture.pdf paper/figures/fig2_architecture.pdf
echo "✅ fig2_system_architecture -> fig2_architecture"

cp paper_figures/fig4_ablation_study.png paper/figures/fig_ablation_study.png
cp paper_figures/fig4_ablation_study.pdf paper/figures/fig_ablation_study.pdf
echo "✅ fig4_ablation_study -> fig_ablation_study"

cp paper_figures/fig5_quality_radar.png paper/figures/fig_quality_radar.png
cp paper_figures/fig5_quality_radar.pdf paper/figures/fig_quality_radar.pdf
echo "✅ fig5_quality_radar -> fig_quality_radar"

cp paper_figures/fig6_iteration_process.png paper/figures/fig_iteration_example.png
cp paper_figures/fig6_iteration_process.pdf paper/figures/fig_iteration_example.pdf
echo "✅ fig6_iteration_process -> fig_iteration_example"

cp paper_figures/fig7_teaser.png paper/figures/teaser.png 2>/dev/null || true
cp paper_figures/fig7_teaser.pdf paper/figures/teaser.pdf 2>/dev/null || true
echo "✅ fig7_teaser -> teaser"

echo ""
echo "========================================"
echo "Synchronization Complete!"
echo "========================================"
echo ""
echo "Updated files in paper/figures/:"
ls -lth paper/figures/*.png | head -10
