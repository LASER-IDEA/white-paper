import os
import re
from typing import List, Dict, Optional
from pathlib import Path

class Document:
    def __init__(self, content: str, source: str, section: str = ""):
        self.content = content
        self.source = source
        self.section = section

    def __repr__(self):
        return f"Document(source='{self.source}', section='{self.section}', content_len={len(self.content)})"

class KnowledgeBase:
    def __init__(self, doc_dir: str = "docs/latex/sections"):
        """
        Initialize the KnowledgeBase.

        Args:
            doc_dir: Path to the directory containing LaTeX section files.
                     Can be relative to project root or absolute.
        """
        # Resolve path relative to project root if it's relative
        project_root = Path(__file__).parent.parent.parent
        self.doc_dir = (project_root / doc_dir).resolve()

        if not self.doc_dir.exists():
            # Fallback for when running in different context or if path is different
            self.doc_dir = Path(doc_dir).resolve()

        self.documents: List[Document] = []
        self.load_documents()

    def load_documents(self):
        """Loads all .tex files from the document directory and chunks them."""
        if not self.doc_dir.exists():
            print(f"Warning: Document directory {self.doc_dir} does not exist.")
            return

        for file_path in self.doc_dir.glob("*.tex"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = self._chunk_content(content, file_path.name)
                    self.documents.extend(chunks)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

        print(f"Loaded {len(self.documents)} chunks from {self.doc_dir}")

    def _chunk_content(self, content: str, source: str) -> List[Document]:
        """
        Splits LaTeX content into chunks based on sections/subsections.
        Removes basic LaTeX formatting.
        """
        chunks = []

        # Simple regex to split by \section or \subsection
        # This is a naive implementation but sufficient for this task
        # We look for \section{...} or \subsection{...}

        # Split by \section or \subsection, keeping the delimiter
        # The regex looks for lines starting with \section or \subsection
        pattern = r'(\\section\{[^}]+\}|\\subsection\{[^}]+\})'
        parts = re.split(pattern, content)

        current_section = "Introduction"
        if parts:
            # First part is usually preamble or text before first section
            if parts[0].strip():
                clean_text = self._clean_latex(parts[0])
                if clean_text:
                    chunks.append(Document(clean_text, source, current_section))

            # Iterate through the rest
            for i in range(1, len(parts), 2):
                header = parts[i]
                body = parts[i+1] if i+1 < len(parts) else ""

                # Extract section title
                title_match = re.search(r'\\(sub)?section\{([^}]+)\}', header)
                if title_match:
                    current_section = title_match.group(2)

                full_text = header + "\n" + body
                clean_text = self._clean_latex(full_text)

                if clean_text:
                    chunks.append(Document(clean_text, source, current_section))

        return chunks

    def _clean_latex(self, text: str) -> str:
        """Removes common LaTeX commands to make text more readable for LLM."""
        # Remove comments
        text = re.sub(r'%.*', '', text)

        # Remove \newpage, \clearpage
        text = re.sub(r'\\(newpage|clearpage)', '', text)

        # Remove \cite{...} but maybe keep a marker? For now, remove.
        text = re.sub(r'\\cite\{[^}]+\}', '', text)

        # Remove \ref{...}
        text = re.sub(r'\\ref\{[^}]+\}', '', text)

        # Replace \textbf{...}, \textit{...} with just the content
        text = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', text)

        # Remove \begin{...} and \end{...} tags but keep content
        text = re.sub(r'\\(begin|end)\{[^}]+\}', '', text)

        # Remove \item
        text = re.sub(r'\\item', '-', text)

        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Search for documents relevant to the query.
        Since we don't have a vector store, we'll use a simple keyword/overlap score.
        For a small dataset, this is often "good enough".
        """
        if not self.documents:
            return []

        query_terms = set(query.lower().split())

        scores = []
        for doc in self.documents:
            doc_terms = set(doc.content.lower().split())
            # Jaccard similarity or simple intersection count
            intersection = query_terms.intersection(doc_terms)
            score = len(intersection)

            # Bonus for section title match
            if any(term in doc.section.lower() for term in query_terms):
                score += 2

            scores.append((doc, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return top_k docs, filtering out 0 scores if any
        results = [doc for doc, score in scores[:top_k] if score > 0]

        # If no results found (score 0), and query is generic, maybe return introduction?
        # Or just return nothing.
        # If the corpus is small, maybe return all relevant ones.

        # Fallback: if very few results, return top ones regardless of score,
        # assuming the user wants *some* context from the blue book.
        if not results and self.documents:
            return self.documents[:1] # Return at least one

        return results

    def get_all_content(self) -> str:
        """Returns all content concatenated."""
        return "\n\n".join([f"--- Section: {d.section} ---\n{d.content}" for d in self.documents])
