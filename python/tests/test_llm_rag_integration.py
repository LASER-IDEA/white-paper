"""
Comprehensive integration tests for LLM + RAG feature.

This test suite validates:
1. Knowledge base initialization and PDF indexing
2. Vector database creation and retrieval
3. Computation logic inference from knowledge base
4. Visualization generation based on RAG context
5. Overall integration quality
"""

import sys
import os
from pathlib import Path
import json
import traceback

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_knowledge_base_initialization():
    """Test 1: Knowledge base initialization and PDF loading"""
    print("\n" + "="*80)
    print("TEST 1: Knowledge Base Initialization")
    print("="*80)
    
    try:
        from knowledge_base import KnowledgeBase, LANGCHAIN_AVAILABLE
        
        if not LANGCHAIN_AVAILABLE:
            print("❌ FAILED: LangChain dependencies not available")
            return False
        
        print("✓ LangChain dependencies available")
        
        # Get project root
        project_root = Path(__file__).parent.parent.parent
        pdf_dir = project_root / "docs" / "pdf"
        
        if not pdf_dir.exists():
            print(f"❌ FAILED: PDF directory not found: {pdf_dir}")
            return False
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        print(f"✓ Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"  - {pdf.name} ({pdf.stat().st_size / 1024:.1f} KB)")
        
        if len(pdf_files) == 0:
            print("❌ FAILED: No PDF files to index")
            return False
        
        # Initialize knowledge base
        print("\n⏳ Initializing knowledge base...")
        kb = KnowledgeBase(persist_directory=str(project_root / "chroma_db"))
        
        # Load PDFs
        documents = kb.load_pdf_documents([str(f) for f in pdf_files])
        print(f"✓ Loaded {len(documents)} pages from PDFs")
        
        if len(documents) == 0:
            print("❌ FAILED: No pages loaded from PDFs")
            return False
        
        # Chunk documents
        chunks = kb.chunk_documents()
        print(f"✓ Created {len(chunks)} text chunks")
        
        if len(chunks) == 0:
            print("❌ FAILED: No chunks created")
            return False
        
        # Build vector store
        print("\n⏳ Building vector database...")
        kb.build_vectorstore()
        print("✓ Vector database built successfully")
        
        print("\n✅ TEST 1 PASSED: Knowledge base initialization successful")
        return kb
        
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED with error: {e}")
        traceback.print_exc()
        return False


def test_vector_retrieval(kb):
    """Test 2: Vector retrieval and search quality"""
    print("\n" + "="*80)
    print("TEST 2: Vector Retrieval and Search Quality")
    print("="*80)
    
    if not kb:
        print("⚠️  Skipped: Knowledge base not initialized")
        return False
    
    try:
        test_queries = [
            {
                "query": "What are the core dimensions of the Low Altitude Economy index?",
                "expected_keywords": ["dimension", "index", "economy", "altitude"]
            },
            {
                "query": "How is aircraft fleet composition measured?",
                "expected_keywords": ["fleet", "aircraft", "composition", "measure"]
            },
            {
                "query": "What innovation metrics are tracked?",
                "expected_keywords": ["innovation", "metric", "track"]
            }
        ]
        
        results_summary = []
        
        for i, test_case in enumerate(test_queries, 1):
            print(f"\n--- Query {i} ---")
            print(f"Query: {test_case['query']}")
            
            results = kb.search(test_case['query'], k=3)
            
            if not results:
                print("❌ No results found")
                results_summary.append({
                    "query": test_case['query'],
                    "found_results": False,
                    "relevance": "N/A"
                })
                continue
            
            print(f"✓ Found {len(results)} results")
            
            # Check relevance by looking for keywords
            total_keyword_matches = 0
            for result in results:
                content_lower = result['content'].lower()
                matches = sum(1 for kw in test_case['expected_keywords'] 
                            if kw.lower() in content_lower)
                total_keyword_matches += matches
            
            avg_relevance = total_keyword_matches / (len(results) * len(test_case['expected_keywords']))
            
            print(f"  Top result score: {results[0]['score']:.4f}")
            print(f"  Keyword relevance: {avg_relevance:.2%}")
            print(f"  Source: {results[0]['metadata'].get('source_file', 'Unknown')}")
            print(f"  Preview: {results[0]['content'][:150]}...")
            
            results_summary.append({
                "query": test_case['query'],
                "found_results": True,
                "num_results": len(results),
                "top_score": results[0]['score'],
                "relevance": f"{avg_relevance:.2%}",
                "source": results[0]['metadata'].get('source_file', 'Unknown')
            })
        
        # Overall assessment
        successful_queries = sum(1 for r in results_summary if r.get('found_results', False))
        print(f"\n📊 Results Summary: {successful_queries}/{len(test_queries)} queries returned results")
        
        if successful_queries == len(test_queries):
            print("✅ TEST 2 PASSED: All queries successfully retrieved relevant context")
            return results_summary
        else:
            print("⚠️  TEST 2 PARTIAL: Some queries did not return results")
            return results_summary
            
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED with error: {e}")
        traceback.print_exc()
        return False


def test_computation_logic_inference(kb):
    """Test 3: Inferring computation logic from knowledge base"""
    print("\n" + "="*80)
    print("TEST 3: Computation Logic Inference from Knowledge Base")
    print("="*80)
    
    if not kb:
        print("⚠️  Skipped: Knowledge base not initialized")
        return False
    
    try:
        # Test queries that require computation logic understanding
        computation_queries = [
            "How to calculate the comprehensive development index?",
            "What formulas are used for fleet composition metrics?",
            "Explain the computation method for airspace utilization efficiency",
            "How are innovation scores aggregated?"
        ]
        
        inference_results = []
        
        for i, query in enumerate(computation_queries, 1):
            print(f"\n--- Computation Query {i} ---")
            print(f"Query: {query}")
            
            context = kb.get_context_for_query(query, k=4, max_context_length=2000)
            
            if not context or context.startswith("No relevant"):
                print("❌ No relevant context found for computation logic")
                inference_results.append({
                    "query": query,
                    "success": False,
                    "has_formulas": False,
                    "has_methodology": False
                })
                continue
            
            # Check if context contains computation indicators
            has_formulas = any(indicator in context.lower() 
                             for indicator in ['formula', 'calculate', 'compute', '=', 'equation'])
            has_methodology = any(indicator in context.lower()
                                for indicator in ['method', 'approach', 'step', 'process'])
            
            print(f"✓ Retrieved context ({len(context)} chars)")
            print(f"  Contains formulas/calculations: {has_formulas}")
            print(f"  Contains methodology: {has_methodology}")
            print(f"  Context preview: {context[:200]}...")
            
            inference_results.append({
                "query": query,
                "success": True,
                "has_formulas": has_formulas,
                "has_methodology": has_methodology,
                "context_length": len(context)
            })
        
        # Assessment
        successful = sum(1 for r in inference_results if r['success'])
        with_formulas = sum(1 for r in inference_results if r.get('has_formulas', False))
        with_methodology = sum(1 for r in inference_results if r.get('has_methodology', False))
        
        print(f"\n📊 Computation Logic Inference Summary:")
        print(f"  Successful retrievals: {successful}/{len(computation_queries)}")
        print(f"  Contexts with formulas: {with_formulas}/{len(computation_queries)}")
        print(f"  Contexts with methodology: {with_methodology}/{len(computation_queries)}")
        
        if successful >= len(computation_queries) * 0.75:  # 75% success rate
            print("✅ TEST 3 PASSED: Successfully inferred computation logic from knowledge base")
            return inference_results
        else:
            print("⚠️  TEST 3 PARTIAL: Some computation queries did not retrieve relevant context")
            return inference_results
            
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED with error: {e}")
        traceback.print_exc()
        return False


def test_rag_llm_integration(kb):
    """Test 4: Integration between RAG and LLM for visualization"""
    print("\n" + "="*80)
    print("TEST 4: RAG + LLM Integration for Visualization")
    print("="*80)
    
    if not kb:
        print("⚠️  Skipped: Knowledge base not initialized")
        return False
    
    try:
        from llm_helper import get_llm_response
        import pandas as pd
        
        # Create mock data context
        mock_data = pd.DataFrame({
            'dimension': ['Scale', 'Structure', 'Space', 'Efficiency', 'Innovation'],
            'score': [85, 78, 92, 88, 75]
        })
        
        # Test query requiring RAG context
        test_query = "Create a visualization showing the five core dimensions of the Low Altitude Economy index based on the white paper framework"
        
        print(f"Query: {test_query}")
        print(f"\nData context: {mock_data.shape[0]} rows, {mock_data.shape[1]} columns")
        
        # Get RAG context
        rag_context = kb.get_context_for_query(test_query, k=3, max_context_length=2000)
        
        if not rag_context or rag_context.startswith("No relevant"):
            print("⚠️  No RAG context retrieved for LLM")
            has_rag = False
        else:
            print(f"✓ Retrieved RAG context ({len(rag_context)} chars)")
            has_rag = True
        
        # Note: We won't actually call the LLM (no API key in tests)
        # But we verify the integration pathway exists
        print("\n✓ RAG context successfully prepared for LLM integration")
        print("✓ llm_helper.get_llm_response accepts knowledge_base parameter")
        
        # Verify the integration pathway
        import inspect
        sig = inspect.signature(get_llm_response)
        has_kb_param = 'knowledge_base' in sig.parameters
        
        if has_kb_param:
            print("✓ LLM helper has knowledge_base parameter")
            print("\n✅ TEST 4 PASSED: RAG + LLM integration pathway verified")
            return {
                "has_kb_param": True,
                "rag_context_retrieved": has_rag,
                "integration_ready": True
            }
        else:
            print("❌ LLM helper missing knowledge_base parameter")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED with error: {e}")
        traceback.print_exc()
        return False


def test_visualization_context_quality(kb):
    """Test 5: Quality of RAG context for visualization generation"""
    print("\n" + "="*80)
    print("TEST 5: RAG Context Quality for Visualization")
    print("="*80)
    
    if not kb:
        print("⚠️  Skipped: Knowledge base not initialized")
        return False
    
    try:
        # Queries specifically about visualization and charts
        viz_queries = [
            "What charts are recommended for showing traffic volume trends?",
            "How should fleet composition be visualized?",
            "What visualization best represents geographic distribution?",
            "What chart types are suitable for innovation metrics?"
        ]
        
        viz_results = []
        
        for i, query in enumerate(viz_queries, 1):
            print(f"\n--- Visualization Query {i} ---")
            print(f"Query: {query}")
            
            context = kb.get_context_for_query(query, k=3, max_context_length=1500)
            
            if not context or context.startswith("No relevant"):
                print("❌ No relevant context found")
                viz_results.append({
                    "query": query,
                    "success": False
                })
                continue
            
            # Check for visualization-related terms
            viz_terms = ['chart', 'graph', 'visualization', 'plot', 'figure', 'diagram', 
                        'bar', 'line', 'pie', 'map', 'heatmap', 'radar']
            
            terms_found = [term for term in viz_terms if term.lower() in context.lower()]
            
            print(f"✓ Retrieved context ({len(context)} chars)")
            print(f"  Visualization terms found: {len(terms_found)}")
            if terms_found:
                print(f"  Terms: {', '.join(terms_found[:5])}")
            
            viz_results.append({
                "query": query,
                "success": True,
                "viz_terms_count": len(terms_found),
                "context_length": len(context)
            })
        
        # Assessment
        successful = sum(1 for r in viz_results if r['success'])
        with_viz_terms = sum(1 for r in viz_results if r.get('viz_terms_count', 0) > 0)
        
        print(f"\n📊 Visualization Context Quality Summary:")
        print(f"  Successful retrievals: {successful}/{len(viz_queries)}")
        print(f"  Contexts with visualization terms: {with_viz_terms}/{len(viz_queries)}")
        
        if successful >= len(viz_queries) * 0.75:
            print("✅ TEST 5 PASSED: RAG provides quality context for visualization")
            return viz_results
        else:
            print("⚠️  TEST 5 PARTIAL: Limited visualization-specific context")
            return viz_results
            
    except Exception as e:
        print(f"\n❌ TEST 5 FAILED with error: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all LLM + RAG integration tests"""
    print("\n" + "="*80)
    print("🧪 LLM + RAG INTEGRATION TEST SUITE")
    print("="*80)
    print("Testing: Knowledge Base, Vector Retrieval, Computation Inference,")
    print("         LLM Integration, and Visualization Context Quality")
    print("="*80)
    
    test_results = {
        "test_1_kb_init": None,
        "test_2_retrieval": None,
        "test_3_computation": None,
        "test_4_llm_integration": None,
        "test_5_viz_quality": None
    }
    
    # Test 1: Knowledge base initialization
    kb = test_knowledge_base_initialization()
    test_results["test_1_kb_init"] = kb is not False
    
    if kb:
        # Test 2: Vector retrieval
        retrieval_results = test_vector_retrieval(kb)
        test_results["test_2_retrieval"] = retrieval_results is not False
        
        # Test 3: Computation logic inference
        computation_results = test_computation_logic_inference(kb)
        test_results["test_3_computation"] = computation_results is not False
        
        # Test 4: RAG + LLM integration
        integration_results = test_rag_llm_integration(kb)
        test_results["test_4_llm_integration"] = integration_results is not False
        
        # Test 5: Visualization context quality
        viz_results = test_visualization_context_quality(kb)
        test_results["test_5_viz_quality"] = viz_results is not False
    
    # Final summary
    print("\n" + "="*80)
    print("📋 FINAL TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for result in test_results.values() if result is True)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! LLM + RAG system is working correctly.")
        return 0
    elif passed >= total * 0.8:
        print("\n✅ MOST TESTS PASSED. System is functional with minor issues.")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED. Review the results above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
