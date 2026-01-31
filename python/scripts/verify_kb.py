import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from knowledge_base import KnowledgeBase

def main():
    print("Testing KnowledgeBase...")

    # Initialize KB
    kb = KnowledgeBase()

    print(f"Loaded {len(kb.documents)} document chunks.")

    # Print first few docs to check parsing
    for i, doc in enumerate(kb.documents[:2]):
        print(f"\n--- Document {i} ---")
        print(f"Section: {doc.section}")
        print(f"Source: {doc.source}")
        print(f"Content Preview: {doc.content[:100]}...")

    # Test search
    query = "index calculation"
    print(f"\nSearching for '{query}'...")
    results = kb.search(query)

    print(f"Found {len(results)} results.")
    for res in results:
        print(f"- From {res.section}: {res.content[:50]}...")

    # Test another query
    query = "Innovation"
    print(f"\nSearching for '{query}'...")
    results = kb.search(query)
    print(f"Found {len(results)} results.")
    for res in results:
        print(f"- From {res.section}: {res.content[:50]}...")

if __name__ == "__main__":
    main()
