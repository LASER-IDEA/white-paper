"""
Graph Store Implementations for GraphRAG
Supports both Neo4j (production) and NetworkX (fallback/testing)
"""

import json
import os
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Try to import Neo4j
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

# Try to import NetworkX
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False


@dataclass
class Entity:
    """Entity in knowledge graph"""
    id: str
    type: str
    name: str
    properties: Dict[str, Any]


@dataclass
class Relationship:
    """Relationship between entities"""
    source: str
    target: str
    type: str
    properties: Dict[str, Any]


class BaseGraphStore(ABC):
    """Abstract base class for graph stores"""
    
    @abstractmethod
    def query_expansion(self, entities: List[str]) -> List[str]:
        """Expand query using graph relationships"""
        pass
    
    @abstractmethod
    def get_entity_context(self, entity_names: List[str]) -> Dict[str, Any]:
        """Get rich context for entities"""
        pass
    
    @abstractmethod
    def initialize_lae_domain(self):
        """Initialize with Low Altitude Economy domain knowledge"""
        pass


class NetworkXGraphStore(BaseGraphStore):
    """
    In-memory Graph Store using NetworkX
    Fallback when Neo4j is unavailable
    """
    
    def __init__(self):
        if not NETWORKX_AVAILABLE:
            raise ImportError("NetworkX not installed. Run: pip install networkx")
        
        self.graph = nx.DiGraph()
        self._initialized = False
        print("Using NetworkX in-memory graph store")
    
    def query_expansion(self, entities: List[str]) -> List[str]:
        """Expand query using graph relationships (multi-hop)"""
        if not self._initialized:
            self.initialize_lae_domain()
        
        expanded = set(entities)
        
        for entity in entities:
            # Find matching nodes (case-insensitive)
            matching_nodes = [
                n for n in self.graph.nodes()
                if entity.lower() in n.lower() or n.lower() in entity.lower()
            ]
            
            for node in matching_nodes:
                expanded.add(node)
                
                # 1-hop expansion
                if self.graph.has_node(node):
                    neighbors = list(self.graph.neighbors(node)) + \
                               list(self.graph.predecessors(node))
                    expanded.update(neighbors)
                    
                    # 2-hop expansion (limited)
                    for neighbor in neighbors[:5]:  # Limit to avoid explosion
                        hop2 = list(self.graph.neighbors(neighbor)) + \
                               list(self.graph.predecessors(neighbor))
                        expanded.update(hop2[:3])
        
        return list(expanded)
    
    def get_entity_context(self, entity_names: List[str]) -> Dict[str, Any]:
        """Get rich context for entities including relationships"""
        if not self._initialized:
            self.initialize_lae_domain()
        
        context = {"entities": [], "relationships": []}
        seen_rels = set()
        
        for name in entity_names:
            # Find matching node
            matching_nodes = [
                n for n in self.graph.nodes()
                if name.lower() in n.lower() or n.lower() in name.lower()
            ]
            
            for node in matching_nodes:
                if self.graph.has_node(node):
                    node_data = self.graph.nodes[node]
                    context["entities"].append({
                        "name": node,
                        "type": node_data.get("type", "Unknown"),
                        "properties": {k: v for k, v in node_data.items() if k != "type"}
                    })
                    
                    # Get relationships
                    for successor in self.graph.successors(node):
                        edge_data = self.graph.edges[node, successor]
                        rel_key = (node, successor, edge_data.get("relation", "related"))
                        if rel_key not in seen_rels:
                            seen_rels.add(rel_key)
                            context["relationships"].append({
                                "source": node,
                                "target": successor,
                                "type": edge_data.get("relation", "related"),
                                "properties": dict(edge_data)
                            })
        
        return context
    
    def initialize_lae_domain(self):
        """Initialize graph with Low Altitude Economy domain knowledge"""
        if self._initialized:
            return
        
        # Clear and rebuild
        self.graph.clear()
        
        # Domain entities from INDEX_DEFINITIONS.md and white papers
        entities = [
            # Dimensions
            ("规模与增长", {"type": "Dimension", "description": "Scale & Growth"}),
            ("结构与主体", {"type": "Dimension", "description": "Structure & Entity"}),
            ("时空特征", {"type": "Dimension", "description": "Time & Space"}),
            ("效能与质量", {"type": "Dimension", "description": "Efficiency & Quality"}),
            ("创新与融合", {"type": "Dimension", "description": "Innovation & Integration"}),
            
            # Metrics - Scale
            ("飞行时长", {"type": "Metric", "dimension": "规模与增长", "unit": "小时"}),
            ("飞行架次", {"type": "Metric", "dimension": "规模与增长", "unit": "次"}),
            ("机队规模", {"type": "Metric", "dimension": "规模与增长", "unit": "架"}),
            ("市场规模", {"type": "Metric", "dimension": "规模与增长", "unit": "亿元"}),
            
            # Metrics - Structure
            ("企业数量", {"type": "Metric", "dimension": "结构与主体", "unit": "家"}),
            ("持证驾驶员", {"type": "Metric", "dimension": "结构与主体", "unit": "人"}),
            ("起降点数量", {"type": "Metric", "dimension": "结构与主体", "unit": "个"}),
            
            # Metrics - SpaceTime
            ("空域利用率", {"type": "Metric", "dimension": "时空特征", "unit": "%"}),
            ("航线密度", {"type": "Metric", "dimension": "时空特征", "unit": "条/km²"}),
            ("高峰时段", {"type": "Metric", "dimension": "时空特征", "unit": "小时"}),
            
            # Metrics - Efficiency
            ("任务质量指数", {"type": "Metric", "dimension": "效能与质量", "unit": "TQI"}),
            ("载运率", {"type": "Metric", "dimension": "效能与质量", "unit": "%"}),
            ("准点率", {"type": "Metric", "dimension": "效能与质量", "unit": "%"}),
            
            # Metrics - Innovation
            ("专利数量", {"type": "Metric", "dimension": "创新与融合", "unit": "件"}),
            ("研发投入", {"type": "Metric", "dimension": "创新与融合", "unit": "万元"}),
            ("技术成熟度", {"type": "Metric", "dimension": "创新与融合", "unit": "TRL"}),
            
            # Aircraft types
            ("多旋翼无人机", {"type": "AircraftType", "category": "MultiRotor", "altitude": "<120m"}),
            ("固定翼无人机", {"type": "AircraftType", "category": "FixedWing", "altitude": "<3000m"}),
            ("直升机", {"type": "AircraftType", "category": "Helicopter", "altitude": "<3000m"}),
            ("eVTOL", {"type": "AircraftType", "category": "eVTOL", "altitude": "<6000m"}),
            ("复合翼无人机", {"type": "AircraftType", "category": "Hybrid", "altitude": "<3000m"}),
            
            # Operation purposes
            ("物流配送", {"type": "Purpose", "category": "Logistics"}),
            ("测绘勘察", {"type": "Purpose", "category": "Surveying"}),
            ("应急救援", {"type": "Purpose", "category": "Emergency"}),
            ("个人消费", {"type": "Purpose", "category": "Personal"}),
            ("巡检巡查", {"type": "Purpose", "category": "Inspection"}),
            ("农林植保", {"type": "Purpose", "category": "Agriculture"}),
            
            # Regions - Shenzhen districts
            ("宝安区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("龙岗区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("福田区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("南山区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("罗湖区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("光明区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("盐田区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("龙华区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("坪山区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            ("大鹏新区", {"type": "Region", "city": "Shenzhen", "type_detail": "district"}),
            
            # User types
            ("企业用户", {"type": "UserType"}),
            ("个人用户", {"type": "UserType"}),
            ("政府用户", {"type": "UserType"}),
            
            # Core concepts
            ("低空经济", {"type": "Concept", "definition": "Low Altitude Economy"}),
            ("UAM", {"type": "Concept", "definition": "Urban Air Mobility"}),
            ("UAS", {"type": "Concept", "definition": "Unmanned Aircraft System"}),
            ("UTM", {"type": "Concept", "definition": "UAS Traffic Management"}),
            ("适航认证", {"type": "Concept", "definition": "Airworthiness Certification"}),
            ("低空飞行服务", {"type": "Concept", "definition": "Low Altitude Flight Services"}),
            
            # Policies
            ("无人驾驶航空器飞行管理暂行条例", {"type": "Policy", "year": 2024, "issuer": "国务院"}),
            ("低空经济发展指导意见", {"type": "Policy", "year": 2023, "issuer": "民航局"}),
            ("深圳低空经济促进条例", {"type": "Policy", "year": 2024, "issuer": "深圳市"}),
        ]
        
        # Add entities
        for name, props in entities:
            self.graph.add_node(name, **props)
        
        # Define relationships
        relationships = [
            # Dimension-Metric relationships
            ("规模与增长", "includes", "飞行时长"),
            ("规模与增长", "includes", "飞行架次"),
            ("规模与增长", "includes", "机队规模"),
            ("规模与增长", "includes", "市场规模"),
            ("结构与主体", "includes", "企业数量"),
            ("结构与主体", "includes", "持证驾驶员"),
            ("时空特征", "includes", "空域利用率"),
            ("时空特征", "includes", "航线密度"),
            ("效能与质量", "includes", "任务质量指数"),
            ("创新与融合", "includes", "专利数量"),
            
            # Aircraft capabilities
            ("多旋翼无人机", "used_for", "物流配送"),
            ("多旋翼无人机", "used_for", "巡检巡查"),
            ("多旋翼无人机", "used_for", "农林植保"),
            ("固定翼无人机", "used_for", "测绘勘察"),
            ("固定翼无人机", "used_for", "巡检巡查"),
            ("直升机", "used_for", "应急救援"),
            ("直升机", "used_for", "个人消费"),
            ("eVTOL", "used_for", "个人消费"),
            ("eVTOL", "used_for", "物流配送"),
            
            # Policy regulations
            ("无人驾驶航空器飞行管理暂行条例", "regulates", "多旋翼无人机"),
            ("无人驾驶航空器飞行管理暂行条例", "regulates", "固定翼无人机"),
            ("无人驾驶航空器飞行管理暂行条例", "regulates", "直升机"),
            ("深圳低空经济促进条例", "promotes", "低空经济"),
            ("宝安区", "part_of", "低空经济"),
            ("南山区", "part_of", "低空经济"),
            
            # Measurement relationships
            ("飞行时长", "measures", "低空经济"),
            ("企业数量", "measures", "结构与主体"),
            ("空域利用率", "measures", "时空特征"),
            
            # Concept relationships
            ("UAM", "subset_of", "低空经济"),
            ("UAS", "subset_of", "低空经济"),
            ("UTM", "supports", "UAM"),
            ("低空飞行服务", "enables", "UAM"),
        ]
        
        # Add relationships
        for source, relation, target in relationships:
            if self.graph.has_node(source) and self.graph.has_node(target):
                self.graph.add_edge(source, target, relation=relation)
        
        self._initialized = True
        print(f"Initialized NetworkX graph with {self.graph.number_of_nodes()} entities and {self.graph.number_of_edges()} relationships")


class Neo4jGraphStore(BaseGraphStore):
    """Production Neo4j Graph Store"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "vispaper2026")
        self.driver = None
        self._available = False
        
        if NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                self.driver.verify_connectivity()
                self._available = True
                print(f"Connected to Neo4j at {self.uri}")
            except Exception as e:
                print(f"Neo4j connection failed: {e}")
        else:
            print("Neo4j driver not installed")
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def is_available(self) -> bool:
        return self._available
    
    def query_expansion(self, entities: List[str]) -> List[str]:
        """Expand query using graph relationships"""
        if not self._available:
            return entities
        
        expanded = set(entities)
        
        try:
            with self.driver.session() as session:
                for entity in entities:
                    # 1-hop expansion
                    result = session.run("""
                        MATCH (n)-[]-(m)
                        WHERE n.name CONTAINS $name OR $name CONTAINS n.name
                        RETURN DISTINCT m.name as related
                        LIMIT 10
                    """, name=entity)
                    
                    for record in result:
                        if record["related"]:
                            expanded.add(record["related"])
                    
                    # 2-hop expansion
                    result = session.run("""
                        MATCH (n)-[]-()-[]-(m)
                        WHERE n.name CONTAINS $name OR $name CONTAINS n.name
                        AND n <> m
                        RETURN DISTINCT m.name as related
                        LIMIT 5
                    """, name=entity)
                    
                    for record in result:
                        if record["related"]:
                            expanded.add(record["related"])
        
        except Exception as e:
            print(f"Graph query error: {e}")
        
        return list(expanded)
    
    def get_entity_context(self, entity_names: List[str]) -> Dict[str, Any]:
        """Get rich context for entities"""
        if not self._available:
            return {"entities": [], "relationships": []}
        
        context = {"entities": [], "relationships": []}
        seen_rels = set()
        
        try:
            with self.driver.session() as session:
                for name in entity_names:
                    # Get entity info
                    result = session.run("""
                        MATCH (n)
                        WHERE n.name CONTAINS $name OR $name CONTAINS n.name
                        RETURN n as entity, labels(n) as labels
                        LIMIT 5
                    """, name=name)
                    
                    for record in result:
                        entity_data = dict(record["entity"])
                        entity_data["labels"] = record["labels"]
                        context["entities"].append(entity_data)
                    
                    # Get relationships
                    result = session.run("""
                        MATCH (n)-[r]-(m)
                        WHERE n.name CONTAINS $name OR $name CONTAINS n.name
                        RETURN n.name as source, type(r) as rel_type, 
                               m.name as target, properties(r) as rel_props
                        LIMIT 10
                    """, name=name)
                    
                    for record in result:
                        rel_key = (record["source"], record["target"], record["rel_type"])
                        if rel_key not in seen_rels:
                            seen_rels.add(rel_key)
                            context["relationships"].append({
                                "source": record["source"],
                                "target": record["target"],
                                "type": record["rel_type"],
                                "properties": dict(record["rel_props"])
                            })
        
        except Exception as e:
            print(f"Entity context error: {e}")
        
        return context
    
    def initialize_lae_domain(self):
        """Initialize graph with LAEV domain knowledge"""
        if not self._available:
            print("Neo4j not available, skipping initialization")
            return
        
        # Delegate to NetworkX version for data
        nx_store = NetworkXGraphStore()
        nx_store.initialize_lae_domain()
        
        try:
            with self.driver.session() as session:
                # Clear existing
                session.run("MATCH (n) DETACH DELETE n")
                
                # Create constraints
                try:
                    session.run("CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (n:Entity) REQUIRE n.name IS UNIQUE")
                except:
                    pass
                
                # Add entities
                for node, data in nx_store.graph.nodes(data=True):
                    label = data.get("type", "Entity")
                    props = {k: v for k, v in data.items() if k != "type"}
                    props["name"] = node
                    
                    # Create node with dynamic label
                    session.run(f"""
                        CREATE (n:{label} $props)
                    """, props=props)
                
                # Add relationships
                for source, target, data in nx_store.graph.edges(data=True):
                    rel_type = data.get("relation", "RELATED").upper()
                    session.run(f"""
                        MATCH (a {{name: $source}}), (b {{name: $target}})
                        CREATE (a)-[:{rel_type}]->(b)
                    """, source=source, target=target)
                
                print("Neo4j graph initialized with LAEV domain knowledge")
        
        except Exception as e:
            print(f"Failed to initialize Neo4j: {e}")


def create_graph_store(prefer_neo4j: bool = True) -> BaseGraphStore:
    """
    Factory function to create appropriate graph store
    
    Args:
        prefer_neo4j: Try Neo4j first, fallback to NetworkX
    
    Returns:
        Graph store instance
    """
    if prefer_neo4j and NEO4J_AVAILABLE:
        try:
            store = Neo4jGraphStore()
            if store.is_available():
                store.initialize_lae_domain()
                return store
        except Exception as e:
            print(f"Neo4j failed, falling back to NetworkX: {e}")
    
    # Fallback to NetworkX
    store = NetworkXGraphStore()
    store.initialize_lae_domain()
    return store


if __name__ == "__main__":
    # Test graph store
    print("Testing Graph Store...")
    
    store = create_graph_store(prefer_neo4j=False)
    
    # Test query expansion
    query_entities = ["多旋翼无人机", "物流配送"]
    expanded = store.query_expansion(query_entities)
    print(f"\nQuery: {query_entities}")
    print(f"Expanded: {expanded}")
    
    # Test context retrieval
    context = store.get_entity_context(expanded[:3])
    print(f"\nContext entities: {len(context['entities'])}")
    print(f"Context relationships: {len(context['relationships'])}")
