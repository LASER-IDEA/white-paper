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

# Copy requirements files
COPY requirements*.txt /app/

# Install dependencies in batches to reduce peak disk usage
# Dependencies are split into multiple files to reduce peak disk usage during build:
# - requirements-core.txt: Core dependencies (streamlit, pandas, numpy, scipy, etc.)
# - requirements-ml.txt: AI/ML dependencies (openai, langchain, etc.)  
# - requirements-vectordb.txt: Vector DB and document processing (chromadb, pypdf, sentence-transformers)
#
# This batched approach significantly reduces peak disk usage during the build process
# by installing lighter packages first, then progressively installing heavier ML packages.
# This is necessary because GitHub Actions runners have limited disk space and installing
# all dependencies at once causes "No space left on device" errors.
RUN pip install --no-cache-dir --user -r requirements-core.txt && \
    pip install --no-cache-dir --user -r requirements-ml.txt && \
    pip install --no-cache-dir --user -r requirements-vectordb.txt && \
    find /root/.local -type d -name '__pycache__' -prune -exec rm -rf {} + && \
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
