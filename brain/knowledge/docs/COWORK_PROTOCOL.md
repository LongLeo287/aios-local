# COWORK_PROTOCOL.md — AI OS Multi-Agent Collaboration Standard
# Version: 1.0 | Date: 2026-03-17
# Authority: Tier 2

---

## What Is a Cowork Session?

A **Cowork Session** is a coordinated multi-agent collaboration where 2+ AI agents
(potentially on different models) work in parallel on a shared problem, with
structured handoffs and context sharing.

---

## Session Bootstrap

```
1. orchestrator_pro receives cowork request
2. Assigns roles to agents:
   - Define: [ROLE] → [MODEL] → [OBJECTIVE]
   - Example: ARCHITECT → Claude → "Design the data model"
              DEVIL'S_ADVOCATE → GPT-4o → "Challenge all assumptions"

3. Create shared context doc: cowork/sessions/<name>/context.md
4. Launch: open-claude-cowork (or parallel Antigravity instances)
5. Set synchronization cadence: every N turns OR on major output
```

---

## Role Assignment Rules

| Rule | Description |
|---|---|
| **Single owner** | Each task subtask has exactly ONE owner agent |
| **No duplication** | Two agents never work on same subtask simultaneously |
| **Handoff explicit** | Agent says "HANDING OFF TO [ROLE]:" before passing |
| **Context shared** | All agents READ shared context; only owner WRITES |
| **Escalation path** | Disagreement → orchestrator_pro decides |

---

## Shared Context Format

```markdown
# Cowork Session: <name>
Started: <timestamp>
Agents: [ARCH: Claude] [QA: GPT-4o] [WRITER: Gemini]
Goal: <session goal>

## Agreed Decisions
- Decision 1: <what was agreed>
- Decision 2: <what was agreed>

## Open Questions
- Q1: <question> → Owner: [AGENT]
- Q2: <question> → Owner: [AGENT]

## Handoff Queue
- <from> → <to>: <what's being handed off>
```

---

## Session Templates

### Template 1: Code Review Cowork

```
AGENT 1 (Claude/Developer):
  - Write the implementation
  - Output: code diff + implementation notes

AGENT 2 (GPT-4o/Reviewer):
  - Apply 5-axis review (code-reviewer subagent protocol)
  - Output: verdict + issues list

HANDOFF: Agent 2 → Agent 1 for fixes
FINAL: Agent 1 delivers fixed code
```

### Template 2: Research + Writing Cowork

```
AGENT 1 (Gemini/Researcher):
  - Deep web research on topic
  - Output: structured findings + sources

AGENT 2 (Claude/Writer):
  - Read findings → write draft
  - Output: polished article/report

HANDOFF: Agent 1 → Agent 2 (findings)
FINAL: Agent 2 delivers publication-ready content
```

### Template 3: Architecture Review Cowork

```
AGENT 1 (Claude/Architect):
  - Design system architecture
  - Output: architecture doc + ADR

AGENT 2 (GPT-4o/Devil's Advocate):
  - Challenge all assumptions
  - Output: risk list + alternative approaches

SYNTHESIS: orchestrator_pro merges insights
FINAL: Refined architecture doc
```

### Template 4: Full Agency Cowork

```
PM (Claude):       Requirements + task breakdown
DEVELOPER (Claude Code): Implementation
QA (subagent):     Code review
DESIGNER (ui-ux-agent): UI/UX review
WRITER (content-agent): Documentation

Coordination: orchestrator_pro
Context: cowork/sessions/full-agency/context.md
```

---

## Output Collection

After each cowork session:
1. Collect outputs from all agents
2. orchestrator_pro synthesizes into final deliverable
3. Write session receipt: `telemetry/receipts/cowork_<name>_<ts>.json`
4. Archive context: `cowork/sessions/<name>/` (keep for 30 days)

---

*"A team of specialized agents outperforms any single generalist."*
