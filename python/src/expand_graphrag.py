"""
Expand GraphRAG with more entities from PDFs
Using efficient batch processing
"""

import json
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str, max_pages: int = 10) -> str:
    """Extract text from PDF (limited pages for speed)"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages[:max_pages]):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def batch_extract_entities(text_chunks: List[str], llm_client) -> Dict:
    """Extract entities from multiple chunks in one LLM call"""
    
    # Combine chunks
    combined_text = "\n\n---\n\n".join(text_chunks[:3])  # Max 3 chunks
    
    system_prompt = """Extract entities from Low Altitude Economy text.

Entity types:
- Company: 企业名称 (DJI, EHang, 亿航, 大疆, 峰飞, 小鹏汇天)
- Technology: 技术 (自主飞行, 避障, 超视距, 感知)
- Policy: 政策 (适航认证, 低空飞行管理, 管理条例)
- Application: 应用 (物流, 载人, 巡检, 测绘, 消防)
- Region: 地区 (城市名)
- Metric: 指标 (飞行时长, 架次, 空域利用率)

Output JSON:
{
  "entities": [
    {"name": "entity", "type": "Company|Technology|Policy|Application|Region|Metric", "description": "brief"}
  ],
  "relationships": [
    {"source": "A", "target": "B", "relation": "produces|uses|regulates|part_of"}
  ]
}

Limit: 30 entities, 20 relationships."""

    try:
        response = llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=f"Text:\n{combined_text[:8000]}",  # Limit text length
            temperature=0.3
        )
        
        # Parse JSON
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
        
        return json.loads(json_str)
    except Exception as e:
        print(f"Extraction error: {e}")
        return {"entities": [], "relationships": []}


def main():
    from llm_client import LLMClient
    from agents.graph_store import NetworkXGraphStore
    
    print("="*70)
    print("EXPANDING GraphRAG Knowledge Base")
    print("="*70)
    
    # Initialize
    llm = LLMClient(provider="deepseek")
    graph_store = NetworkXGraphStore()
    graph_store.initialize_lae_domain()
    
    initial_e = graph_store.graph.number_of_nodes()
    initial_r = graph_store.graph.number_of_edges()
    
    print(f"\nInitial: {initial_e} entities, {initial_r} relations")
    
    # Additional entities to add (manually curated from domain knowledge)
    additional_entities = [
        # More companies
        ("亿航智能", "Company", "EHang, eVTOL manufacturer, 纳斯达克上市"),
        ("大疆创新", "Company", "DJI, global drone leader"),
        ("小鹏汇天", "Company", "Xpeng AeroHT, flying car developer"),
        ("峰飞航空", "Company", "AutoFlight, eVTOL company"),
        ("吉利沃飞长空", "Company", "Geely's eVTOL subsidiary"),
        ("时的科技", "Company", "TCab Tech, eVTOL startup"),
        ("御风未来", "Company", "Furture Wings, eVTOL company"),
        ("零重力飞机工业", "Company", "Zero Gravity Aircraft Industry"),
        
        # More technologies
        ("自主飞行", "Technology", "Autonomous flight"),
        ("超视距飞行", "Technology", "BVLOS - Beyond Visual Line of Sight"),
        ("感知与避障", "Technology", "Sense and avoid technology"),
        ("垂直起降", "Technology", "VTOL - Vertical Take-Off and Landing"),
        ("分布式电推进", "Technology", "DEP - Distributed Electric Propulsion"),
        ("飞控系统", "Technology", "Flight control system"),
        ("电池管理系统", "Technology", "BMS - Battery Management System"),
        ("5G通信", "Technology", "5G communication for UTM"),
        ("北斗导航", "Technology", "BeiDou navigation system"),
        
        # More applications
        ("城市空中交通", "Application", "UAM - Urban Air Mobility"),
        ("空中出租车", "Application", "Air taxi service"),
        ("医疗急救", "Application", "Medical emergency transport"),
        ("消防灭火", "Application", "Firefighting"),
        ("电力巡检", "Application", "Power line inspection"),
        ("石油管道巡检", "Application", "Pipeline inspection"),
        ("农药喷洒", "Application", "Agricultural spraying"),
        ("航拍测绘", "Application", "Aerial surveying and mapping"),
        ("物流配送", "Application", "Logistics and delivery"),
        ("载人运输", "Application", "Passenger transport"),
        
        # More regions
        ("粤港澳大湾区", "Region", "Greater Bay Area"),
        ("长三角", "Region", "Yangtze River Delta"),
        ("京津冀", "Region", "Beijing-Tianjin-Hebei region"),
        ("成渝地区", "Region", "Chengdu-Chongqing region"),
        ("合肥", "Region", "Hefei, pilot city"),
        ("芜湖", "Region", "Wuhu, pilot city"),
        ("杭州", "Region", "Hangzhou"),
        ("南京", "Region", "Nanjing"),
        ("广州", "Region", "Guangzhou"),
        ("成都", "Region", "Chengdu"),
        
        # More policies/concepts
        ("低空飞行管理条例", "Policy", "Low altitude flight management regulations"),
        ("民用无人驾驶航空发展路线图", "Policy", "Civil UAV development roadmap"),
        ("国家空域基础分类办法", "Policy", "National airspace classification"),
        ("特定类运行", "Policy", "Specific category operations"),
        ("审定类运行", "Policy", "Certified category operations"),
        ("轻型无人机", "Policy", "Light UAV category"),
        ("小型无人机", "Policy", "Small UAV category"),
        ("中型无人机", "Policy", "Medium UAV category"),
        ("大型无人机", "Policy", "Large UAV category"),
        
        # More metrics
        ("飞行架次", "Metric", "Number of flights"),
        ("飞行里程", "Metric", "Total flight distance"),
        ("载货量", "Metric", "Cargo capacity"),
        ("载客量", "Metric", "Passenger capacity"),
        ("运营收入", "Metric", "Operating revenue"),
        ("事故率", "Metric", "Accident rate"),
        ("准点率", "Metric", "On-time rate"),
    ]
    
    # Additional relationships
    additional_relations = [
        ("大疆创新", "produces", "多旋翼无人机"),
        ("亿航智能", "produces", "eVTOL"),
        ("小鹏汇天", "develops", "飞行汽车"),
        ("峰飞航空", "produces", "eVTOL"),
        ("自主飞行", "requires", "感知与避障"),
        ("超视距飞行", "requires", "5G通信"),
        ("超视距飞行", "requires", "北斗导航"),
        ("城市空中交通", "uses", "eVTOL"),
        ("空中出租车", "uses", "eVTOL"),
        ("物流配送", "uses", "多旋翼无人机"),
        ("医疗急救", "uses", "直升机"),
        ("农药喷洒", "uses", "多旋翼无人机"),
        ("电力巡检", "uses", "多旋翼无人机"),
        ("粤港澳大湾区", "part_of", "低空经济"),
        ("长三角", "part_of", "低空经济"),
        ("低空飞行管理条例", "regulates", "多旋翼无人机"),
        ("低空飞行管理条例", "regulates", "eVTOL"),
        ("适航认证", "required_for", "eVTOL"),
        ("飞行时长", "measures", "低空经济"),
        ("飞行架次", "measures", "低空经济"),
    ]
    
    # Add entities
    added_e = 0
    for name, etype, desc in additional_entities:
        if not graph_store.graph.has_node(name):
            graph_store.graph.add_node(name, type=etype, description=desc)
            added_e += 1
    
    # Add relationships
    added_r = 0
    for source, relation, target in additional_relations:
        if not graph_store.graph.has_node(source):
            graph_store.graph.add_node(source, type="Entity")
        if not graph_store.graph.has_node(target):
            graph_store.graph.add_node(target, type="Entity")
        if not graph_store.graph.has_edge(source, target):
            graph_store.graph.add_edge(source, target, relation=relation)
            added_r += 1
    
    # Try to extract from PDFs (quick version)
    pdf_dir = Path("/data1/xh/workspace/white-paper/docs/pdf")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    print(f"\nProcessing {len(pdf_files)} PDFs...")
    
    all_text = ""
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(str(pdf_file), max_pages=5)
        all_text += text + "\n"
    
    print(f"Extracted {len(all_text)} characters")
    
    # Extract with LLM (one batch)
    if len(all_text) > 500:
        print("Extracting entities with LLM...")
        
        # Split into chunks
        chunks = [all_text[i:i+3000] for i in range(0, min(len(all_text), 9000), 3000)]
        
        extraction = batch_extract_entities(chunks, llm)
        
        # Add extracted entities
        for entity in extraction.get("entities", []):
            name = entity.get("name", "").strip()
            etype = entity.get("type", "Entity")
            desc = entity.get("description", "")
            if name and len(name) > 1 and not graph_store.graph.has_node(name):
                graph_store.graph.add_node(name, type=etype, description=desc)
                added_e += 1
        
        # Add extracted relationships
        for rel in extraction.get("relationships", []):
            source = rel.get("source", "")
            target = rel.get("target", "")
            relation = rel.get("relation", "related")
            if source and target:
                if not graph_store.graph.has_node(source):
                    graph_store.graph.add_node(source, type="Entity")
                if not graph_store.graph.has_node(target):
                    graph_store.graph.add_node(target, type="Entity")
                if not graph_store.graph.has_edge(source, target):
                    graph_store.graph.add_edge(source, target, relation=relation)
                    added_r += 1
        
        print(f"✓ LLM extraction: {len(extraction.get('entities', []))} entities, {len(extraction.get('relationships', []))} relations")
    
    # Stats
    final_e = graph_store.graph.number_of_nodes()
    final_r = graph_store.graph.number_of_edges()
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Initial:  {initial_e} entities, {initial_r} relations")
    print(f"Added:    {added_e} entities, {added_r} relations")
    print(f"Final:    {final_e} entities, {final_r} relations")
    
    # Save
    output = {
        "entities": [{"name": n, **d} for n, d in graph_store.graph.nodes(data=True)],
        "relationships": [{"source": s, "target": t, "relation": d.get("relation", "related")} 
                         for s, t, d in graph_store.graph.edges(data=True)],
        "stats": {
            "initial_entities": initial_e,
            "initial_relations": initial_r,
            "final_entities": final_e,
            "final_relations": final_r,
            "added_entities": added_e,
            "added_relations": added_r
        }
    }
    
    output_file = Path("/data1/xh/workspace/white-paper/experiments/results/expanded_graphrag.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {output_file}")
    
    # Show samples
    print("\nSample entities by type:")
    from collections import defaultdict
    by_type = defaultdict(list)
    for node, data in graph_store.graph.nodes(data=True):
        by_type[data.get('type', 'Unknown')].append(node)
    
    for etype, entities in sorted(by_type.items()):
        print(f"\n  {etype} ({len(entities)}):")
        for e in entities[:5]:
            print(f"    - {e}")
        if len(entities) > 5:
            print(f"    ... and {len(entities)-5} more")
    
    print("\n" + "="*70)
    print("GraphRAG Expansion Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
