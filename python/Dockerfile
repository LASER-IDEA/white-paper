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

# Install dependencies to a separate directory and clean up in same layer
RUN pip install --no-cache-dir --user -r requirements.txt && \
    find /root/.local -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
    find /root/.local -type d -name 'tests' -exec rm -rf {} + 2>/dev/null || true && \
    find /root/.local -type d -name '*.dist-info' -exec rm -rf {}/RECORD {} + 2>/dev/null || true

# Runtime stage - minimal final image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

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
