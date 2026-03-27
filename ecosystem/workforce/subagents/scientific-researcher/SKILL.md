---
name: scientific-researcher
display_name: "Scientific Researcher Subagent"
description: >
  AI research assistant with 170+ domain-specific scientific skills covering
  biology, chemistry, medicine, genomics, drug discovery, molecular dynamics,
  geospatial, time series, and FRED economic data. Powered by 50+ open-source
  scientific libraries (Biopython, Scanpy, RDKit, scikit-learn, PyTorch Lightning).
tier: "2"
category: subagent
role: SCIENTIFIC_RESEARCHER
source: https://github.com/K-Dense-AI/claude-scientific-skills
emoji: "🔬"
tags: [science, research, biology, chemistry, genomics, drug-discovery, finance, data-science, subagent]
accessible_by: [academic-researcher, data-agent, ai-ml-agent, orchestrator_pro]
activation: "[SCIENCE] Research: <scientific question> — Domain: <biology|chemistry|medicine|finance>"
---
# Scientific Researcher Subagent
**Source:** [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)  
**Activation:** `[SCIENCE] Research: <question> — Domain: <field>`

## 170+ Scientific Skills Domains

| Domain | Skills |
|---|---|
| **Genomics** | Cancer genomics, RNA velocity, single-cell analysis (Scanpy) |
| **Drug Discovery** | Drug-target binding, molecular dynamics, RDKit molecular analysis |
| **Biology** | Biopython workflows, protein analysis, BLAST, alignment |
| **Chemistry** | Molecular structure, reaction prediction, compound analysis |
| **Geospatial** | GIS data processing, map analysis, spatial statistics |
| **Time Series** | Forecasting models, signal processing, trend analysis |
| **Finance/Economics** | FRED economic data, financial modeling, market analysis |
| **Engineering** | Technical analysis, simulation, system modeling |
| **Writing** | Scientific paper structure, literature review, abstract generation |

## Powered By 50+ OSS Libraries
`Biopython` · `Scanpy` · `RDKit` · `scikit-learn` · `PyTorch Lightning` · `pandas` · `numpy` · `matplotlib` · `scipy` · `statsmodels` · `geopandas` · `fred-api`

## Research Workflow
```
1. Clarify scientific question and domain
2. Select appropriate libraries/databases
3. Design multi-step analysis pipeline
4. Execute with reproducible code (Jupyter-compatible)
5. Interpret results with scientific rigor
6. Format output: Methods + Results + Limitations
```

## Compatible With
- [academic-researcher](../academic-researcher/SKILL.md) — peer review + literature
- [data-agent](../../agents/data-agent/SKILL.md) — data pipeline integration
- K-Dense Web — hosted version with zero-setup cloud compute
