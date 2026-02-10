# Requirements Files

This directory contains split requirements files to optimize Docker builds for constrained environments.

## Files

- `requirements.txt` - Full list of dependencies (master copy maintained in `config/requirements.txt`)
- `requirements-core.txt` - Core dependencies (streamlit, pandas, numpy, scipy, etc.)
- `requirements-ml.txt` - AI/ML dependencies (openai, langchain, etc.)
- `requirements-vectordb.txt` - Vector DB and document processing (chromadb, pypdf, sentence-transformers)

## Why Split Requirements?

GitHub Actions runners have limited disk space (~14GB available). When installing all dependencies at once using `pip install -r requirements.txt`, the build process runs out of space because large packages like torch, transformers, and chromadb (with all their dependencies) require significant temporary storage during installation.

By splitting requirements into smaller batches and installing them sequentially, we significantly reduce peak disk usage during the build process.

## Maintenance

The split requirements files are automatically generated during the CI/CD build process from `config/requirements.txt`. 

If you need to update dependencies:
1. Edit `config/requirements.txt` 
2. The split files will be automatically generated during the Docker build in CI/CD

For local development, you can generate the split files manually:
```bash
# From the repository root
# Core dependencies (lines 1-7)
sed -n '1,7p' config/requirements.txt > python/requirements-core.txt

# ML dependencies (line 8 and lines 10-12, skipping comment on line 9)
sed -n '8p' config/requirements.txt > python/requirements-ml.txt
sed -n '10,12p' config/requirements.txt >> python/requirements-ml.txt

# Vector DB dependencies (lines 13-15)
sed -n '13,15p' config/requirements.txt > python/requirements-vectordb.txt
```

## Docker Build

The Dockerfile uses these split files to install dependencies in batches:
1. Install core dependencies first (lighter packages)
2. Install ML dependencies second
3. Install vector DB dependencies last (heaviest packages)

This approach keeps peak disk usage within GitHub Actions runner limits while maintaining build reliability.
