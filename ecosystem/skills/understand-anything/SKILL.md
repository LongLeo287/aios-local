---
name: understand-anything
description: Turn any codebase into an interactive knowledge graph you can explore, search, and ask questions about. Use when onboarding to a new codebase, doing impact analysis, or helping junior devs navigate complex repos.
---

# Understand Anything — Codebase Knowledge Graph

## When to Use
- Onboarding to a new codebase or module
- Understanding unfamiliar code before making changes
- Diff impact analysis (what does changing X break?)
- Helping team members navigate a complex repo

## Setup (One-time per project)
```bash
# Already installed as Antigravity plugin
# Activate with:
/understand-anything analyze
# Or:
/ua analyze
```

## Commands

### Analyze Codebase
```bash
/ua analyze --path ./         # Analyze current directory
/ua analyze --path ./src      # Analyze specific folder
```

### Explore Knowledge Graph
```bash
/ua explore                   # Open interactive dashboard
/ua search "authentication"   # Fuzzy + semantic search
/ua ask "How does auth work?" # Plain English questions
```

### Get Guided Tour
```bash
/ua tour                      # Generate guided walkthrough
/ua tour --persona junior     # Adapt to experience level
```

### Diff Impact Analysis
```bash
/ua diff HEAD~1               # What does this change affect?
/ua diff --file auth.py       # Impact of specific file change
```

### Visualize Layers
```bash
/ua layers                    # Show architectural layers
/ua graph --module payments   # Module-specific graph
```

## Output
- Interactive knowledge graph (browser dashboard)
- Plain-English summaries per module
- Persona-adaptive UI (Junior Dev / PM / AI Developer)
- Dependency maps and call graphs

## Multi-Platform Install
```bash
# Antigravity (current agent — already active)
# Plugin installed at: skills/understand-anything/

# Claude Code
claude mcp add understand-anything

# Codex
codex plugin install understand-anything
```

## Notes
- Source: github.com/Lum1104/Understand-Anything
- Built with multi-agent pipeline
- Antigravity natively supported
- Owner: Dept 1 (Engineering) — use for code review + onboarding
