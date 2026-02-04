# Streamlit RAG LLM App - Docker Deployment

This directory contains the Streamlit application with RAG (Retrieval-Augmented Generation) and LLM capabilities.

## Quick Start with Docker

### Build the Docker Image

```bash
# From the python directory
docker build -t streamlit-rag-llm:latest .
```

### Run the Container

```bash
# Basic run
docker run -p 8501:8501 streamlit-rag-llm:latest

# With API key for LLM features
docker run -p 8501:8501 \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  -e DEEPSEEK_BASE_URL=https://api.deepseek.com/v1 \
  streamlit-rag-llm:latest
```

### Access the Application

Once running, access the application at: http://localhost:8501

## Environment Variables

The following environment variables can be configured:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key (required for LLM features)
- `DEEPSEEK_BASE_URL`: DeepSeek API base URL (default: https://api.deepseek.com/v1)
- `DEEPSEEK_CHAT_MODEL`: Chat model name (default: deepseek-chat)
- `DEEPSEEK_REASONER_MODEL`: Reasoner model name (default: deepseek-reasoner)

## Deployment to Cloud Platforms

### Streamlit Community Cloud

1. Visit https://share.streamlit.io
2. Connect your GitHub repository
3. Select `python/src/app.py` as the main app file
4. Add secrets in the Streamlit Cloud dashboard:
   - `DEEPSEEK_API_KEY`
   - `DEEPSEEK_BASE_URL`

### Railway

1. Create a new project on Railway
2. Connect your GitHub repository
3. Set the build context to `python/`
4. Add environment variables in the Railway dashboard

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add environment variables in the Render dashboard

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
```

## Features

- **AI-Powered Analysis**: Natural language data exploration with DeepSeek LLM
- **Interactive Charts**: Dynamic visualizations with ECharts
- **Data Processing**: CSV upload and analysis capabilities
- **RAG Integration**: Retrieval-augmented generation for enhanced insights

## Directory Structure

```
python/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── llm_helper.py       # LLM integration and RAG logic
│   ├── data_factory.py     # Mock data generation
│   ├── data_processor.py   # Data processing utilities
│   ├── charts.py           # Chart generation functions
│   └── utils/
│       └── logger.py       # Logging utilities
├── data/                   # Sample data files
├── tests/                  # Unit tests
├── Dockerfile              # Docker configuration
├── .dockerignore           # Docker ignore patterns
└── requirements.txt        # Python dependencies
```

## Security Notes

- Never commit real API keys to version control
- Use environment variables or secrets management for sensitive data
- The application includes input validation and security measures
- See [SECURITY.md](../SECURITY.md) for more details

## Support

For issues or questions, please open an issue on GitHub.
