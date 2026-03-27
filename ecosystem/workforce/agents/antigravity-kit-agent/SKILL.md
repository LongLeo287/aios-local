---
name: antigravity-kit-orchestrator
display_name: "Antigravity Kit Orchestrator"
description: >
  Transforms AI agents into a 20-specialist multi-agent dev environment with
  intelligent routing, 40+ skill files, 11 workflow templates, and slash commands.
  Based on the popular vudovn/antigravity-kit (open-source kit for Antigravity IDE).
tier: "2"
category: agent
role: KIT_ORCHESTRATOR
source: https://github.com/vudovn/antigravity-kit
emoji: "🧰"
tags: [antigravity, multi-agent, routing, skills, slash-commands, kit, orchestrator]
activation: "[AG-KIT] /create <task> | /orchestrate <multi-agent goal>"
install: "npx @vudovn/ag-kit init"
---
# Antigravity Kit Orchestrator
**Source:** [vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit)  
**Install:** `npx @vudovn/ag-kit init` (zero-config)

## 20 Specialist Agents (auto-routed)

| Domain | Agents |
|---|---|
| **Engineering** | Frontend, Backend, Security Auditor, Debugger, QA |
| **Product** | Project Manager, UX Designer |
| **Ops** | DevOps, MCP Builder, Database |
| **Content** | SEO Agent, Content Writer |
| **AI/Dev** | Game Dev, API Designer, Docker Specialist |

## 40+ Skills Library
React patterns · TypeScript · Docker commands · Security audits · API design · Database validation · MCP building · Brainstorming · Content optimization · Debugging protocols

## 11 Slash Commands
```
/create       → new feature or app from scratch
/review       → code quality review
/brainstorm   → explore design options
/debug        → systematic debugging flow
/deploy       → deployment pipeline
/enhance      → improve existing code
/orchestrate  → coordinate multiple agents
/plan         → granular task breakdown
/preview      → local preview changes
/status       → project status report
/test         → generate and run tests
```

## Socratic Gate Protocol
Before implementation, the kit asks:
- **New features**: clarify goal, scope, users
- **Bug fixes**: confirm understanding + impact
- **Vague requests**: strategic questions first

## Auto Context
Drop files into `.context/` → auto-injected into every prompt  
Drop Python functions into `engine/src/tools/` → auto-discovered as tools

## AI OS Alignment
Kit's 20 specialists overlap with AI OS's 23 agents — use for cross-compatible routing.
