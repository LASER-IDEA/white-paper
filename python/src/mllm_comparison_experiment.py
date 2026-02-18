"""
MLLM Visual Evaluation Comparison Experiment
对比三种视觉评估方法：
1. Heuristic (代码规则)
2. Local MLLM (Qwen2.5-VL-7B)
3. API MLLM (qwen-vl-max)

Metrics:
- 评估时间
- 评分一致性
- 反馈质量
- 资源消耗
"""

import sys
import os
import io
import json
import time
import base64
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

# 加载环境变量
load_dotenv(Path(__file__).parent.parent.parent / ".env")


@dataclass
class EvaluationResult:
    """评估结果"""
    method: str
    score: float = 0.0
    dimensions: Dict[str, float] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    evaluation_time: float = 0.0
    confidence: float = 0.0
    raw_response: str = ""
    error: Optional[str] = None


class HeuristicEvaluator:
    """启发式评估器"""
    
    def evaluate(self, code: str, query: str) -> EvaluationResult:
        start = time.time()
        result = EvaluationResult(method="Heuristic")
        
        # 简单规则检查
        checks = {
            "has_title": "TitleOpts" in code,
            "has_xaxis": "add_xaxis" in code,
            "has_yaxis": "add_yaxis" in code or "Pie" in code,
            "has_data": "add_yaxis" in code or ".add(" in code,
            "has_colors": "color" in code.lower(),
            "has_legend": "LegendOpts" in code,
            "has_tooltip": "TooltipOpts" in code,
        }
        
        # 计算分数
        passed = sum(checks.values())
        total = len(checks)
        score = passed / total
        
        # 生成反馈
        issues = []
        suggestions = []
        
        if not checks["has_title"]:
            issues.append("Missing chart title")
            suggestions.append("Add TitleOpts(title='Your Title')")
        if not checks["has_legend"]:
            issues.append("Missing legend for multi-series data")
            suggestions.append("Add LegendOpts()")
        if not checks["has_tooltip"]:
            issues.append("Missing tooltip for data exploration")
            suggestions.append("Add TooltipOpts()")
        
        result.score = score
        result.dimensions = {
            "readability": 0.7 if checks["has_title"] else 0.4,
            "aesthetics": 0.6 if checks["has_colors"] else 0.4,
            "data_encoding": 0.8 if checks["has_data"] else 0.3,
            "appropriateness": 0.7
        }
        result.issues = issues
        result.suggestions = suggestions
        result.evaluation_time = time.time() - start
        result.confidence = 0.8
        
        return result


class LocalMLLMEvaluator:
    """本地 MLLM 评估器"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self._loaded = False
    
    def _load_model(self):
        if self._loaded:
            return
        
        import torch
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
        
        cache_dir = "/data1/xh/workspace/white-paper/huggingface_cache"
        model_path = f"{cache_dir}/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/*"
        
        import glob
        snapshots = glob.glob(model_path)
        if snapshots:
            model_path = snapshots[0]
        
        print(f"    [Local MLLM] Loading model from {model_path}...")
        
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
            local_files_only=True
        )
        self.processor = AutoProcessor.from_pretrained(
            model_path,
            trust_remote_code=True,
            local_files_only=True
        )
        self._loaded = True
        print(f"    [Local MLLM] Model loaded!")
    
    def evaluate(self, image_data: bytes, query: str) -> EvaluationResult:
        start = time.time()
        result = EvaluationResult(method="Local MLLM")
        
        try:
            self._load_model()
            
            import torch
            image = Image.open(io.BytesIO(image_data))
            
            prompt = f"""Evaluate this chart for query: "{query}"
Rate 0-1: Readability, Aesthetics, Data Encoding, Appropriateness.
Format:
Readability: [score]
Aesthetics: [score]
Data Encoding: [score]
Appropriateness: [score]
Issues: [list]
Suggestions: [list]"""
            
            messages = [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": prompt}]}]
            
            text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.processor(text=[text], images=[image], padding=True, return_tensors="pt")
            inputs = inputs.to(self.model.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs, max_new_tokens=512, temperature=0.2)
            
            generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
            response = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)[0]
            
            result.raw_response = response
            result = self._parse_response(result, response)
            
        except Exception as e:
            result.error = str(e)
            result.score = 0.5
        
        result.evaluation_time = time.time() - start
        return result
    
    def _parse_response(self, result: EvaluationResult, response: str) -> EvaluationResult:
        import re
        
        patterns = {
            'readability': r'Readability[:\s]+([0-9.]+)',
            'aesthetics': r'Aesthetics[:\s]+([0-9.]+)',
            'data_encoding': r'Data Encoding[:\s]+([0-9.]+)',
            'appropriateness': r'Appropriateness[:\s]+([0-9.]+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                result.dimensions[key] = float(match.group(1))
        
        if result.dimensions:
            result.score = sum(result.dimensions.values()) / len(result.dimensions)
        
        return result


class APIMLLMEvaluator:
    """API MLLM 评估器 (qwen-vl-max)"""
    
    def __init__(self):
        self.api_key = os.getenv("QWEN_API_KEY")
        self.base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = os.getenv("QWEN_VL_MODEL", "qwen-vl-max")
    
    def evaluate(self, image_data: bytes, query: str) -> EvaluationResult:
        start = time.time()
        result = EvaluationResult(method="API MLLM (qwen-vl-max)")
        
        try:
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            prompt = f"""Evaluate this chart for query: "{query}"
Rate 0-1: Readability, Aesthetics, Data Encoding, Appropriateness.
Format:
Readability: [score]
Aesthetics: [score]
Data Encoding: [score]
Appropriateness: [score]
Issues: [list]
Suggestions: [list]"""
            
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                        {"type": "text", "text": prompt}
                    ]
                }],
                "temperature": 0.2,
                "max_tokens": 1024
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            result.raw_response = content
            result = self._parse_response(result, content)
            
        except Exception as e:
            result.error = str(e)
            result.score = 0.5
        
        result.evaluation_time = time.time() - start
        return result
    
    def _parse_response(self, result: EvaluationResult, response: str) -> EvaluationResult:
        import re
        
        patterns = {
            'readability': r'Readability[:\s]+([0-9.]+)',
            'aesthetics': r'Aesthetics[:\s]+([0-9.]+)',
            'data_encoding': r'Data Encoding[:\s]+([0-9.]+)',
            'appropriateness': r'Appropriateness[:\s]+([0-9.]+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                result.dimensions[key] = float(match.group(1))
        
        if result.dimensions:
            result.score = sum(result.dimensions.values()) / len(result.dimensions)
        
        return result


def generate_test_cases() -> List[Tuple[bytes, str, str]]:
    """生成测试用例"""
    cases = []
    
    # 测试用例 1: 高质量图表
    img1 = Image.new('RGB', (800, 600), color='white')
    draw1 = ImageDraw.Draw(img1)
    colors = ['#002FA7', '#f59e0b', '#ea580c', '#dc2626', '#b91c1c']
    for i, c in enumerate(colors):
        h = np.random.randint(200, 400)
        draw1.rectangle([100+i*130, 450-h, 200+i*130, 450], fill=c, outline='black')
        draw1.text((150+i*130, 470), f"R{i+1}", fill='black')
    draw1.text((400, 30), "Flight Operations by Region", fill='black')
    draw1.text((400, 550), "Region", fill='black')
    draw1.text((50, 300), "Operations", fill='black')
    buf1 = io.BytesIO()
    img1.save(buf1, format='PNG')
    cases.append((buf1.getvalue(), "Compare flight operations across regions", "high"))
    
    # 测试用例 2: 中等质量图表
    img2 = Image.new('RGB', (800, 600), color='white')
    draw2 = ImageDraw.Draw(img2)
    for i in range(5):
        h = np.random.randint(150, 350)
        draw2.rectangle([100+i*130, 450-h, 200+i*130, 450], fill='gray')
    draw2.text((400, 30), "Monthly Trends", fill='black')
    buf2 = io.BytesIO()
    img2.save(buf2, format='PNG')
    cases.append((buf2.getvalue(), "Show monthly trends over time", "medium"))
    
    # 测试用例 3: 低质量图表
    img3 = Image.new('RGB', (800, 600), color='white')
    draw3 = ImageDraw.Draw(img3)
    for i in range(5):
        h = np.random.randint(50, 500)
        draw3.rectangle([50+i*150, 550-h, 130+i*150, 550], fill=np.random.choice(['red', 'green', 'blue']))
    buf3 = io.BytesIO()
    img3.save(buf3, format='PNG')
    cases.append((buf3.getvalue(), "Show data distribution", "low"))
    
    return cases


def run_comparison():
    """运行对比实验"""
    print("="*70)
    print("MLLM Visual Evaluation Comparison")
    print("="*70)
    
    # 生成测试用例
    print("\n[1] Generating test cases...")
    test_cases = generate_test_cases()
    print(f"    Generated {len(test_cases)} test cases")
    
    # 初始化评估器
    print("\n[2] Initializing evaluators...")
    heuristic = HeuristicEvaluator()
    api_mllm = APIMLLMEvaluator()
    local_mllm = LocalMLLMEvaluator()
    
    # 模拟代码 (用于 Heuristic)
    sample_code = """
from pyecharts.charts import Bar
from pyecharts import options as opts

chart = Bar()
chart.add_xaxis(['A', 'B', 'C', 'D', 'E'])
chart.add_yaxis('Series', [100, 200, 150, 80, 170])
chart.set_global_opts(
    title_opts=opts.TitleOpts(title='Chart Title'),
    legend_opts=opts.LegendOpts(),
    tooltip_opts=opts.TooltipOpts()
)
"""
    
    results = {
        "heuristic": [],
        "api_mllm": [],
        "local_mllm": []
    }
    
    # 运行评估
    for i, (img_data, query, quality) in enumerate(test_cases, 1):
        print(f"\n[3.{i}] Evaluating: {query[:50]}... (Quality: {quality})")
        
        # Heuristic
        print("    Running Heuristic...")
        h_result = heuristic.evaluate(sample_code, query)
        results["heuristic"].append(h_result)
        print(f"      Score: {h_result.score:.2f}, Time: {h_result.evaluation_time:.3f}s")
        
        # API MLLM
        print("    Running API MLLM (qwen-vl-max)...")
        a_result = api_mllm.evaluate(img_data, query)
        results["api_mllm"].append(a_result)
        print(f"      Score: {a_result.score:.2f}, Time: {a_result.evaluation_time:.2f}s")
        
        # Local MLLM (仅第一个用例，因为太慢)
        if i == 1:
            print("    Running Local MLLM (Qwen2.5-VL)...")
            l_result = local_mllm.evaluate(img_data, query)
            results["local_mllm"].append(l_result)
            print(f"      Score: {l_result.score:.2f}, Time: {l_result.evaluation_time:.2f}s")
    
    # 汇总结果
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    for method, res_list in results.items():
        if res_list:
            avg_time = sum(r.evaluation_time for r in res_list) / len(res_list)
            avg_score = sum(r.score for r in res_list) / len(res_list)
            print(f"\n{method}:")
            print(f"  Avg Time: {avg_time:.3f}s")
            print(f"  Avg Score: {avg_score:.2f}")
    
    # 保存结果
    output = {
        "test_cases": len(test_cases),
        "results": {
            method: [{
                "score": r.score,
                "time": r.evaluation_time,
                "dimensions": r.dimensions,
                "issues": r.issues,
                "error": r.error
            } for r in res_list]
            for method, res_list in results.items()
        }
    }
    
    with open("experiments/results/mllm_comparison_final.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ Results saved to experiments/results/mllm_comparison_final.json")
    print("="*70)


if __name__ == "__main__":
    run_comparison()
