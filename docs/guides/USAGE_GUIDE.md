# 🚀 LLM RAG Application Usage Guide

This guide explains how to use the deployed Low Altitude Economy LLM RAG (Retrieval-Augmented Generation) application.

## 📋 Table of Contents

1. [What is the LLM RAG Application?](#what-is-the-llm-rag-application)
2. [Accessing the Application](#accessing-the-application)
3. [Using the Application](#using-the-application)
4. [Features Overview](#features-overview)
5. [Example Use Cases](#example-use-cases)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## What is the LLM RAG Application?

The LLM RAG Application is an AI-powered dashboard that combines:

- **📊 Interactive Data Visualization**: View and explore Low Altitude Economy metrics across 5 core dimensions
- **🤖 AI Assistant**: Ask natural language questions and get intelligent responses
- **📚 RAG Knowledge Base**: Retrieval-Augmented Generation system that pulls relevant context from white paper documents to enhance AI responses
- **🎯 Smart Analytics**: Automatic chart generation and data insights

The system uses:
- **DeepSeek LLM** for intelligent responses
- **ChromaDB Vector Database** for semantic search across white papers
- **LangChain** for RAG pipeline
- **Streamlit** for the interactive web interface

---

## Accessing the Application

### Option 1: Live Deployment (if available)

If the application has been deployed to a cloud platform, you can access it directly:

- **Streamlit Community Cloud**: Check with your team for the deployment URL
- **Railway/Render**: Access via the provided deployment URL
- **Docker Deployment**: Access at `http://your-server:8501`

### Option 2: Local Deployment

#### Using Docker (Recommended)

1. **Pull or build the Docker image**:
   ```bash
   # If image is available in a registry
   docker pull your-registry/streamlit-rag-llm:latest
   
   # Or build locally from the repository
   cd white-paper/python
   docker build -t streamlit-rag-llm:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 \
     -e DEEPSEEK_API_KEY=your_api_key_here \
     streamlit-rag-llm:latest
   ```

3. **Access the application**:
   - Open your browser and navigate to: `http://localhost:8501`

#### Using Python Directly

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/LASER-IDEA/white-paper.git
   cd white-paper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r config/requirements.txt
   ```

3. **Set up environment variables** (optional, for AI features):
   ```bash
   # Copy the example environment file
   cp config/.env.example .env
   
   # Edit .env and add your DeepSeek API key
   # DEEPSEEK_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**:
   ```bash
   # Using the convenience script
   python run_python_app.py
   
   # Or manually
   cd python
   streamlit run src/app.py
   ```

5. **Access the application**:
   - Streamlit will automatically open your browser
   - Or navigate to: `http://localhost:8501`

---

## Using the Application

### Navigation

The application has multiple tabs, each serving different purposes:

1. **📊 Index Overview**: View comprehensive metrics and indices
2. **📈 Scale & Growth**: Analyze traffic volume and market size trends
3. **🏗️ Structure & Entity**: Explore fleet composition and entity distribution
4. **🗺️ Space & Geography**: View airspace utilization and regional patterns
5. **⚡ Efficiency & Quality**: Examine operational metrics and quality standards
6. **🚀 Innovation & Integration**: Track technology adoption and market integration
7. **🤖 AI Assistant**: Interactive chat interface with RAG-enhanced responses
8. **📁 Data Processing**: Upload and process your own CSV data

### Using the AI Assistant (Main Feature)

The **AI Assistant** tab is where the LLM RAG system shines:

#### Step 1: Navigate to AI Assistant

Click on the **🤖 AI Assistant** tab in the sidebar.

#### Step 2: Check RAG Status

Look for the status indicator at the top of the page:
- ✅ **RAG Knowledge Base: Active** - The system is ready with document context
- ℹ️ **RAG Knowledge Base: Not Available** - AI will work but without document context

#### Step 3: Ask Questions

Type your question in the text input box. Examples:

**General Questions:**
- "What are the five core dimensions of the Low Altitude Economy index?"
- "How is the index calculated?"
- "What metrics are most important for measuring scale and growth?"

**Specific Data Questions:**
- "What are the main types of aircraft in the fleet?"
- "How is airspace utilization measured?"
- "What innovation metrics are tracked?"

**Analytical Questions:**
- "What trends do you see in flight operations?"
- "Compare efficiency metrics across different regions"
- "Analyze the relationship between fleet size and market growth"

#### Step 4: Review Responses

The AI Assistant will:
1. **Search the knowledge base** for relevant context from white papers
2. **Generate a response** using the DeepSeek LLM with document context
3. **Create visualizations** if appropriate for your query
4. **Provide sources** when citing information from documents

#### Step 5: Request Visualizations

You can explicitly request charts:
- "Show me a chart of flight operations over time"
- "Create a bar chart comparing regional metrics"
- "Visualize the fleet composition"

The AI will generate interactive charts using ECharts.

---

## Features Overview

### 1. RAG-Enhanced Responses

**How it works:**
- Your question is converted to embeddings
- Similar document chunks are retrieved from the vector database
- Retrieved context is added to the LLM prompt
- LLM generates a response informed by actual white paper content

**Benefits:**
- Responses are grounded in domain-specific documents
- Reduces hallucinations and incorrect information
- Provides citations and sources
- More accurate and relevant answers

### 2. Smart Model Selection

The system automatically chooses the right model:
- **Simple queries** → `deepseek-chat` (fast responses)
- **Complex analysis** → `deepseek-reasoner` (deep reasoning)

### 3. Interactive Visualizations

All charts are interactive:
- **Hover** to see detailed values
- **Click** legend items to show/hide series
- **Zoom** on time-series charts
- **Export** charts as images

### 4. Data Processing

Upload your own CSV files:
1. Go to **📁 Data Processing** tab
2. Upload a CSV file with flight/economic data
3. The system will analyze and visualize your data
4. Ask the AI questions about your uploaded data

---

## Example Use Cases

### Use Case 1: Understanding Index Components

**Goal**: Learn about the index structure

**Steps**:
1. Navigate to AI Assistant
2. Ask: "Explain the five core dimensions of the Low Altitude Economy index"
3. Review the response with document citations
4. Follow up: "Which dimension is most important for policy makers?"

### Use Case 2: Analyzing Trends

**Goal**: Understand market trends

**Steps**:
1. Navigate to **📈 Scale & Growth** tab
2. Review the visualizations
3. Switch to AI Assistant
4. Ask: "What seasonal patterns do you see in flight operations?"
5. Request: "Create a chart showing monthly traffic patterns"

### Use Case 3: Regional Comparison

**Goal**: Compare different regions

**Steps**:
1. Navigate to **🗺️ Space & Geography** tab
2. View the map visualizations
3. Switch to AI Assistant
4. Ask: "Compare airspace utilization between Beijing and Shenzhen"
5. Follow up: "What factors contribute to these differences?"

### Use Case 4: Deep Dive on Metrics

**Goal**: Understand specific metrics

**Steps**:
1. Navigate to AI Assistant
2. Ask: "How is operational efficiency calculated?"
3. Review the formula and context from documents
4. Ask: "Show me efficiency trends over the past year"
5. Analyze the generated visualization

### Use Case 5: Custom Data Analysis

**Goal**: Analyze your own data

**Steps**:
1. Navigate to **📁 Data Processing** tab
2. Upload your CSV file
3. Switch to AI Assistant
4. Ask: "Analyze the data I just uploaded"
5. Request specific visualizations or insights

---

## Troubleshooting

### Application Won't Start

**Issue**: Error when running the application

**Solutions**:
1. Check Python version: `python --version` (should be 3.8+)
2. Reinstall dependencies: `pip install -r config/requirements.txt`
3. Check for port conflicts: Make sure port 8501 is available
4. Try with Docker instead of local Python

### RAG Knowledge Base Not Available

**Issue**: "RAG Knowledge Base: Not Available" message

**Solutions**:
1. Install RAG dependencies: `pip install -r config/requirements-rag.txt`
2. Check if PDF files exist in `docs/pdf/` directory
3. Delete `chroma_db/` folder and restart to rebuild
4. Check disk space (requirements vary based on document count; typically 200MB-1GB for models and database)

### AI Assistant Not Responding

**Issue**: No response from AI queries

**Solutions**:
1. Check if `DEEPSEEK_API_KEY` is set correctly
2. Verify API key is valid and has quota
3. Check internet connection
4. Look for error messages in terminal/logs
5. Try simpler queries first

### Slow First Run

**Issue**: Application takes long time on first startup

**Explanation**: This is normal! The first run needs to:
- Download embedding model (size varies by model; typically 80MB-400MB)
- Process all PDF documents
- Build vector database

**Solutions**:
- Wait for 2-5 minutes on first run
- Subsequent runs will be instant (uses cached database)
- Progress is shown in terminal

### Charts Not Displaying

**Issue**: Visualizations don't show up

**Solutions**:
1. Check browser console for JavaScript errors
2. Try a different browser (Chrome/Firefox recommended)
3. Clear browser cache
4. Disable ad blockers temporarily
5. Check if JavaScript is enabled

### Out of Memory Errors

**Issue**: Application crashes with memory errors

**Solutions**:
1. Close other applications
2. Use Docker with memory limits: `docker run -m 2g ...`
3. Reduce batch size in queries
4. Process smaller datasets

---

## FAQ

### Q1: Do I need a DeepSeek API key?

**A**: The API key is optional. Without it:
- ✅ You can view all dashboards and visualizations
- ✅ You can process and analyze data
- ❌ You cannot use the AI Assistant feature

### Q2: How much does it cost to use DeepSeek API?

**A**: DeepSeek offers competitive pricing. Check [DeepSeek pricing](https://www.deepseek.com/pricing) for current rates. The application uses tokens efficiently.

### Q3: Can I use other LLM providers?

**A**: Currently, the application is configured for DeepSeek. To use other providers (OpenAI, Anthropic, etc.), you would need to modify `python/src/llm_helper.py`.

### Q4: What documents are in the knowledge base?

**A**: The RAG system indexes all PDFs in `docs/pdf/`:
- Low-Altitude Economy White Paper.pdf
- scale_growth_report.pdf
- structure_entity_report.pdf
- time_space_report.pdf
- efficiency_quality_report.pdf
- innovation_integration_report.pdf

### Q5: Can I add my own documents?

**A**: Yes! 
1. Add PDF files to `docs/pdf/` directory
2. Delete the `chroma_db/` folder
3. Restart the application
4. The system will rebuild the database with your new documents

### Q6: Is my data secure?

**A**: 
- ✅ Data processing happens locally or in your deployment
- ✅ Only queries are sent to DeepSeek API (not your full dataset)
- ✅ Vector database is stored locally
- ⚠️ Use caution with sensitive/proprietary data

### Q7: Can I use this offline?

**A**: Partially.
- ✅ Dashboards and visualizations work offline
- ✅ Data processing works offline
- ✅ RAG vector search works offline (after initial setup)
- ❌ LLM features require internet (API calls to DeepSeek)

### Q8: How do I update the application?

**A**: 
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r config/requirements.txt

# Restart the application
python run_python_app.py
```

### Q9: Can I deploy this to production?

**A**: Yes! The application is production-ready. See deployment options in [python/README.md](python/README.md) for:
- Streamlit Community Cloud
- Railway
- Render
- Docker-based deployments

### Q10: How do I report issues or request features?

**A**: Open an issue on the [GitHub repository](https://github.com/LASER-IDEA/white-paper/issues) with:
- Clear description of the problem/feature
- Steps to reproduce (for bugs)
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

---

## Additional Resources

- **Technical Documentation**: [RAG_IMPLEMENTATION.md](RAG_IMPLEMENTATION.md) - Deep dive into the RAG architecture
- **Deployment Guide**: [python/README.md](python/README.md) - Docker and cloud deployment instructions
- **Main Documentation**: [README.md](README.md) - Project overview and setup
- **Security**: [SECURITY.md](SECURITY.md) - Security best practices
- **Index Definitions**: [INDEX_DEFINITIONS.md](INDEX_DEFINITIONS.md) - Detailed metric definitions

---

## Support

For additional help:

1. **Check Documentation**: Review the files listed above
2. **Run Demo**: Try `python python/src/demo_rag.py` to test RAG independently
3. **GitHub Issues**: Search existing issues or create a new one
4. **Contact Team**: Reach out to repository maintainers

---

**Happy analyzing! 🚁📊🤖**
