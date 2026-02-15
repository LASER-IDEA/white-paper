"""
Base Agent Class with Common Functionality
IEEE VIS 2026 - Multi-Agent Architecture Core
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import json
from datetime import datetime


@dataclass
class AgentState:
    """Shared state across agents - tracks the full pipeline"""
    user_query: str
    intent: Optional[Dict[str, Any]] = None
    retrieved_context: Optional[List[Dict]] = None
    generated_code: Optional[str] = None
    execution_result: Optional[Dict] = None
    visual_feedback: Optional[Dict] = None
    iteration_count: int = 0
    max_iterations: int = 3
    execution_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for logging"""
        return {
            "user_query": self.user_query,
            "intent": self.intent,
            "retrieved_context_count": len(self.retrieved_context) if self.retrieved_context else 0,
            "has_generated_code": self.generated_code is not None,
            "execution_result": self.execution_result,
            "visual_feedback": self.visual_feedback,
            "iteration_count": self.iteration_count,
            "history_length": len(self.execution_history)
        }


class BaseAgent(ABC):
    """Base class for all agents in the LAEV system"""
    
    def __init__(self, name: str, llm_provider: str = "deepseek"):
        self.name = name
        self.llm_provider = llm_provider
        self.action_log: List[Dict] = []
    
    @abstractmethod
    def execute(self, state: AgentState) -> AgentState:
        """Execute agent's task and return updated state"""
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log agent actions for debugging, visualization, and paper"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "action": action,
            "details": details
        }
        self.action_log.append(entry)
        print(f"[{self.name}] {action}")


class AgentPipeline:
    """Orchestrates the multi-agent pipeline"""
    
    def __init__(self, agents: List[BaseAgent], max_iterations: int = 3):
        self.agents = agents
        self.max_iterations = max_iterations
        self.pipeline_log: List[Dict] = []
    
    def run(self, user_query: str) -> AgentState:
        """Execute full pipeline"""
        state = AgentState(
            user_query=user_query,
            max_iterations=self.max_iterations
        )
        
        for iteration in range(self.max_iterations):
            state.iteration_count = iteration + 1
            
            # Execute each agent in sequence
            for agent in self.agents:
                state = agent.execute(state)
                self._log_step(agent.name, state)
            
            # Check if we need to iterate
            if self._should_stop(state):
                break
        
        return state
    
    def _log_step(self, agent_name: str, state: AgentState):
        """Log pipeline step"""
        self.pipeline_log.append({
            "agent": agent_name,
            "state": state.to_dict()
        })
    
    def _should_stop(self, state: AgentState) -> bool:
        """Determine if pipeline should stop iterating"""
        # Stop if execution successful (with or without visual feedback)
        if state.execution_result and state.execution_result.get("success"):
            # If visual feedback available, check score
            if state.visual_feedback:
                score = state.visual_feedback.get("overall_score", 0)
                if score >= 0.7:  # Slightly lower threshold
                    return True
            else:
                # No visual feedback but execution succeeded - stop
                return True
        return False
