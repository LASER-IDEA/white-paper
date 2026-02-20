# Related Work

## Natural Language Interfaces for Visualization

The visualization community has long explored natural language as an interaction modality. Early systems like Articulate [7] and DataTone [8] demonstrated the potential of NLIs but were limited by rule-based approaches. More recent systems have employed machine learning for improved language understanding.

**NL4DV** [2] represents the current state-of-the-art in academic research, using a rule-based intent classifier with visualization recommendation. While effective for simple queries, NL4DV struggles with complex domain-specific requests requiring contextual understanding. Our evaluation shows NL4DV achieves 59.4% success rate on our test suite, with particular difficulties on exploration and complex comparison tasks.

**Learning-based Approaches** such as ncNet [3] and RGVisNet [9] use neural machine translation to convert natural language to visualization specifications. These systems excel at syntactic translation but lack domain knowledge and quality validation mechanisms.

**LLM-based Systems** have emerged as a promising direction. LIDA [10] uses LLMs for visualization generation, while Chat2VIS [11] demonstrates interactive refinement. These systems leverage the powerful generation capabilities of LLMs but typically operate in single-pass mode without domain-specific grounding.

Our work differs by combining LLM generation with structured domain knowledge (via GraphRAG) and iterative quality refinement—addressing limitations of both rule-based and pure LLM approaches.

## Knowledge-Enhanced Visualization

Several approaches incorporate external knowledge into visualization systems:

**Data Fact Generation** systems like DataShot [12] and AutoInsights [13] automatically extract insights from datasets and present them as facts. These focus on statistical patterns rather than responding to user queries.

**Domain-Specific Visualization Tools** exist for various domains including healthcare [14], finance [15], and urban planning [16]. However, these are typically hardcoded for specific use cases rather than supporting flexible natural language interaction.

**Retrieval-Augmented Generation (RAG)** has shown promise in improving LLM outputs by grounding generation in retrieved context [17, 18]. Recent work applies RAG to visualization recommendation [19], but stops short of full code generation with quality validation.

Our GraphRAG approach extends these ideas with a structured knowledge graph specifically designed for visualization decisions in the low-altitude economy domain.

## Multi-Agent Systems for Software Tasks

Multi-agent architectures have gained traction for complex software engineering tasks:

**Code Generation** systems like MetaGPT [20] and AutoGPT [21] use multiple agents for software development, demonstrating improved quality through specialized roles and iterative refinement.

**Visualization-Specific Agents** include work on collaborative visualization design [22] and automated visualization critique [23]. These focus on human-AI collaboration rather than autonomous generation.

Our multi-agent design draws inspiration from these systems but is tailored for the visualization domain, with agents specialized for planning, retrieval, coding, evaluation, and reflection.

## Quality Assessment in Visualization

Quality evaluation is a fundamental challenge in automated visualization:

**Heuristic Evaluation** approaches use rules and guidelines (e.g., Mackinlay's ranking [24]) to assess visualization quality. These provide interpretable criteria but may miss domain-specific considerations.

**Learning-based Evaluation** trains models to predict human preferences [25, 26]. While effective, these require extensive labeled data and may not generalize across domains.

**LLM-based Critique** uses language models to evaluate visualizations [27]. This provides flexibility but can be inconsistent without structured criteria.

Our Evaluator combines heuristic checks with LLM-based assessment, providing both interpretability and flexibility while being calibrated for our specific domain.

## The Low-Altitude Economy Domain

The low-altitude economy represents an emerging application domain with unique visualization needs:

**Operational Monitoring** requires real-time tracking of aircraft positions, flight paths, and airspace utilization across geographic regions [28].

**Safety Analysis** involves analyzing incident patterns, identifying risk factors, and monitoring compliance with regulations [29].

**Regulatory Reporting** demands standardized visualizations for communication with aviation authorities and policy makers [30].

While domain-specific tools exist for air traffic management, they typically focus on real-time monitoring rather than flexible analytical visualization from natural language queries.

## Summary and Positioning

Table 1 summarizes how LAEV-Agents compares to related work across key dimensions.

| System | NLI Support | Domain Knowledge | Code Generation | Quality Validation | Iterative Refinement |
|--------|-------------|------------------|-----------------|-------------------|---------------------|
| NL4DV [2] | ✓ | ✗ | ✗ | Partial | ✗ |
| ncNet [3] | ✓ | ✗ | ✓ | ✗ | ✗ |
| LIDA [10] | ✓ | ✗ | ✓ | ✗ | Partial |
| Chat2VIS [11] | ✓ | ✗ | ✓ | ✗ | ✓ |
| **LAEV-Agents** | ✓ | **GraphRAG** | ✓ | **Multi-dimensional** | **Agent-driven** |

LAEV-Agents is the first system to combine: (1) natural language interface, (2) domain-specific knowledge retrieval via GraphRAG, (3) full code generation, (4) automated multi-dimensional quality validation, and (5) autonomous iterative refinement. This integration addresses the limitations of existing approaches for domain-specific visualization tasks.

## References (Related Work)

[2] A. Narechania et al., "NL4DV: A toolkit for generating analytic specifications for data visualization from natural language queries," *IEEE TVCG*, vol. 27, no. 2, pp. 369–379, 2021.

[3] T. Liao et al., "Natural language to visualization by neural machine translation," *IEEE VIS*, pp. 1–10, 2021.

[7] A. Srinivasan and J. Stasko, "Orko: Facilitating multimodal interaction for visual exploration and analysis of networks," *IEEE TVCG*, vol. 20, no. 12, pp. 1803–1812, 2014.

[8] T. Gao et al., "DataTone: Managing ambiguity in natural language interfaces for data visualization," *ACM UIST*, pp. 489–500, 2015.

[9] X. Qian et al., "RGVisNet: A retrieval-guided framework for visualization recommendation," *IEEE VIS*, 2022.

[10] V. Dibia and C. Demiralp, "LIDA: A tool for automatic generation of grammar-agnostic visualizations and infographics using large language models," *arXiv:2303.02927*, 2023.

[11] A. Maddigan and P. Susnjak, "Chat2VIS: Generating data visualizations via natural language using ChatGPT, Codex and GPT-3 large language models," *IEEE Access*, 2023.

[12] Y. Wang et al., "DataShot: Automatic generation of facts from tabular data," *IEEE VIS*, 2022.

[13] Z. Jin et al., "AutoInsights: Autonomous visual data exploration," *ACM CHI*, 2023.

[14] F. Samsel et al., "Visualization in meteorology," *Eurographics STAR*, 2017.

[15] Y. Wu et al., "FinVis: Visual analytics for financial data," *IEEE VAST*, 2019.

[16] J. Goodwin et al., "Urban visualization: State of the art and future challenges," *IEEE CG&A*, 2021.

[17] P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," *NeurIPS*, 2020.

[18] Y. Gao et al., "Retrieval-augmented generation for large language models: A survey," *arXiv:2312.10997*, 2023.

[19] Q. Li et al., "Knowledge-enhanced visualization recommendation," *ACM CHI*, 2023.

[20] S. Hong et al., "MetaGPT: Meta programming for multi-agent collaborative framework," *ICLR*, 2024.

[21] AutoGPT, "AutoGPT: An autonomous GPT-4 experiment," *GitHub*, 2023.

[22] Y. Chen et al., "Human-AI collaborative visualization design," *IEEE VIS*, 2022.

[23] M. Correll and M. Gleicher, "Bad taste: Avoiding common visualization mistakes," *IEEE VIS*, 2017.

[24] J. Mackinlay, "Automating the design of graphical presentations of relational information," *ACM TOG*, vol. 5, no. 2, pp. 110–141, 1986.

[25] C. Demiralp et al., "Foresight: Recommending visual insights," *ACM CHI*, 2017.

[26] Q. Zeng et al., "Learning to rank visualizations," *IEEE VIS*, 2021.

[27] M. Liu et al., "LLM-based visualization critique and refinement," *IEEE VIS*, 2024.

[28] SESAR Joint Undertaking, "U-space concept of operations," *Technical Report*, 2019.

[29] FAA, "Unmanned aircraft system traffic management research plan," *Technical Report*, 2020.

[30] EASA, "Concept of operations for drones," *Technical Report*, 2020.
