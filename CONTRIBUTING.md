# Contributing to LAEV-Agents

Thank you for your interest in contributing to LAEV-Agents! This document provides guidelines and instructions for contributing to the project.

## 🎯 Ways to Contribute

- **🐛 Bug Reports**: Report issues you encounter
- **💡 Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve docs, add examples
- **🔧 Code Contributions**: Submit pull requests
- **🧪 Testing**: Add tests or help test new features

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/white-paper.git
cd white-paper
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r config/requirements.txt
pip install -r config/requirements-dev.txt  # Development dependencies

# Set up pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## 📝 Code Standards

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Use type hints
def process_query(query: str, max_iter: int = 3) -> Dict[str, Any]:
    """
    Process a user query and return visualization result.
    
    Args:
        query: Natural language query string
        max_iter: Maximum refinement iterations
        
    Returns:
        Dictionary containing visualization result and metadata
        
    Raises:
        ValueError: If query is empty or invalid
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    # ... implementation
```

### Key Rules

- **Line Length**: 100 characters maximum
- **Quotes**: Use double quotes for strings
- **Imports**: Group as stdlib, third-party, local
- **Docstrings**: Use Google style for all public functions
- **Type Hints**: Add type hints for function signatures

### Example

```python
"""
Module description.

This module provides functionality for X.
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime

import pandas as pd
from pyecharts.charts import Bar

from .base import BaseAgent


class MyAgent(BaseAgent):
    """
    Brief description of the agent.
    
    Longer description explaining the agent's purpose,
    key features, and usage examples.
    
    Attributes:
        name: Agent identifier
        config: Configuration dictionary
    
    Example:
        >>> agent = MyAgent("test")
        >>> result = agent.process("query")
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        """
        Initialize the agent.
        
        Args:
            name: Unique name for this agent instance
            config: Optional configuration dictionary
        """
        super().__init__(name)
        self.config = config or {}
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process a query.
        
        Args:
            query: Input query string
            
        Returns:
            Processing result dictionary
            
        Raises:
            ValueError: If query format is invalid
            RuntimeError: If processing fails
        """
        try:
            # Implementation
            return {"success": True, "data": None}
        except ValueError as e:
            self.logger.error(f"Invalid query: {e}")
            raise
        except Exception as e:
            self.logger.exception("Processing failed")
            raise RuntimeError(f"Processing failed: {e}") from e
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest python/tests/ -v

# Run specific test file
python -m pytest python/tests/test_knowledge_base.py -v

# Run with coverage
python -m pytest python/tests/ --cov=python/src --cov-report=html
```

### Writing Tests

```python
import pytest
from agents import LAEVOrchestrator


def test_orchestrator_basic_query():
    """Test orchestrator with simple query."""
    orchestrator = LAEVOrchestrator(use_full_agents=False)
    result = orchestrator.process("Show flight trends")
    
    assert result["success"] is True
    assert "chart_html" in result
    assert result["iterations"] >= 1
```

## 📝 Documentation

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: int, param2: str) -> bool:
    """
    Short description.
    
    Longer description if needed. Can span multiple lines
    and include detailed explanations.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is not a string
        
    Example:
        >>> function_name(1, "test")
        True
    """
```

### README Updates

When adding features, update:
- README.md (main features list)
- USAGE_GUIDE.md (if user-facing)
- AGENTS.md (if agent-related)

## 🔀 Submitting Changes

### 1. Before Committing

```bash
# Format code
black python/src/ --line-length 100

# Check imports
isort python/src/ --profile black

# Run tests
python -m pytest python/tests/ -v

# Type checking
mypy python/src/ --ignore-missing-imports
```

### 2. Commit Messages

Use conventional commits format:

```
feat: add new visualization type
fix: correct color scheme in dark mode
docs: update API documentation
test: add tests for evaluator agent
refactor: simplify orchestrator logic
perf: improve query processing speed
chore: update dependencies
```

### 3. Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Create PR** with clear description

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Step-by-step instructions
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: 
   - OS version
   - Python version
   - Dependencies versions
6. **Logs**: Relevant error messages or logs

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run '...'
2. Enter query '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 20.04
- Python: 3.10.0
- Version: v2.0.0

**Logs**
```
Error traceback here
```
```

## 💡 Feature Requests

When suggesting features:

1. **Use case**: Describe the problem you're trying to solve
2. **Proposed solution**: Your idea for implementation
3. **Alternatives**: Other approaches you've considered
4. **Additional context**: Mockups, examples, etc.

## 🏷️ Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## 📞 Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation first

## ⚖️ Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📚 Resources

- [Project README](README.md)
- [Usage Guide](USAGE_GUIDE.md)
- [Architecture Guide](AGENTS.md)
- [API Documentation](docs/api/)

---

Thank you for contributing to LAEV-Agents! 🎉
