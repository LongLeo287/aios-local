# AI OS Corp -- Master System Map
# Version: 2.0 | Date: 2026-03-24 | Owner: Antigravity
# Authority: Tier 0 -- Single Source of Truth for all operational flows
# NOTE: v2.0 rewritten clean UTF-8 (v1.0 had cp1252 corruption)

---

## 1. BOOT SEQUENCE

Using Antigravity? --> Read GEMINI.md   (loads FIRST every session)
Using Claude Code? --> Read CLAUDE.md

Antigravity: GEMINI.md -> AI_OS_CONTEXT.md -> blackboard.json -> SKILL_REGISTRY.json
Claude Code: CLAUDE.md -> SOUL.md -> GOVERNANCE.md -> AGENTS.md -> blackboard.json

---

## 2. CORP DAILY CYCLE (8 Phases)

Trigger: "aos corp start" | Ref: system/system/ops/workflows/corp-daily-cycle.md

Phase 0: SYSTEM HEALTH (ports, blackboard, skill-discovery-auto)
Phase 1: CEO BRIEF (mission, kpi, escalations, proposals)
Phase 2: C-SUITE PLANNING (depts goals -> blackboard)
Phase 3: DEPT HEADS EXECUTE (21 dept briefs)
Phase 4: WORKER EXECUTION (tasks -> receipts)
Phase 5: QA GATE (system/system/ops/workflows/qa-gate.md)
Phase 6: CEO REVIEW (-> decisions_log.md)
Phase 7: RETRO & RESET (RETRO_<date>.md, kpi update, IDLE reset)
Phase 8: SKILL HARVEST (skill-discovery-auto -> SKILL_REGISTRY update)

---

## 3. DEPT STRUCTURE -- 21 Departments

TIER 0: EXECUTIVE
  CEO (Human) | C-Suite: CFO, COO, CMO, CTO

TIER 1: CORE BUSINESS (11 depts)
  01 Engineering         backend-architect-agent   [AUTONOMOUS]
  02 QA Testing          test-manager-agent        [GATE]
  03 IT Infra            it-manager-agent          [AUTONOMOUS]
  04 Marketing           growth-agent              [AUTONOMOUS]
  05 Support             channel-agent             [AUTONOMOUS]
  06 HR & People         hr-manager-agent          [GATE]
  07 system/security/GRC        strix-agent               [GATE -- ALL new tools]
  08 Finance             cost-manager-agent        [GATE]
  09 Planning/PMO        pmo-agent                 [AUTONOMOUS]
  10 Monitoring          monitor-agent             [AUTONOMOUS]
  11 Operations          ops-agent                 [AUTONOMOUS]

TIER 2: SPECIALIZED (7 depts)
  12 Legal               legal-agent               [GATE]
  13 R&D                 rd-lead-agent             [AUTONOMOUS]
  14 OD/Learning         learning-agent            [AUTONOMOUS]
  15 Client Reception    reception-agent           [AUTONOMOUS]
  16 Strategy            product-manager-agent     [GATE]
  17 System Health       system-health-agent       [AUTONOMOUS]
  18 Content Review      review-chief-agent        [GATE]

TIER 3: GOVERNANCE (3 depts)
  19 Content Intake/CIV  civ-agent                 [GATE 1 -- All External]
  20 Registry/Capability registry-manager-agent    [AUTONOMOUS]
  21 Asset Library       library-manager-agent     [AUTONOMOUS]

TIER 4: FACILITY (1 dept)
  22 Cleanup & Sanitation facility-agent           [AUTONOMOUS] -- Skill: facility_cleanup

---

## 4. PLUGIN TIERS (RULE-TIER-01)

TIER 1 (always on): Mem0, Firecrawl, LightRAG, CrewAI, GitNexus
TIER 2 (lazy-load): vibe-kanban, agentune, tai-video, etc.
TIER 3 (blacklisted): Conflict with Tier 1 -- abort on detection

---

## 5. CIV PIPELINE v1.2

Rule: RULE-CIV-01 in GEMINI.md + CLAUDE.md
Ref:  system/system/ops/workflows/content-intake-flow.md

STEP 0: LightRAG :9621 local check
STEP 1: CIV ticket -> system/security/QUARANTINE/incoming/<type>/
STEP 2: classifier-agent -> REPO|WEB|DOC|IMAGE|TEXT|PLUGIN
STEP 3A (REPO): vet_repo.ps1 (12-stage) + strix scan
STEP 3.5: content-analyst (open-notebook :5055 OR Claude Code fallback) -- 6 Qs
STEP 3.6: GAP PROPOSAL -> CEO Telegram [A/B/C/D] (ASYNC)
STEP 4: content-validator -> quality score + VALUE_TYPE (9 types)
STEP 5: ingest-router -> skill-discovery-auto + knowledge-distribution-flow

---

## 6. COMMAND MAP

aos corp start    -> corp-daily-cycle.md (full 8 phases)
aos corp brief    -> Phase 1 CEO BRIEF only
aos ingest <url>  -> content-intake-flow.md
aos skill health  -> skill-discovery-auto.md
aos retro         -> corp-learning-loop.md
Any link/repo/URL -> RULE-CIV-01 (auto-trigger CIV)

---

## 7. SKILLS (14 installed)

Registry: brain/shared-context/SKILL_REGISTRY.json
Fast Index: brain/shared-context/FAST_INDEX.json

agent-shield | agentshield | agentune | context7 | continuous-learning-v2
ecc-patterns | framework-standards | git-mcp | observability | sequential-thinking
tai-video | trivy | understand-anything | vibe-kanban

---

## 8. SERVICES

Ollama        :11434  LIVE   (gemma2:2b + nomic-embed-text)
ClawTask API  :7474   LIVE   (8 modules: llm,ollama,bot,notebook,setup,gitnexus,ag_auto,deepagents)
GitNexus      :4747   LIVE   (local code graph â€” ecosystem/tools/gitnexus/gitnexus_server.py)
ag-auto-accept :7476  LIVE   (subprocess auto-accept â€” ecosystem/tools/ag-auto-accept/ag_auto_accept.py)
DeepAgents ACP :8765  LIVE   (agent comms protocol â€” ecosystem/ecosystem/plugins/deepagents/main.py)
LightRAG      :9621   START: python system/system/ops/scripts/lightrag_server.py
open-notebook :5055   FALLBACK: Claude Code RESEARCHER role
Langfuse/LobeChat    [ASSIMILATED] -> monitor-agent & channel-agent (Plug & Play Strategy)

---

## 9. NOTIFICATIONS

Ref: system/system/ops/workflows/notification-bridge.md
Config: .env TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID (@aios_corp_bot)

Alert -> Telegram | blackboard.json | escalations.md | system/telemetry/receipts/
Types: GAP_PROPOSAL, SECURITY_ALERT, CIV_COMPLETE, SYSTEM_ERROR, ...

---

## 10. CANONICAL PATHS

brain/shared-context/brain/corp/kpi_scoreboard.json
brain/shared-context/brain/corp/escalations.md
brain/shared-context/brain/corp/mission.md
brain/shared-context/brain/corp/proposals/
brain/shared-context/brain/corp/daily_briefs/
brain/shared-context/blackboard.json
brain/shared-context/SKILL_REGISTRY.json
brain/brain/corp/memory/departments/<dept>.md
brain/brain/corp/memory/global/decisions_log.md
brain/brain/corp/memory/global/gaps_register.md
brain/brain/corp/gaps/GAP-<date>-<domain>.md
system/security/QUARANTINE/
system/telemetry/receipts/
AOS_ROOT: d:\AI OS CORP\AI OS

---

## 11. HANDOFF PROTOCOL

Ref: system/system/ops/workflows/claude-code-handoff.md

Antigravity -> Claude Code:
  blackboard.json handoff_trigger:ACTIVE + target_agent:Claude Code
  ecosystem/subagents/mq/claude_code_tasks.md (task detail)

Claude Code unique capabilities:
  bash execution | sub-agents isolated context | 200K code gen | DEVELOPER->QA self-review

Claude Code -> Antigravity:
  blackboard.json handoff_trigger:COMPLETE + target_agent:Antigravity

---

*v2.0 | 2026-03-24 | Clean UTF-8 rewrite*

