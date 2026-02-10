# Dockerfile for deploying the Streamlit RAG LLM application
# Multi-stage build to optimize disk space usage

# Builder stage - install dependencies
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies and clean up in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies in batches to reduce peak disk usage
# First batch: Core dependencies
RUN pip install --no-cache-dir --user streamlit streamlit-echarts pyecharts pandas numpy scipy python-dotenv

# Second batch: AI/ML dependencies
RUN pip install --no-cache-dir --user openai langchain langchain-community langchain-openai

# Third batch: Vector DB and document processing
RUN pip install --no-cache-dir --user chromadb pypdf sentence-transformers

# Clean up to reduce image size
RUN find /root/.local -type d -name '__pycache__' -prune -exec rm -rf {} + && \
    find /root/.local -type d -name 'tests' -prune -exec rm -rf {} + && \
    find /root/.local -name '*.pyc' -delete

# Runtime stage - minimal final image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY . /app/

# Update PATH to include user-installed packages
ENV PATH=/root/.local/bin:$PATH

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
