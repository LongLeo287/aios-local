# [RULE-STRUCTURE-01] AI OS System & Data Structure
# Issued by: CEO LongLeo | Date: 2026-03-22 | Status: MANDATORY
# Scope: All agents — Antigravity, Claude Code, Orchestrator Pro, all Corp workers
# NOTE: No hardcoded paths per RULE-DYNAMIC-01. Use relative paths from AI_OS_ROOT.

---

## 1. SYSTEM STRUCTURE — Agent Tiers

```
TIER 0: CEO (Human — LongLeo)
         │
TIER 1: ANTIGRAVITY (Orchestrator — Gemini)
         Boot: GEMINI.md
         │
TIER 2: CLAUDE CODE CLI (Executor — only when terminal open)
         Boot: CLAUDE.md
         Fallback: ORCHESTRATOR PRO (when Claude Code offline)
         │
TIER 3: SPECIALIST AGENTS (Corp Dept Workers)
         N departments — count from corp/org_chart.yaml (do NOT hardcode)
         │
TIER 4: SUBAGENTS (spawned per task)
```

**Rule:** Higher tier ALWAYS overrides lower tier.
**Rule:** Antigravity + Claude Code share the SAME project workspace — different boot file, same data.

---

## 2. DATA STRUCTURE — Source of Truth

> **AI_OS_ROOT** = directory containing GEMINI.md + CLAUDE.md (discovered at boot, NOT hardcoded)
> All paths below are RELATIVE to AI_OS_ROOT.

```
<AI_OS_ROOT>/                             ← PROJECT ROOT (Source of Truth for ALL agents)
│
├── GEMINI.md                             ← Antigravity boot entry point
├── CLAUDE.md                             ← Claude Code boot entry point
│
├── brain/
│   ├── shared-context/                ← SHARED — all agents read/write
│   │   ├── blackboard.json            ← Active task state (ALL agents sync here)
│   │   ├── AGENTS.md                  ← Agent roster & authority
│   │   ├── SOUL.md                    ← Platform identity
│   │   ├── GOVERNANCE.md              ← Safety anchors & rules
│   │   ├── THESIS.md                  ← 34 Pillars
│   │   └── SKILL_REGISTRY.json        ← All skills index
│   │
│   ├── skills/                        ← Skill definitions (all agents load on demand)
│   │   └── [skill-name]/SKILL.md
│   │
│   └── knowledge/                     ← Reference library (all agents read)
│       ├── notes/                     ← CEO notes + rules (RULE-*.md)
│       └── repos/, web/, docs/...     ← KI artifacts
│
├── corp/
│   ├── memory/
│   │   ├── global/                    ← Cross-dept decisions, decisions_log.md
│   │   ├── agents/                    ← Per-agent memory (notebook_agent.md, etc.)
│   │   └── departments/               ← Per-dept cycle memory
│   │
│   ├── departments/                   ← N dept configs + rules + MANAGER_PROMPT (see org_chart.yaml)
│   ├── sops/                          ← Standard Operating Procedures
│   │   └── workflows/                 ← Workflow definitions
│   └── prompts/                       ← Agent prompt templates
│
├── infra/
│   └── llm/
│       └── router.yaml                ← LLM routing rules (all agents use)
│
├── ops/
│   ├── runtime/                       ← Runtime state (ephemeral, not for boot)
│   │   ├── notebooks/                 ← Notebook agent store
│   │   └── blackboard.json            ← OPS MIRROR ONLY (not source of truth)
│   ├── scripts/config.json            ← Service URLs (ports, endpoints)
│   └── workflows/                     ← Boot + daily cycle workflows
│
├── tools/
│   ├── clawtask/                      ← ClawTask API server (port 7474)
│   │   ├── module_*.py                ← Feature modules
│   │   └── tests/                     ← CI/CD tests (run only when port 7474 UP)
│   └── mcp/                           ← MCP servers (Antigravity + Claude)
│
├── plugins/                           ← External plugins (vetted via Dept: CIV)
└── channels/                          ← Remote bridges (Telegram, Discord, Zalo)
    └── telegram_bridge.py             ← Telegram (only active when service running)
```

> Paths in this diagram are RELATIVE to AI_OS_ROOT. See RULE-DYNAMIC-01 for discovery rules.

---

## 3. CRITICAL PATHS — Agents Must Know

| Data | Path | Who reads |
|------|------|-----------|
| **Blackboard (primary)** | `brain/shared-context/blackboard.json` | ALL agents at boot |
| **Blackboard (ops mirror)** | `ops/runtime/blackboard.json` | Runtime only, NOT at boot |
| **LLM routing** | `infra/llm/router.yaml` | All agents when calling LLM |
| **Service config** | `ops/scripts/config.json` | Modules needing service URLs |
| **Agent memory** | `corp/memory/agents/<name>.md` | Agent on session start |
| **Dept memory** | `corp/memory/departments/<dept>.md` | Dept head at Phase 3 |
| **Skills** | `brain/skills/<name>/SKILL.md` | Worker on task start |
| **CI/CD tests** | `tools/clawtask/tests/` | Only when port 7474 UP |
| **Telegram** | `channels/telegram_bridge.py` | Only when service connected |

---

## 4. AGENT DATA DOMAINS

| Agent | Reads | Writes |
|-------|-------|--------|
| **Antigravity** | All project files | blackboard, corp/memory, proposals, daily_briefs |
| **Claude Code** | All project files | code files, telemetry/receipts, blackboard (handoff) |
| **Corp Workers** | dept config + memory + skills | receipts, dept memory, blackboard updates |
| **Notebook Agent** | content input, blackboard | ops/runtime/notebooks/, blackboard (primary) |

---

## 5. SERVICE AVAILABILITY GATES

```
Service         Port    Active when
────────────────────────────────────────────────────
ClawTask API    7474    Docker running OR direct python start
9router         20128   Docker running
Ollama          11434   Ollama app running
Open-notebook   5055    Docker running (full mode only)
Telegram bot    3000    nullclaw bot service running
```

**Rule: Always check if service is UP before using it. Never assume.**
- CI/CD tests → only run if `localhost:7474` responds
- Telegram notify → only fire if `localhost:3000` OR `/api/telegram/test` responds
- LLM calls → use router.yaml for fallback chain (9router → Ollama → extractive)

---

## 6. SYNCHRONIZATION RULES

- **blackboard.json** is the ONLY cross-agent state sync channel
- Notebook agent writes to `brain/shared-context/blackboard.json` → all agents see it
- `ops/runtime/blackboard.json` = runtime operation mirror only (NOT for boot reads)
- **receipts** go to `telemetry/receipts/<dept>/<task-id>.json`
- **proposals** go to `shared-context/corp/proposals/PROPOSAL_<date>_<topic>.md`

---

*Issued: 2026-03-22 | All agents must load this after RULE-STORAGE-01 during boot*
