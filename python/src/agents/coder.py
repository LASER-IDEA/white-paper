"""
Coder Agent: Code Generation with Multi-Strategy Support
IEEE VIS 2026 - Enhanced with multiple generation strategies
"""

import json
import re
from typing import Dict, Any, List, Optional
from .base import BaseAgent, AgentState


class CoderAgent(BaseAgent):
    """
    Coder Agent generates visualization code with:
    - Multiple generation strategies (conservative, creative, domain-specific)
    - Error recovery and retry
    - Style consistency enforcement
    """
    
    # Enhanced system prompt with design patterns
    SYSTEM_PROMPT_TEMPLATE = """You are the Coder Agent for LAEV visualization system.
Generate executable Python code using PyECharts.

CRITICAL RULES:
1. Use ONLY these imports: from pyecharts import options as opts, from pyecharts.charts import Line, Bar, Pie, Scatter
2. DO NOT use try-except blocks
3. DO NOT use return statement - create a 'chart' variable instead
4. Return ONLY the code, no explanations
5. Ensure the code is syntactically valid Python
6. The last line should assign the chart object to a variable named 'chart'

EXAMPLE CODE FORMAT:
```python
from pyecharts import options as opts
from pyecharts.charts import Line

chart = Line()
chart.add_xaxis(['A', 'B', 'C'])
chart.add_yaxis("Values", [1, 2, 3])
chart.set_global_opts(title_opts=opts.TitleOpts(title="My Chart"))
```

COLOR_SCHEME = ['#002FA7', '#f59e0b', '#ea580c', '#dc2626', '#b91c1c']

Available chart types and their usage:
- Line/Area: trends over time
- Bar: comparisons
- Pie: proportions  
- Scatter: correlations
- Radar: multi-dimensional comparison
- Map: spatial distribution
- Heatmap: matrix data
- Gauge: single metric display
- Calendar: temporal patterns
- Polar: cyclical data

Generate code that:
1. Creates the chart object
2. Adds data (use realistic mock data if needed)
3. Configures styling consistently
4. Returns the chart object
"""
    
    # Domain-specific chart templates for Low Altitude Economy
    CHART_TEMPLATES = {
        "polar_clock": '''
from pyecharts.charts import Polar
from pyecharts import options as opts
import datetime

hours = list(range(24))
values = [10, 8, 5, 3, 2, 4, 8, 15, 25, 35, 45, 50, 
          48, 45, 40, 35, 38, 45, 55, 50, 40, 30, 20, 15]

chart = Polar(init_opts=opts.InitOpts(theme="light", width="800px", height="600px"))
chart.add_schema(
    angleaxis_opts=opts.AngleAxisOpts(
        data=hours,
        type_="category",
        start_angle=90,
        axislabel_opts=opts.LabelOpts(formatter="{value}h")
    ),
    radiusaxis_opts=opts.RadiusAxisOpts(min_=0),
    polar={"center": ["50%", "50%"]}
)
chart.add(
    "Flight Activity",
    [[i, v] for i, v in enumerate(values)],
    type_="bar",
    coordinate_system="polar",
    itemstyle_opts=opts.ItemStyleOpts(color="#002FA7")
)
chart.set_global_opts(
    title_opts=opts.TitleOpts(title="{title}"),
    legend_opts=opts.LegendOpts(is_show=True)
)
''',
        "control_chart": '''
from pyecharts.charts import Line, Gauge
from pyecharts import options as opts
import datetime

dates = [(datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).strftime("%Y-%m-%d") 
         for i in range(30)]
values = [85 + (i % 10 - 5) for i in range(30)]
ucl = [92] * 30
lcl = [78] * 30

chart = Line(init_opts=opts.InitOpts(theme="light", width="900px", height="400px"))
chart.add_xaxis(dates)
chart.add_yaxis("TQI", values, is_smooth=True, 
                itemstyle_opts=opts.ItemStyleOpts(color="#002FA7"))
chart.add_yaxis("UCL", ucl, is_smooth=True, 
                linestyle_opts=opts.LineStyleOpts(color="#ea580c", type_="dashed"))
chart.add_yaxis("LCL", lcl, is_smooth=True, 
                linestyle_opts=opts.LineStyleOpts(color="#ea580c", type_="dashed"))
chart.set_global_opts(
    title_opts=opts.TitleOpts(title="{title}"),
    yaxis_opts=opts.AxisOpts(min_=70, max_=100),
    tooltip_opts=opts.TooltipOpts(trigger="axis")
)
''',
        "radar": '''
from pyecharts.charts import Radar
from pyecharts import options as opts

dimensions = ["Scale", "Structure", "Space", "Efficiency", "Innovation"]
values = [[75, 80, 70, 85, 65]]

chart = Radar(init_opts=opts.InitOpts(theme="light", width="700px", height="600px"))
chart.add_schema(
    schema=[opts.RadarIndicatorItem(name=d, max_=100) for d in dimensions],
    shape="polygon"
)
chart.add("Development Index", values, 
          areastyle_opts=opts.AreaStyleOpts(opacity=0.3, color="#002FA7"),
          linestyle_opts=opts.LineStyleOpts(color="#002FA7"))
chart.set_global_opts(title_opts=opts.TitleOpts(title="{title}"))
'''
    }
    
    def __init__(self, llm_provider: str = "deepseek", strategy: str = "adaptive"):
        super().__init__("Coder", llm_provider)
        self.strategy = strategy  # "conservative", "creative", "domain_specific"
        self.colors = ["#002FA7", "#f59e0b", "#ea580c", "#dc2626", "#b91c1c"]
    
    def execute(self, state: AgentState) -> AgentState:
        """Generate code based on intent and context"""
        chart_type = self._determine_chart_type(state)
        
        # Try different strategies in order of reliability
        code = None
        errors = []
        
        strategies = self._get_strategy_order()
        
        for strategy in strategies:
            try:
                if strategy == "template":
                    code = self._template_generation(state, chart_type)
                elif strategy == "llm_with_context":
                    code = self._llm_generation(state, chart_type, with_context=True)
                else:  # fallback
                    code = self._llm_generation(state, chart_type, with_context=False)
                
                # Validate generated code
                if self._validate_code(code):
                    break
                else:
                    errors.append(f"{strategy}: validation failed")
                    code = None
                    
            except Exception as e:
                errors.append(f"{strategy}: {str(e)}")
                code = None
        
        if code:
            state.generated_code = code
            self.log_action("Code Generation", {
                "chart_type": chart_type,
                "strategy": strategy,
                "code_length": len(code)
            })
        else:
            state.generated_code = self._fallback_code(chart_type)
            self.log_action("Code Generation Failed", {"errors": errors})
        
        return state
    
    def _get_strategy_order(self) -> List[str]:
        """Determine generation strategy order"""
        if self.strategy == "conservative":
            return ["template", "llm_with_context", "llm_basic"]
        elif self.strategy == "creative":
            return ["llm_with_context", "template", "llm_basic"]
        else:  # adaptive
            return ["template", "llm_with_context", "llm_basic"]
    
    def _determine_chart_type(self, state: AgentState) -> str:
        """Determine chart type from intent or use default"""
        if state.intent and "visualization_plan" in state.intent:
            plans = state.intent["visualization_plan"]
            if plans:
                return plans[0].get("chart_type", "line")
        return "line"
    
    def _template_generation(self, state: AgentState, chart_type: str) -> Optional[str]:
        """Generate code using predefined templates"""
        template = self.CHART_TEMPLATES.get(chart_type)
        if template:
            # Extract title from query
            title = state.user_query[:30] + "..."
            return template.format(title=title)
        return None
    
    def _llm_generation(self, state: AgentState, chart_type: str, with_context: bool) -> str:
        """Generate code using LLM"""
        from llm_client import LLMClient
        
        llm = LLMClient(provider=self.llm_provider)
        
        # System prompt now has hardcoded colors, no format needed
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE
        
        prompt = self._build_generation_prompt(state, chart_type, with_context)
        
        response = llm.generate(
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.3 if self.strategy == "conservative" else 0.5
        )
        
        # Extract code from response
        code = self._extract_code(response)
        return code
    
    def _build_generation_prompt(self, state: AgentState, chart_type: str, with_context: bool) -> str:
        """Build prompt for code generation"""
        prompt_parts = [
            f"Generate Python code for a {chart_type} chart.",
            f"User query: {state.user_query}",
            f"Chart type: {chart_type}"
        ]
        
        if with_context and state.retrieved_context:
            context_str = json.dumps(state.retrieved_context, ensure_ascii=False, indent=2)
            prompt_parts.append(f"\nDomain context:\n{context_str}")
        
        if state.intent:
            intent_str = json.dumps(state.intent, ensure_ascii=False)[:500]
            prompt_parts.append(f"\nIntent analysis:\n{intent_str}")
        
        prompt_parts.append("\nGenerate the complete Python code:")
        
        return "\n".join(prompt_parts)
    
    def _extract_code(self, response: str) -> str:
        """Extract code from LLM response"""
        # Try to extract code block
        code_pattern = r"```python\n(.*?)\n```"
        matches = re.findall(code_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # Try without language specifier
        code_pattern = r"```\n(.*?)\n```"
        matches = re.findall(code_pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # Assume entire response is code
        return response.strip()
    
    def _validate_code(self, code: str) -> bool:
        """Basic code validation"""
        if not code or len(code) < 50:
            return False
        
        # Check for required imports
        required_imports = ["pyecharts"]
        for imp in required_imports:
            if imp not in code:
                return False
        
        # Check for dangerous patterns
        dangerous = ["import os", "import sys", "__import__", "eval(", "exec(", "open(", "file("]
        for pattern in dangerous:
            if pattern in code:
                return False
        
        return True
    
    def _fallback_code(self, chart_type: str) -> str:
        """Minimal fallback code"""
        return f'''
from pyecharts.charts import Line
from pyecharts import options as opts

chart = Line()
chart.add_xaxis(["A", "B", "C"])
chart.add_yaxis("Value", [1, 2, 3])
chart.set_global_opts(title_opts=opts.TitleOpts(title="Fallback Chart"))
'''
