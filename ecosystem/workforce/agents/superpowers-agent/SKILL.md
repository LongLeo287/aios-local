---
name: superpowers-workflow
display_name: "Superpowers Workflow Agent"
description: >
  Transforms AI coding agents from reactive assistants into senior developers
  via structured TDD-enforced workflow: Brainstorm → Plan → Execute (subagents)
  → Review. Enforces RED-GREEN-REFACTOR, DRY/YAGNI, and Spec-compliance.
tier: "2"
category: agent
role: WORKFLOW_ARCHITECT
source: https://github.com/obra/superpowers
emoji: "⚡"
tags: [tdd, planning, brainstorming, subagent, workflow, code-review, git-worktree, agent]
activation: "[SUPERPOWERS] /superpowers:brainstorm <feature idea>"
---
# Superpowers Workflow Agent
**Source:** [obra/superpowers](https://github.com/obra/superpowers)  
**Activation:** `/superpowers:brainstorm` → `/superpowers:write-plan` → `/superpowers:execute-plan`

## Workflow Phases

| Phase | Command | What happens |
|---|---|---|
| **1. Brainstorm** | `/superpowers:brainstorm` | Socratic questioning → design options → user approval |
| **2. Plan** | `/superpowers:write-plan` | Break work into 2-5 min tasks with file paths + verification |
| **3. Execute** | `/superpowers:execute-plan` | Dispatch fresh subagents per task, 2-stage review |
| **4. Review** | Auto | Severity-based code review after each task |

## Core Rules

1. **TDD Mandatory**: Write failing tests BEFORE writing code (RED → GREEN → REFACTOR)
2. **No premature code**: If code is written before tests → auto-deleted
3. **DRY + YAGNI**: No duplication, no speculative features
4. **Subagent per task**: Each task gets a fresh context window
5. **Git worktrees**: Parallel task branches for independent development

## Slash Commands
```
/superpowers:brainstorm   → clarify the problem space
/superpowers:write-plan   → generate granular task list
/superpowers:execute-plan → run all tasks autonomously
/superpowers:debug        → systematic root cause tracing
/superpowers:review       → code quality gate check
```

## AI OS Integration
This workflow pattern aligns with the AI OS **BMAD Sprint** Cowork template.  
Use `superpowers:execute-plan` to drive Claude Code subagent delegation autonomously.
