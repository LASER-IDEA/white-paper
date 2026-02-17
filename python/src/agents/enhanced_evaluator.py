"""
Enhanced Intelligent Evaluator Agent
增强版智能评估器 - 多维度深度评估

核心增强:
1. 代码执行验证 (Execution Verification)
2. LLM-based 深度代码分析
3. 数据一致性检查
4. 意图对齐度评估
5. 多维度融合评分
6. 历史案例学习
7. 自适应权重调整

Author: Enhanced for IEEE VIS 2026
"""

import os
import sys
import json
import re
import ast
import traceback
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base import BaseAgent, AgentState


@dataclass
class EvaluationDimension:
    """评估维度数据类"""
    name: str
    score: float = 0.0
    weight: float = 1.0
    confidence: float = 1.0
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class CodeExecutionResult:
    """代码执行结果"""
    success: bool = False
    html_output: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    warnings: List[str] = field(default_factory=list)


@dataclass
class EnhancedEvaluationResult:
    """增强评估结果"""
    overall_score: float = 0.0
    confidence: float = 0.0
    is_pass: bool = False
    dimensions: Dict[str, EvaluationDimension] = field(default_factory=dict)
    execution_result: Optional[CodeExecutionResult] = None
    reflection_needed: bool = False
    improvement_potential: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": self.overall_score,
            "confidence": self.confidence,
            "is_pass": self.is_pass,
            "reflection_needed": self.reflection_needed,
            "improvement_potential": self.improvement_potential,
            "dimensions": {k: {
                "score": v.score,
                "weight": v.weight,
                "confidence": v.confidence,
                "issues": v.issues,
                "suggestions": v.suggestions
            } for k, v in self.dimensions.items()},
            "execution": {
                "success": self.execution_result.success if self.execution_result else False,
                "error": self.execution_result.error_message if self.execution_result else None
            } if self.execution_result else None
        }


class CodeExecutor:
    """
    代码执行验证器
    实际运行生成的代码，验证可执行性和输出
    """
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.execution_history = []
    
    def execute(self, code: str, query: str) -> CodeExecutionResult:
        """
        安全执行生成的代码
        
        Returns:
            CodeExecutionResult: 执行结果
        """
        import time
        import io
        import contextlib
        
        result = CodeExecutionResult()
        start_time = time.time()
        
        try:
            # 1. 语法检查
            try:
                ast.parse(code)
            except SyntaxError as e:
                result.error_message = f"Syntax Error: {str(e)}"
                result.execution_time = time.time() - start_time
                return result
            
            # 2. 准备执行环境
            exec_globals = {
                '__builtins__': __builtins__,
                'print': lambda *args, **kwargs: None,  # 静默print
            }
            
            # 安全导入常用库
            safe_modules = [
                'pyecharts', 'json', 'os', 'sys', 'math', 'random',
                'datetime', 'collections', 'itertools', 'typing'
            ]
            
            for module in safe_modules:
                try:
                    exec_globals[module] = __import__(module)
                except:
                    pass
            
            # 3. 执行代码
            output_buffer = io.StringIO()
            
            with contextlib.redirect_stdout(output_buffer):
                with contextlib.redirect_stderr(output_buffer):
                    exec(code, exec_globals)
            
            # 4. 检查是否生成了图表对象
            chart_var = self._find_chart_variable(exec_globals)
            
            if chart_var:
                # 尝试渲染 HTML
                try:
                    chart_obj = exec_globals[chart_var]
                    if hasattr(chart_obj, 'render_embed'):
                        html_output = chart_obj.render_embed()
                        result.html_output = html_output
                        result.success = True
                    elif hasattr(chart_obj, 'dump_options_with_quotes'):
                        # 处理 Grid/Timeline 等复合图表
                        html_output = chart_obj.render_embed()
                        result.html_output = html_output
                        result.success = True
                    else:
                        result.warnings.append("Chart object found but render method unclear")
                        result.success = True  # 仍然认为成功
                except Exception as e:
                    result.error_message = f"Render Error: {str(e)}"
                    result.warnings.append(f"Code executed but rendering failed: {str(e)}")
            else:
                # 检查是否有其他输出
                output = output_buffer.getvalue()
                if output:
                    result.warnings.append(f"Code produced output but no chart object detected")
                    result.success = True  # 可能有其他形式的输出
                else:
                    result.warnings.append("No chart object or output detected")
            
            result.execution_time = time.time() - start_time
            
        except Exception as e:
            result.error_message = f"Execution Error: {str(e)}"
            result.execution_time = time.time() - start_time
            result.warnings.append(traceback.format_exc())
        
        self.execution_history.append({
            "query": query,
            "success": result.success,
            "time": result.execution_time
        })
        
        return result
    
    def _find_chart_variable(self, namespace: Dict) -> Optional[str]:
        """在命名空间中查找图表变量"""
        chart_patterns = ['chart', 'c', 'bar', 'line', 'pie', 'scatter', 
                         'map', 'graph', 'page', 'grid']
        
        # 先尝试常见变量名
        for pattern in chart_patterns:
            if pattern in namespace:
                obj = namespace[pattern]
                if self._is_chart_object(obj):
                    return pattern
        
        # 遍历所有变量
        for name, obj in namespace.items():
            if not name.startswith('_') and self._is_chart_object(obj):
                return name
        
        return None
    
    def _is_chart_object(self, obj) -> bool:
        """检查对象是否为图表对象"""
        class_name = type(obj).__name__
        chart_classes = ['Chart', 'Bar', 'Line', 'Pie', 'Scatter', 'Map', 
                        'Grid', 'Page', 'Timeline', 'Overlap']
        return any(cls in class_name for cls in chart_classes)


class LLMCodeAnalyzer:
    """
    LLM-based 代码深度分析器
    使用 LLM 进行语义级代码质量评估
    """
    
    def __init__(self, provider: str = "deepseek"):
        self.provider = provider
        self.analysis_cache = {}
    
    def analyze(self, code: str, query: str, execution_result: CodeExecutionResult) -> Dict[str, Any]:
        """
        深度分析代码质量
        
        Returns:
            {
                "code_quality": 0.0-1.0,
                "intent_alignment": 0.0-1.0,
                "best_practices": 0.0-1.0,
                "issues": [str],
                "suggestions": [str],
                "improvement_plan": str
            }
        """
        # 检查缓存
        cache_key = hash(code + query)
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        try:
            from llm_client import LLMClient
            
            llm = LLMClient(provider=self.provider)
            
            system_prompt = """You are an expert Python data visualization code reviewer.
Analyze the provided PyECharts code for quality, correctness, and alignment with user intent.

Evaluate on:
1. Code Quality (0-1): Clean code, proper structure, error handling
2. Intent Alignment (0-1): Does it correctly implement the user's request?
3. Best Practices (0-1): Follows visualization best practices, efficient code

Provide specific, actionable feedback.

Output JSON format:
{
    "code_quality": 0.0-1.0,
    "intent_alignment": 0.0-1.0,
    "best_practices": 0.0-1.0,
    "issues": ["specific issue 1", "issue 2"],
    "suggestions": ["actionable suggestion 1", "suggestion 2"],
    "improvement_plan": "Step-by-step improvement strategy"
}"""
            
            # 构建包含执行结果的上下文
            execution_info = ""
            if execution_result:
                if execution_result.success:
                    execution_info = f"\nCode Execution: SUCCESS (took {execution_result.execution_time:.2f}s)"
                    if execution_result.warnings:
                        execution_info += f"\nWarnings: {execution_result.warnings}"
                else:
                    execution_info = f"\nCode Execution: FAILED\nError: {execution_result.error_message}"
            
            user_prompt = f"""User Query: {query}

Generated Code:
```python
{code}
```
{execution_info}

Analyze this visualization code comprehensively."""
            
            response = llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2
            )
            
            # 解析 JSON
            analysis = self._parse_analysis(response)
            
            # 缓存结果
            self.analysis_cache[cache_key] = analysis
            
            return analysis
            
        except Exception as e:
            print(f"[LLM Analyzer] Error: {e}")
            return {
                "code_quality": 0.5,
                "intent_alignment": 0.5,
                "best_practices": 0.5,
                "issues": [f"Analysis failed: {str(e)}"],
                "suggestions": [],
                "improvement_plan": "Retry analysis or use heuristic evaluation"
            }
    
    def _parse_analysis(self, response: str) -> Dict[str, Any]:
        """解析 LLM 分析结果"""
        import json
        
        try:
            # 尝试提取 JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            analysis = json.loads(json_str)
            
            # 确保所有字段存在
            defaults = {
                "code_quality": 0.5,
                "intent_alignment": 0.5,
                "best_practices": 0.5,
                "issues": [],
                "suggestions": [],
                "improvement_plan": ""
            }
            
            for key, value in defaults.items():
                if key not in analysis:
                    analysis[key] = value
            
            return analysis
            
        except:
            # 解析失败返回默认值
            return {
                "code_quality": 0.5,
                "intent_alignment": 0.5,
                "best_practices": 0.5,
                "issues": ["Failed to parse LLM analysis"],
                "suggestions": ["Check code manually"],
                "improvement_plan": response[:500]  # 返回原始响应的前500字符
            }


class DataConsistencyChecker:
    """
    数据一致性检查器
    验证图表数据与查询意图的一致性
    """
    
    def check(self, code: str, query: str, html_output: Optional[str]) -> Dict[str, Any]:
        """
        检查数据一致性
        
        Returns:
            {
                "data_completeness": 0.0-1.0,
                "data_accuracy": 0.0-1.0,
                "field_coverage": 0.0-1.0,
                "issues": [str],
                "extracted_fields": [str]
            }
        """
        issues = []
        extracted_fields = []
        
        # 1. 提取代码中的数据字段
        field_patterns = [
            r'add_yaxis\([\'"]([^\'"]*)[\'"]',
            r'add\([\'"]([^\'"]*)[\'"]',
            r'xaxis_opts.*?name=[\'"]([^\'"]*)[\'"]',
            r'yaxis_opts.*?name=[\'"]([^\'"]*)[\'"]',
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, code)
            extracted_fields.extend(matches)
        
        # 2. 检查查询中的关键词是否在代码中体现
        query_keywords = self._extract_keywords(query)
        matched_keywords = []
        
        for keyword in query_keywords:
            if keyword.lower() in code.lower():
                matched_keywords.append(keyword)
        
        field_coverage = len(matched_keywords) / max(len(query_keywords), 1)
        
        # 3. 检查数据完整性
        data_completeness = self._check_data_completeness(code)
        
        # 4. 生成问题报告
        if field_coverage < 0.5:
            issues.append(f"Low field coverage: {field_coverage:.0%} of query keywords found in code")
        
        if not extracted_fields:
            issues.append("No data fields detected in code")
        
        return {
            "data_completeness": data_completeness,
            "data_accuracy": 0.8 if field_coverage > 0.5 else 0.5,  # 简化估计
            "field_coverage": field_coverage,
            "issues": issues,
            "extracted_fields": extracted_fields,
            "matched_keywords": matched_keywords
        }
    
    def _extract_keywords(self, query: str) -> List[str]:
        """从查询中提取关键词"""
        # 领域关键词库
        domain_keywords = [
            'flight', 'drone', 'uav', 'operation', 'mission',
            'region', 'area', 'zone', 'time', 'date', 'month', 'year',
            'duration', 'distance', 'altitude', 'speed', 'operator',
            'purpose', 'type', 'model', 'status', 'weather'
        ]
        
        query_lower = query.lower()
        found = [kw for kw in domain_keywords if kw in query_lower]
        
        return found
    
    def _check_data_completeness(self, code: str) -> float:
        """检查数据完整性"""
        score = 0.5
        
        # 检查数据系列
        if 'add_yaxis' in code or '.add(' in code:
            score += 0.2
        
        # 检查坐标轴
        if 'add_xaxis' in code:
            score += 0.15
        
        # 检查标题
        if 'TitleOpts' in code:
            score += 0.1
        
        # 检查数据标签
        if 'LabelOpts' in code or 'label_opts' in code:
            score += 0.05
        
        return min(score, 1.0)


class EnhancedEvaluatorAgent(BaseAgent):
    """
    增强版智能评估器 Agent
    整合多维度智能评估
    """
    
    def __init__(self, 
                 llm_provider: str = "deepseek",
                 use_llm_analysis: bool = True,
                 execution_timeout: int = 10):
        super().__init__(name="EnhancedEvaluator", llm_provider=llm_provider)
        
        # 子模块
        self.code_executor = CodeExecutor(timeout=execution_timeout)
        self.llm_analyzer = LLMCodeAnalyzer(provider=llm_provider) if use_llm_analysis else None
        self.data_checker = DataConsistencyChecker()
        
        # 配置
        self.use_llm_analysis = use_llm_analysis
        self.pass_threshold = 0.75
        
        # 评估历史 (用于自适应学习)
        self.evaluation_history = []
        self.dimension_weights = {
            "syntax_validity": 0.15,
            "execution_success": 0.20,
            "code_quality": 0.15,
            "intent_alignment": 0.20,
            "data_consistency": 0.15,
            "visual_completeness": 0.15
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """执行评估（抽象方法实现）"""
        return self.process(state)
    
    def process(self, state: AgentState) -> AgentState:
        """
        执行增强评估
        """
        print(f"\n[{self.name}] Starting enhanced evaluation...")
        
        code = state.generated_code or ""
        query = state.user_query
        iteration = state.iteration_count
        
        # 1. 代码执行验证
        print("  [1/6] Code execution verification...")
        execution_result = self.code_executor.execute(code, query)
        
        # 2. LLM 深度分析
        print("  [2/6] LLM-based code analysis...")
        llm_analysis = {}
        if self.llm_analyzer and execution_result.success:
            llm_analysis = self.llm_analyzer.analyze(code, query, execution_result)
        
        # 3. 数据一致性检查
        print("  [3/6] Data consistency check...")
        data_check = self.data_checker.check(code, query, execution_result.html_output)
        
        # 4. 语法和结构检查
        print("  [4/6] Syntax and structure analysis...")
        syntax_dim = self._evaluate_syntax(code)
        
        # 5. 视觉完整性检查
        print("  [5/6] Visual completeness check...")
        visual_dim = self._evaluate_visual_completeness(code, execution_result)
        
        # 6. 融合评分
        print("  [6/6] Fusion scoring...")
        result = self._fusion_score(
            execution_result=execution_result,
            llm_analysis=llm_analysis,
            data_check=data_check,
            syntax_dim=syntax_dim,
            visual_dim=visual_dim
        )
        
        # 记录历史
        self.evaluation_history.append({
            "query": query,
            "score": result.overall_score,
            "pass": result.is_pass,
            "iteration": iteration
        })
        
        # 更新状态
        state.execution_result = {
            "enhanced_evaluation": result.to_dict(),
            "execution_success": execution_result.success,
            "execution_error": execution_result.error_message,
            "execution_warnings": execution_result.warnings,
            "quality_score": result.overall_score,
            "evaluation_passed": result.is_pass
        }
        
        # 生成反馈
        if not result.is_pass or result.reflection_needed:
            feedback = self._generate_feedback(result)
            state.visual_feedback = {
                "feedback": feedback,
                "score": result.overall_score,
                "issues": [i for d in result.dimensions.values() for i in d.issues]
            }
            print(f"  Feedback: {feedback[:100]}...")
        
        print(f"  Score: {result.overall_score:.2f} | Pass: {result.is_pass} | "
              f"Confidence: {result.confidence:.2f}")
        
        return state
    
    def _evaluate_syntax(self, code: str) -> EvaluationDimension:
        """评估语法正确性"""
        dim = EvaluationDimension(name="syntax_validity", weight=0.15)
        
        try:
            ast.parse(code)
            dim.score = 1.0
            dim.details["syntax_valid"] = True
        except SyntaxError as e:
            dim.score = 0.0
            dim.issues.append(f"Syntax error: {str(e)}")
            dim.suggestions.append("Fix syntax error before proceeding")
            dim.details["syntax_valid"] = False
            dim.details["error"] = str(e)
        
        return dim
    
    def _evaluate_visual_completeness(self, code: str, 
                                     execution_result: CodeExecutionResult) -> EvaluationDimension:
        """评估视觉完整性"""
        dim = EvaluationDimension(name="visual_completeness", weight=0.15)
        
        checks = {
            "title": "TitleOpts" in code,
            "xaxis": "add_xaxis" in code,
            "yaxis": "add_yaxis" in code or "Pie" in code,
            "data": "add_yaxis" in code or ".add(" in code,
            "legend": "LegendOpts" in code,
            "tooltip": "TooltipOpts" in code or "tooltip_opts" in code,
            "colors": "color" in code.lower() or "itemstyle" in code.lower()
        }
        
        passed = sum(checks.values())
        total = len(checks)
        dim.score = passed / total
        dim.details["checks"] = checks
        
        # 记录缺失项
        missing = [k for k, v in checks.items() if not v]
        if missing:
            dim.issues.append(f"Missing visual elements: {', '.join(missing)}")
            dim.suggestions.extend([
                f"Add {m}" for m in missing[:3]
            ])
        
        # 执行成功加分
        if execution_result.success:
            dim.score = min(dim.score + 0.1, 1.0)
        
        return dim
    
    def _fusion_score(self,
                     execution_result: CodeExecutionResult,
                     llm_analysis: Dict,
                     data_check: Dict,
                     syntax_dim: EvaluationDimension,
                     visual_dim: EvaluationDimension) -> EnhancedEvaluationResult:
        """
        多维度融合评分
        """
        result = EnhancedEvaluationResult()
        result.execution_result = execution_result
        
        # 维度 1: 语法有效性
        result.dimensions["syntax"] = syntax_dim
        
        # 维度 2: 执行成功
        exec_dim = EvaluationDimension(name="execution", weight=0.20)
        exec_dim.score = 1.0 if execution_result.success else 0.0
        if not execution_result.success:
            exec_dim.issues.append(f"Execution failed: {execution_result.error_message}")
            exec_dim.suggestions.append("Fix execution error")
        result.dimensions["execution"] = exec_dim
        
        # 维度 3: 代码质量 (来自 LLM 或启发式)
        quality_dim = EvaluationDimension(name="code_quality", weight=0.15)
        if llm_analysis:
            quality_dim.score = llm_analysis.get("code_quality", 0.5)
            quality_dim.issues.extend(llm_analysis.get("issues", []))
            quality_dim.suggestions.extend(llm_analysis.get("suggestions", []))
        else:
            # 启发式评估
            quality_dim.score = self._heuristic_code_quality(syntax_dim, visual_dim)
        result.dimensions["code_quality"] = quality_dim
        
        # 维度 4: 意图对齐 (来自 LLM 或启发式)
        intent_dim = EvaluationDimension(name="intent_alignment", weight=0.20)
        if llm_analysis:
            intent_dim.score = llm_analysis.get("intent_alignment", 0.5)
        else:
            intent_dim.score = data_check.get("field_coverage", 0.5)
        intent_dim.details["field_coverage"] = data_check.get("field_coverage", 0)
        intent_dim.issues.extend(data_check.get("issues", []))
        result.dimensions["intent_alignment"] = intent_dim
        
        # 维度 5: 数据一致性
        data_dim = EvaluationDimension(name="data_consistency", weight=0.15)
        data_dim.score = (data_check.get("data_completeness", 0.5) + 
                         data_check.get("data_accuracy", 0.5)) / 2
        data_dim.details["extracted_fields"] = data_check.get("extracted_fields", [])
        data_dim.details["matched_keywords"] = data_check.get("matched_keywords", [])
        result.dimensions["data_consistency"] = data_dim
        
        # 维度 6: 视觉完整性
        result.dimensions["visual"] = visual_dim
        
        # 计算加权总分
        total_weight = sum(d.weight for d in result.dimensions.values())
        weighted_sum = sum(d.score * d.weight for d in result.dimensions.values())
        result.overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # 计算置信度
        result.confidence = self._calculate_confidence(result.dimensions, llm_analysis)
        
        # 判断是否通过
        result.is_pass = (result.overall_score >= self.pass_threshold and 
                         execution_result.success and
                         syntax_dim.score == 1.0)
        
        # 判断是否需要反思
        result.reflection_needed = (
            not result.is_pass or
            result.overall_score < 0.85 or
            len([i for d in result.dimensions.values() for i in d.issues]) > 2
        )
        
        # 改进潜力
        result.improvement_potential = 1.0 - result.overall_score
        
        return result
    
    def _heuristic_code_quality(self, syntax_dim: EvaluationDimension, 
                                visual_dim: EvaluationDimension) -> float:
        """启发式代码质量评估"""
        return (syntax_dim.score * 0.4 + visual_dim.score * 0.6)
    
    def _calculate_confidence(self, dimensions: Dict[str, EvaluationDimension],
                            llm_analysis: Dict) -> float:
        """计算评估置信度"""
        # 基于多个因素计算
        factors = []
        
        # 维度一致性
        scores = [d.score for d in dimensions.values()]
        score_variance = np.var(scores) if scores else 0
        factors.append(1.0 - score_variance)  # 方差越小置信度越高
        
        # LLM 可用性
        factors.append(1.0 if llm_analysis else 0.6)
        
        # 执行成功
        exec_dim = dimensions.get("execution")
        factors.append(1.0 if exec_dim and exec_dim.score == 1.0 else 0.7)
        
        return sum(factors) / len(factors)
    
    def _generate_feedback(self, result: EnhancedEvaluationResult) -> str:
        """生成改进反馈"""
        feedback_parts = []
        
        # 收集所有问题
        all_issues = []
        all_suggestions = []
        
        for dim in result.dimensions.values():
            all_issues.extend(dim.issues)
            all_suggestions.extend(dim.suggestions)
        
        # 按重要性排序
        if not result.execution_result or not result.execution_result.success:
            feedback_parts.append("CRITICAL: Code execution failed. Please fix errors first.")
        
        if all_issues:
            feedback_parts.append(f"Issues found ({len(all_issues)}):")
            for i, issue in enumerate(all_issues[:5], 1):  # 最多5个问题
                feedback_parts.append(f"  {i}. {issue}")
        
        if all_suggestions:
            feedback_parts.append("\nSuggestions:")
            for i, sug in enumerate(all_suggestions[:3], 1):
                feedback_parts.append(f"  {i}. {sug}")
        
        if result.improvement_potential > 0.3:
            feedback_parts.append(f"\nImprovement potential: {result.improvement_potential:.0%}")
        
        return "\n".join(feedback_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取评估统计"""
        if not self.evaluation_history:
            return {}
        
        scores = [h["score"] for h in self.evaluation_history]
        passes = sum(1 for h in self.evaluation_history if h["pass"])
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "average_score": sum(scores) / len(scores),
            "pass_rate": passes / len(self.evaluation_history),
            "min_score": min(scores),
            "max_score": max(scores)
        }


# 便捷函数
def evaluate_with_enhanced(code: str, 
                          query: str, 
                          llm_provider: str = "deepseek") -> Dict[str, Any]:
    """
    使用增强评估器快速评估
    """
    from agents.base import AgentState
    
    agent = EnhancedEvaluatorAgent(llm_provider=llm_provider)
    state = AgentState(user_query=query, generated_code=code)
    
    result_state = agent.process(state)
    
    eval_result = result_state.execution_result or {}
    
    return {
        "score": eval_result.get("quality_score", 0),
        "passed": eval_result.get("evaluation_passed", False),
        "details": eval_result.get("enhanced_evaluation", {}),
        "feedback": result_state.visual_feedback.get("feedback", "") if result_state.visual_feedback else ""
    }


if __name__ == "__main__":
    # 测试
    test_code = """
from pyecharts.charts import Line
from pyecharts import options as opts

chart = Line()
chart.add_xaxis(['Jan', 'Feb', 'Mar', 'Apr', 'May'])
chart.add_yaxis('Sales', [120, 200, 150, 80, 170])
chart.set_global_opts(
    title_opts=opts.TitleOpts(title='Monthly Sales Trend'),
    xaxis_opts=opts.AxisOpts(name='Month'),
    yaxis_opts=opts.AxisOpts(name='Sales (k$)')
)
"""
    
    print("="*70)
    print("Enhanced Evaluator Test")
    print("="*70)
    
    result = evaluate_with_enhanced(test_code, "Show monthly sales trend")
    
    print("\nEvaluation Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
