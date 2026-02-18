#!/bin/bash
# 自动监控实验完成并更新报告

cd /data1/xh/workspace/white-paper
source /home/xh/miniconda3/etc/profile.d/conda.sh
conda activate py310

LOG_FILE="experiments/results/full_comparison_rerun_20260218_000025.log"
PID=2818736

echo "========================================"
echo "Monitoring experiment completion..."
echo "PID: $PID"
echo "Log: $LOG_FILE"
echo "========================================"

# 监控循环
while true; do
    # 检查进程是否还在运行
    if ! ps -p $PID > /dev/null; then
        echo ""
        echo "🎉 Experiment completed!"
        echo "Starting auto-update..."
        echo "========================================"
        
        # 执行更新脚本
        python3 experiments/auto_update_results.py
        
        echo "========================================"
        echo "✅ All updates completed!"
        echo "========================================"
        break
    fi
    
    # 显示进度
    if [ -f "$LOG_FILE" ]; then
        PROGRESS=$(grep -c "^\[" "$LOG_FILE" 2>/dev/null || echo "0")
        echo -ne "\r⏳ Experiment running... ~$PROGRESS queries processed (PID: $PID)"
    fi
    
    sleep 30
done
