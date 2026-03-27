# AI OS Corp — Vocabulary & Glossary
# Maintained by: OD & Learning Dept
# Last updated: 2026-03-20 (Cycle 3)

---

## Core Corp Terms

| Term | Definition |
|------|-----------|
| **CYCLE** | One full 7-phase operational day for AI OS Corp. Named numerically: Cycle 1, Cycle 2, etc. |
| **SPRINT** | A focused execution period within a cycle, typically scoped to 1-2 depts. |
| **MQ (Message Queue)** | Files in `subagents/mq/<dept>_tasks.md` — the official task dispatch channel from C-Suite to Dept Heads. |
| **GATE** | Quality checkpoint a task must pass before being marked DONE. Four gates: QA, Content, Security, Legal. |
| **RECEIPT** | Proof-of-completion document written by the reviewer agent after a GATE pass. Stored in `telemetry/qa_receipts/`. |
| **BLACKBOARD** | `shared-context/blackboard.json` — Corp-wide state tracker. Real-time snapshot of session. |
| **BRIEF** | A dept's daily output document. Stored in `corp/daily_briefs/<dept>.md`. |
| **RETRO** | End-of-cycle retrospective. Stored in `corp/proposals/RETRO_<date>.md`. |
| **OKR** | Objective & Key Result. Corp measurement framework. Defined in `corp/proposals/OKR_*.md`. |
| **HANDOFF** | Final section of a daily brief directing output to the next receiving dept. |
| **ESCALATION** | Formal issue raise when a task is blocked. L1→Worker, L2→Manager, L3→C-Suite, L4→CEO. |

## Agent Tiers

| Tier | Label | Description |
|------|-------|-------------|
| T0 | CEO | Sếp (human). Ultimate authority. |
| T1 | Orchestrator | Antigravity. Corp-wide orchestration. Acts as CEO proxy. |
| T2 | C-Suite | CTO, CMO, COO, CFO, CSO. Dept oversight + strategic decisions. |
| T3 | Dept Head | Per-dept manager agents. Executes MQ tasks. Writes daily briefs. |
| T4 | Worker | Specialist agents. Execute specific sub-tasks under dept head. |

## Task Status Labels

| Status | Meaning |
|--------|---------|
| `todo` | Defined, not started |
| `in_progress` | Active execution |
| `blocked` | Cannot proceed — escalation required |
| `in_review` | Waiting for GATE decision |
| `done` | GATE passed, receipt written |
| `deferred` | Intentionally moved to future cycle |
| `cancelled` | Dropped — no longer needed |

## File Conventions

| Convention | Example | Meaning |
|-----------|---------|---------|
| `<DEPT>-<CYCLE>-<SEQ>` | `ENG-01-001` | Task ID format |
| `RETRO_<YYYY-MM-DD>.md` | `RETRO_2026-03-20.md` | Retrospec file |
| `OKR_CYCLE<N>_<date>.md` | `OKR_CYCLE1_2026-03-20.md` | OKR document |
| `C<N>-<DEPT>-<SEQ>` | `C2-ENG-001` | Cycle-prefixed task (Cycle 2+) |

## Infrastructure Shorthand

| Short | Meaning |
|-------|---------|
| ClawTask | Task management API at `localhost:7474` |
| `blackboard` | `shared-context/blackboard.json` |
| `mq/` | `subagents/mq/` — message queues |
| Strix | Security vetting agent/protocol (v2.0) |
| GATE_QA | Engineering output quality check |
| GATE_SECURITY | Strix-based repo/plugin security scan |
| GATE_CONTENT | Document quality + format review |
| GATE_LEGAL | License + compliance review |

## Corp Abbreviations

| Abbr | Full Form |
|------|----------|
| ENG | Engineering |
| OPS | Operations |
| REG | Registry & Capability |
| STR | Strategy |
| HLT | System Health |
| MKT | Marketing |
| HR | HR & People |
| SEC | Security GRC |
| FIN | Finance |
| PMO | Planning & PMO |
| OD | OD & Learning |
| QA | QA & Testing |
| IT | IT Infra |
| SUP | Support |
| CR | Content Review |
| CI | Content Intake |
| AL | Asset Library |
| CLR | Client Reception |
| MON | Monitoring & Inspection |
| RD | R&D |
| LGL | Legal |

---

*This glossary is a living document. Submit additions via `od_learning.md` daily brief.*
