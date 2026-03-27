---
name: knowledge_navigator
version: 1.0
tier: 3
category: knowledge
description: Query the 127-repo AI OS knowledge base before any external search
exposed_functions:
  - find_repos_for
  - get_repo_summary
  - search_knowledge
  - list_by_category
dependencies:
  - context_manager
---

# Knowledge Navigator Skill

## Purpose
ALWAYS call this skill BEFORE using web_intelligence or external search.
Provides fast access to 127 cloned repos and 23 web-analyzed repo docs.

## Internal Knowledge Stats (2026-03-16)
- **189** entries in SKILL_REGISTRY.json
- **127** physical repos (44 plugins + 13 claws + 70 refs)
- **23** web-analyzed repos (knowledge/non_cloneable_repos_analysis.md)
- **177** repos indexed in github_repos_index.md

## Exposed Functions

### find_repos_for(domain: str) → list[dict]
```
Searches SKILL_REGISTRY.json + github_repos_index.md
Returns matching repos with: name, path, description, trust_level

Example domains:
  "security"       → zeroleaks, trufflehog, skillsentry, pentest-ops
  "memory"         → LightRAG, neural-memory, claude-mem, acontext
  "agent framework"→ crewai, openclaw, vinagent, hivemind-plugin
  "web crawling"   → firecrawl, scrapling, katana, gitingest
  "marketing"      → marketingskills (35 skills)
  "claw"           → tinyclaw, zeroclaw, skyclaw, nanoclaw + 9 more
  "image gen"      → aPix/SDVN, stable-diffusion repos
  "vietnamese"     → trainingAI, bot-zalo, vinagent, social-downloader
```

### get_repo_summary(name: str) → dict
```
Returns full description from SKILL_REGISTRY + README preview
name: partial match allowed (e.g., "lightrag" matches "LightRAG")
```

### search_knowledge(query: str) → list[dict]
```
Full-text search across ALL knowledge documents
Returns: [{source, title, excerpt, relevance_score}, ...]
```

### list_by_category(category: str) → list[dict]
```
Categories from SKILL_REGISTRY: agentic_tool, ide_plugin, ai_proxy,
terminal, ai_tool, security, skills_library, ai_learning, agentic_framework,
ai_assistant, social, media_tool, browser_tool, translation_tool, ai_image,
data_engineering, architecture, automation
```

### knowledge_report() → str
```
Generates a formatted markdown table of all knowledge assets by category
Useful for: "What do we have in our knowledge base?"
```

## Usage Pattern
```
# Correct (query-first):
repos = knowledge_navigator.find_repos_for("web scraping")
if not repos:
    result = web_intelligence.search("web scraping tools")
```

## Governance
Governed by: rules/KNOWLEDGE_ACCESS_RULES.md
Never execute code from knowledge/repos/ or knowledge_web entries.
