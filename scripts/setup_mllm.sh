#!/bin/bash
# 部署 Qwen2.5-VL MLLM 评估器
# 针对 3x RTX 4090 (72GB VRAM) 优化

set -e

echo "=============================================="
echo "MLLM Visual Evaluator Setup"
echo "=============================================="

# 检查 conda 环境
if ! command -v conda &> /dev/null; then
    echo "Error: Conda not found. Please install Anaconda/Miniconda first."
    exit 1
fi

# 激活环境
source $(conda info --base)/etc/profile.d/conda.sh
conda activate py310

echo ""
echo "Step 1: Installing dependencies..."
pip install -q transformers accelerate qwen-vl-utils

# 可选：安装 playwright 用于 HTML 转图片
echo ""
echo "Step 2: Installing Playwright (for HTML to image conversion)..."
pip install -q playwright
playwright install chromium

echo ""
echo "Step 3: Downloading Qwen2.5-VL-7B model..."
echo "This may take 10-20 minutes depending on your network..."

python3 << 'PYTHON_EOF'
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
import torch

print("Loading model (this will download ~16GB)...")
model_name = "Qwen/Qwen2.5-VL-7B-Instruct"

# 下载模型
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True
)

processor = AutoProcessor.from_pretrained(
    model_name,
    trust_remote_code=True
)

print("Model downloaded successfully!")
print(f"Model device map: {model.hf_device_map}")
PYTHON_EOF

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "You can now use the MLLM evaluator:"
echo "  python python/src/visual_evaluator_mllm.py"
echo ""
echo "To run comparison experiment:"
echo "  python experiments/compare_heuristic_mllm.py"
echo ""
