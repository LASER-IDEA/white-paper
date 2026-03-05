"""
MLLM-based Visual Evaluation Module
使用本地 Qwen2.5-VL 模型进行图表质量评估

Requirements:
    pip install torch torchvision transformers accelerate qwen-vl-utils
"""

import os
import re
import torch
from typing import Dict, Any, Optional
from PIL import Image
import io
import base64


class MLLMVisualEvaluator:
    """
    基于多模态大语言模型的可视化质量评估器
    使用 Qwen2.5-VL 本地部署
    """
    
    def __init__(self, model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct", device: str = "auto", 
                 cache_dir: str = None, local_files_only: bool = True):
        """
        初始化 MLLM 评估器
        
        Args:
            model_name: HuggingFace 模型名称
            device: 运行设备 (auto/cuda/cpu)
            cache_dir: 本地缓存目录
            local_files_only: 是否只使用本地文件
        """
        self.model_name = model_name
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.local_files_only = local_files_only
        
        # 设置缓存目录
        if cache_dir is None:
            self.cache_dir = "/data1/xh/workspace/white-paper/huggingface_cache"
        else:
            self.cache_dir = cache_dir
        
        # 查找本地模型路径
        self.local_model_path = self._find_local_model_path()
        
        # 延迟加载模型 (只在需要时加载)
        self._model = None
        self._processor = None
        
        print(f"[MLLM Evaluator] Initialized with device: {self.device}")
        print(f"[MLLM Evaluator] Cache dir: {self.cache_dir}")
        print(f"[MLLM Evaluator] Local model path: {self.local_model_path}")
        if torch.cuda.is_available():
            print(f"[MLLM Evaluator] Available GPUs: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    
    def _find_local_model_path(self) -> str:
        """查找本地模型路径"""
        import glob
        
        # 尝试找到 snapshot 目录
        model_cache_pattern = f"{self.cache_dir}/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/*"
        snapshots = glob.glob(model_cache_pattern)
        
        if snapshots:
            return snapshots[0]  # 返回第一个 snapshot 路径
        
        # 备用路径
        fallback_path = f"{self.cache_dir}/Qwen2.5-VL-7B-Instruct"
        if os.path.exists(fallback_path):
            return fallback_path
        
        return None
    
    def _load_model(self):
        """延迟加载模型"""
        if self._model is not None:
            return
        
        if self.local_model_path is None:
            raise ValueError("Local model not found. Please download the model first.")
        
        print(f"[MLLM Evaluator] Loading model from: {self.local_model_path}")
        
        try:
            from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
            
            # 从本地路径加载模型
            self._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.local_model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True,
                local_files_only=self.local_files_only
            )
            
            # 从本地路径加载处理器
            self._processor = AutoProcessor.from_pretrained(
                self.local_model_path,
                trust_remote_code=True,
                local_files_only=self.local_files_only
            )
            
            print("[MLLM Evaluator] Model loaded successfully from local cache")
            
        except Exception as e:
            print(f"[MLLM Evaluator] Error loading model: {e}")
            print("[MLLM Evaluator] Please install: pip install transformers accelerate qwen-vl-utils")
            raise
    
    def evaluate(self, chart_html: str, query: str, image_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        评估可视化图表质量
        
        Args:
            chart_html: PyECharts 生成的 HTML 代码
            query: 用户原始查询
            image_data: 图表图片数据 (bytes)，如不提供则自动生成
            
        Returns:
            质量评估结果字典
        """
        self._load_model()
        
        # 如果没有提供图片，从 HTML 生成
        if image_data is None:
            image_data = self._html_to_image(chart_html)
        
        # 构建评估 prompt
        prompt = self._build_evaluation_prompt(query)
        
        # 调用 MLLM 进行评估
        result = self._call_mllm(image_data, prompt)
        
        # 解析结果
        parsed = self._parse_evaluation(result)
        
        return parsed
    
    def _html_to_image(self, html_content: str) -> bytes:
        """
        将 HTML 转换为图片
        使用 playwright 截图，增加超时时间
        """
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                # 启动浏览器，设置更长的超时
                browser = p.chromium.launch(
                    args=['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
                )
                
                context = browser.new_context(
                    viewport={"width": 1000, "height": 700},
                    bypass_csp=True  # 绕过内容安全策略
                )
                
                page = context.new_page()
                
                # 设置超时为 60 秒
                page.set_default_timeout(60000)
                
                # 加载 HTML
                page.set_content(html_content, wait_until='networkidle')
                
                # 等待图表渲染完成（等待 canvas 或 svg 元素）
                page.wait_for_selector('canvas, svg', timeout=30000)
                
                # 额外等待确保渲染完成
                page.wait_for_timeout(2000)
                
                # 截图
                screenshot = page.screenshot(
                    type="png",
                    full_page=False,
                    clip={'x': 0, 'y': 0, 'width': 1000, 'height': 700}
                )
                
                browser.close()
                return screenshot
                
        except ImportError:
            print("[MLLM Evaluator] Playwright not installed")
            return None
        except Exception as e:
            print(f"[MLLM Evaluator] Error converting HTML to image: {str(e)[:80]}")
            return None
    
    def _build_evaluation_prompt(self, query: str) -> str:
        """构建评估用的 prompt"""
        prompt = f"""你是一个数据可视化质量评估专家。请评估这张图表的质量。

用户查询意图: {query}

请从以下四个维度进行评分 (0-1 分，保留两位小数)，并给出简要理由：

1. **可读性 (Readability)**: 图表是否有清晰的标题、轴标签、图例、数据标签？
2. **美观性 (Aesthetics)**: 颜色搭配是否协调？布局是否合理？视觉层次是否清晰？
3. **数据编码 (Data Encoding)**: 图表类型是否适合展示这些数据？数据映射是否正确？
4. **适用性 (Appropriateness)**: 图表是否符合用户查询意图？是否完整回答了问题？

请按以下格式输出：
```
可读性: [分数]
美观性: [分数]
数据编码: [分数]
适用性: [分数]
总体评分: [平均分]
主要问题: [列出1-3个主要问题]
改进建议: [给出具体改进建议]
```
"""
        return prompt
    
    def _call_mllm(self, image_data: bytes, prompt: str) -> str:
        """调用 MLLM 模型"""
        if image_data is None:
            raise ValueError("Image data is required for MLLM evaluation")
        
        # 将图片转换为 PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # 准备消息
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # 处理输入
        text = self._processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        
        inputs = self._processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt"
        )
        
        # 移动到设备
        inputs = inputs.to(self._model.device)
        
        # 生成
        with torch.no_grad():
            generated_ids = self._model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9
            )
        
        # 解码输出
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        response = self._processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]
        
        return response
    
    def _parse_evaluation(self, response: str) -> Dict[str, Any]:
        """解析 MLLM 的评估结果"""
        result = {
            "readability": 0.7,
            "aesthetics": 0.7,
            "data_encoding": 0.7,
            "appropriateness": 0.7,
            "overall_score": 0.7,
            "issues": [],
            "suggestions": [],
            "raw_response": response
        }
        
        try:
            # 使用正则提取分数
            readability_match = re.search(r'可读性[:\s]+([0-9.]+)', response)
            aesthetics_match = re.search(r'美观性[:\s]+([0-9.]+)', response)
            encoding_match = re.search(r'数据编码[:\s]+([0-9.]+)', response)
            appropriateness_match = re.search(r'适用性[:\s]+([0-9.]+)', response)
            overall_match = re.search(r'总体评分[:\s]+([0-9.]+)', response)
            
            if readability_match:
                result["readability"] = float(readability_match.group(1))
            if aesthetics_match:
                result["aesthetics"] = float(aesthetics_match.group(1))
            if encoding_match:
                result["data_encoding"] = float(encoding_match.group(1))
            if appropriateness_match:
                result["appropriateness"] = float(appropriateness_match.group(1))
            if overall_match:
                result["overall_score"] = float(overall_match.group(1))
            else:
                # 计算平均分
                result["overall_score"] = (
                    result["readability"] + result["aesthetics"] + 
                    result["data_encoding"] + result["appropriateness"]
                ) / 4
            
            # 提取问题和建议
            issues_match = re.search(r'主要问题[:\s]+([^\n]+(?:\n[^\n]+)*)', response)
            if issues_match:
                issues_text = issues_match.group(1).strip()
                result["issues"] = [i.strip() for i in issues_text.split('\n') if i.strip()]
            
            suggestions_match = re.search(r'改进建议[:\s]+([^\n]+(?:\n[^\n]+)*)', response)
            if suggestions_match:
                suggestions_text = suggestions_match.group(1).strip()
                result["suggestions"] = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
                
        except Exception as e:
            print(f"[MLLM Evaluator] Error parsing response: {e}")
            result["parse_error"] = str(e)
        
        return result


class HybridVisualEvaluator:
    """
    混合评估器：结合 Heuristic 和 MLLM
    - 简单情况：使用 Heuristic (快速)
    - 复杂情况或争议：使用 MLLM (准确)
    """
    
    def __init__(self, use_mllm: bool = True, mllm_threshold: float = 0.7):
        """
        初始化混合评估器
        
        Args:
            use_mllm: 是否启用 MLLM
            mllm_threshold: Heuristic 评分低于此值时触发 MLLM 评估
        """
        self.use_mllm = use_mllm
        self.mllm_threshold = mllm_threshold
        
        # Heuristic 评估器
        from agents.visual_evaluator import VisualQualityEvaluator
        self.heuristic_evaluator = VisualQualityEvaluator()
        
        # MLLM 评估器 (延迟加载)
        self._mllm_evaluator = None
    
    def evaluate(self, code: str, query: str, chart_html: str = None) -> Dict[str, Any]:
        """
        评估图表质量
        
        Args:
            code: 生成的代码
            query: 用户查询
            chart_html: 图表 HTML (可选，用于 MLLM 评估)
            
        Returns:
            评估结果
        """
        # 第一步：Heuristic 评估
        heuristic_result = self.heuristic_evaluator.evaluate(code, query)
        
        # 如果启用 MLLM 且评分低于阈值，使用 MLLM 进行二次评估
        if (self.use_mllm and 
            chart_html and 
            heuristic_result.get("overall_score", 1.0) < self.mllm_threshold):
            
            try:
                if self._mllm_evaluator is None:
                    self._mllm_evaluator = MLLMVisualEvaluator()
                
                mllm_result = self._mllm_evaluator.evaluate(chart_html, query)
                
                # 合并结果 (优先使用 MLLM 结果)
                return {
                    **heuristic_result,
                    "mllm_scores": {
                        "readability": mllm_result.get("readability"),
                        "aesthetics": mllm_result.get("aesthetics"),
                        "data_encoding": mllm_result.get("data_encoding"),
                        "appropriateness": mllm_result.get("appropriateness"),
                        "overall_score": mllm_result.get("overall_score"),
                    },
                    "mllm_issues": mllm_result.get("issues", []),
                    "mllm_suggestions": mllm_result.get("suggestions", []),
                    "evaluation_method": "hybrid"
                }
                
            except Exception as e:
                print(f"[Hybrid Evaluator] MLLM evaluation failed: {e}")
                return {**heuristic_result, "evaluation_method": "heuristic_only"}
        
        return {**heuristic_result, "evaluation_method": "heuristic"}


# 便捷函数
def evaluate_with_mllm(chart_html: str, query: str, model_name: str = None) -> Dict[str, Any]:
    """
    使用 MLLM 评估图表的便捷函数
    
    Args:
        chart_html: 图表 HTML
        query: 用户查询
        model_name: 模型名称 (可选)
        
    Returns:
        评估结果
    """
    evaluator = MLLMVisualEvaluator(model_name=model_name) if model_name else MLLMVisualEvaluator()
    return evaluator.evaluate(chart_html, query)


def compare_heuristic_vs_mllm(code: str, query: str, chart_html: str) -> Dict[str, Any]:
    """
    对比 Heuristic 和 MLLM 评估结果
    
    用于论文实验：验证 Heuristic 方法的有效性
    """
    # Heuristic 评估
    from agents.visual_evaluator import VisualQualityEvaluator
    heuristic = VisualQualityEvaluator()
    h_result = heuristic.evaluate(code, query)
    
    # MLLM 评估
    mllm = MLLMVisualEvaluator()
    m_result = mllm.evaluate(chart_html, query)
    
    return {
        "heuristic": h_result,
        "mllm": m_result,
        "comparison": {
            "readability_diff": abs(h_result.get("readability", 0) - m_result.get("readability", 0)),
            "aesthetics_diff": abs(h_result.get("aesthetics", 0) - m_result.get("aesthetics", 0)),
            "data_encoding_diff": abs(h_result.get("data_encoding", 0) - m_result.get("data_encoding", 0)),
            "appropriateness_diff": abs(h_result.get("appropriateness", 0) - m_result.get("appropriateness", 0)),
            "overall_diff": abs(h_result.get("overall_score", 0) - m_result.get("overall_score", 0)),
        }
    }


if __name__ == "__main__":
    # 测试代码
    print("="*60)
    print("MLLM Visual Evaluator Test")
    print("="*60)
    
    # 检查 GPU
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    
    # 初始化评估器
    print("\nInitializing MLLM Visual Evaluator...")
    evaluator = MLLMVisualEvaluator()
    
    print("\nReady! Use evaluate() method to assess charts.")
    print("="*60)
