# Introduction

## The Rise of Low-Altitude Economy

The low-altitude economy (LAE) has emerged as a transformative force in modern transportation and logistics, encompassing unmanned aerial vehicles (UAVs), electric vertical take-off and landing (eVTOL) aircraft, and urban air mobility (UAM) systems [1]. With the global drone market projected to reach $43 billion by 2025 and commercial drone operations expanding rapidly across logistics, agriculture, and emergency response, the need for effective data analysis tools has never been greater.

In this domain, stakeholders—from air traffic controllers to logistics operators—must continuously monitor complex operational metrics: flight patterns across hundreds of routes, safety incidents distributed across geographic regions, fleet utilization rates varying by time and weather conditions, and regulatory compliance metrics spanning multiple jurisdictions. Effective visualization of this data is essential for informed decision-making, yet creating appropriate visualizations requires both deep domain expertise and technical proficiency in visualization tools.

## Challenges in Domain-Specific Visualization

Natural language interfaces (NLIs) for data visualization have gained significant attention, promising to democratize data analysis by enabling users to generate charts through conversational queries [2, 3, 4]. Systems like NL4DV [2] translate natural language into visualization specifications, while recent large language model (LLM)-based approaches generate code directly [5, 6].

However, when applied to domain-specific contexts like the low-altitude economy, existing approaches face three fundamental limitations:

**Lack of Domain Knowledge**. General-purpose NLIs lack understanding of domain-specific concepts, metrics, and relationships. For example, a query like "Show me UAM corridor efficiency" requires knowledge of what constitutes a UAM corridor, how efficiency is measured, and which visualization best represents this metric. Without such domain grounding, systems either fail or produce generic, inappropriate visualizations.

**No Quality Assurance**. Most systems generate visualizations in a single pass without validation. A system might produce syntactically valid but semantically incorrect code—using a pie chart for temporal trends, or failing to include essential chart elements like titles and axis labels. Users without visualization expertise may not recognize these deficiencies.

**Static Architecture**. Existing systems employ fixed pipelines that cannot adapt to query complexity. Simple queries ("Show flight count") and complex analyses ("Compare weekend vs weekday patterns across regions with trend lines") receive the same processing, leading to either oversimplified complex queries or unnecessarily elaborate simple ones.

## Our Approach: LAEV-Agents

We present **LAEV-Agents** (Low-Altitude Economy Visualization Agents), a multi-agent system that combines retrieval-augmented generation (RAG) with iterative refinement for domain-specific visualization generation. Our system architecture consists of five specialized agents (Figure 1):

- **Planner**: Analyzes user intent and decomposes complex queries into subtasks
- **Retriever**: Gathers relevant context from a domain knowledge graph
- **Coder**: Generates visualization code using PyECharts
- **Evaluator**: Assesses output quality across multiple dimensions
- **Reflector**: Triggers refinement iterations when quality is insufficient

**Key Innovation 1: GraphRAG for Domain Knowledge**. We construct a knowledge graph with 130 entities and 71 relationships specific to the low-altitude economy, including aircraft types (multirotor, eVTOL), operational purposes (logistics, emergency response), regulatory frameworks, geographic regions, and performance metrics. This enables context-aware retrieval that grounds visualization decisions in domain expertise.

**Key Innovation 2: Multi-Dimensional Quality Assessment**. Our Evaluator performs automated quality checks across four dimensions: readability (labels, titles, legends), aesthetics (color usage, spacing), data encoding (appropriateness of chart type for data relationships), and domain appropriateness (alignment with visualization best practices for the domain). Scores below threshold trigger automatic refinement.

**Key Innovation 3: Adaptive Iteration**. The system dynamically adjusts processing based on query complexity and intermediate results. Simple queries may complete in one pass, while complex analyses undergo multiple refinement cycles guided by the Reflector agent.

## Empirical Results

We evaluated LAEV-Agents against two strong baselines—NL4DV [2], a state-of-the-art academic system (TVCG 2021), and Direct LLM prompting with DeepSeek—using 32 curated queries spanning six task types: trend analysis, comparison, distribution, correlation, exploration, and anomaly detection.

Results demonstrate that LAEV-Agents achieves **90.6% success rate**, significantly outperforming NL4DV (59.4%) and approaching Direct LLM (100%) while providing quality guarantees the baseline lacks. Key findings include:

- **Superior performance on complex queries**: 100% success on exploration tasks (e.g., "Provide a comprehensive dashboard") where NL4DV fails completely (0%)
- **Domain expertise advantage**: +31 percentage points over NL4DV overall
- **Efficient execution**: Average 25.1s per query, comparable to Direct LLM (26.0s)
- **Quality assurance**: Automated visual evaluation with average score of 0.75 across readability, aesthetics, data encoding, and appropriateness

Ablation studies reveal meaningful contributions from each component: the multi-agent architecture provides substantial improvement over direct LLM, while GraphRAG specifically enhances performance on domain-specific queries requiring specialized knowledge.

## Contributions

This paper makes the following contributions:

1. **LAEV-Agents**: The first multi-agent system for domain-specific visualization generation, combining RAG with iterative refinement (Section 3).

2. **Design Space Formalization**: A systematic characterization of visualization tasks, data dimensions, and chart types for the low-altitude economy domain (Section 4).

3. **Empirical Evaluation**: Comprehensive comparison demonstrating superior performance on complex, domain-specific queries compared to state-of-the-art baselines (Section 6).

4. **Open Implementation**: Source code and experimental framework released for reproducibility and extension to other domains.

## Paper Organization

The remainder of this paper is organized as follows. Section 2 reviews related work in natural language visualization and multi-agent systems. Section 3 presents our system architecture and design rationale. Section 4 describes our design space formalization. Section 5 details the implementation. Section 6 presents evaluation results. Section 7 discusses limitations and future work.

## References (Introduction)

[1] X. Chen et al., "Low-altitude economy: Development status and future trends," *Transportation Research*, 2024.

[2] A. Narechania et al., "NL4DV: A toolkit for generating analytic specifications for data visualization from natural language queries," *IEEE TVCG*, 2021.

[3] T. Liao et al., "Natural language to visualization by neural machine translation," *IEEE VIS*, 2021.

[4] D. Moritz et al., "Formalizing visualization design knowledge as constraints," *IEEE TVCG*, 2019.

[5] OpenAI, "GPT-4 technical report," *arXiv:2303.08774*, 2023.

[6] DeepSeek-AI, "DeepSeek-V2: A strong, economical, and efficient mixture-of-experts language model," *arXiv:2405.04434*, 2024.
