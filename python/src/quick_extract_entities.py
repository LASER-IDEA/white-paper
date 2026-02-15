"""
Quick entity extraction from PDF - processes key pages only
"""

import json
from pathlib import Path
from pypdf import PdfReader


def extract_from_pdf(pdf_path: str, max_pages: int = 5) -> str:
    """Extract text from first N pages"""
    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages[:max_pages]):
        text += page.extract_text() + "\n"
    return text


def main():
    from llm_client import LLMClient
    from agents.graph_store import NetworkXGraphStore
    
    print("=" * 70)
    print("Quick PDF Entity Extraction")
    print("=" * 70)
    
    # Initialize
    llm = LLMClient(provider="deepseek")
    graph_store = NetworkXGraphStore()
    graph_store.initialize_lae_domain()
    
    initial_e = graph_store.graph.number_of_nodes()
    initial_r = graph_store.graph.number_of_edges()
    
    # Key entities to add manually from white paper knowledge
    additional_entities = [
        # Companies
        ("DJI", "Company", "大疆创新, global drone leader"),
        ("EHang", "Company", "亿航智能, eVTOL manufacturer"),
        ("Xpeng AeroHT", "Company", "小鹏汇天, flying car developer"),
        ("AutoFlight", "Company", "峰飞航空, eVTOL company"),
        ("Lilium", "Company", "German eVTOL company"),
        ("Joby Aviation", "Company", "US eVTOL company"),
        
        # Technologies
        (" sense and avoid", "Technology", "感知与避障技术"),
        ("BVLOS", "Technology", "Beyond Visual Line of Sight, 超视距飞行"),
        ("eVTOL", "AircraftType", "Electric Vertical Take-Off and Landing"),
        ("UTM", "Technology", "UAS Traffic Management, 无人机交通管理系统"),
        ("Remote ID", "Technology", "远程识别技术"),
        ("Geofencing", "Technology", "电子围栏技术"),
        
        # Applications
        ("Aerial Photography", "Application", "航拍"),
        ("Precision Agriculture", "Application", "精准农业"),
        ("Infrastructure Inspection", "Application", "基础设施巡检"),
        ("Medical Delivery", "Application", "医疗配送"),
        ("Firefighting", "Application", "消防救援"),
        ("Surveillance", "Application", "安防监控"),
        
        # Regions
        ("Shanghai", "Region", "上海"),
        ("Beijing", "Region", "北京"),
        ("Guangzhou", "Region", "广州"),
        ("Chengdu", "Region", "成都"),
        ("Hefei", "Region", "合肥, low-altitude economy pilot city"),
        ("Wuhu", "Region", "芜湖, low-altitude economy pilot city"),
        
        # Policies/Concepts
        ("Airworthiness Certification", "Policy", "适航认证"),
        ("Type Certificate", "Policy", "型号合格证"),
        ("Production Certificate", "Policy", "生产许可证"),
        ("Standard Category", "Policy", "标准类无人机"),
        ("Specific Category", "Policy", "特定类无人机"),
        ("Light UAV", "Policy", "轻型无人机"),
        
        # Metrics
        ("Payload Capacity", "Metric", "载重能力, kg"),
        ("Endurance", "Metric", "续航能力, minutes"),
        ("Range", "Metric", "航程, km"),
        ("Cruise Speed", "Metric", "巡航速度, km/h"),
        ("Safety Rate", "Metric", "安全率, percentage"),
    ]
    
    # Relationships
    additional_relations = [
        ("DJI", "produces", "多旋翼无人机"),
        ("EHang", "produces", "eVTOL"),
        ("Xpeng AeroHT", "develops", "飞行汽车"),
        ("eVTOL", "requires", "适航认证"),
        ("BVLOS", "requires", "UTM"),
        ("Medical Delivery", "uses", "eVTOL"),
        ("Precision Agriculture", "uses", "多旋翼无人机"),
        ("Shanghai", "part_of", "低空经济"),
        ("Beijing", "part_of", "低空经济"),
        ("Payload Capacity", "measures", "低空经济"),
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
    
    # Try to extract from PDFs (limited)
    pdf_dir = Path("/data1/xh/workspace/white-paper/docs/pdf")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    print(f"\nProcessing {len(pdf_files)} PDFs (first 3 pages each)...")
    
    all_text = ""
    for pdf_file in pdf_files:
        text = extract_from_pdf(str(pdf_file), max_pages=3)
        all_text += text + "\n"
    
    print(f"Extracted {len(all_text)} characters")
    
    # Use LLM to extract from combined text
    if len(all_text) > 1000:
        print("\nExtracting entities with LLM...")
        
        system_prompt = """Extract entities from the text about Low Altitude Economy.
Return JSON format:
{
  "entities": [
    {"name": "entity name", "type": "Company|Technology|Policy|Region", "description": "brief"}
  ]
}
Limit to 20 most important entities."""

        try:
            response = llm.generate(
                system_prompt=system_prompt,
                user_prompt=f"Text:\n{all_text[:3000]}",
                temperature=0.3
            )
            
            # Parse JSON
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            extraction = json.loads(json_str)
            
            for entity in extraction.get("entities", []):
                name = entity.get("name", "").strip()
                etype = entity.get("type", "Entity")
                desc = entity.get("description", "")
                if name and not graph_store.graph.has_node(name):
                    graph_store.graph.add_node(name, type=etype, description=desc)
                    added_e += 1
            
            print(f"✓ LLM extraction successful")
        except Exception as e:
            print(f"✗ LLM extraction failed: {e}")
    
    # Stats
    final_e = graph_store.graph.number_of_nodes()
    final_r = graph_store.graph.number_of_edges()
    
    print("\n" + "=" * 70)
    print("Results")
    print("=" * 70)
    print(f"Initial: {initial_e} entities, {initial_r} relations")
    print(f"Final:   {final_e} entities, {final_r} relations")
    print(f"Added:   {added_e} entities, {added_r} relations")
    
    # Save
    output = {
        "entities": [{"name": n, **d} for n, d in graph_store.graph.nodes(data=True)],
        "relationships": [{"source": s, "target": t, "relation": d.get("relation", "related")} 
                         for s, t, d in graph_store.graph.edges(data=True)]
    }
    
    output_file = Path("/data1/xh/workspace/white-paper/experiments/results/extracted_entities.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {output_file}")
    print("\nSample entities:")
    for node, data in list(graph_store.graph.nodes(data=True))[-10:]:
        print(f"  - {node} ({data.get('type', 'Unknown')})")


if __name__ == "__main__":
    main()
