"""
Unit tests for the knowledge_base module.
"""

import unittest
import sys
from pathlib import Path
import ast

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestKnowledgeBaseModuleStructure(unittest.TestCase):
    """Test the knowledge base module structure without importing it."""
    
    def test_module_exists(self):
        """Test that knowledge_base.py file exists."""
        kb_path = Path(__file__).parent.parent / "src" / "knowledge_base.py"
        self.assertTrue(kb_path.exists(), "knowledge_base.py should exist")
    
    def test_module_has_required_classes(self):
        """Test that the module has required classes and functions."""
        kb_path = Path(__file__).parent.parent / "src" / "knowledge_base.py"
        with open(kb_path, 'r') as f:
            tree = ast.parse(f.read())
        
        # Check for classes
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        self.assertIn('KnowledgeBase', classes, "Should have KnowledgeBase class")
        
        # Check for functions
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        self.assertIn('initialize_knowledge_base', functions, 
                     "Should have initialize_knowledge_base function")
        self.assertIn('test_knowledge_base', functions,
                     "Should have test_knowledge_base function")


class TestLLMHelperIntegration(unittest.TestCase):
    """Test llm_helper integration with knowledge base."""
    
    def test_llm_helper_has_kb_parameter(self):
        """Test that get_llm_response accepts knowledge_base parameter."""
        llm_path = Path(__file__).parent.parent / "src" / "llm_helper.py"
        with open(llm_path, 'r') as f:
            tree = ast.parse(f.read())
        
        # Find get_llm_response function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'get_llm_response':
                args = [arg.arg for arg in node.args.args]
                self.assertIn('knowledge_base', args,
                            "get_llm_response should have knowledge_base parameter")
                return
        
        self.fail("get_llm_response function not found")


class TestAppIntegration(unittest.TestCase):
    """Test app.py integration with knowledge base."""
    
    def test_app_imports_knowledge_base(self):
        """Test that app.py imports knowledge_base module."""
        app_path = Path(__file__).parent.parent / "src" / "app.py"
        with open(app_path, 'r') as f:
            content = f.read()
        
        self.assertIn('import knowledge_base', content,
                     "app.py should import knowledge_base")
        self.assertIn('KNOWLEDGE_BASE_AVAILABLE', content,
                     "app.py should check for knowledge base availability")
        self.assertIn('st.session_state.kb', content,
                     "app.py should store kb in session state")
    
    def test_app_passes_kb_to_llm_helper(self):
        """Test that app.py passes kb to llm_helper."""
        app_path = Path(__file__).parent.parent / "src" / "app.py"
        with open(app_path, 'r') as f:
            content = f.read()
        
        self.assertIn('knowledge_base=st.session_state.kb', content,
                     "app.py should pass kb to llm_helper")


class TestRequirements(unittest.TestCase):
    """Test that requirements are properly defined."""
    
    def test_main_requirements_has_rag_deps(self):
        """Test that main requirements.txt includes RAG dependencies."""
        req_path = Path(__file__).parent.parent.parent / "config" / "requirements.txt"
        with open(req_path, 'r') as f:
            content = f.read()
        
        required_packages = ['langchain', 'chromadb', 'pypdf', 'sentence-transformers']
        for package in required_packages:
            self.assertIn(package, content,
                        f"requirements.txt should include {package}")
    
    def test_separate_rag_requirements_exists(self):
        """Test that separate RAG requirements file exists."""
        rag_req_path = Path(__file__).parent.parent.parent / "config" / "requirements-rag.txt"
        self.assertTrue(rag_req_path.exists(),
                       "requirements-rag.txt should exist for optional install")


if __name__ == '__main__':
    print("Running knowledge base tests...")
    print("-" * 80)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
        if result.failures:
            print(f"\nFailures: {len(result.failures)}")
        if result.errors:
            print(f"Errors: {len(result.errors)}")
    print("=" * 80)
    
    sys.exit(0 if result.wasSuccessful() else 1)
