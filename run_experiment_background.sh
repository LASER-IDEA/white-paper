#!/bin/bash
# Run full comparison experiment in background

cd /data1/xh/workspace/white-paper
source /home/xh/miniconda3/etc/profile.d/conda.sh
conda activate py310

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="experiments/results/full_comparison_rerun_${TIMESTAMP}.log"

echo "Starting experiment at $(date)" > "$LOG_FILE"
echo "Log file: $LOG_FILE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

nohup python3 experiments/run_full_comparison.py >> "$LOG_FILE" 2>&1 &
PID=$!

echo "Experiment started with PID: $PID"
echo "PID: $PID" >> "$LOG_FILE"
echo ""
echo "To monitor progress:"
echo "  tail -f $LOG_FILE"
echo ""
echo "To check status:"
echo "  ps aux | grep $PID"
