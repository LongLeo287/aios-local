---
name: vibe-kanban
description: AI-native Kanban board that orchestrates Claude Code, Codex, and other AI coding agents as workers. Use for managing multi-agent development tasks, parallel worktrees, and visual task tracking.
---

# Vibe Kanban — AI-Native Task Orchestration

## What it Does
Kanban board designed specifically for AI coding agents.
- Each card = a task that can be assigned to an AI agent
- Agents work in parallel git worktrees
- Visual overview of all AI tasks in flight
- 10X output throughput claim (272 releases — battle-tested)

## Relationship with ClawTask
| | ClawTask | Vibe Kanban |
|--|---------|------------|
| Type | Python API + LLM integration | Kanban UI + agent orchestration |
| Focus | Task tracking, escalation, KPI | Visual board + parallel agents |
| Conflict | ❌ None — different layers | Can complement |
| Use together | ClawTask = backend | Vibe Kanban = frontend board |

**Decision: No conflict — can use alongside ClawTask.**

## Quick Start
```bash
# Install (requires Node.js 18+)
npx vibe-kanban

# Or self-host:
git clone https://github.com/BloopAI/vibe-kanban
cd vibe-kanban && npm install && npm run dev
```

## Key Workflows
1. Create task card → assign to AI agent (Claude/Codex/Antigravity)
2. Agent works in isolated git worktree
3. PR created automatically when done
4. Review → merge from board

## Notes
- Source: github.com/BloopAI/vibe-kanban | 272 releases
- License: MIT
- Self-hostable
- Owner: Dept 1 (Engineering) — optional UI for managing AI dev tasks
- Status: APPROVED — no conflict with ClawTask confirmed
