"""
Retriever Agent: Production GraphRAG-enhanced Context Retrieval
IEEE VIS 2026 - Supports both Neo4j and NetworkX backends
"""

import json
import os
from typing import Dict, Any, List, Optional
from .base import BaseAgent, AgentState
from .graph_store import create_graph_store, BaseGraphStore


class RetrieverAgent(BaseAgent):
    """
    Production Retriever Agent using real GraphRAG + Vector RAG
    
    Automatically selects backend:
    - Neo4j (if available and configured)
    - NetworkX (fallback, in-memory)
    """
    
    def __init__(self, llm_provider: str = "deepseek", knowledge_base=None):
        super().__init__("Retriever", llm_provider)
        self.knowledge_base = knowledge_base
        
        # Create graph store (auto-selects best available)
        try:
            self.graph_store = create_graph_store(prefer_neo4j=True)
            print(f"Retriever using graph store: {type(self.graph_store).__name__}")
        except Exception as e:
            print(f"Failed to create graph store: {e}")
            self.graph_store = None
    
    def execute(self, state: AgentState) -> AgentState:
        """Execute retrieval with GraphRAG + Vector RAG"""
        query = state.user_query
        intent = state.intent or {}
        
        contexts = []
        
        # Stage 1: Vector search from knowledge base (real)
        if self.knowledge_base:
            kb_context = self._vector_search(query)
            if kb_context:
                contexts.append({"source": "vector_kb", "content": kb_context})
        
        # Stage 2: Entity extraction and Graph expansion (real)
        entities = self._extract_entities(query)
        graph_entities = []
        if entities and self.graph_store:
            try:
                expanded = self.graph_store.query_expansion(entities)
                if expanded:
                    graph_context = self.graph_store.get_entity_context(expanded)
                    if graph_context.get("entities"):
                        contexts.append({
                            "source": "graph_rag",
                            "content": self._format_graph_context(graph_context),
                            "entities": expanded
                        })
                        graph_entities = expanded
            except Exception as e:
                print(f"GraphRAG error: {e}")
        
        # Stage 3: Data schema context (real)
        try:
            schema_context = self._get_data_schema()
            contexts.append({"source": "data_schema", "content": schema_context})
        except Exception as e:
            print(f"Schema context error: {e}")
        
        # Stage 4: Intent-based context
        if intent:
            intent_context = self._format_intent_context(intent)
            contexts.append({"source": "intent", "content": intent_context})
        
        state.retrieved_context = contexts
        
        self.log_action("Context Retrieval", {
            "query": query[:50],
            "entities_found": entities,
            "graph_entities_expanded": len(graph_entities),
            "context_sources": [c["source"] for c in contexts]
        })
        
        return state
    
    def _vector_search(self, query: str, k: int = 3) -> List[Dict]:
        """Real vector similarity search from knowledge base"""
        if not self.knowledge_base:
            return []
        
        try:
            results = self.knowledge_base.get_context_for_query(query, k=k)
            return results if results else []
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract entities from query using keyword matching"""
        # Comprehensive entity dictionary
        entity_keywords = {
            # Aircraft types
            "多旋翼无人机", "固定翼无人机", "直升机", "eVTOL", "复合翼无人机",
            "MultiRotor", "FixedWing", "Helicopter", 
            # Purposes  
            "物流配送", "测绘勘察", "应急救援", "个人消费", "巡检巡查", "农林植保",
            "Logistics", "Surveying", "Emergency", "Personal", "Inspection", "Agriculture",
            # Regions
            "宝安区", "龙岗区", "福田区", "南山区", "罗湖区", "光明区", "盐田区", "龙华区", "坪山区", "大鹏新区",
            "Baoan", "Longgang", "Futian", "Nanshan", "Luohu",
            # Metrics
            "飞行时长", "飞行架次", "机队规模", "企业数量", "空域利用率", "航线密度",
            "duration", "flight hours", "fleet size", "enterprise", 
            # Dimensions
            "规模与增长", "结构与主体", "时空特征", "效能与质量", "创新与融合",
            # Concepts
            "低空经济", "UAM", "UTM", "无人机",
            "low altitude", "drone", "UAS"
        }
        
        found = []
        query_lower = query.lower()
        
        for kw in entity_keywords:
            if kw.lower() in query_lower:
                found.append(kw)
        
        return list(set(found))
    
    def _get_data_schema(self) -> str:
        """Get real data schema from dataset"""
        try:
            import sys
            sys.path.insert(0, '/data1/xh/workspace/white-paper/experiments')
            from data.dataset_loader import get_dataset
            
            dataset = get_dataset()
            metadata = dataset.get_domain_metadata()
            
            schema_lines = ["Available Data Schema:"]
            
            for attr, info in metadata.get("attribute_semantics", {}).items():
                line = f"  - {attr} ({info['type']}): {info.get('description', '')}"
                if "categories" in info:
                    line += f" [{', '.join(info['categories'][:3])}...]"
                schema_lines.append(line)
            
            return "\n".join(schema_lines)
            
        except Exception as e:
            # Fallback schema
            return """Available Data Schema:
  - date (temporal): Flight operation date
  - time (temporal): Flight operation time  
  - region (spatial): Operation district (Baoan, Longgang, Futian, etc.)
  - duration (numerical): Flight duration in minutes
  - distance (numerical): Flight distance in kilometers
  - aircraft_type (categorical): MultiRotor, FixedWing, Helicopter
  - purpose (categorical): Logistics, Surveying, Emergency, Personal, Inspection
  - user_type (categorical): Enterprise, Personal, Unknown
  - altitude (numerical): Maximum flight altitude in meters"""
    
    def _format_graph_context(self, graph_data: Dict) -> str:
        """Format graph context for LLM consumption"""
        lines = ["Domain Knowledge Graph Context:"]
        
        if graph_data.get("entities"):
            lines.append("\nRelevant Concepts:")
            for e in graph_data["entities"][:8]:
                name = e.get("name", "Unknown")
                entity_type = e.get("type", "Unknown")
                desc = e.get("properties", {}).get("description", "")
                if desc:
                    lines.append(f"  - {name} ({entity_type}): {desc}")
                else:
                    lines.append(f"  - {name} ({entity_type})")
        
        if graph_data.get("relationships"):
            lines.append("\nKey Relationships:")
            seen = set()
            count = 0
            for r in graph_data["relationships"]:
                if count >= 8:
                    break
                key = (r["source"], r["type"], r["target"])
                if key not in seen:
                    seen.add(key)
                    lines.append(f"  - {r['source']} --[{r['type']}]--> {r['target']}")
                    count += 1
        
        return "\n".join(lines)
    
    def _format_intent_context(self, intent: Dict) -> str:
        """Format intent analysis as context"""
        lines = ["Intent Analysis:"]
        
        if "intent" in intent:
            intent_info = intent["intent"]
            lines.append(f"  Task Type: {intent_info.get('type', 'unknown')}")
            lines.append(f"  Description: {intent_info.get('description', 'N/A')}")
        
        if "data_requirements" in intent:
            reqs = intent["data_requirements"]
            if "dimensions" in reqs:
                lines.append(f"  Required Dimensions: {', '.join(reqs['dimensions'])}")
        
        if "visualization_plan" in intent:
            lines.append("  Recommended Charts:")
            for plan in intent["visualization_plan"][:3]:
                chart_type = plan.get("chart_type", "unknown")
                rationale = plan.get("rationale", "")
                lines.append(f"    - {chart_type}: {rationale}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the retriever
    print("Testing Retriever Agent...")
    
    retriever = RetrieverAgent()
    
    from agents.base import AgentState
    
    # Test queries
    test_queries = [
        "Show me flight trends for multirotor drones in Baoan district",
        "Compare enterprise users vs personal users",
        "What is the distribution of flight purposes?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        state = AgentState(user_query=query)
        result_state = retriever.execute(state)
        
        print(f"\nRetrieved {len(result_state.retrieved_context)} context sources:")
        for i, ctx in enumerate(result_state.retrieved_context, 1):
            print(f"\n{i}. Source: {ctx['source']}")
            if isinstance(ctx['content'], str):
                preview = ctx['content'][:300].replace('\n', ' ')
                print(f"   Content: {preview}...")
            else:
                print(f"   Content: {len(str(ctx['content']))} chars")
