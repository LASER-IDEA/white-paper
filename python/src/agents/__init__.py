"""
LAEV-Agents: Multi-Agent System for Low Altitude Economy Visualization
IEEE VIS 2026 Submission

This module implements a multi-agent architecture for intelligent 
visualization generation with the following agents:

- PlannerAgent: Intent analysis and task decomposition
- RetrieverAgent: GraphRAG-enhanced context retrieval  
- CoderAgent: Code generation with multi-strategy support
- EvaluatorAgent: Multi-dimensional quality assessment
- ReflectorAgent: Iterative refinement and error recovery

Usage:
    from agents import LAEVOrchestrator
    
    orchestrator = LAEVOrchestrator()
    result = orchestrator.process("Show me flight trends in Shenzhen")
"""

# Base classes
from .base import BaseAgent, AgentState, AgentPipeline

# Agents
from .planner import PlannerAgent
from .retriever import RetrieverAgent
from .coder import CoderAgent
from .evaluator import EvaluatorAgent, SimpleEvaluatorAgent, CodeExecutor
from .reflector import ReflectorAgent, SimpleReflectorAgent

# Visual Evaluator
from .visual_evaluator import VisualEvaluator, evaluate_visual_quality

# Graph Store
from .graph_store import (
    BaseGraphStore,
    NetworkXGraphStore,
    Neo4jGraphStore,
    create_graph_store,
    Entity,
    Relationship
)

# Orchestration
from .orchestrator import LAEVOrchestrator, generate_visualization

__version__ = "1.0.0"
__author__ = "LAEV Research Team"

__all__ = [
    # Base classes
    "BaseAgent",
    "AgentState", 
    "AgentPipeline",
    
    # Agents
    "PlannerAgent",
    "RetrieverAgent",
    "CoderAgent",
    "EvaluatorAgent",
    "SimpleEvaluatorAgent",
    "ReflectorAgent",
    "SimpleReflectorAgent",
    
    # Graph Store
    "BaseGraphStore",
    "NetworkXGraphStore",
    "Neo4jGraphStore",
    "create_graph_store",
    "Entity",
    "Relationship",
    
    # Utilities
    "CodeExecutor",
    "VisualEvaluator",
    "evaluate_visual_quality",
    
    # Orchestration
    "LAEVOrchestrator",
    "generate_visualization"
]
