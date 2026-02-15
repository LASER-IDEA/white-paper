# LAEV Experiments

IEEE VIS 2026 Submission - Experimental Framework

## Overview

This directory contains the complete experimental framework for comparing LAEV-Agents against baselines (NL4DV, Direct LLM).

## Directory Structure

```
experiments/
├── data/
│   ├── dataset_loader.py      # Real flight data loader
│   └── test_queries.py        # 30 curated test queries
├── baselines/
│   └── nl4dv_baseline.py      # NL4DV and Direct LLM wrappers
├── results/                    # Experiment outputs (generated)
├── analysis/                   # Analysis scripts (to be added)
├── run_experiment.py          # Main experiment runner
└── README.md                  # This file
```

## Prerequisites

### 1. Neo4j (for GraphRAG)

```bash
# Option 1: Docker
docker run -d \
  --name neo4j-vis \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/vispaper2026 \
  neo4j:5.15-community

# Option 2: Local install (Ubuntu)
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 5' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
sudo systemctl start neo4j
```

### 2. Python Dependencies

```bash
pip install neo4j-driver networkx pandas pyecharts

# NL4DV (cloned as submodule)
cd ../nl4dv
pip install -e .
```

### 3. API Keys

Set environment variables:

```bash
export DEEPSEEK_API_KEY="your_key_here"
# or
export OPENAI_API_KEY="your_key_here"
```

## Running Experiments

### Full Comparison (All Systems)

```bash
python run_experiment.py --systems all
```

### Specific Systems Only

```bash
# Compare LAEV vs NL4DV only
python run_experiment.py --systems nl4dv laev

# Compare LAEV vs Direct LLM only
python run_experiment.py --systems direct_llm laev
```

### Quick Test (First 5 Queries)

```bash
python run_experiment.py --queries 5
```

### Full Agent Implementation

```bash
python run_experiment.py --full-agents
```

## Test Query Set

30 carefully designed queries covering:

| Task Type | Simple | Medium | Complex | Total |
|-----------|--------|--------|---------|-------|
| Trend Analysis | 2 | 0 | 1 | 3 |
| Comparison | 2 | 0 | 1 | 3 |
| Distribution | 2 | 0 | 1 | 3 |
| Correlation | 1 | 1 | 1 | 3 |
| Exploration | 2 | 0 | 1 | 3 |
| Anomaly Detection | 0 | 2 | 0 | 2 |
| **Total** | **9** | **3** | **5** | **17** |

*Note: Full set has 30 queries*

## Output Format

Results are saved as JSON:

```json
{
  "experiment_info": {
    "timestamp": "2026-02-14T12:00:00",
    "total_queries": 30,
    "systems_tested": ["nl4dv", "laev_agents"]
  },
  "query_results": [
    {
      "query_id": "TREND-01",
      "query_en": "Show the trend of flight operations over time",
      "task_type": "trend_analysis",
      "complexity": "simple",
      "system_results": {
        "nl4dv": {
          "success": true,
          "vega_spec": {...},
          "chart_type": "line",
          "execution_time": 1.23
        },
        "laev_agents": {
          "success": true,
          "chart_code": "...",
          "execution_time": 2.45,
          "iterations": 1
        }
      }
    }
  ]
}
```

## Evaluation Metrics

### Quantitative

1. **Success Rate**: Percentage of queries generating valid visualizations
2. **Execution Time**: Average time per query
3. **Code Quality**: Syntax validity, execution success
4. **Task Accuracy**: Whether generated chart matches expected type

### Qualitative (User Study)

1. **Usability**: SUS (System Usability Scale) score
2. **Usefulness**: Perceived helpfulness (1-5 Likert)
3. **Trust**: Confidence in system output (1-5 Likert)
4. **Open-ended feedback**: Qualitative insights

## Experiment Stages

### Stage 1: Automated Comparison
- Run all 30 queries on all systems
- Measure success rate and execution time
- Generate quantitative comparison

### Stage 2: Ablation Study
- Test LAEV-Agents variants:
  - Full system (all agents)
  - Without GraphRAG (vector only)
  - Without Multi-Agent (single pass)
  - Without Visual Feedback

### Stage 3: User Study
- 15-20 participants (domain experts + general users)
- 5 tasks per participant
- Think-aloud protocol
- SUS questionnaire

## Reproducibility

### Environment
- Python 3.9+
- Ubuntu 22.04 / macOS / Windows WSL
- Docker (for Neo4j)

### Random Seeds
All random operations use fixed seed `42` for reproducibility.

### Version Pinning
Key dependencies:
- neo4j-driver==5.15.0
- pandas==2.2.3
- pyecharts==2.0.6

## Troubleshooting

### Neo4j Connection Failed
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# Check logs
docker logs neo4j-vis

# Reset Neo4j
docker rm -f neo4j-vis
docker run -d --name neo4j-vis -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/vispaper2026 \
  neo4j:5.15-community
```

### NL4DV Import Error
```bash
# Ensure NL4DV is in Python path
export PYTHONPATH="${PYTHONPATH}:/data1/xh/workspace/white-paper/nl4dv"

# Or install in development mode
cd ../nl4dv && pip install -e .
```

### API Rate Limits
- DeepSeek: 100 requests/minute (free tier)
- OpenAI: Depends on tier
- Implement exponential backoff in code

## Citation

If you use this experimental framework, please cite:

```bibtex
@article{laev2026,
  title={LAEV-Agents: Multi-Agent Retrieval-Augmented Generation for Domain-Specific Visual Analytics},
  author={[Authors]},
  journal={IEEE Transactions on Visualization and Computer Graphics},
  year={2026}
}
```

## Contact

For questions about the experiments, please open an issue on GitHub.
