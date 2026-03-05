# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Low Altitude Economy (LAE) Visualization Dashboard** with AI-powered analytics, dual-platform implementation, and a multi-agent system for intelligent visualization generation. It's being developed for IEEE VIS 2026 submission.

**Key Components:**
- Python Streamlit app (`python/`) with RAG and multi-agent visualization
- TypeScript React app (`web/`) for PDF reports and professional dashboards
- Multi-agent system (`python/src/agents/`) for NL2Vis generation
- Interactive demo (`demo/`) with Streamlit/Gradio interfaces
- Experimental framework (`experiments/`) for system evaluation

---

## Common Commands

### Python Streamlit Application

```bash
# Install dependencies
pip install -r config/requirements.txt

# Run the main application
python run_python_app.py
# OR manually: cd python && streamlit run src/app.py

# Run tests
cd python
python -m pytest tests/ -v
python tests/test_knowledge_base.py  # Run specific test

# RAG demo
python python/src/demo_rag.py
```

### Demo Application

```bash
cd demo
python run_demo.py  # Interactive launcher

# Direct launch
streamlit run app.py      # Streamlit interface
python app_gradio.py      # Gradio interface
```

### TypeScript/React Web Application

```bash
cd web
npm install
npm run dev      # Development server
npm run build    # Production build
```

### Docker Deployment

```bash
# Build Python app Docker image
cd python
docker build -t streamlit-rag-llm:latest .
docker run -p 8501:8501 -e DEEPSEEK_API_KEY=your_key streamlit-rag-llm:latest
```

---

## Environment Configuration

Copy `config/.env.example` to `.env` and configure:

```bash
# Default LLM provider (deepseek, openai, anthropic, local)
DEFAULT_LLM_PROVIDER=deepseek

# API keys (at least one required)
DEEPSEEK_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

**RAG Knowledge Base:** Automatically initializes on first run by indexing PDFs in `docs/pdf/`. Rebuild by deleting `chroma_db/` directory.

---

## High-Level Architecture

### Multi-Agent System (`python/src/agents/`)

The LAEV-Agents system uses a 5-agent pipeline for natural language to visualization:

1. **PlannerAgent**: Parses user query, analyzes intent, decomposes tasks
2. **RetrieverAgent**: Retrieves context via GraphRAG (Neo4j + Vector DB)
3. **CoderAgent**: Generates PyECharts code with multiple strategies (adaptive/conservative)
4. **EvaluatorAgent**: Multi-dimensional quality assessment (syntax, correctness, aesthetics)
5. **ReflectorAgent**: Iterative refinement and error recovery

**Usage:**
```python
from agents import LAEVOrchestrator

orchestrator = LAEVOrchestrator(
    llm_provider="deepseek",
    use_full_agents=True,  # Full or simplified mode
    max_iterations=3
)
result = orchestrator.process("Show flight trends over time")
```

**Agent Modes:**
- `use_full_agents=True`: Complete implementation with MLLM visual evaluation
- `use_full_agents=False`: Simplified version with heuristic evaluation (faster)

### RAG Knowledge Base (`python/src/knowledge_base.py`)

- Uses ChromaDB for vector storage
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Auto-indexes PDFs from `docs/pdf/`
- Persistent storage in `chroma_db/`

### GraphRAG (`python/src/agents/graph_store.py`)

Combines knowledge graph (Neo4j) with vector retrieval:
- 130+ domain entities and relationships
- Supports NetworkX (in-memory) and Neo4j (persistent) backends

### Dual Platform Consistency

Chart types must be implemented in both:
- Python: `python/src/charts.py` (PyECharts)
- TypeScript: `web/src/components/charts/Charts.tsx` (ECharts React)

Use warm colors (`#f59e0b`, `#ea580c`, etc.) for contrast with Klein blue theme (`#002FA7`).

---

## Key Data Structures

### Index Computation (21 Metrics)

See `INDEX_DEFINITIONS.md` for complete formulas:

**5 Core Dimensions:**
1. Scale & Growth: Traffic Index, Operation Intensity, Active Fleet, Growth Momentum
2. Structure & Entity: Market Concentration (CR50), Commercial Maturity, Diversity Index
3. Time & Space: Regional Balance (Gini), All-Time Operation (Entropy), Seasonal Stability, Hub Connectivity
4. Efficiency & Quality: Per-Aircraft Efficiency, Long-Endurance Ratio, Coverage, Task Completion Quality
5. Innovation & Integration: Micro-circulation, Airspace Utilization (Entropy), Production/Consumption Ratio, Night Economy, Leading Enterprise Index

**Comprehensive Prosperity Index (LA-PI):** Weighted aggregation (40% Scale, 20% Structure, 20% Innovation, 10% TimeSpace, 10% Efficiency)

### Flight Data Schema

Required columns for index computation:
- `date_str`: YYYY-MM-DD format
- `sn`: Aircraft serial number
- `duration`, `distance`, `altitude`: Numeric values
- `aircraft_type`, `aircraft_model`: Aircraft classification
- `entity`: Company/operator
- `user_type`: Enterprise/Individual/Government
- `region`, `start_region`, `end_region`: Geographic data
- `is_planned`, `is_effective`: Task completion flags

---

## Security Considerations

**Critical:** The system uses LLM-generated code execution. Always validate:

1. **Code Injection Prevention:** `validate_and_execute_chart_code()` in `llm_helper.py` uses AST parsing to block dangerous operations (eval, __import__, file I/O)

2. **Input Validation:**
   - File uploads: Max 10 MB, CSV max 100,000 rows
   - Path traversal: Use `pathlib.Path` with `.is_relative_to()`

3. **API Keys:** Always from environment variables, never hardcoded

4. **Dependencies:** All from trusted PyPI/npm sources

---

## Testing Strategy

### Unit Tests
```bash
cd python
python -m pytest tests/ -v
```

Test files:
- `test_knowledge_base.py`: RAG functionality
- `test_llm_rag_integration.py`: LLM + RAG integration
- `test_index_computation.py`: Index calculation

### Experiments

Run experimental comparisons:
```bash
cd experiments
python run_experiment.py --systems all              # All systems
python run_experiment.py --queries 5               # Quick test
python run_experiment.py --full-agents              # Full agent implementation
```

### Ablation Study

Test system variants:
- Full system (all agents)
- Without GraphRAG (vector only)
- Without Multi-Agent (single pass)
- Without Visual Evaluation

---

## Important File Locations

| Purpose | Location |
|---------|----------|
| Main Python app | `python/src/app.py` |
| Charts library | `python/src/charts.py` |
| LLM helper | `python/src/llm_helper.py` |
| LLM client | `python/src/utils/llm_client.py` |
| Knowledge base | `python/src/knowledge_base.py` |
| Multi-agent system | `python/src/agents/` |
| MLLM evaluators | `python/src/evaluators/` |
| Graph entity extraction | `python/src/graph/` |
| Demo app | `demo/app.py`, `demo/app_gradio.py` |
| React app | `web/src/App.tsx`, `web/src/components/charts/Charts.tsx` |
| PDFs for RAG | `docs/pdf/` |
| Vector DB cache | `chroma_db/` |
| Environment template | `config/.env.example` |
| Test queries | `experiments/data/test_queries.py` |
| Build scripts | `scripts/` |
| Documentation | `docs/`, `docs/guides/`, `docs/technical/` |

---

## Common Patterns

### Adding a New Chart Type

1. Python (`python/src/charts.py`):
   ```python
   def generate_new_chart(data: pd.DataFrame) -> str:
       # Use CHART_CONFIG and COLORS constants
       return pyecharts_option.to_dict()
   ```

2. TypeScript (`web/src/components/charts/Charts.tsx`):
   - Add to chart type union in `types.ts`
   - Implement ECharts option generation

### Adding a New LLM Provider

1. Add to `LLMProviderRegistry.PROVIDERS` in `python/src/llm_providers.py`
2. Update `.env.example` with new API key variable
3. Test with `python python/src/demo_rag.py`

### Troubleshooting Common Issues

- **RAG Knowledge Base Not Available:** `pip install -r config/requirements.txt` and delete `chroma_db/` to rebuild
- **Slow First Run:** Normal - downloads embedding model (~90MB) and processes PDFs. Subsequent runs load from cache.
- **Import Errors (agents):** Ensure parent project is installed: `cd python && pip install -e .`

---

## Documentation References

- `README.md`: Project overview and quick start
- `docs/technical/AGENTS.md`: AI coding agent guide
- `docs/guides/USAGE_GUIDE.md`: User-facing application guide
- `docs/technical/INDEX_DEFINITIONS.md`: Complete metric definitions with formulas
- `docs/technical/INSTALL.md`: Installation instructions
- `experiments/README.md`: Experimental framework guide
- `demo/README.md`: Demo application usage
- `docs/kimi/`: Technical documentation (RAG implementation, test reports, etc.)
- `docs/TODO.md`: IEEE VIS 2026 submission checklist (current branch: `ieee-vis`)
- `docs/CHANGELOG.md`: Project change log
