---
id: KI-2026-03-22-agent-architecture-foundation
type: REFERENCE
domain: agent_architecture
dept: all
created: 2026-03-22
foundation: true
tags: ['agents', 'architecture', 'acp', 'swarm', 'orchestrator', 'react']
---

# AI OS Corp — Agent Architecture Reference

## AI OS Agent Architecture

### Agent Hierarchy
```
CEO (ClawTask + Antigravity)
  └── Orchestrator (orchestrator_pro)
        ├── Department Heads (28 agents in workforce/agents/)
        └── Task-Level Subagents (38 in workforce/subagents/)
```

### Agent Patterns Used
1. **ReAct** — Think → Act → Observe loop (antigravity default)
2. **Plan+Execute** — orchestrator_pro breaks tasks, subagents execute
3. **Reflection** — cognitive_reflector reviews completed work
4. **Swarm** — `swarm-dispatch.md` for parallel multi-agent execution
5. **Memory** — mem0 plugin for persistent cross-session agent memory

### Communication Protocols
- **ACP WebSocket** (:8765) — real-time agent-to-agent via DeepAgents main.py
- **Blackboard** (`brain/shared-context/blackboard.json`) — shared async state
- **ClawTask API** (:7474) — REST task dispatch, status tracking
- **Telegram** (:3000) — human-in-the-loop via nullclaw bot

### Key Agents
| Agent | Role | Dept |
|-------|------|------|
| orchestrator_pro | Task decomposition | All |
| knowledge_agent | KI ingest + retrieval | R&D |
| security_agent | Code scan + threat check | Security |
| archivist | Long-term memory consolidation | Knowledge |
| repo_ingest_agent | Repository onboarding | Engineering |

---
*Foundation KI — created 2026-03-22*
