"""
Extract entities and relationships from PDF white papers
for GraphRAG knowledge base expansion
"""

import os
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
        if start >= len(text):
            break
    return chunks


def extract_entities_from_chunk(chunk: str, llm_client) -> Dict[str, Any]:
    """
    Use LLM to extract entities and relationships from text chunk
    """
    system_prompt = """You are an expert in knowledge graph extraction.
Your task is to extract entities and relationships from text about Low Altitude Economy.

Extract the following types of entities:
- Aircraft types (e.g., multirotor drone, fixed-wing, helicopter, eVTOL)
- Companies/Enterprises (e.g., DJI, EHang, Xpeng, 亿航, 大疆)
- Technologies (e.g., autonomous flight, sense and avoid, UTM, BVLOS)
- Regulations/Policies (e.g., airworthiness certification, flight permits, 适航认证)
- Applications/Scenarios (e.g., aerial photography, cargo delivery, passenger transport, 物流配送, 载人飞行)
- Locations/Regions (e.g., Shenzhen, Shanghai, Beijing, 深圳, 上海)
- Metrics/Indicators (e.g., flight hours, payload capacity, safety rate, 飞行时长, 载重)

Output format (JSON):
{
    "entities": [
        {"name": "entity name", "type": "AircraftType|Company|Technology|Policy|Application|Region|Metric", "description": "brief description"}
    ],
    "relationships": [
        {"source": "entity1", "target": "entity2", "relation": "relationship type", "description": "context"}
    ]
}

Only include entities and relationships that are clearly mentioned in the text.
Respond with valid JSON only."""

    user_prompt = f"""Extract entities and relationships from the following text about Low Altitude Economy:

---
{chunk}
---

Provide your response in JSON format."""

    try:
        response = llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        # Try to parse JSON
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
        
        return json.loads(json_str)
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return {"entities": [], "relationships": []}


def merge_extractions(extractions: List[Dict]) -> Dict[str, Any]:
    """Merge multiple extraction results, removing duplicates"""
    all_entities = {}
    all_relationships = set()
    
    for extraction in extractions:
        # Merge entities (use name as key)
        for entity in extraction.get("entities", []):
            name = entity.get("name", "").strip()
            if name and len(name) > 1:
                if name not in all_entities:
                    all_entities[name] = entity
        
        # Merge relationships
        for rel in extraction.get("relationships", []):
            source = rel.get("source", "").strip()
            target = rel.get("target", "").strip()
            relation = rel.get("relation", "").strip()
            if source and target and relation:
                rel_key = (source, relation, target)
                all_relationships.add(rel_key)
    
    return {
        "entities": list(all_entities.values()),
        "relationships": [
            {"source": s, "relation": r, "target": t}
            for s, r, t in all_relationships
        ]
    }


def update_graph_store(extraction: Dict[str, Any], graph_store):
    """Update graph store with extracted entities and relationships"""
    added_entities = 0
    added_relations = 0
    
    # Add entities
    for entity in extraction.get("entities", []):
        name = entity.get("name", "")
        entity_type = entity.get("type", "Entity")
        description = entity.get("description", "")
        
        if name and not graph_store.graph.has_node(name):
            graph_store.graph.add_node(
                name,
                type=entity_type,
                description=description
            )
            added_entities += 1
    
    # Add relationships
    for rel in extraction.get("relationships", []):
        source = rel.get("source", "")
        target = rel.get("target", "")
        relation = rel.get("relation", "related")
        
        if source and target:
            # Add nodes if they don't exist
            if not graph_store.graph.has_node(source):
                graph_store.graph.add_node(source, type="Entity")
            if not graph_store.graph.has_node(target):
                graph_store.graph.add_node(target, type="Entity")
            
            # Add edge
            if not graph_store.graph.has_edge(source, target):
                graph_store.graph.add_edge(source, target, relation=relation)
                added_relations += 1
    
    return added_entities, added_relations


def main():
    """Main extraction workflow"""
    from llm_client import LLMClient
    from agents.graph_store import NetworkXGraphStore
    
    print("=" * 70)
    print("PDF Entity Extraction for GraphRAG")
    print("=" * 70)
    
    # Initialize
    print("\nInitializing...")
    llm = LLMClient(provider="deepseek")
    graph_store = NetworkXGraphStore()
    graph_store.initialize_lae_domain()
    
    initial_entities = graph_store.graph.number_of_nodes()
    initial_relations = graph_store.graph.number_of_edges()
    
    print(f"Initial graph: {initial_entities} entities, {initial_relations} relationships")
    
    # PDF files to process
    pdf_dir = Path("/data1/xh/workspace/white-paper/docs/pdf")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    print(f"\nFound {len(pdf_files)} PDF files")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf.name}")
    
    all_extractions = []
    total_chunks = 0
    
    # Process each PDF
    for pdf_idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'='*70}")
        print(f"Processing PDF {pdf_idx}/{len(pdf_files)}: {pdf_file.name}")
        print('='*70)
        
        # Extract text
        text = extract_text_from_pdf(str(pdf_file))
        if not text:
            print("  No text extracted, skipping...")
            continue
        
        print(f"  Extracted {len(text)} characters")
        
        # Chunk text (limit to first 10000 chars for speed)
        chunks = chunk_text(text[:10000])
        print(f"  Split into {len(chunks)} chunks")
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            print(f"    Chunk {i+1}/{len(chunks)}...", end=" ")
            extraction = extract_entities_from_chunk(chunk, llm)
            
            if extraction.get("entities"):
                all_extractions.append(extraction)
                total_chunks += 1
                print(f"✓ {len(extraction['entities'])} entities, {len(extraction['relationships'])} relations")
            else:
                print("✗ no entities found")
    
    # Merge all extractions
    print("\n" + "=" * 70)
    print("Merging and Updating Graph Store")
    print("=" * 70)
    
    merged = merge_extractions(all_extractions)
    print(f"Total unique entities: {len(merged['entities'])}")
    print(f"Total unique relationships: {len(merged['relationships'])}")
    
    # Update graph store
    added_e, added_r = update_graph_store(merged, graph_store)
    print(f"\nAdded to graph: {added_e} new entities, {added_r} new relations")
    
    # Save results
    output_dir = Path("/data1/xh/workspace/white-paper/experiments/results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "extracted_entities.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"\nSaved extraction to: {output_file}")
    
    # Print final stats
    final_entities = graph_store.graph.number_of_nodes()
    final_relations = graph_store.graph.number_of_edges()
    
    print("\n" + "=" * 70)
    print("Final Graph Statistics")
    print("=" * 70)
    print(f"Entities: {final_entities} (added {final_entities - initial_entities})")
    print(f"Relationships: {final_relations} (added {final_relations - initial_relations})")
    
    # Show sample new entities
    print("\nSample extracted entities:")
    for entity in merged.get("entities", [])[:15]:
        print(f"  - {entity.get('name')} ({entity.get('type')})")
    
    print("\n" + "=" * 70)
    print("Extraction Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
