"""
Reflector Agent: Iterative Refinement and Error Recovery
IEEE VIS 2026 - Self-reflection and improvement loop
"""

import json
from typing import Dict, Any, Optional, List
from .base import BaseAgent, AgentState


class ReflectorAgent(BaseAgent):
    """
    Reflector Agent analyzes failures and generates improvement suggestions.
    
    Key Capabilities:
    1. Error classification (syntax, logic, design)
    2. Root cause analysis
    3. Specific fix suggestions for Coder Agent
    4. Learning from previous iterations
    """
    
    SYSTEM_PROMPT = """You are the Reflector Agent for LAEV visualization system.
Analyze code execution failures and provide specific improvement suggestions.

Error Classification:
- SYNTAX: Python syntax errors, import issues
- LOGIC: Chart configuration errors, missing data
- DESIGN: Poor visualization choices, missing labels
- DATA: Wrong data format, insufficient data points

Output JSON format:
{
    "error_classification": "SYNTAX|LOGIC|DESIGN|DATA",
    "root_cause": "Detailed explanation of what went wrong",
    "fix_strategy": "One of: syntax_fix, data_correction, chart_redesign, simplification",
    "specific_suggestions": [
        "Concrete suggestion 1",
        "Concrete suggestion 2"
    ],
    "modified_requirements": {
        "chart_type": "optional alternative chart type",
        "simplification_level": "reduce_complexity|keep_same",
        "additional_constraints": [...]
    }
}"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        super().__init__("Reflector", llm_provider)
        self.error_patterns = self._load_error_patterns()
    
    def _load_error_patterns(self) -> Dict[str, Dict]:
        """Load common error patterns and fixes"""
        return {
            "AttributeError": {
                "classification": "LOGIC",
                "suggestion": "Check chart object method names and initialization"
            },
            "NameError": {
                "classification": "SYNTAX",
                "suggestion": "Ensure all variables are defined before use"
            },
            "ImportError": {
                "classification": "SYNTAX",
                "suggestion": "Verify import statements are correct"
            },
            "TypeError": {
                "classification": "LOGIC",
                "suggestion": "Check data types passed to chart methods"
            },
            "missing_axis": {
                "classification": "LOGIC",
                "suggestion": "Ensure both xaxis and yaxis are configured"
            },
            "empty_chart": {
                "classification": "DATA",
                "suggestion": "Add mock data or handle empty data gracefully"
            }
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """Analyze execution result and prepare for next iteration"""
        
        # Check if we should stop
        if self._should_stop(state):
            self.log_action("Iteration Complete", {"reason": "Success or max iterations"})
            return state
        
        # Analyze failure
        analysis = self._analyze_failure(state)
        
        # Update state with reflection
        state.execution_history.append({
            "iteration": state.iteration_count,
            "analysis": analysis
        })
        
        self.log_action("Reflection", {
            "classification": analysis["error_classification"],
            "fix_strategy": analysis["fix_strategy"]
        })
        
        return state
    
    def _should_stop(self, state: AgentState) -> bool:
        """Determine if iteration should stop"""
        # Max iterations reached
        if state.iteration_count >= state.max_iterations:
            return True
        
        # Success with good score
        if state.execution_result:
            if state.execution_result.get("success"):
                score = state.execution_result.get("overall_score", 0)
                if score >= 0.75:
                    return True
        
        return False
    
    def _analyze_failure(self, state: AgentState) -> Dict[str, Any]:
        """Analyze why execution failed"""
        execution = state.execution_result or {}
        
        if execution.get("success"):
            return {
                "error_classification": "NONE",
                "root_cause": "Execution successful",
                "fix_strategy": "none",
                "specific_suggestions": []
            }
        
        error_msg = execution.get("error", "Unknown error")
        
        # Try pattern matching first
        for pattern, info in self.error_patterns.items():
            if pattern in error_msg:
                return {
                    "error_classification": info["classification"],
                    "root_cause": error_msg,
                    "fix_strategy": "pattern_fix",
                    "specific_suggestions": [info["suggestion"]]
                }
        
        # Use LLM for complex analysis
        return self._llm_analysis(state, error_msg)
    
    def _llm_analysis(self, state: AgentState, error_msg: str) -> Dict[str, Any]:
        """Use LLM for error analysis"""
        from llm_client import LLMClient
        
        try:
            llm = LLMClient(provider=self.llm_provider)
            
            prompt = f"""Analyze this visualization generation failure:

User Query: {state.user_query}
Generated Code:
```python
{state.generated_code}
```

Error Message: {error_msg}

Intent Analysis: {json.dumps(state.intent, ensure_ascii=False) if state.intent else "N/A"}

Provide your analysis."""
            
            response = llm.generate(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.3
            )
            
            # Try to parse JSON
            try:
                return json.loads(response)
            except:
                # Fallback
                return {
                    "error_classification": "UNKNOWN",
                    "root_cause": error_msg,
                    "fix_strategy": "simplification",
                    "specific_suggestions": ["Simplify the chart design", "Use a basic chart type"]
                }
                
        except Exception as e:
            return {
                "error_classification": "UNKNOWN",
                "root_cause": str(e),
                "fix_strategy": "simplification",
                "specific_suggestions": ["Retry with simplified approach"]
            }
    
    def get_improvement_prompt(self, state: AgentState) -> str:
        """Generate prompt for improvement iteration"""
        if not state.execution_history:
            return ""
        
        last_analysis = state.execution_history[-1]["analysis"]
        
        suggestions = last_analysis.get("specific_suggestions", [])
        modified_reqs = last_analysis.get("modified_requirements", {})
        
        prompt_parts = [
            "The previous attempt failed. Please improve based on this feedback:",
            "",
            f"Error Type: {last_analysis.get('error_classification')}",
            f"Root Cause: {last_analysis.get('root_cause')}",
            "",
            "Suggestions:"
        ]
        
        for suggestion in suggestions:
            prompt_parts.append(f"- {suggestion}")
        
        if modified_reqs.get("chart_type"):
            prompt_parts.append(f"\nConsider using: {modified_reqs['chart_type']}")
        
        if modified_reqs.get("simplification_level") == "reduce_complexity":
            prompt_parts.append("\nSimplify the design significantly.")
        
        prompt_parts.append("\nGenerate improved code:")
        
        return "\n".join(prompt_parts)


class SimpleReflectorAgent(BaseAgent):
    """Simplified reflector for initial implementation"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        super().__init__("SimpleReflector", llm_provider)
    
    def execute(self, state: AgentState) -> AgentState:
        """Simple reflection - just increment counter"""
        if state.execution_result and state.execution_result.get("success"):
            self.log_action("Success", {"iteration": state.iteration_count})
        else:
            self.log_action("Needs Retry", {
                "iteration": state.iteration_count,
                "error": state.execution_result.get("error", "Unknown") if state.execution_result else "None"
            })
        
        return state
