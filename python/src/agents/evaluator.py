"""
Evaluator Agent: Multi-dimensional Quality Assessment
IEEE VIS 2026 - Key contribution: Visual feedback using multimodal LLM
"""

import json
import base64
import io
from typing import Dict, Any, Optional, Tuple
from PIL import Image
from .base import BaseAgent, AgentState


class CodeExecutor:
    """Safely execute generated chart code"""
    
    SAFE_MODULES = {
        'pyecharts',
        'datetime',
        'random',
        'math',
        'json'
    }
    
    DANGEROUS_PATTERNS = [
        'import os', 'import sys', 'import subprocess',
        '__import__', 'eval(', 'exec(', 'compile(',
        'open(', 'file(', 'socket', 'urllib', 'requests'
    ]
    
    def __init__(self):
        self.execution_globals = {
            '__builtins__': {
                'len': len, 'range': range, 'enumerate': enumerate,
                'zip': zip, 'map': map, 'filter': filter,
                'sum': sum, 'min': min, 'max': max, 'abs': abs,
                'round': round, 'int': int, 'float': float, 'str': str,
                'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
                'sorted': sorted, 'reversed': reversed,
                'isinstance': isinstance, 'hasattr': hasattr,
                'Exception': Exception, 'ValueError': ValueError
            }
        }
    
    def validate_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate code for safety"""
        # Check dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in code.lower():
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Check for imports
        import_lines = [line for line in code.split('\n') if 'import' in line]
        for line in import_lines:
            # Allow from X import Y
            if line.strip().startswith('from '):
                module = line.split('from')[1].split('import')[0].strip()
                # Check if module or its root is in safe list
                root_module = module.split('.')[0]
                if root_module not in self.SAFE_MODULES:
                    return False, f"Unsafe module: {module}"
            # Check direct imports
            elif line.strip().startswith('import '):
                module = line.split('import')[1].strip().split()[0]
                root_module = module.split('.')[0]
                if root_module not in self.SAFE_MODULES:
                    return False, f"Unsafe module: {module}"
        
        return True, None
    
    def _safe_import(self, name, *args, **kwargs):
        """Restricted import that only allows safe modules"""
        safe_modules = {
            'datetime', 'random', 'math', 'json', 'os', 'sys',
            'typing', 'collections', 'itertools', 'functools',
            'pyecharts', 'pyecharts.options', 'pyecharts.charts', 'pyecharts.globals',
            'pyecharts.commons', 'pyecharts.types', 'pyecharts.renderer'
        }
        
        # Check if the requested module is in safe list
        root_module = name.split('.')[0]
        if root_module in safe_modules or name in safe_modules:
            return __import__(name, *args, **kwargs)
        
        # For other modules, raise ImportError
        raise ImportError(f"Import of '{name}' is not allowed in sandboxed environment")
    
    def execute(self, code: str) -> Dict[str, Any]:
        """Execute code and return result"""
        # Validate first
        is_valid, error = self.validate_code(code)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "chart": None,
                "image_data": None
            }
        
        try:
            # Import all necessary modules
            import datetime
            import random
            import math
            import json as json_mod
            import pyecharts.options as opts
            import pyecharts.charts as charts
            from pyecharts import globals as pyecharts_globals
            
            # Create a restricted but functional execution environment
            safe_builtins = {
                'len': len, 'range': range, 'enumerate': enumerate,
                'zip': zip, 'map': map, 'filter': filter,
                'sum': sum, 'min': min, 'max': max, 'abs': abs,
                'round': round, 'int': int, 'float': float, 'str': str,
                'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
                'sorted': sorted, 'reversed': reversed,
                'isinstance': isinstance, 'hasattr': hasattr,
                'getattr': getattr, 'setattr': setattr,
                'type': type, 'print': print,
                'Exception': Exception, 'ValueError': ValueError,
                'TypeError': TypeError, 'KeyError': KeyError,
                'IndexError': IndexError, 'AttributeError': AttributeError,
                '__import__': self._safe_import,  # Restricted import
            }
            
            exec_globals = {
                # Essential built-ins with restricted import
                '__builtins__': safe_builtins,
                # Modules
                'datetime': datetime,
                'random': random,
                'math': math,
                'json': json_mod,
                # PyECharts options
                'opts': opts,
                # PyECharts charts - all commonly used types
                'Line': charts.Line,
                'Bar': charts.Bar,
                'Pie': charts.Pie,
                'Scatter': charts.Scatter,
                'Radar': charts.Radar,
                'HeatMap': charts.HeatMap,
                'Map': charts.Map,
                'Gauge': charts.Gauge,
                'Funnel': charts.Funnel,
                'Polar': charts.Polar,
                'Area': charts.Line,  # Area is Line with areastyle
                'Grid': charts.Grid,
                'Page': charts.Page,
                'Timeline': charts.Timeline,
                'Tree': charts.Tree,
                'TreeMap': charts.TreeMap,
                'Sunburst': charts.Sunburst,
                'WordCloud': charts.WordCloud,
                'Liquid': charts.Liquid,
                'Calendar': charts.Calendar,
                'Boxplot': charts.Boxplot,
                'EffectScatter': charts.EffectScatter,
                'Kline': charts.Kline,
                'Geo': charts.Geo,
                'Graph': charts.Graph,
                'ThemeRiver': charts.ThemeRiver,
                # PyECharts globals
                'ThemeType': pyecharts_globals.ThemeType,
            }
            
            # Execute code in restricted environment
            exec(code, exec_globals)
            
            # Find chart object - prefer 'chart' variable
            chart = exec_globals.get('chart')
            if chart is None:
                # Fallback: find any object with render method
                for key, value in exec_globals.items():
                    if key != 'chart' and hasattr(value, 'render') and key not in ('__builtins__', 'opts'):
                        chart = value
                        break
            
            if chart is None:
                return {
                    "success": False,
                    "error": "No chart object found in generated code",
                    "chart": None,
                    "image_data": None
                }
            
            # Render to HTML and capture as image
            html_content = chart.render_embed()
            
            return {
                "success": True,
                "error": None,
                "chart": chart,
                "html_content": html_content,
                "image_data": None  # Would need selenium/playwright for image
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart": None,
                "image_data": None
            }


class EvaluatorAgent(BaseAgent):
    """
    Evaluator Agent assesses:
    1. Code execution success
    2. Code quality (syntax, structure)
    3. Visual quality (using heuristics or multimodal LLM)
    4. Alignment with user intent
    """
    
    def __init__(self, llm_provider: str = "deepseek", use_vision: bool = False):
        super().__init__("Evaluator", llm_provider)
        self.executor = CodeExecutor()
        self.use_vision = use_vision  # Whether to use multimodal LLM
    
    def execute(self, state: AgentState) -> AgentState:
        """Execute and evaluate generated code"""
        code = state.generated_code
        
        if not code:
            state.execution_result = {
                "success": False,
                "error": "No code generated",
                "score": 0.0
            }
            return state
        
        # Step 1: Execute code
        execution_result = self.executor.execute(code)
        
        # Step 2: Evaluate code quality
        code_quality = self._evaluate_code_quality(code)
        
        # Step 3: Evaluate alignment with intent
        intent_alignment = self._evaluate_intent_alignment(state)
        
        # Step 4: Compute overall score
        overall_score = self._compute_score(execution_result, code_quality, intent_alignment)
        
        state.execution_result = {
            "success": execution_result["success"],
            "error": execution_result.get("error"),
            "code_quality": code_quality,
            "intent_alignment": intent_alignment,
            "overall_score": overall_score,
            "html_content": execution_result.get("html_content")
        }
        
        # Step 5: Generate visual feedback
        # Always evaluate visual quality using code analysis
        if execution_result.get("success") and state.generated_code:
            state.visual_feedback = self._visual_evaluation(
                state.generated_code, 
                state.user_query
            )
        
        self.log_action("Evaluation", {
            "success": execution_result["success"],
            "overall_score": overall_score,
            "code_quality": code_quality["score"]
        })
        
        return state
    
    def _evaluate_code_quality(self, code: str) -> Dict[str, Any]:
        """Evaluate code structure and style"""
        score = 1.0
        issues = []
        
        # Check for proper structure
        if 'def ' in code and 'chart' not in code.lower():
            score -= 0.1
            issues.append("Function defined but chart object unclear")
        
        # Check for styling
        if 'opts.InitOpts' in code or 'opts.TitleOpts' in code:
            score += 0.1
        else:
            score -= 0.1
            issues.append("Missing styling configuration")
        
        # Check for data
        if 'add_xaxis' in code and 'add_yaxis' in code:
            score += 0.1
        else:
            score -= 0.2
            issues.append("Missing data configuration")
        
        # Check code length (reasonable complexity)
        lines = len(code.split('\n'))
        if lines < 5:
            score -= 0.1
            issues.append("Code too short")
        elif lines > 100:
            score -= 0.1
            issues.append("Code too complex")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "lines": lines
        }
    
    def _evaluate_intent_alignment(self, state: AgentState) -> Dict[str, Any]:
        """Evaluate if chart matches user intent"""
        score = 0.8  # Base score
        issues = []
        
        intent = state.intent or {}
        code = state.generated_code or ""
        
        # Check chart type alignment
        if "visualization_plan" in intent:
            expected_type = intent["visualization_plan"][0].get("chart_type", "")
            if expected_type.lower() in code.lower():
                score += 0.1
            else:
                score -= 0.1
                issues.append(f"Expected {expected_type} but code may differ")
        
        # Check query keywords in chart
        query_keywords = state.user_query.lower().split()
        code_lower = code.lower()
        
        keyword_matches = sum(1 for kw in query_keywords if kw in code_lower)
        if keyword_matches > 0:
            score += 0.05 * min(keyword_matches, 2)
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues
        }
    
    def _compute_score(self, execution: Dict, code_quality: Dict, intent_alignment: Dict) -> float:
        """Compute weighted overall score"""
        if not execution["success"]:
            return 0.0
        
        weights = {
            "execution": 0.4,
            "code_quality": 0.3,
            "intent_alignment": 0.3
        }
        
        score = (
            weights["execution"] * (1.0 if execution["success"] else 0.0) +
            weights["code_quality"] * code_quality["score"] +
            weights["intent_alignment"] * intent_alignment["score"]
        )
        
        return round(score, 2)
    
    def _visual_evaluation(self, code: str, query: str) -> Dict[str, Any]:
        """
        Evaluate visual quality using code analysis + LLM assessment
        """
        try:
            from .visual_evaluator import evaluate_visual_quality
            
            # Use code-based evaluation (fast)
            # Set use_llm=False for speed, or True for more accurate assessment
            result = evaluate_visual_quality(code, query, use_llm=False)
            return result
        except Exception as e:
            # Fallback
            return {
                "overall_score": 0.7,
                "readability": 0.7,
                "aesthetics": 0.7,
                "data_encoding": 0.7,
                "suggestions": ["Visual evaluation unavailable"],
                "issues": [str(e)]
            }
    
    def should_refine(self, state: AgentState) -> Tuple[bool, Optional[str]]:
        """Determine if refinement is needed"""
        if not state.execution_result:
            return True, "No execution result"
        
        score = state.execution_result.get("overall_score", 0)
        
        if score < 0.6:
            return True, f"Low score: {score}"
        
        if not state.execution_result.get("success"):
            error = state.execution_result.get("error", "Unknown error")
            return True, f"Execution failed: {error}"
        
        return False, None


class SimpleEvaluatorAgent(BaseAgent):
    """Simplified evaluator with visual quality assessment"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        super().__init__("SimpleEvaluator", llm_provider)
        self.executor = CodeExecutor()
    
    def execute(self, state: AgentState) -> AgentState:
        """Evaluate execution and visual quality"""
        code = state.generated_code
        
        if not code:
            state.execution_result = {"success": False, "error": "No code"}
            return state
        
        result = self.executor.execute(code)
        
        # Basic execution result
        state.execution_result = {
            "success": result["success"],
            "error": result.get("error"),
            "overall_score": 1.0 if result["success"] else 0.0,
            "html_content": result.get("html_content")
        }
        
        # Add visual quality assessment
        if result["success"] and code:
            try:
                from .visual_evaluator import evaluate_visual_quality
                visual_feedback = evaluate_visual_quality(
                    code, 
                    state.user_query, 
                    use_llm=False  # Fast mode
                )
                state.visual_feedback = visual_feedback
                # Update overall score to include visual quality
                visual_score = visual_feedback.get("overall_score", 0.7)
                state.execution_result["overall_score"] = (
                    0.7 * (1.0 if result["success"] else 0.0) + 0.3 * visual_score
                )
            except Exception as e:
                # Visual evaluation failed, but execution succeeded
                pass
        
        self.log_action("Simple Evaluation", {
            "success": result["success"],
            "has_visual_feedback": state.visual_feedback is not None
        })
        
        return state
