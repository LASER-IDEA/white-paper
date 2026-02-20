# LAEV-Agents Interactive Demo

A professional web-based demo for the LAEV-Agents (Low Altitude Economy Visualization Agents) system.

Choose between **Streamlit** (modern, feature-rich) or **Gradio** (simple, compatible) interfaces.

## 🎬 Quick Start

### Option 1: Using the Interactive Launcher (Recommended)

```bash
cd demo
python run_demo.py
```

Then select your preferred UI (Streamlit or Gradio).

### Option 2: Direct Launch

**Streamlit (default, feature-rich):**
```bash
streamlit run app.py
# URL: http://localhost:8501
```

**Gradio (lightweight, compatible):**
```bash
python app_gradio.py
# URL: http://localhost:7860
```

## 📋 Prerequisites

1. **Python 3.10+**
2. **API Keys** (set in `.env` file in project root):
   - `DEEPSEEK_API_KEY` - For DeepSeek LLM
   - `OPENAI_API_KEY` - Alternative LLM provider
   - `QWEN_API_KEY` - For Qwen MLLM (optional, for visual evaluation)

3. **Parent Project Setup**:
   ```bash
   cd ../python
   pip install -e .
   ```

## 🎨 Features

### Core Functionality
- **Natural Language Queries**: Type any visualization request in plain English
- **Multi-Agent Pipeline**: Watch Planner → Retriever → Coder → Evaluator → Reflector in action
- **Real-time Visualization**: See generated PyECharts visualizations instantly
- **Quality Metrics**: View processing time, iterations, and quality scores

### User Interface Options

**Streamlit Version (`app.py`):**
- 🎨 Modern design with gradient styling and animations
- 📊 Rich agent timeline visualization
- 📜 Query history with rerun capability
- 💻 Generated code viewer with syntax highlighting
- 🎛️ Sidebar settings panel

**Gradio Version (`app_gradio.py`):**
- ⚡ Lightweight and fast loading
- 🔄 Broader browser compatibility
- 📱 Mobile-friendly responsive design
- 🎯 Simplified, focused interface

### Supported Query Types
1. **Trend Analysis**: "Show flight trends over time"
2. **Comparison**: "Compare regions by flight duration"
3. **Distribution**: "Show aircraft type distribution"
4. **Correlation**: "Weather vs flight delays"
5. **Exploration**: "Comprehensive operations dashboard"
6. **Anomaly Detection**: "Find unusual flight patterns"

## 🔧 Configuration

### LLM Providers
Select from the sidebar:
- **DeepSeek** (default): Recommended for best performance
- **OpenAI**: GPT-4 or GPT-3.5-turbo
- **Anthropic**: Claude models

### Agent Modes
- **Fast Mode** (default): Simplified agents for quicker responses
- **Full Mode**: Complete agent implementation with visual evaluation

### Iteration Settings
Adjust max iterations (1-5) for refinement cycles.

## 📁 Project Structure

```
demo/
├── app.py              # Streamlit application (feature-rich)
├── app_gradio.py       # Gradio application (lightweight)
├── run_demo.py         # Interactive launcher script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🐛 Troubleshooting

### Import Errors
If you see import errors, ensure the parent project is set up:
```bash
cd ../python
pip install -r ../config/requirements.txt
```

### API Key Issues
Create a `.env` file in the project root:
```bash
cd ..
echo "DEEPSEEK_API_KEY=your_key_here" > .env
```

### Module Not Found
Make sure you're running from the demo directory:
```bash
cd /path/to/white-paper/demo
python run_demo.py
```

## 📝 Example Queries

Try these queries to explore the system:

1. **Simple Trend**:
   ```
   Show monthly flight operations trend
   ```

2. **Multi-dimensional Comparison**:
   ```
   Compare weekend vs weekday flight patterns across regions
   ```

3. **Complex Dashboard**:
   ```
   Provide a comprehensive dashboard of low-altitude economy operations
   ```

4. **Anomaly Detection**:
   ```
   Identify any unusual flight patterns in the data
   ```

## 🔗 Integration

The demo uses the parent project's:
- `agents.LAEVOrchestrator`: Main multi-agent pipeline
- `agents.generate_visualization`: Convenience function
- Knowledge Graph with 130+ entities
- PyECharts code generation

## 📄 Citation

If you use this system in your research, please cite:

```bibtex
@inproceedings{laev_agents_2026,
  title={LAEV-Agents: Multi-Agent System for Low Altitude Economy Visualization},
  author={LAEV Research Team},
  booktitle={IEEE VIS 2026},
  year={2026}
}
```

## 📧 Support

For issues or questions:
- Check the main project README: `../README.md`
- Review the usage guide: `../USAGE_GUIDE.md`
- Open an issue on GitHub

---

**Made with ❤️ for IEEE VIS 2026**
