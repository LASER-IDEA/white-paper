"""
Agent Orchestrator: Coordinates Multi-Agent Pipeline
IEEE VIS 2026 - Main entry point for LAEV-Agent system
"""

import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import asdict
from .base import BaseAgent, AgentState, AgentPipeline
from .planner import PlannerAgent
from .retriever import RetrieverAgent
from .coder import CoderAgent
from .evaluator import EvaluatorAgent, SimpleEvaluatorAgent
from .reflector import ReflectorAgent, SimpleReflectorAgent


class LAEVOrchestrator:
    """
    Main orchestrator for the LAEV Multi-Agent System.
    
    Usage:
        orchestrator = LAEVOrchestrator(use_full_agents=True)
        result = orchestrator.process("Show me flight trend in Shenzhen")
    """
    
    def __init__(
        self,
        llm_provider: str = "deepseek",
        use_full_agents: bool = True,
        max_iterations: int = 3,
        knowledge_base=None
    ):
        """
        Initialize orchestrator.
        
        Args:
            llm_provider: LLM provider name
            use_full_agents: Use full implementation (True) or simplified (False)
            max_iterations: Maximum refinement iterations
            knowledge_base: Optional RAG knowledge base
        """
        self.llm_provider = llm_provider
        self.max_iterations = max_iterations
        self.knowledge_base = knowledge_base
        
        # Create agents
        self.agents = self._create_agents(use_full_agents)
        
        # Create pipeline
        self.pipeline = AgentPipeline(
            agents=list(self.agents.values()),
            max_iterations=max_iterations
        )
        
        # Callbacks for UI updates
        self.progress_callbacks: List[Callable] = []
    
    def _create_agents(self, use_full: bool) -> Dict[str, BaseAgent]:
        """Create agent instances"""
        # Use simplified evaluators/reflector if not full mode
        if use_full:
            return {
                "planner": PlannerAgent(self.llm_provider),
                "retriever": RetrieverAgent(self.llm_provider, self.knowledge_base),
                "coder": CoderAgent(self.llm_provider, strategy="adaptive"),
                "evaluator": EvaluatorAgent(self.llm_provider, use_vision=False),
                "reflector": ReflectorAgent(self.llm_provider)
            }
        else:
            # Simplified version for quick testing
            return {
                "planner": PlannerAgent(self.llm_provider),
                "retriever": RetrieverAgent(self.llm_provider, self.knowledge_base),
                "coder": CoderAgent(self.llm_provider, strategy="conservative"),
                "evaluator": SimpleEvaluatorAgent(self.llm_provider),
                "reflector": SimpleReflectorAgent(self.llm_provider)
            }
    
    def process(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query through multi-agent pipeline.
        
        Args:
            user_query: Natural language query
            
        Returns:
            Complete result with chart, execution info, and agent logs
        """
        # Run pipeline
        final_state = self.pipeline.run(user_query)
        
        # Compile result
        result = {
            "success": False,
            "query": user_query,
            "chart_code": None,
            "chart_html": None,
            "execution_result": None,
            "agent_trace": self._compile_trace(final_state),
            "iterations": final_state.iteration_count,
            "error": None
        }
        
        if final_state.execution_result:
            result["execution_result"] = final_state.execution_result
            result["success"] = final_state.execution_result.get("success", False)
            
            if result["success"]:
                result["chart_code"] = final_state.generated_code
                result["chart_html"] = final_state.execution_result.get("html_content")
                # Include visual feedback if available
                if final_state.visual_feedback:
                    result["visual_feedback"] = final_state.visual_feedback
            else:
                result["error"] = final_state.execution_result.get("error")
        
        return result
    
    def _compile_trace(self, state: AgentState) -> List[Dict]:
        """Compile agent execution trace for debugging and visualization"""
        trace = []
        
        # Add each agent's actions
        for agent_name, agent in self.agents.items():
            for log in agent.action_log:
                trace.append({
                    "agent": log["agent"],
                    "timestamp": log["timestamp"],
                    "action": log["action"],
                    "details": log["details"]
                })
        
        # Sort by timestamp
        trace.sort(key=lambda x: x["timestamp"])
        
        return trace
    
    def get_design_space(self) -> Dict[str, Any]:
        """Get formalized design space (for paper contribution)"""
        if "planner" in self.agents:
            return self.agents["planner"].design_space
        return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "total_queries": len(self.pipeline.pipeline_log),
            "average_iterations": sum(
                log["state"]["iteration_count"] for log in self.pipeline.pipeline_log
            ) / max(1, len(self.pipeline.pipeline_log)),
            "success_rate": sum(
                1 for log in self.pipeline.pipeline_log 
                if log["state"]["execution_result"] and log["state"]["execution_result"].get("success")
            ) / max(1, len(self.pipeline.pipeline_log))
        }


# Convenience function for direct usage
def generate_visualization(
    query: str,
    llm_provider: str = "deepseek",
    knowledge_base=None
) -> Dict[str, Any]:
    """
    One-shot function to generate visualization from query.
    
    Args:
        query: Natural language query
        llm_provider: LLM provider
        knowledge_base: Optional RAG knowledge base
        
    Returns:
        Visualization result
    """
    orchestrator = LAEVOrchestrator(
        llm_provider=llm_provider,
        use_full_agents=False,  # Use simplified for speed
        knowledge_base=knowledge_base
    )
    return orchestrator.process(query)
