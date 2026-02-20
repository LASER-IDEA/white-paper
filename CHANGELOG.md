# Changelog

All notable changes to the LAEV-Agents project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Interactive web demo with Streamlit and Gradio interfaces
- Docker Compose configuration for easy deployment
- Comprehensive installation guide (INSTALL.md)
- Contributing guidelines (CONTRIBUTING.md)
- MIT License
- Development dependencies file (requirements-dev.txt)

### Changed
- Improved documentation coverage
- Enhanced .gitignore for better repository hygiene

## [2.2.0] - 2026-02-18

### Added
- MLLM visual evaluation comparison (local vs API)
- Knowledge graph schema visualization
- Paper readiness dashboard
- Experiment result visualization scripts

### Fixed
- COLOR_SCHEME bug in evaluator (fixed 3 failing queries)
- Success rate improved from 90.6% to 98.0%

### Changed
- Expanded test queries from 32 to 50
- Updated all LaTeX files with new data
- Synchronized figures between directories

## [2.1.0] - 2026-02-15

### Added
- Full comparison experiment with 50 queries
- Ablation study implementation
- Multi-provider LLM support (DeepSeek, OpenAI, Anthropic)
- Local Qwen2.5-VL-7B MLLM support

### Changed
- Enhanced orchestrator with progress callbacks
- Improved agent state management
- Updated evaluation metrics in paper

## [2.0.0] - 2026-02-14

### Added
- Multi-Agent Architecture (Planner, Retriever, Coder, Evaluator, Reflector)
- GraphRAG implementation with NetworkX
- Knowledge base with 130 entities and 71 relationships
- Visual quality evaluator with 4 dimensions
- Iterative refinement mechanism

### Changed
- Complete system redesign from single LLM to multi-agent
- Migrated from NL4DV-style to agent-based approach
- New PyECharts-based visualization generation

## [1.8.0] - 2026-02-10

### Added
- RAG (Retrieval-Augmented Generation) support
- ChromaDB vector database integration
- PDF document processing for knowledge base
- LangChain integration

### Changed
- Enhanced LLM helper with RAG context
- Improved response quality with retrieved context

## [1.5.0] - 2026-02-05

### Added
- Dual-platform implementation (Python + TypeScript)
- Streamlit-based Python application
- React-based TypeScript application
- GitHub Pages deployment workflow

### Changed
- Unified visualization library between platforms
- Consistent design language across implementations

## [1.0.0] - 2026-02-01

### Added
- Initial project setup
- Low Altitude Economy Development Index Dashboard
- 5 core dimensions: Scale, Structure, Space, Efficiency, Innovation
- 18 key metrics for LAE analysis
- ECharts visualization support
- Mock data generation system
- Basic AI integration with DeepSeek API

---

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```

## Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v2.2.0 | 2026-02-18 | 98% success rate, MLLM comparison |
| v2.1.0 | 2026-02-15 | 50 queries, ablation study |
| v2.0.0 | 2026-02-14 | Multi-agent architecture |
| v1.8.0 | 2026-02-10 | RAG support |
| v1.5.0 | 2026-02-05 | Dual-platform |
| v1.0.0 | 2026-02-01 | Initial release |

---

For detailed commit history, see [GitHub commits](https://github.com/LASER-IDEA/white-paper/commits/main).
