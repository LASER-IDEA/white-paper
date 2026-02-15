"""
Visual Quality Evaluator for Charts
Uses code analysis + LLM-based assessment for visualization quality
"""

import json
import re
from typing import Dict, Any, List, Tuple
from .base import BaseAgent, AgentState


class VisualEvaluator:
    """
    Evaluates visual quality of generated charts using:
    1. Code-based heuristics (fast)
    2. LLM-based assessment (more accurate)
    """
    
    # Chart type appropriateness rules
    CHART_RULES = {
        "line": {
            "good_for": ["trend", "time", "temporal", "change", "over time"],
            "requires": ["add_xaxis", "add_yaxis"],
            "optional": ["is_smooth", "markarea_opts"]
        },
        "bar": {
            "good_for": ["compare", "ranking", "category", "distribution"],
            "requires": ["add_xaxis", "add_yaxis"],
            "optional": ["bar_width", "category_gap"]
        },
        "pie": {
            "good_for": ["proportion", "percentage", "share", "distribution"],
            "requires": ["add"],
            "optional": ["radius", "center", "rosetype"]
        },
        "scatter": {
            "good_for": ["correlation", "relationship", "compare", "distribution"],
            "requires": ["add_xaxis", "add_yaxis"],
            "optional": ["symbol_size", "itemstyle_opts"]
        },
        "radar": {
            "good_for": ["multidimensional", "compare", "profile", "score"],
            "requires": ["add_schema", "add"],
            "optional": ["areastyle_opts"]
        },
        "heatmap": {
            "good_for": ["matrix", "correlation", "density", "pattern"],
            "requires": ["add_xaxis", "add_yaxis", "add"],
            "optional": ["visualmap_opts"]
        }
    }
    
    def __init__(self, llm_provider: str = "deepseek", use_llm: bool = True):
        self.llm_provider = llm_provider
        self.use_llm = use_llm
    
    def evaluate(self, code: str, query: str, html_content: str = None) -> Dict[str, Any]:
        """
        Evaluate visual quality
        
        Returns:
            {
                "overall_score": float (0-1),
                "readability": float (0-1),
                "aesthetics": float (0-1),
                "data_encoding": float (0-1),
                "appropriateness": float (0-1),
                "suggestions": [str],
                "issues": [str]
            }
        """
        # Step 1: Code-based analysis (fast)
        code_analysis = self._analyze_code_quality(code, query)
        
        # Step 2: LLM-based assessment (if enabled)
        if self.use_llm:
            try:
                llm_assessment = self._llm_assess(code, query)
                # Combine scores (weighted average)
                combined = self._combine_scores(code_analysis, llm_assessment)
                return combined
            except Exception as e:
                # Fall back to code analysis
                print(f"LLM assessment failed: {e}, using code analysis")
                return code_analysis
        
        return code_analysis
    
    def _analyze_code_quality(self, code: str, query: str) -> Dict[str, Any]:
        """Analyze code for visualization quality"""
        scores = {
            "readability": 0.5,
            "aesthetics": 0.5,
            "data_encoding": 0.5,
            "appropriateness": 0.5
        }
        issues = []
        suggestions = []
        
        # 1. Check for basic structure
        has_title = "TitleOpts" in code
        has_xaxis = "add_xaxis" in code
        has_yaxis = "add_yaxis" in code or "Pie" in code  # Pie doesn't need yaxis
        has_data = "add_yaxis" in code or "add" in code
        
        if not has_title:
            issues.append("Missing chart title")
            suggestions.append("Add a descriptive title using TitleOpts")
        else:
            scores["readability"] += 0.15
        
        if not (has_xaxis and has_yaxis):
            issues.append("Missing axis configuration")
        else:
            scores["data_encoding"] += 0.2
        
        if not has_data:
            issues.append("No data added to chart")
        else:
            scores["data_encoding"] += 0.2
        
        # 2. Check chart type appropriateness
        detected_chart = self._detect_chart_type(code)
        query_lower = query.lower()
        
        if detected_chart:
            rules = self.CHART_RULES.get(detected_chart, {})
            good_for = rules.get("good_for", [])
            
            # Check if query keywords match chart strengths
            matches = sum(1 for keyword in good_for if keyword in query_lower)
            if matches > 0:
                scores["appropriateness"] = 0.7 + min(0.3, matches * 0.1)
            else:
                scores["appropriateness"] = 0.5
                suggestions.append(f"Consider if {detected_chart} is the best chart type for this query")
        
        # 3. Check aesthetic elements
        has_colors = "color" in code.lower() or "itemstyle" in code.lower()
        has_tooltips = "TooltipOpts" in code or "tooltip" in code.lower()
        has_legend = "LegendOpts" in code or "legend" in code.lower()
        
        if has_colors:
            scores["aesthetics"] += 0.15
        if has_tooltips:
            scores["aesthetics"] += 0.1
            scores["readability"] += 0.1
        if has_legend:
            scores["readability"] += 0.1
        
        # 4. Check for advanced features
        has_animation = "animation" in code.lower()
        has_responsive = "width" in code or "height" in code
        
        if has_animation:
            scores["aesthetics"] += 0.05
        
        # Cap scores at 1.0
        for key in scores:
            scores[key] = min(1.0, max(0.0, scores[key]))
        
        # Calculate overall score
        overall = sum(scores.values()) / len(scores)
        
        return {
            "overall_score": round(overall, 2),
            "readability": round(scores["readability"], 2),
            "aesthetics": round(scores["aesthetics"], 2),
            "data_encoding": round(scores["data_encoding"], 2),
            "appropriateness": round(scores["appropriateness"], 2),
            "detected_chart_type": detected_chart,
            "suggestions": suggestions if suggestions else ["Chart looks good!"],
            "issues": issues if issues else []
        }
    
    def _detect_chart_type(self, code: str) -> str:
        """Detect chart type from code"""
        chart_patterns = [
            (r"Scatter\s*\(", "scatter"),
            (r"Line\s*\(", "line"),
            (r"Bar\s*\(", "bar"),
            (r"Pie\s*\(", "pie"),
            (r"Radar\s*\(", "radar"),
            (r"HeatMap\s*\(", "heatmap"),
            (r"Map\s*\(", "map"),
            (r"Gauge\s*\(", "gauge"),
            (r"Funnel\s*\(", "funnel"),
            (r"Polar\s*\(", "polar"),
            (r"TreeMap\s*\(", "treemap"),
        ]
        
        for pattern, chart_type in chart_patterns:
            if re.search(pattern, code):
                return chart_type
        
        return None
    
    def _llm_assess(self, code: str, query: str) -> Dict[str, Any]:
        """Use LLM to assess visualization quality"""
        from llm_client import LLMClient
        
        llm = LLMClient(provider=self.llm_provider)
        
        system_prompt = """You are a data visualization expert.
Evaluate the quality of a PyECharts visualization based on its code and the user's query.

Scoring criteria (0-1 scale):
- readability: Can users easily read and understand the chart?
- aesthetics: Is the chart visually appealing and professional?
- data_encoding: Are data relationships clearly encoded?
- appropriateness: Is this the right chart type for the query?

Output JSON format:
{
    "readability": 0.0-1.0,
    "aesthetics": 0.0-1.0,
    "data_encoding": 0.0-1.0,
    "appropriateness": 0.0-1.0,
    "suggestions": ["specific improvement 1", "specific improvement 2"],
    "issues": ["issue 1", "issue 2"]
}

Be critical but fair. Scores should reflect actual quality."""

        user_prompt = f"""User Query: {query}

Generated Code:
```python
{code[:2000]}
```

Evaluate this visualization."""

        response = llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        # Parse JSON
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
        
        assessment = json.loads(json_str)
        
        # Calculate overall score
        scores = [
            assessment.get("readability", 0.5),
            assessment.get("aesthetics", 0.5),
            assessment.get("data_encoding", 0.5),
            assessment.get("appropriateness", 0.5)
        ]
        assessment["overall_score"] = round(sum(scores) / len(scores), 2)
        
        return assessment
    
    def _combine_scores(self, code_analysis: Dict, llm_assessment: Dict) -> Dict[str, Any]:
        """Combine code-based and LLM-based scores"""
        # Weight: 60% code analysis, 40% LLM (code is more reliable for basic checks)
        weights = {"code": 0.6, "llm": 0.4}
        
        combined = {}
        for metric in ["readability", "aesthetics", "data_encoding", "appropriateness"]:
            code_score = code_analysis.get(metric, 0.5)
            llm_score = llm_assessment.get(metric, 0.5)
            combined[metric] = round(
                weights["code"] * code_score + weights["llm"] * llm_score, 
                2
            )
        
        # Overall score
        combined["overall_score"] = round(sum(combined.values()) / len(combined), 2)
        
        # Combine suggestions (prioritize LLM suggestions)
        suggestions = llm_assessment.get("suggestions", [])
        if not suggestions or suggestions == ["Chart looks good!"]:
            suggestions = code_analysis.get("suggestions", [])
        combined["suggestions"] = suggestions[:3]  # Limit to 3
        
        # Combine issues
        issues = llm_assessment.get("issues", [])
        if not issues:
            issues = code_analysis.get("issues", [])
        combined["issues"] = issues[:3]
        
        combined["detected_chart_type"] = code_analysis.get("detected_chart_type")
        
        return combined


# Integration function for EvaluatorAgent
def evaluate_visual_quality(code: str, query: str, use_llm: bool = True) -> Dict[str, Any]:
    """
    Convenience function to evaluate visualization quality
    
    Args:
        code: Generated chart code
        query: Original user query
        use_llm: Whether to use LLM-based assessment (slower but more accurate)
    
    Returns:
        Quality assessment dictionary
    """
    evaluator = VisualEvaluator(use_llm=use_llm)
    return evaluator.evaluate(code, query)


if __name__ == "__main__":
    # Test
    test_code = """
from pyecharts.charts import Line
from pyecharts import options as opts

chart = Line()
chart.add_xaxis(['Jan', 'Feb', 'Mar'])
chart.add_yaxis('Sales', [100, 200, 150])
chart.set_global_opts(title_opts=opts.TitleOpts(title='Monthly Sales'))
"""
    
    evaluator = VisualEvaluator(use_llm=False)
    result = evaluator.evaluate(test_code, "Show sales trend")
    
    print("Visual Quality Assessment:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
