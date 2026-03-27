---
id: insight_engine
name: Insight Engine
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Cross-domain pattern discovery and trend analysis.

accessible_by:
  - Researcher
  - Analyst

dependencies:
  - reasoning_engine
  - neural_memory

exposed_functions:
  - name: pattern_recognition
  - name: trend_analysis
  - name: cross_domain_synthesis

consumed_by:
  - cognitive_evolver
emits_events:
  - insight_discovered
listens_to: []
---
# ðŸ§  Insight Engine Skill (Pattern Discovery)

This skill provides the AI OS with "Intuition" â€” finding non-obvious correlations across different knowledge domains.

## ðŸ› ï¸ Core Functions:
1.  **Correlation Scan (/correlate):**
    - Compare facts in `Cosmic Memory` with project files.
    - Find "Topic Clusters" (e.g., "Performance" notes often appear with "Storage" code).
2.  **Hypothesis Generator (/hypothesize):**
    - Suggest high-value actions based on clusters.
    - Example: "Detected cluster: 'Memory Leak' and 'Popup'. Suggestion: Optimize popup memory disposal."
3.  **Knowledge Gap Analysis (/gap):**
    - Identify areas where code exists but documentation or lessons-learned are missing.

## ðŸ“‹ Instructions:
Before starting a major feature or after a long debugging session:
1. Run `/correlate` to check if there's an existing insight that can help.
2. Log new insights to strictly at `.agents/knowledge-hub/graph_index.json`.

## Principle:
*"Insight is the ability to see the invisible connection between the visible."*

