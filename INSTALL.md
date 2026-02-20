# Installation Guide

Complete installation guide for LAEV-Agents.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
- [Development Setup](#development-setup)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)

## 💻 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows 10/11
- **Python**: 3.10 or higher
- **RAM**: 8GB (16GB recommended)
- **Disk**: 5GB free space
- **Network**: Internet connection for API calls

### Optional (for Local MLLM)
- **GPU**: NVIDIA GPU with 16GB+ VRAM (for local Qwen2.5-VL)
- **CUDA**: 11.8 or higher

## 🚀 Quick Install

### Option 1: Using Conda (Recommended)

```bash
# Clone repository
git clone https://github.com/LASER-IDEA/white-paper.git
cd white-paper

# Create conda environment
conda create -n laev python=3.10 -y
conda activate laev

# Install dependencies
pip install -r config/requirements.txt

# Set up environment variables
cp config/.env.example .env
# Edit .env with your API keys

# Run the application
python run_python_app.py
```

### Option 2: Using venv

```bash
# Clone repository
git clone https://github.com/LASER-IDEA/white-paper.git
cd white-paper

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r config/requirements.txt

# Set up environment
cp config/.env.example .env
# Edit .env file

# Run application
streamlit run python/src/app.py
```

## 📦 Detailed Installation

### 1. Clone Repository

```bash
git clone https://github.com/LASER-IDEA/white-paper.git
cd white-paper
```

### 2. Set Up Python Environment

#### Using Conda (Recommended for data science)

```bash
conda create -n laev python=3.10
conda activate laev
```

#### Using venv (Standard Python)

```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

#### Core Dependencies

```bash
pip install -r config/requirements.txt
```

#### Development Dependencies (Optional)

```bash
pip install -r config/requirements-dev.txt
```

#### For RAG Features

```bash
pip install -r config/requirements-rag.txt
```

#### For Local MLLM (Optional)

```bash
pip install torch transformers accelerate
```

### 4. Configure Environment Variables

```bash
# Copy template
cp config/.env.example .env

# Edit .env file with your favorite editor
nano .env  # or vim, code, etc.
```

Required variables:

```bash
# LLM API Keys (at least one required)
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: For Aliyun Qwen MLLM
QWEN_API_KEY=your_qwen_key_here

# Optional: Hugging Face (for local models)
HUGGINGFACE_TOKEN=your_hf_token_here
```

### 5. Initialize Knowledge Base (for RAG)

The knowledge base initializes automatically on first run. To manually rebuild:

```bash
# Delete existing database
rm -rf chroma_db/

# Run initialization
python python/src/demo_rag.py
```

### 6. Verify Installation

```bash
# Run tests
python -m pytest python/tests/ -v

# Run quick demo
python demo/run_demo.py
```

## 🔧 Development Setup

### 1. Install Development Tools

```bash
pip install -r config/requirements-dev.txt
```

### 2. Set Up Pre-commit Hooks

```bash
pre-commit install
```

### 3. Configure IDE

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### 4. Running in Development Mode

```bash
# Python app with auto-reload
streamlit run python/src/app.py --server.runOnSave true

# Or use convenience script
python run_python_app.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t laev-agents:latest ./python

# Run container
docker run -p 8501:8501 \
  -e DEEPSEEK_API_KEY=your_key \
  -v $(pwd)/.env:/app/.env \
  laev-agents:latest
```

### Docker Compose Configuration

See `docker-compose.yml` for:
- Streamlit web interface
- ChromaDB vector database
- Redis cache (optional)
- Nginx reverse proxy (optional)

## 🎯 Platform-Specific Instructions

### Ubuntu/Debian

```bash
# Install Python 3.10
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Install system dependencies
sudo apt install build-essential libffi-dev

# Continue with Quick Install
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Continue with Quick Install
```

### Windows

```powershell
# Install Python from Microsoft Store or python.org
# Enable Windows Subsystem for Linux (recommended)
wsl --install

# Then follow Ubuntu instructions inside WSL
```

## 🌐 Web Application Setup

### TypeScript/React Version

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🧪 Testing Installation

### Run All Tests

```bash
python -m pytest python/tests/ -v --tb=short
```

### Run Specific Tests

```bash
# Knowledge base tests
python -m pytest python/tests/test_knowledge_base.py -v

# LLM integration tests
python -m pytest python/tests/test_llm_rag_integration.py -v

# Index computation tests
python -m pytest python/tests/test_index_computation.py -v
```

### Manual Testing

```bash
# Test orchestrator
python -c "
from agents import LAEVOrchestrator
orch = LAEVOrchestrator(use_full_agents=False)
result = orch.process('Show flight trends')
print('Success:', result['success'])
"
```

## 🔍 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

```bash
# Ensure you're in the correct directory
cd /path/to/white-paper

# Reinstall dependencies
pip install -r config/requirements.txt --force-reinstall
```

#### 2. API Key Errors

```bash
# Check .env file exists
ls -la .env

# Verify API key is set
grep DEEPSEEK_API_KEY .env

# Test API connectivity
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  https://api.deepseek.com/v1/models
```

#### 3. ChromaDB Issues

```bash
# Clear and rebuild database
rm -rf chroma_db/
python python/src/knowledge_base.py
```

#### 4. CUDA/GPU Issues (for Local MLLM)

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# If False, install CPU-only PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

#### 5. Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill process or use different port
streamlit run python/src/app.py --server.port 8502
```

### Getting Help

1. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) for usage instructions
2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
3. Open an issue on GitHub with:
   - Error message
   - System information
   - Steps to reproduce

## 📊 Performance Optimization

### For Production Deployment

```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

# Enable caching
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

### Memory Optimization

```bash
# Limit ChromaDB memory usage
export CHROMADB_MEMORY_LIMIT=2G

# Use quantized models for local MLLM
export USE_4BIT_QUANTIZATION=true
```

## ✅ Post-Installation Checklist

- [ ] Python environment activated
- [ ] All dependencies installed
- [ ] .env file configured with API keys
- [ ] Knowledge base initialized (for RAG)
- [ ] Tests passing
- [ ] Web interface accessible
- [ ] Demo application running

## 🎉 Next Steps

1. **Try the Demo**: `python demo/run_demo.py`
2. **Read Usage Guide**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
3. **Explore Examples**: Check `python/src/demo_rag.py`
4. **Read Paper**: See `paper/` directory

---

For updates and more information, visit: https://github.com/LASER-IDEA/white-paper
