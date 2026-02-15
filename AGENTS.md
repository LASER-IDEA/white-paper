# AGENTS.md - AI Coding Agent Guide

This file provides essential information for AI coding agents working on the **Low Altitude Economy Development Index Dashboard** project.

---

## Project Overview

This is a dual-platform dashboard for analyzing and visualizing China's Low Altitude Economy (LAE) development metrics. The project combines:

- **Python Streamlit Application** (`python/`): Interactive data exploration with AI-powered analysis
- **TypeScript React Application** (`web/`): Professional reporting with PDF export capabilities

**Key Features:**
- 5 Core Dimensions: Scale, Structure, Space, Efficiency, Innovation
- 18 Key Metrics with interactive visualizations
- AI-Powered Analysis with RAG (Retrieval-Augmented Generation)
- RAG Knowledge Base using ChromaDB and LangChain
- Multi-provider LLM support (DeepSeek, OpenAI, Anthropic, Local)

**Language:** Mixed (English code, Chinese UI/content)

---

## Technology Stack

### Python Backend
- **Framework**: Streamlit 1.28+
- **Visualization**: PyECharts, streamlit-echarts
- **Data Processing**: pandas, numpy, scipy
- **AI/RAG**: langchain, langchain-community, chromadb, sentence-transformers, openai
- **PDF Processing**: pypdf
- **Environment**: python-dotenv

### TypeScript Frontend
- **Framework**: React 19+, TypeScript 5.8+
- **Build Tool**: Vite 6.2+
- **Visualization**: ECharts 5.6+, echarts-gl, recharts
- **PDF Export**: html2pdf.js
- **Styling**: Tailwind CSS (via CDN in index.html)

### Infrastructure
- **CI/CD**: GitHub Actions
- **Deployment**: GitHub Pages (web), Streamlit Community Cloud/Docker (Python)
- **Containerization**: Docker with multi-stage builds
- **PDF Generation**: Playwright + Express.js

---

## Project Structure

```
white-paper/
├── python/                          # Python Streamlit Application
│   ├── src/
│   │   ├── app.py                  # Main Streamlit entry point
│   │   ├── charts.py               # PyEcharts visualization library
│   │   ├── data_factory.py         # Mock data generation (模拟数据生成)
│   │   ├── data_processor.py       # Data processing utilities
│   │   ├── llm_helper.py           # AI integration with RAG support
│   │   ├── llm_providers.py        # Multi-provider LLM registry
│   │   ├── knowledge_base.py       # RAG vector database module
│   │   ├── demo_rag.py             # RAG demonstration script
│   │   └── utils/
│   │       ├── generate_mock_csv.py
│   │       └── logger.py           # Structured logging utility
│   ├── data/                       # Sample datasets
│   │   ├── sample_flight_data.csv
│   │   └── shenzhen.json
│   ├── tests/                      # Unit and integration tests
│   │   ├── test.py                 # Basic chart tests
│   │   ├── test_knowledge_base.py  # RAG tests
│   │   ├── test_llm_rag_integration.py
│   │   └── test_index_computation.py
│   ├── Dockerfile                  # Multi-stage Docker build
│   └── README.md
│
├── web/                            # TypeScript React Application
│   ├── src/
│   │   ├── App.tsx                 # Main React component
│   │   ├── index.tsx               # Entry point
│   │   ├── types.ts                # TypeScript type definitions
│   │   ├── components/
│   │   │   ├── ReportPage.tsx      # Report page layout
│   │   │   ├── BackToTop.tsx       # UI utility component
│   │   │   └── charts/
│   │   │       └── Charts.tsx      # ECharts React components
│   │   └── utils/
│   │       └── mockData.ts         # Mock data utilities
│   ├── public/
│   │   └── data/
│   │       └── shenzhen.json       # Geographic data
│   ├── index.html                  # HTML template with Tailwind CDN
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts              # Vite configuration with base path
│
├── config/                         # Configuration files
│   ├── requirements.txt            # Python dependencies
│   ├── requirements-rag.txt        # RAG-specific dependencies
│   └── .env.example                # Environment template
│
├── docs/                           # Documentation and PDFs
│   ├── pdf/                        # White papers for RAG
│   │   ├── Low-Altitude Economy White Paper.pdf
│   │   ├── scale_growth_report.pdf
│   │   ├── structure_entity_report.pdf
│   │   ├── time_space_report.pdf
│   │   ├── efficiency_quality_report.pdf
│   │   └── innovation_integration_report.pdf
│   └── figures/                    # Generated chart exports
│
├── scripts/                        # Build and automation scripts
│   └── generate-pdfs.js            # PDF generation using Playwright
│
├── .github/workflows/              # CI/CD pipelines
│   ├── deploy.yml                  # Deploy React app to GitHub Pages
│   ├── deploy-streamlit.yml        # Build and validate Streamlit Docker
│   ├── main.yml                    # Auto-update contributors
│   └── build-and-merge-pdfs.yml    # PDF generation workflow
│
├── run_python_app.py               # Convenience script to run Python app
├── run_web_app.py                  # Convenience script to run web app
└── AGENTS.md                       # This file
```

---

## Build and Run Commands

### Python Streamlit Application

**Prerequisites:** Python 3.8+

```bash
# Install dependencies
pip install -r config/requirements.txt

# Run the application
python run_python_app.py
# OR manually:
cd python && streamlit run src/app.py

# Run tests
cd python && python -m pytest tests/
# OR run specific test:
cd python && python tests/test_knowledge_base.py
```

**Environment Setup:**
```bash
# Copy environment template
cp config/.env.example .env

# Edit .env with your API keys (for AI features)
# DEEPSEEK_API_KEY=your_key_here
```

### TypeScript React Application

**Prerequisites:** Node.js 16+, npm or yarn

```bash
# Using convenience script
python run_web_app.py

# Manual approach
cd web
npm install
npm run dev      # Development server on port 3000
npm run build    # Production build to dist/
npm run preview  # Preview production build
```

### Docker Deployment

```bash
# Build Docker image (from python/ directory)
cd python
docker build -t streamlit-rag-llm:latest .

# Run container
docker run -p 8501:8501 \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  streamlit-rag-llm:latest
```

### PDF Generation

```bash
# Generate PDF reports from web app
npm run generate-pdfs
# OR manually:
node scripts/generate-pdfs.js
```

---

## Code Style Guidelines

### Python

- **Type Hints**: Use type annotations for function signatures
  ```python
  def get_llm_response(
      query: str, 
      data_context: DataType, 
      api_key: Optional[str] = None
  ) -> Tuple[str, Optional[str]]:
  ```

- **Docstrings**: Use Google-style docstrings
  ```python
  """
  Brief description of function.
  
  Args:
      param1: Description
      param2: Description
      
  Returns:
      Description of return value
      
  Raises:
      ExceptionType: When/why raised
  """
  ```

- **Imports**: Group imports (stdlib, third-party, local)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Security**: Never use eval/exec without validation (see `validate_and_execute_chart_code()`)

### TypeScript

- **Types**: Always define interfaces in `types.ts`
- **Components**: Use functional components with explicit props types
  ```typescript
  interface ComponentProps {
    data: MetricData;
    pageNumber: number;
  }
  
  const Component: React.FC<ComponentProps> = ({ data, pageNumber }) => {
    // ...
  };
  ```

- **Naming**: PascalCase for components/interfaces, camelCase for functions/variables
- **Exports**: Prefer named exports for utilities, default exports for components

---

## Testing Instructions

### Python Tests

```bash
cd python

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python tests/test_knowledge_base.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

**Test Files:**
- `test.py`: Basic chart rendering tests
- `test_knowledge_base.py`: RAG functionality tests
- `test_llm_rag_integration.py`: LLM + RAG integration tests
- `test_index_computation.py`: Index calculation tests

### Manual Testing

**RAG Demo:**
```bash
cd python
python src/demo_rag.py
```

**Web App Visual Testing:**
```bash
cd web
npm run dev
# Open http://localhost:3000
```

---

## Security Considerations

### Critical Security Measures

1. **Code Injection Prevention**
   - AI-generated code is validated using AST parsing (`validate_and_execute_chart_code()`)
   - Dangerous operations (eval, __import__, file operations) are blocked
   - Only safe imports allowed: pyecharts, pandas, numpy, datetime, math

2. **Input Validation**
   - File uploads: Max 10 MB, CSV max 100,000 rows
   - File type validation for CSV/JSON
   - Path traversal prevention using `pathlib.Path` and `.is_relative_to()`

3. **API Key Security**
   - Keys stored in `.env` (never commit to version control)
   - Masked in UI using `type="password"`
   - Use environment variables for all sensitive configuration

4. **Command Injection Prevention**
   - Use `spawnSync(array)` instead of `execSync(string)` for subprocess calls

### Security Checklist for New Features

- [ ] All user inputs validated
- [ ] File operations use safe path handling
- [ ] No dangerous functions (eval/exec) without validation
- [ ] Dependencies from trusted sources (PyPI/npm)
- [ ] Secrets not hardcoded
- [ ] Error messages don't leak sensitive information

---

## Key Modules Reference

### LLM Providers (`python/src/llm_providers.py`)

Registry for multiple LLM providers:
- `deepseek`: deepseek-chat, deepseek-reasoner
- `openai`: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- `anthropic`: claude-3-opus, claude-3-sonnet, claude-3-haiku
- `local`: llama3, mistral, codellama (via Ollama)

Usage:
```python
from llm_providers import LLMProviderRegistry, get_default_provider

# Get available providers
available = LLMProviderRegistry.get_available_providers()

# Get API key for provider
api_key = LLMProviderRegistry.get_api_key('deepseek')
```

### Knowledge Base (`python/src/knowledge_base.py`)

RAG implementation using ChromaDB:
- Auto-loads PDFs from `docs/pdf/`
- Uses HuggingFace embeddings (all-MiniLM-L6-v2)
- Persistent vector storage in `chroma_db/`

Usage:
```python
from knowledge_base import initialize_knowledge_base

kb = initialize_knowledge_base()
context = kb.get_context_for_query(query, k=3)
```

### Charts (`python/src/charts.py` & `web/src/components/charts/Charts.tsx`)

Chart type mappings (Python ↔ TypeScript):
- Area charts, Line charts, Bar charts
- Maps (geo-heatmap), Polar charts
- Radar, Gauge, Funnel, Calendar, TreeMap
- Box plots, Histograms, Chord diagrams

**Note:** Color scheme uses warm colors (`#f59e0b`, `#ea580c`, etc.) for contrast with Klein blue theme (`#002FA7`).

---

## Deployment Process

### Web App (GitHub Pages)

1. Push to `main` branch triggers `.github/workflows/deploy.yml`
2. Builds with `base: '/white-paper/'` in vite.config.ts
3. Deploys `web/dist/` to GitHub Pages
4. Live at: https://LASER-IDEA.github.io/white-paper/

### Streamlit App (Docker)

1. Push to `main` triggers `.github/workflows/deploy-streamlit.yml`
2. Validates Python app compilation
3. Builds Docker image with multi-stage build
4. Output: `streamlit-rag-llm:latest` image

### PDF Generation

1. Trigger workflow or run locally: `npm run generate-pdfs`
2. Temporarily modifies vite.config.ts (base: '/')
3. Builds web app, serves locally, generates PDFs with Playwright
4. Outputs to `docs/pdf/` directory

---

## Common Development Tasks

### Adding a New Chart Type

1. **Python**: Add function in `python/src/charts.py`
   - Follow existing pattern with type hints
   - Use `CHART_CONFIG` and `COLORS` constants
   - Handle empty data gracefully

2. **TypeScript**: Add component in `web/src/components/charts/Charts.tsx`
   - Add to chart type union in `types.ts`
   - Implement ECharts option generation
   - Ensure responsive sizing

3. **Update**: Add mock data in `data_factory.py` and `mockData.ts`

### Adding a New LLM Provider

1. Add provider config to `LLMProviderRegistry.PROVIDERS` in `llm_providers.py`
2. Update `.env.example` with new API key variables
3. Test with `python/src/demo_rag.py`

### Adding PDF Documents to RAG

1. Add PDF files to `docs/pdf/` directory
2. Delete `chroma_db/` folder to force rebuild
3. Restart application - will auto-index new documents

---

## Environment Variables

Copy `config/.env.example` to `.env` and configure:

```bash
# Default Provider Selection
DEFAULT_LLM_PROVIDER=deepseek  # Options: deepseek, openai, anthropic, local

# DeepSeek
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic
ANTHROPIC_API_KEY=your_key_here

# Local (Ollama)
LOCAL_BASE_URL=http://localhost:11434/v1
```

---

## Troubleshooting

**RAG Knowledge Base Not Available:**
```bash
pip install -r config/requirements.txt
# Delete chroma_db/ and restart to rebuild
```

**Slow First Run:**
- Normal - downloads embedding model (~90MB)
- Subsequent runs load from cache instantly

**Docker Build Fails (Disk Space):**
- Uses batched requirements installation
- Check `python/Dockerfile` for multi-stage build

**Web App Shows Blank Page:**
- Check browser console for 404 errors
- Verify `base` path in vite.config.ts matches deployment path

---

## Documentation References

- `README.md` - Project overview and quick start
- `USAGE_GUIDE.md` - User-facing application guide
- `RAG_IMPLEMENTATION.md` - RAG technical details
- `IMPROVEMENTS.md` - Latest enhancements
- `TEST_REPORT.md` - Testing results
- `SECURITY.md` - Security best practices
- `INDEX_DEFINITIONS.md` - Metric definitions

---

**Last Updated:** February 2026
**Version:** 2.0.0
