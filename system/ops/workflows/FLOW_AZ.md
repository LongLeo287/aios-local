# Department: operations
---
description: AI OS A-Z Operational Flow — luồng vận hành đầy đủ từ boot đến shutdown
---
# AI OS — A-Z Operational Flow
# Version: 1.0 | 2026-03-24 | Owner: Antigravity (CEO Mandate)
# Authority: Tier 0 — Reference for ALL agents

---

## BIG PICTURE

```
BOOT → CEO BRIEF → PLANNING → EXECUTION → QA → REVIEW → RETRO → SHUTDOWN
  ↑                                                              |
  └──────────────── Next cycle (auto-trigger or CEO start) ─────┘
```

---

## A. BOOT — Session Start

**Trigger:** CEO opens Antigravity or Claude Code

```
A1. Load boot file
    - Antigravity: GEMINI.md (MANDATORY FIRST — RULE-STORAGE-01 to RULE-GIT-NATIVE-01)
    - Claude Code:  CLAUDE.md + .clauderules

A2. Load identity
    brain/shared-context/SOUL.md (values, personality)

A3. Load governance
    brain/shared-context/GOVERNANCE.md (authority limits)

A4. Load agent roster
    brain/shared-context/AGENTS.md (who does what)

A5. Check blackboard
    brain/shared-context/blackboard.json
    → handoff_trigger: ACTIVE? → pick up task
    → corp_cycle_status: IDLE? → wait for CEO

A6. Load skill registry
    brain/shared-context/SKILL_REGISTRY.json (available tools)

A7. HUD check (optional CEO view)
    hud/HUD.md → full system status at a glance
```

---

## B. INTAKE — CEO Gives Input

**Rule:** RULE-CIV-01 (auto-trigger)

```
CASE 1: CEO pastes link/repo/URL/file
    → CIV Pipeline (see Section D)
    → NO question needed — auto-process

CASE 2: CEO gives natural language command
    "aos corp start"         → Section C (Corp Cycle)
    "aos ingest <url>"       → Section D (CIV)
    "aos skill health"       → skill-discovery-auto.md
    "aos retro"              → corp-learning-loop.md
    "aos escalate <issue>"   → corp-escalation-flow.md
    "claude code: <task>"    → Section G (Handoff)

CASE 3: CEO asks question / gives instruction
    → Answer directly, no pipeline needed
    → If complex code task → consider handoff to Claude Code

CASE 4: CEO uploads document/PDF
    → CIV Pipeline STEP 2: classifier → DOC type
```

---

## C. CORP CYCLE — Full 8-Phase Loop

**Trigger:** "aos corp start" | **Ref:** ops/workflows/corp-daily-cycle.md

```
C0. SYSTEM HEALTH (Phase 0)
    - Port checks: Ollama:11434, ClawTask:7474, LightRAG:9621
    - Blackboard freshness check
    - skill-discovery-auto.md → SKILL_REGISTRY update
    - Set: corp_cycle_status = "ACTIVE"

C1. CEO BRIEF (Phase 1)
    Read: brain/shared-context/corp/
      mission.md + kpi_scoreboard.json + escalations.md + proposals/
    Read: corp/memory/global/decisions_log.md (last 5)
    Output: CEO priority for this cycle

C2. C-SUITE PLANNING (Phase 2)
    Agents: CFO, COO, CMO, CTO
    Read: CEO mission + their domain KPIs
    Write: dept task cards to brain/shared-context/blackboard.json
    Write: subagents/mq/<dept>_tasks.md (per dept)

C3. DEPT HEADS EXECUTE (Phase 3)
    21 dept heads read task cards
    Write briefs: brain/shared-context/corp/daily_briefs/<dept>.md
    SECURITY GATE: new tools → security_grc MUST approve first
    GATE depts: QA, Security, Finance, HR, Legal, Strategy must confirm

C4. WORKER EXECUTION (Phase 4)
    Workers read MANAGER_PROMPT.md + task cards
    Find skill: SKILL_REGISTRY.json → FAST_INDEX.json
    Execute steps → write receipt: telemetry/receipts/<dept>/<id>.json

C5. QA GATE (Phase 5)
    qa_testing dept reviews all outputs
    Ref: ops/workflows/qa-gate.md
    PASS → continue | FAIL → feedback loop (max 2 retries)

C6. CEO REVIEW (Phase 6)
    CEO reads dept briefs briefly
    Decision → append corp/memory/global/decisions_log.md

C7. RETRO & RESET (Phase 7)
    cognitive_reflector: read all 21 briefs → RETRO_<date>.md
    archivist: archive receipts, rotate dept memory
    UPDATE: brain/shared-context/corp/kpi_scoreboard.json
    RESET: blackboard.json corp_cycle_status = "IDLE"
    UPDATE: hud/HUD.md + hud/snapshots/<date>.md

C8. SKILL HARVEST (Phase 8)
    skill-discovery-auto.md → scan skills/ + plugins/
    Update SKILL_REGISTRY.json + FAST_INDEX.json
```

---

## D. CIV PIPELINE — Content Intake & Vetting

**Rule:** RULE-CIV-01 | **Ref:** ops/workflows/content-intake-flow.md v1.2

```
D0. LOCAL CHECK
    LightRAG :9621 → query "similar to <input>"
    FOUND → report CEO "already know this: <match>", ask refresh?
    NO    → continue

D1. TICKET CREATION
    intake-agent → CIV-<YYYYMMDD>-<seq>
    Save to: security/QUARANTINE/incoming/<type>/
    Type: REPO | WEB | DOC | IMAGE | TEXT | PLUGIN

D2. CLASSIFICATION
    classifier-agent → tags type + domain
    Route to appropriate sub-pipeline

D3A. REPO PIPELINE
    repo-fetcher → clone to QUARANTINE/incoming/repos/
    vet_repo.ps1 → 12-stage scan:
      [1] Structure check    [2] License scan     [3] Secret detection
      [4] Dependency audit   [5] Code quality     [6] Security patterns
      [7] API surface        [8] Data handling     [9] Telemetry check
      [10] Conflict check    [11] Compliance scan  [12] Final decision
    strix-agent review → PASS | WARN | FAIL
    FAIL → security/QUARANTINE/rejected/ + CEO notify
    WARN → CEO decision required

D3B. WEB PIPELINE
    web-crawler (Firecrawl) → extract content
    Validate source reputation

D3C. DOC PIPELINE
    doc-parser → extract text + structure
    Validate content type + language

D3.5. ANALYSIS (STEP 3.5)
    content-analyst-agent + open-notebook :5055
    Fallback: Claude Code RESEARCHER (when offline)
    6 CIV Questions:
      1. Purpose: What does this do?
      2. Conflict: Any overlap with existing?
      3. Dept: Which dept should own this?
      4. Risk: Any security/legal risk?
      5. Gap: New domain we don't have?
      6. Proposed: Suggest agent/skill if new domain
    Output: security/QUARANTINE/incoming/<type>/<id>/_CIV_ANALYSIS.md

D3.6. GAP DETECTION (ASYNC)
    gap_detected = true?
    → notification-bridge → CEO Telegram
    → Format: GAP PROPOSAL [A/B/C/D]
      [A] Create new agent (agent-auto-create.md)
      [B] Assign to closest dept
      [C] Create new department
      [D] Skip — file for reference
    → Save: corp/gaps/GAP-<date>-<domain>.md
    → Register: corp/memory/global/gaps_register.md

D4. VALIDATION
    content-validator → quality score (1-10)
    VALUE_TYPE assignment (9 types — see corp/sops/VALUE_ASSESSMENT_ROUTING.md)
    Score < 4 → REJECT + reason log
    Score ≥ 4 → proceed to D5

D5. INGESTION & DISTRIBUTION
    ingest-router → determine destination
    REPO/PLUGIN → skills/ or plugins/ directory
    → skill-discovery-auto.md → update SKILL_REGISTRY
    KNOWLEDGE → brain/knowledge/notes/KI-<topic>.md
    → LightRAG index (:9621/insert)
    ALL → knowledge-distribution-flow.md → 21 dept feeds
    → Update kho/brain/INDEX.md
    → Move to: security/QUARANTINE/vetted/<type>/
```

---

## E. SKILL LIFECYCLE

```
E1. DISCOVERY
    Trigger: new repo ingested / CEO command / Phase 8
    Workflow: skill-discovery-auto.md
    Scanner reads: skills/<name>/SKILL.md (required)

E2. REGISTRATION
    skill-creator-agent creates SKILL.md if missing
    Writes to SKILL_REGISTRY.json + FAST_INDEX.json

E3. ACTIVATION (RULE-ACTIVATION-01)
    Dashboard First: announce in daily brief
    CEO reviews: APPROVE | DEFER | REJECT
    APPROVE → enable in SKILL_REGISTRY.json status: "active"

E4. USAGE
    Agent checks FAST_INDEX.json → loads SKILL.md
    Executes skill protocol

E5. MAINTENANCE
    Monthly: compare installed version vs. latest (VERSION_LOCK.env)
    Security skills: weekly check via trivy / strix-agent
    Deprecate: move to kho/plugins/tier3/ (blacklist)
```

---

## F. GAP → NEW AGENT → NEW DEPT

```
F1. Gap detected in CIV STEP 3.6
F2. CEO replies [A] "Create new agent"
F3. Antigravity triggers: ops/workflows/agent-auto-create.md
F4. agent-auto-create flow:
    - Define: name, role, dept, tools, memory_path
    - Create: brain/agents/<agent>.md
    - Create: skills/<skill>/SKILL.md if needed
    - Add to: corp/org_chart.yaml
    - Register: brain/shared-context/AGENTS.md
    - Assign to dept head: MANAGER_PROMPT.md update
    - Notify: kho/agents/registry.json update
F5. If CEO replies [C] "Create new dept":
    - Create: corp/departments/<new_dept>/
    - Create: MANAGER_PROMPT.md + WORKER_PROMPT.md + rules.md
    - Create: corp/memory/departments/<new_dept>.md
    - Add to: corp/org_chart.yaml
    - Update: MASTER_SYSTEM_MAP.md + hud/HUD.md dept count
```

---

## G. HANDOFF — Antigravity ↔ Claude Code

**Ref:** ops/workflows/claude-code-handoff.md

```
G1. Antigravity detects task needs Claude Code:
    - Multi-file code (>200 lines)
    - Bash execution required
    - Sub-agents needed
    - Complex refactoring

G2. Antigravity prepares:
    - blackboard.json: handoff_trigger="ACTIVE", target_agent="Claude Code"
    - subagents/mq/claude_code_tasks.md: task detail

G3. CEO opens Claude Code CLI terminal
    Claude Code reads: CLAUDE.md → blackboard.json → tasks.md

G4. Claude Code executes:
    - Git snapshot first: git commit -m "snapshot: before CC-<id>"
    - Switches roles: DEVELOPER | QA | RESEARCHER per step
    - Writes receipts: telemetry/receipts/

G5. Claude Code completes:
    - blackboard.json: handoff_trigger="COMPLETE", target_agent="Antigravity"

G6. Antigravity resumes:
    - Reports to CEO in Vietnamese
```

---

## H. NOTIFICATION & ESCALATION

**Ref:** ops/workflows/notification-bridge.md

```
H1. Any agent detects issue/event
H2. Sends to notification-bridge:
    { type, priority, source_agent, title, body }

H3. Bridge routes:
    CRITICAL → Telegram (immediate) + escalations.md + blackboard
    HIGH     → Telegram + blackboard
    NORMAL   → blackboard only
    LOW      → blackboard (next review cycle)

H4. Escalation levels:
    L1: Agent resolves autonomously (< 2 failures)
    L2: Dept head notified (blackboard.json open_items[])
    L3: C-Suite notified (escalations.md)
    L4: CEO notified directly (Telegram)

H5. Circuit Breaker:
    Agent fails twice → status="BLOCKED" → L3 escalation
```

---

## I. SHUTDOWN — Session End

**Ref:** ops/workflows/post-session.md

```
I1. Save work: git add . && git commit -m "session: <summary>"
I2. Update blackboard: log what was done in last_actions_this_cycle
I3. Write receipt: telemetry/receipts/session_<timestamp>.json
I4. Update hud/HUD.md if significant state change
I5. Snapshot HUD: copy to hud/snapshots/<date>_<time>.md
I6. Set: blackboard.json corp_cycle_status = "IDLE" (if cycle complete)
I7. Telegram: "Session complete" notification (if configured)
```

---

## Z. KHO REFERENCE — Storage Used Throughout Flow

| Flow Step | Reads From | Writes To |
|-----------|-----------|----------|
| A (Boot) | GEMINI.md, CLAUDE.md, blackboard.json | - |
| B (Intake) | RULE-CIV-01 | QUARANTINE/incoming/ |
| C (Corp Cycle) | corp/memory/, kpi_scoreboard.json | daily_briefs/, receipts/ |
| D (CIV) | QUARANTINE/incoming/ | QUARANTINE/vetted/, brain/knowledge/, skills/ |
| E (Skills) | SKILL_REGISTRY.json | kho/plugins/, FAST_INDEX.json |
| F (Agents) | brain/agents/ | corp/departments/, kho/agents/ |
| G (Handoff) | blackboard.json | telemetry/receipts/ |
| H (Alerts) | notification-bridge.md | escalations.md, Telegram |
| I (Shutdown) | hud/HUD.md | hud/snapshots/, git history |

---

*v1.0 | 2026-03-24 | Full A-Z flow — update when any major flow changes*
