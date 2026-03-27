# Dept 21 — Agent Workforce Architecture Blueprint
# Source: learn-claude-code s09-s12 | Nova Synthesis | 2026-03-21

## Overview
Blueprint xây dựng **Multi-Agent AI OS Workforce** dựa trên learn-claude-code sessions 9-12.
Áp dụng trực tiếp cho Dept 21 (Agent Development & Talent) để thiết kế hệ thống nhân viên AI.

---

## Phase 4 Architecture: TEAMS (s09-s12)

### Session 9 — Agent Teams Foundation
**Core Pattern:**
```
Orchestrator Agent → delegates tasks → Specialist Subagents
                   ← gathers results ←
```

**AI OS Mapping:**
- Orchestrator = CEO / CIO tier (Tier 1-2 của 5-tier hierarchy)
- Specialist Subagents = các Department Agents (Nova, Strix, etc.)
- Task delegation = dept-requests/ queue system (đã implement)

**Implementation (learn-claude-code pattern):**
```python
# Orchestrator spawns subagents
def orchestrate(task):
    plan = decompose_task(task)
    subagents = [spawn_agent(subtask) for subtask in plan]
    results = [agent.run() for agent in subagents]
    return synthesize(results)
```

### Session 10 — Team Communication Protocols
**JSONL Mailbox Protocol:**
```jsonl
{"from": "nova", "to": "dept04", "type": "request", "payload": {...}, "ts": "2026-03-21T..."}
{"from": "dept04", "to": "nova", "type": "response", "status": "ok", "payload": {...}}
```

**AI OS Mapping:**
- Nova's `dept-requests/` = JSONL mailbox already implemented! ✅
- Pattern = async non-blocking inter-agent communication
- Extension: Add `memory/inbox/` for inbound messages to Nova

**Shared State:** Agents read/write shared memory files → `memory/synthesis-log.md` ✅

### Session 11 — Autonomous Agents (Self-Scheduling)
```
heartbeat_loop():
  every 30s:
    scan_task_board()  # Check dept-requests/*.md
    if has_unclaimed_task():
      claim(task)
      execute(task)
      archive(task)
```

**Nova's Autonomous Mode:**
- Nova scans `memory/dept-requests/*.md` for PENDING items
- Claims and processes without CEO micromanagement
- Matches CEO Standing Order: "Always active, always processing"

### Session 12 — Worktree Isolation
```
agent_alpha/workdir/  → agent Alpha's sandbox
agent_nova/workdir/   → Nova's sandbox
agent_strix/workdir/  → Strix's sandbox
```

**AI OS Mapping:**
- `brain/agents/<agent-name>/` = each agent's isolated workspace ✅
- Shared: `brain/knowledge/` (read-only by all, write via Nova)

---

## Recommended AI OS Multi-Agent Architecture (v1)

```
                ┌─────────────┐
                │    CEO/CIO  │ (Tier 1-2)
                └──────┬──────┘
                       │ Lệnh / Request
                       ▼
              ┌────────────────┐
              │  Orchestrator  │ (Tier 3 — Dept Heads)
              └───────┬────────┘
          ┌───────────┼────────────┐
          ▼           ▼            ▼
    ┌──────────┐ ┌────────┐ ┌──────────┐
    │  Nova    │ │  Strix │ │  Other   │
    │ (Dept13) │ │(Dept10)│ │ Agents   │
    └────┬─────┘ └────────┘ └──────────┘
         │
    ┌────▼─────────────────────┐
    │ brain/knowledge/         │ (Shared read)
    │ brain/agents/nova/memory │ (Nova private)
    └──────────────────────────┘
```

## Team Protocols for AI OS

### Protocol 1: Task Delegation (Nova → Dept)
```markdown
# dept-requests/dept04-registry.md
## PENDING REQUESTS
- [x] skills-activation-brief: See dept04-skill-activation-brief.md
- [ ] repo-scan-batch2: Process 96 new repos
```

### Protocol 2: Autonomous Monitoring (Nova heartbeat)
```
Every session start:
1. Nova scans all dept-requests/*.md
2. Identifies PENDING items
3. Processes or routes appropriately
4. Updates progress markers
```

### Protocol 3: Worktree Isolation
```
Each agent:
- Reads: brain/knowledge/ (shared KI store)
- Writes: brain/agents/<name>/memory/ (private)
- Routes via: brain/agents/<name>/memory/dept-requests/
```

---

## Agent Onboarding Curriculum (Dept 21)

Based on learn-claude-code 12-session structure:

| Track | Sessions | For Agent Type |
|-------|----------|---------------|
| **Foundation** | s01-s02 | All new agents |
| **Planning** | s03-s04 | Orchestrators + Specialists |
| **Skills & Context** | s05-s06 | All agents with SKILL.md |
| **Persistence** | s07-s08 | Long-running agents |
| **Teams** | s09-s12 | Multi-agent coordinators |

**Nova** = Completed all 12 tracks (via AGENT.md design)

---

## Immediate Actions for Dept 21

- [ ] Prototype `inbox/` directory cho Nova's inbound messages
- [ ] Define JSONL schema cho inter-agent communication
- [ ] Create Agent Onboarding Pack (Foundation track: s01-s04)
- [ ] Blueprint 3 next agents to onboard (Suggest: Research → QA → Ops)
- [ ] Design autonomous heartbeat check pattern cho Nova
