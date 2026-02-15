"""
Planner Agent: Intent Analysis and Task Decomposition
IEEE VIS 2026 - Core contribution: Design Space formalization
"""

import json
from typing import Dict, Any, List, Optional
from .base import BaseAgent, AgentState


class PlannerAgent(BaseAgent):
    """
    Planner Agent analyzes user queries using formalized design space.
    
    Key Contribution:
    - Formalized Design Space for Low Altitude Economy visualization
    - Intent classification with confidence scoring
    - Multi-chart recommendation with rationale
    """
    
    SYSTEM_PROMPT = """You are the Planner Agent for LAEV (Low Altitude Economy Visualization).
Analyze user queries and output structured JSON.

RULES:
1. Identify the analytical task type
2. Map to appropriate chart types using design space
3. Provide confidence scores
4. Output valid JSON only

Output format:
{
    "intent": {
        "type": "exploration|comparison|trend|distribution|correlation|anomaly",
        "confidence": 0.0-1.0,
        "description": "detailed explanation"
    },
    "data_requirements": {
        "dimensions": [...],
        "time_range": "...",
        "filters": [...]
    },
    "visualization_plan": [
        {
            "chart_type": "...",
            "rationale": "...",
            "confidence": 0.0-1.0,
            "rank": 1
        }
    ]
}"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        super().__init__("Planner", llm_provider)
        self.design_space = self._init_design_space()
    
    def _init_design_space(self) -> Dict[str, Any]:
        """
        Initialize formalized design space for Low Altitude Economy.
        This is a key contribution for VIS paper - systematic design knowledge.
        """
        return {
            "domain": "Low Altitude Economy",
            "data_dimensions": {
                "temporal": {
                    "granularity": ["hour", "day", "week", "month", "quarter", "year"],
                    "patterns": ["trend", "seasonality", "anomaly", "cycle", "peak_hours"]
                },
                "spatial": {
                    "levels": ["point", "district", "city", "region", "corridor", "airspace_zone"],
                    "types": ["origin", "destination", "route", "zone", "vertiport", "airport"]
                },
                "categorical": {
                    "vehicle_type": ["multirotor", "fixed_wing", "helicopter", "evtOL", "hybrid"],
                    "operation_type": ["logistics", "survey", "emergency", "tourism", "agriculture", "inspection"],
                    "entity_type": ["enterprise", "pilot", "operator", "manufacturer", "airport", "vertiport"]
                },
                "numerical": {
                    "scale_metrics": ["flight_hours", "flight_count", "fleet_size", "revenue", "market_share"],
                    "structure_metrics": ["enterprise_count", "pilot_count", "aircraft_count", "route_count"],
                    "efficiency_metrics": ["load_factor", "ontime_rate", "utilization_rate", "energy_efficiency"],
                    "innovation_metrics": ["patent_count", "rd_investment", "technology_readiness", "integration_score"]
                }
            },
            "task_types": {
                "exploration": {
                    "description": "Understanding data patterns",
                    "charts": ["dashboard", "treemap", "heatmap"]
                },
                "comparison": {
                    "description": "Comparing entities or time periods",
                    "charts": ["bar", "radar", "grouped_bar", "pareto"]
                },
                "trend_analysis": {
                    "description": "Analyzing temporal changes",
                    "charts": ["line", "area", "polar_clock", "calendar"]
                },
                "distribution": {
                    "description": "Understanding value distributions",
                    "charts": ["histogram", "boxplot", "pie", "funnel"]
                },
                "correlation": {
                    "description": "Finding relationships",
                    "charts": ["scatter", "bubble", "chord", "network"]
                },
                "anomaly_detection": {
                    "description": "Identifying unusual patterns",
                    "charts": ["control_chart", "gauge", "highlight_table"]
                }
            },
            "chart_mappings": {
                "line": {"tasks": ["trend_analysis"], "data": ["temporal", "numerical"], "max_dims": 3},
                "area": {"tasks": ["trend_analysis", "exploration"], "data": ["temporal", "numerical"], "max_dims": 3},
                "bar": {"tasks": ["comparison", "distribution"], "data": ["categorical", "numerical"], "max_dims": 2},
                "polar_clock": {"tasks": ["trend_analysis"], "data": ["temporal", "numerical"], "max_dims": 2},
                "choropleth": {"tasks": ["exploration", "comparison"], "data": ["spatial", "numerical"], "max_dims": 2},
                "radar": {"tasks": ["comparison", "exploration"], "data": ["categorical", "numerical"], "max_dims": 6},
                "network": {"tasks": ["correlation", "exploration"], "data": ["spatial", "categorical"], "max_dims": 4},
                "control_chart": {"tasks": ["anomaly_detection"], "data": ["temporal", "numerical"], "max_dims": 2}
            }
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """Analyze query and create visualization plan"""
        from llm_client import LLMClient
        
        llm = LLMClient(provider=self.llm_provider)
        
        prompt = self._build_prompt(state.user_query)
        
        try:
            response = llm.generate(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.2
            )
            
            intent = json.loads(response)
            state.intent = intent
            
            self.log_action("Intent Analysis", {
                "type": intent["intent"]["type"],
                "confidence": intent["intent"]["confidence"],
                "top_chart": intent["visualization_plan"][0]["chart_type"] if intent["visualization_plan"] else "unknown"
            })
            
        except Exception as e:
            # Fallback for robustness
            state.intent = self._fallback_analysis(state.user_query)
            self.log_action("Intent Analysis (Fallback)", {"error": str(e)})
        
        return state
    
    def _build_prompt(self, query: str) -> str:
        """Build prompt with design space context"""
        return f"""User Query: {query}

Design Space Context:
{json.dumps(self.design_space, ensure_ascii=False, indent=2)[:2000]}

Analyze the query considering the design space and provide your structured response."""
    
    def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Rule-based fallback when LLM fails"""
        query_lower = query.lower()
        
        # Simple keyword matching
        if any(w in query_lower for w in ["趋势", "trend", "增长", "growth", "变化", "change"]):
            task_type = "trend_analysis"
            charts = [{"chart_type": "line", "rationale": "Trend analysis", "confidence": 0.8, "rank": 1}]
        elif any(w in query_lower for w in ["比较", "compare", "对比", "排名", "rank"]):
            task_type = "comparison"
            charts = [{"chart_type": "bar", "rationale": "Comparison", "confidence": 0.8, "rank": 1}]
        elif any(w in query_lower for w in ["分布", "distribution", "占比", "proportion"]):
            task_type = "distribution"
            charts = [{"chart_type": "pie", "rationale": "Distribution", "confidence": 0.7, "rank": 1}]
        else:
            task_type = "exploration"
            charts = [{"chart_type": "dashboard", "rationale": "General exploration", "confidence": 0.6, "rank": 1}]
        
        return {
            "intent": {"type": task_type, "confidence": 0.6, "description": f"Fallback analysis for: {query}"},
            "visualization_plan": charts
        }
    
    def get_recommended_chart(self, state: AgentState) -> Optional[str]:
        """Get top chart recommendation"""
        if state.intent and "visualization_plan" in state.intent:
            plans = state.intent["visualization_plan"]
            if plans:
                top = min(plans, key=lambda x: x.get("rank", 99))
                return top.get("chart_type")
        return None
