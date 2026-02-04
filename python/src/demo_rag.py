"""
Demonstration script for the RAG Knowledge Base.

This script shows how to use the knowledge base independently of the Streamlit app.
It's useful for testing and debugging the RAG functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from knowledge_base import KnowledgeBase, LANGCHAIN_AVAILABLE
    
    if not LANGCHAIN_AVAILABLE:
        print("❌ LangChain dependencies not installed.")
        print("\nTo use the RAG knowledge base, install dependencies:")
        print("  pip install langchain langchain-community chromadb pypdf sentence-transformers")
        sys.exit(1)
    
    print("=" * 80)
    print("RAG Knowledge Base Demonstration")
    print("=" * 80)
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    pdf_dir = project_root / "docs" / "pdf"
    
    print(f"\nPDF Directory: {pdf_dir}")
    print(f"Vector DB: {project_root / 'chroma_db'}")
    
    # Check for PDF files
    pdf_files = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []
    print(f"\nFound {len(pdf_files)} PDF files:")
    for pdf in pdf_files[:5]:  # Show first 5
        print(f"  - {pdf.name}")
    if len(pdf_files) > 5:
        print(f"  ... and {len(pdf_files) - 5} more")
    
    if not pdf_files:
        print("\n⚠️  No PDF files found. Knowledge base will be empty.")
        sys.exit(0)
    
    # Initialize knowledge base
    print("\n" + "-" * 80)
    print("Initializing Knowledge Base...")
    print("-" * 80)
    
    kb = KnowledgeBase(persist_directory=str(project_root / "chroma_db"))
    
    # Load PDFs
    print("\nLoading PDF documents...")
    documents = kb.load_pdf_documents([str(f) for f in pdf_files])
    print(f"Loaded {len(documents)} pages total")
    
    # Chunk documents
    print("\nChunking documents...")
    chunks = kb.chunk_documents()
    print(f"Created {len(chunks)} chunks")
    
    # Build vector store
    print("\nBuilding vector database...")
    kb.build_vectorstore()
    print("✅ Vector database ready!")
    
    # Test queries
    print("\n" + "=" * 80)
    print("Testing RAG Retrieval")
    print("=" * 80)
    
    test_queries = [
        "What are the main dimensions of the Low Altitude Economy index?",
        "How is aircraft fleet composition measured?",
        "What metrics are used for innovation and integration?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 80)
        
        results = kb.search(query, k=2)
        
        if results:
            for j, result in enumerate(results, 1):
                source = result['metadata'].get('source_file', 'Unknown')
                page = result['metadata'].get('page', 'N/A')
                score = result['score']
                content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                
                print(f"\n  Result {j}:")
                print(f"    Source: {source}, Page: {page}")
                print(f"    Similarity Score: {score:.4f}")
                print(f"    Content: {content_preview}")
        else:
            print("  No results found")
    
    # Test context generation
    print("\n" + "=" * 80)
    print("Testing Context Generation")
    print("=" * 80)
    
    query = "Explain the five core dimensions of the index"
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    context = kb.get_context_for_query(query, k=3, max_context_length=1000)
    print("\nGenerated Context:")
    print(context[:800] + "..." if len(context) > 800 else context)
    
    print("\n" + "=" * 80)
    print("✅ RAG Knowledge Base demonstration complete!")
    print("=" * 80)
    
    print("\nNext steps:")
    print("  1. Run the Streamlit app: streamlit run src/app.py")
    print("  2. Go to the 'AI Assistant' tab")
    print("  3. Ask questions - responses will be enhanced with document context")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure you're running this from the python directory:")
    print("  cd python")
    print("  python src/demo_rag.py")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
