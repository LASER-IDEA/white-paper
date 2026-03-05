"""
MLLM Visual Evaluator - API Version (Aliyun Bailian)
使用阿里云百炼API调用 Qwen-VL-Max (qwen3vl-plus) 进行视觉评估

Features:
- 基于 HTTP API，无需本地GPU
- 支持 qwen-vl-max (即 qwen3vl-plus)
- 自动 base64 编码图片
- 性能对比: API vs 本地

Author: API-based MLLM for IEEE VIS 2026
"""

import os
import io
import base64
import json
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from pathlib import Path

import requests
from PIL import Image


# 加载环境变量
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")


@dataclass
class APIMetrics:
    """API 性能指标"""
    api_calls: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    errors: int = 0
    
    def record(self, elapsed: float, success: bool = True):
        self.api_calls += 1
        self.total_time += elapsed
        self.avg_time = self.total_time / self.api_calls
        if not success:
            self.errors += 1


@dataclass
class MLLMEvaluationResult:
    """MLLM 评估结果"""
    readability: float = 0.0
    aesthetics: float = 0.0
    data_encoding: float = 0.0
    appropriateness: float = 0.0
    overall_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    raw_response: str = ""
    evaluation_time: float = 0.0
    parse_error: Optional[str] = None
    api_error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "readability": self.readability,
            "aesthetics": self.aesthetics,
            "data_encoding": self.data_encoding,
            "appropriateness": self.appropriateness,
            "overall_score": self.overall_score,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "evaluation_time": self.evaluation_time,
            "parse_error": self.parse_error,
            "api_error": self.api_error
        }


class QwenMLLMAPIEvaluator:
    """
    阿里云百炼 Qwen-VL API 评估器
    """
    
    def __init__(self, 
                 api_key: str = None,
                 base_url: str = None,
                 model: str = None):
        """
        初始化 API 评估器
        
        Args:
            api_key: 阿里云百炼 API Key (默认从环境变量 QWEN_API_KEY)
            base_url: API 基础 URL (默认从环境变量 QWEN_BASE_URL)
            model: 模型名称 (默认从环境变量 QWEN_VL_MODEL)
        """
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.base_url = base_url or os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = model or os.getenv("QWEN_VL_MODEL", "qwen-vl-max")
        
        if not self.api_key:
            raise ValueError("QWEN_API_KEY not found. Please set it in .env file or pass as argument.")
        
        self.metrics = APIMetrics()
        
        print(f"[Qwen MLLM API] Initialized")
        print(f"  Model: {self.model}")
        print(f"  Base URL: {self.base_url}")
        print(f"  API Key: {self.api_key[:8]}...{self.api_key[-4:]}")
    
    def evaluate_single(self, 
                       image_data: bytes, 
                       query: str,
                       prompt_template: str = None) -> MLLMEvaluationResult:
        """
        评估单张图片
        
        Args:
            image_data: 图片数据 (bytes)
            query: 用户查询
            prompt_template: 自定义 prompt
            
        Returns:
            MLLMEvaluationResult
        """
        start_time = time.time()
        result = MLLMEvaluationResult()
        
        try:
            # 构建 prompt
            if prompt_template is None:
                prompt = self._build_evaluation_prompt(query)
            else:
                prompt = prompt_template.format(query=query)
            
            # 调用 API
            response = self._call_api(image_data, prompt)
            result.raw_response = response
            
            # 解析结果
            parsed = self._parse_response(response)
            result.readability = parsed.get("readability", 0.0)
            result.aesthetics = parsed.get("aesthetics", 0.0)
            result.data_encoding = parsed.get("data_encoding", 0.0)
            result.appropriateness = parsed.get("appropriateness", 0.0)
            result.overall_score = parsed.get("overall_score", 0.0)
            result.issues = parsed.get("issues", [])
            result.suggestions = parsed.get("suggestions", [])
            result.parse_error = parsed.get("parse_error")
            
            success = True
            
        except Exception as e:
            result.api_error = str(e)
            success = False
        
        elapsed = time.time() - start_time
        result.evaluation_time = elapsed
        self.metrics.record(elapsed, success)
        
        return result
    
    def evaluate_batch(self,
                      items: List[Tuple[bytes, str]],
                      prompt_template: str = None) -> List[MLLMEvaluationResult]:
        """
        批量评估
        """
        results = []
        print(f"[Qwen MLLM API] Batch evaluation: {len(items)} items")
        
        for i, (image_data, query) in enumerate(items, 1):
            print(f"  [{i}/{len(items)}] Evaluating...", end="\r")
            result = self.evaluate_single(image_data, query, prompt_template)
            results.append(result)
        
        print(f"\n[Qwen MLLM API] Batch complete. Avg time: {self.metrics.avg_time:.2f}s")
        return results
    
    def _call_api(self, image_data: bytes, prompt: str) -> str:
        """
        调用阿里云百炼 API
        """
        # 将图片转为 base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 构建请求
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "temperature": 0.2,
            "max_tokens": 1024
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # 解析响应
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        return content
    
    def _build_evaluation_prompt(self, query: str) -> str:
        """构建评估 Prompt"""
        return f"""You are a data visualization quality expert. Evaluate this chart based on the user's query.

User Query: {query}

Rate the chart on these 4 dimensions (0.00-1.00, 2 decimal places):

1. **Readability** (0-1): Clear title, axis labels, legend, data labels? Easy to read?
2. **Aesthetics** (0-1): Good color scheme? Proper layout? Visual hierarchy?
3. **Data Encoding** (0-1): Appropriate chart type? Correct data mapping?
4. **Appropriateness** (0-1): Answers user's query? Complete and relevant?

Output format:
```
Readability: [score]
Aesthetics: [score]
Data Encoding: [score]
Appropriateness: [score]
Overall: [average]
Issues: [1-3 main issues]
Suggestions: [improvement suggestions]
```

Be critical but fair. A professional chart should score >0.8."""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """解析 API 响应"""
        import re
        
        result = {
            "readability": 0.0,
            "aesthetics": 0.0,
            "data_encoding": 0.0,
            "appropriateness": 0.0,
            "overall_score": 0.0,
            "issues": [],
            "suggestions": [],
            "parse_error": None
        }
        
        try:
            # 提取分数
            patterns = {
                'readability': r'Readability[:\s]+([0-9.]+)',
                'aesthetics': r'Aesthetics[:\s]+([0-9.]+)',
                'data_encoding': r'Data Encoding[:\s]+([0-9.]+)',
                'appropriateness': r'Appropriateness[:\s]+([0-9.]+)',
                'overall_score': r'Overall[:\s]+([0-9.]+)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    result[key] = float(match.group(1))
            
            # 如果没有总体评分，计算平均值
            if result["overall_score"] == 0.0:
                result["overall_score"] = (
                    result["readability"] + result["aesthetics"] + 
                    result["data_encoding"] + result["appropriateness"]
                ) / 4
            
            # 提取 Issues
            issues_match = re.search(r'Issues[:\s]+([^\n]+(?:\n[^\n]+)*)', response, re.IGNORECASE)
            if issues_match:
                issues_text = issues_match.group(1).strip()
                result["issues"] = [i.strip('- ') for i in issues_text.split('\n') if i.strip()]
            
            # 提取 Suggestions
            suggestions_match = re.search(r'Suggestions[:\s]+([^\n]+(?:\n[^\n]+)*)', response, re.IGNORECASE)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1).strip()
                result["suggestions"] = [s.strip('- ') for s in suggestions_text.split('\n') if s.strip()]
                
        except Exception as e:
            result["parse_error"] = str(e)
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        return {
            "api_calls": self.metrics.api_calls,
            "total_time": self.metrics.total_time,
            "avg_time": self.metrics.avg_time,
            "errors": self.metrics.errors,
            "error_rate": self.metrics.errors / max(self.metrics.api_calls, 1)
        }
    
    def print_metrics(self):
        """打印性能指标"""
        print("\n" + "="*60)
        print("Qwen MLLM API Performance Metrics")
        print("="*60)
        print(f"API Calls: {self.metrics.api_calls}")
        print(f"Total Time: {self.metrics.total_time:.2f}s")
        print(f"Average Time: {self.metrics.avg_time:.2f}s")
        print(f"Errors: {self.metrics.errors}")
        print(f"Error Rate: {self.metrics.errors/max(self.metrics.api_calls, 1)*100:.1f}%")
        print("="*60)


def quick_test():
    """
    快速测试 Qwen MLLM API
    """
    import numpy as np
    from PIL import Image, ImageDraw
    
    print("="*70)
    print("Qwen MLLM API (Aliyun Bailian) Test")
    print("="*70)
    
    # 初始化评估器
    try:
        evaluator = QwenMLLMAPIEvaluator()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # 生成测试图片
    print("\n[1] Generating test images...")
    test_images = []
    
    # 高质量图表
    img1 = Image.new('RGB', (800, 600), color='white')
    draw1 = ImageDraw.Draw(img1)
    colors = ['#002FA7', '#f59e0b', '#ea580c', '#dc2626', '#b91c1c']
    for i, c in enumerate(colors):
        h = np.random.randint(150, 350)
        draw1.rectangle([100+i*130, 450-h, 200+i*130, 450], fill=c, outline='black')
    draw1.text((400, 30), "Flight Operations by Region", fill='black')
    buf1 = io.BytesIO()
    img1.save(buf1, format='PNG')
    test_images.append((buf1.getvalue(), "Compare flight operations across regions"))
    
    # 中等质量图表
    img2 = Image.new('RGB', (800, 600), color='white')
    draw2 = ImageDraw.Draw(img2)
    for i in range(5):
        h = np.random.randint(100, 300)
        draw2.rectangle([100+i*130, 450-h, 200+i*130, 450], fill='gray')
    draw2.text((400, 30), "Chart", fill='black')
    buf2 = io.BytesIO()
    img2.save(buf2, format='PNG')
    test_images.append((buf2.getvalue(), "Show monthly trends"))
    
    # 低质量图表
    img3 = Image.new('RGB', (800, 600), color='white')
    draw3 = ImageDraw.Draw(img3)
    for i in range(5):
        h = np.random.randint(50, 500)
        draw3.rectangle([50+i*150, 550-h, 130+i*150, 550], fill=np.random.choice(['red', 'green', 'blue']))
    buf3 = io.BytesIO()
    img3.save(buf3, format='PNG')
    test_images.append((buf3.getvalue(), "Show data distribution"))
    
    print(f"  Generated {len(test_images)} test images")
    
    # 评估
    print("\n[2] Evaluating with Qwen-VL API...")
    results = []
    
    for i, (img_data, query) in enumerate(test_images, 1):
        print(f"\n  [{i}/{len(test_images)}] {query[:40]}...")
        result = evaluator.evaluate_single(img_data, query)
        results.append(result)
        
        print(f"    Score: {result.overall_score:.2f} | Time: {result.evaluation_time:.2f}s")
        print(f"    Readability: {result.readability:.2f} | Aesthetics: {result.aesthetics:.2f}")
        
        if result.api_error:
            print(f"    ⚠️ API Error: {result.api_error[:60]}")
        elif result.parse_error:
            print(f"    ⚠️ Parse Error: {result.parse_error}")
    
    # 打印指标
    evaluator.print_metrics()
    
    # 显示详细结果
    print("\n[3] Detailed Results:")
    for i, (result, (img, query)) in enumerate(zip(results, test_images), 1):
        print(f"\n  Chart {i}: {query[:50]}...")
        print(f"    Overall: {result.overall_score:.2f}")
        print(f"    Dimensions: R={result.readability:.2f}, A={result.aesthetics:.2f}, "
              f"D={result.data_encoding:.2f}, P={result.appropriateness:.2f}")
        if result.issues:
            print(f"    Issues: {result.issues[:2]}")
        if result.suggestions:
            print(f"    Suggestions: {result.suggestions[:2]}")
    
    print("\n" + "="*70)
    print("Test Complete!")
    print("="*70)


if __name__ == "__main__":
    quick_test()
