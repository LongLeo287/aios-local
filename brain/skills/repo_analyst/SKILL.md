---
name: repo_analyst
version: 1.0
tier: 3
category: analysis
description: Analyze, summarize, and compare cloned repos in AI OS knowledge base
exposed_functions:
  - summarize_repo
  - extract_patterns
  - compare_repos
  - find_best_for
dependencies:
  - knowledge_enricher
  - context_manager
---

# Repo Analyst Skill

## Purpose
Deep analysis of repos available in `knowledge/repos/` and `plugins/`.
Extracts architecture patterns, key APIs, and integration points.
Helps Antigravity understand what's available and how to use it.

## Exposed Functions

### summarize_repo(name_or_path: str) → dict
```
Reads: README.md, package.json/requirements.txt, main source files (first 100 lines)
Returns: {
  "name": str,
  "purpose": str (1 sentence),
  "tech_stack": [str],
  "key_features": [str],
  "integration_points": [str],  # APIs, CLIs, imports
  "learning_points": [str],     # What AI OS can learn from this
  "files": int,
  "size_mb": float,
  "trust_level": "HIGH|REFERENCE"
}
```

### extract_patterns(name_or_path: str) → dict
```
Identifies architecture patterns:
  - "agent_loop"        → has planning/execution/reflection cycle
  - "multi_agent"       → multiple agent roles communicating
  - "memory_system"     → vector store / episodic memory
  - "skill_plugin"      → SKILL.md / manifest.json structure
  - "webhook_server"    → Flask/FastAPI receiving webhooks
  - "cli_tool"          → command-line interface
  - "rag_pipeline"      → retrieval-augmented generation

Returns: {"patterns": {pattern_name: confidence_0_to_1}}
```

### compare_repos(name1: str, name2: str) → str
```
Side-by-side comparison formatted as markdown table:
  | Property    | name1 | name2 |
  |-------------|-------|-------|
  | Purpose     | ...   | ...   |
  | Tech Stack  | ...   | ...   |
  | Best For    | ...   | ...   |
  | Limitations | ...   | ...   |
```

### find_best_for(task: str) → list[dict]
```
task: natural language description of what you want to accomplish
Returns: top 3 repos ranked by relevance with explanation
Searches: knowledge/*, plugins/*, SKILL_REGISTRY.json descriptions
```

### generate_integration_guide(name: str) → str
```
Generates step-by-step guide for integrating a repo into AI OS:
  1. Prerequisites
  2. Install steps
  3. Configuration needed
  4. How to invoke via skill/plugin
  5. Example use case
```

## Usage Examples
```
# "What's the best repo for web scraping?"
repo_analyst.find_best_for("web scraping and crawling")
# → [firecrawl, scrapling, katana]

# "How does LightRAG work?"
repo_analyst.summarize_repo("LightRAG")

# "firecrawl vs scrapling — which is better?"
repo_analyst.compare_repos("firecrawl", "scrapling")
```
