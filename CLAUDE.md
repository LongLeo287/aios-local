# CLAUDE.md â€ Claude Code Boot Protocol
# AI OS CORP | Cycle 8 | Last synced: 2026-03-23

---

## SECTION 1 â€ AGENT BOOT RULE

```
CEO má»Ÿ Claude Code CLI?
    YES â€â€â–º Read CLAUDE.md     (Claude Code boot protocol â€ THIS FILE)
    NO  â€â€â–º Read GEMINI.md     (Antigravity boot protocol)
```

**Rule:** No agent reads the wrong boot file.

---

## SECTION 2 â€ BOOT SEQUENCE (MANDATORY)

```
STEP 1  â€â€â–º Read CLAUDE.md                           (THIS FILE â€ entry point)
STEP 2  â€â€â–º Load Identity & Core Values              [brain/shared-context/SOUL.md]
STEP 3  â€â€â–º Load Governance & Rules                  [brain/shared-context/GOVERNANCE.md]
STEP 4  â€â€â–º Load Agent Roster & Roles                [brain/shared-context/AGENTS.md]
STEP 5  â€â€â–º Load Strategy & 40 Pillars               [brain/shared-context/THESIS.md]
STEP 6  â€â€â–º Load Output Format Guide                 [brain/shared-context/report_formats.md]
             (Quick selector rune: brain/corp/prompts/runes/report_formats.md)
STEP 7  â€â€â–º Check Blackboard (active tasks)          [brain/shared-context/blackboard.json]
STEP 8  â€â€â–º Load Skill Registry                      [brain/shared-context/SKILL_REGISTRY.json]
STEP 9  â€â€â–º âš¡ READ & AUTO-EXECUTE TASK QUEUE        [CLAUDE_CODE_TASKS.md]
             â†’ TÃ¬m má»i task cÃ³ Status: READY
             â†’ Nếu auto mode enabled â†’ Tá»° CHáº Y NGAY, khÃ´ng há»i CEO
             â†’ Nếu manual mode â†’ ThÃ´ng bÃ¡o CEO cÃ³ task Ä‘ang chá»
STEP 10 â€â€â–º Begin work (náº¿u khÃ´ng cÃ³ task READY)
```

**On-demand (read when needed, NOT every boot):**
```
â†’ Corp daily cycle    [system/ops/workflows/corp-daily-cycle.md]          â† Trigger: "aos corp start"
â†’ Storage rule        [brain/knowledge/notes/RULE-STORAGE-01-storage-location.md]
â†’ Structure rule      [brain/knowledge/notes/RULE-STRUCTURE-01-system-structure.md]
â†’ No-hardcode policy  [brain/knowledge/notes/RULE-DYNAMIC-01-no-hardcode.md]
â†’ Corp SOP detail     [system/ops/workflows/pre-session.md]               â† Read for freshness checks
â†’ Knowledge ingest    [system/ops/workflows/knowledge-ingest.md]          â† Trigger: "aos ingest <source>"
â†’ Agent auto-create   [system/ops/workflows/agent-auto-create.md]         â† Trigger: called by knowledge-ingest
â†’ Learning loop       [system/ops/workflows/corp-learning-loop.md]        â† Trigger: "aos corp retro"
â†’ **Handoff protocol  [system/ops/workflows/claude-code-handoff.md]       â† Trigger: nháº­n task tá»« Antigravity**
â†’ **CIV intake        [brain/corp/departments/content_intake/WORKER_PROMPT.md] â† Trigger: repo/link task**
â†’ **Master System Map [brain/corp/MASTER_SYSTEM_MAP.md]                       â† Trigger: When in doubt about any flow, mapping, or responsibility**
```

**[RULE-CIV-01 for Claude Code]** Intake link/repo qua Claude Code:
```
Náº¿u CEO Ä‘Æ°a link/repo KHI Ä‘ang dÃ¹ng Claude Code CLI:
  â†’ KHÃNG tá»± clone/read luÃ´n
  â†’ Ghi task vÃ o blackboard + ecosystem/subagents/mq/claude_code_tasks.md
### [RULE-ARCH-03] NATIVE TOOLING & SOP MANDATE
Bn KHNG C T  TO FILE TAY (Scripts, YAMLs, Agent MDs, Workflow) t con s khng! TRC BT K  TNG CP NHT H THNG NO, BN PHI DNG cc file chun trong `system/ops/workflows/`. Mi kin trc hoc tool mi phi c sinh ra t cc Workflow chnh thng. T  Build bng script ngoi l Xm Phm H Thng Trm Trng!

### [RULE-ARCH-04] MANDATORY PRE-FLIGHT SCAN (CHNG TRNG LP)
TRC khi  ra bt k File, Agent, Quy trnh, hay Tool mi no, Claude BT BUC phi chy lnh qut AI OS (`grep_search`, `list_dir`, view `ORG_GRAPH.yaml`)  xc minh 100% chc nng  cha h tn ti. Phi NNG CP h thng c thay v "Sng ch li bnh xe".

### [RULE-ARCH-05] PROACTIVE AUTO-EVOLUTION (T HC V TIN HA)
S mnh ca Claude l t Tch Ly. Khi CEO a cho bn 1 concept mi, 1 kin thc mi, 1 phng php gii quyt khc l  BN KHNG C CH LNH. Phi t ng Ha Thch tri thc : T  Phng ban, t  Agent, t  Rule, Workflow  ng gi v duy tr k nng vnh vin cho OS. S TIN HA PHI NM  MC  AUTO (T NG)!  â†’ Cháº¡y CIV pipeline: STEP 0 (LightRAG) â†’ STEP 1-5 (content-intake-flow.md)
  â†’ QUARANTINE path: <AI_OS_ROOT>\security\QUARANTINE\
  â†’ Ref: brain/corp/departments/content_intake/WORKER_PROMPT.md v1.2
```


**HARD RULE:** Skip any step = violation of AI OS governance.
Do not skip. Do not exceed authority. Do not assume.

**Boot Fallback:** If any boot step file is missing or unreadable:
â†’ Log warning, skip that step, continue with remaining steps
â†’ Report all missing files to CEO at session start â€ DO NOT assume defaults

---

## SECTION 3 â€ CLAUDE CODE SPECIFIC RULES

- **Role:** Tier 2 Executor â€ reads blackboard for tasks assigned by Antigravity
- **Active when:** CEO has Claude Code CLI terminal open
- **Fallback:** Orchestrator Pro takes over when Claude Code is offline
- **Constitution:** Must follow `.clauderules` behavioral constitution at all times
- **Receipts:** Must write receipts to `system/telemetry/receipts/` after each major step
- **2-Strike Rule:** FAIL twice on any task â†’ set `handoff_trigger=BLOCKED`, stop and report

### Behavioral Defaults
- Reporting language: Vietnamese (unless CEO instructs otherwise)
- No autonomous destructive actions without CEO confirmation
- All task completions must update `blackboard.json` â†’ `handoff_trigger: "COMPLETE"`
- Subagent messages land in `ecosystem/subagents/mq/` â€ read them before each session

`

### Plugin Usage Rules

**[RULE-TIER-01]** 3-Tier Plugin Architecture â€ Mandatory:
```
Má»i tool/plugin trong há»‡ thá»‘ng Ä‘Æ°á»£c phÃ¢n thÃ nh 3 táº§ng cá»©ng:

TIER 1 â€ Core Infra (LuÃ´n náº¡p, cháº¡y thÆ°á»ng trá»±c):
  Mem0, Firecrawl, LightRAG, CrewAI, GitNexus
  â†’ Truy cáº­p qua REST API (port 7000/7474) hoáº·c adapter import trá»±c tiáº¿p.
  â†’ KHÃNG cáº§n cÃ i Ä‘áº·t gÃ¬ thÃªm.

TIER 2 â€ Specialized Plugins (Lazy-Load / On-Demand):
  â†’ CHá»ˆ kÃ­ch hoáº¡t khi Task thá»±c sá»± cáº§n tool chuyÃªn ngÃ nh (váº½ áº£nh, Excel...).
  â†’ Quy trÃ¬nh báº¯t buá»™c: Sandbox Init â†’ Execute â†’ Teardown
  â†’ Full workflow: .agents/workflows/plugin-lazy-load.md
  â†’ TUYá»†T Äá»I khÃ´ng cÃ i Tier 2 vÃ o global env / lÃµi há»‡ thá»‘ng.

TIER 3 â€ Obsolete / Conflict (Blacklisted):
  â†’ KhÃ´ng sá»­ dá»¥ng. Conflict vá»›i Tier 1.
  â†’ Náº¿u Claude phÃ¡t hiá»‡n lá»‡nh gá»i Tier 3 â†’ Abort ngay â†’ Escalate CEO.
```

**[RULE-AGENT-MECHANICS-01]** Agent Context Mechanics â€ Know Your Runtime:
```
Learned from: claude-inspector (kangraemin) â€ applied to ALL agents in AI OS

1. BOOT FILE INJECTED EVERY REQUEST
   â†’ CLAUDE.md is loaded in EVERY single API call.
   â†’ Keep boot file lean. Remove stale rules. Every token = cost.

2. MCP TOOLS ARE LAZY-LOADED
   â†’ tools[] grows as MCP servers init. Expected behavior (validates 3-Tier).

3. IMAGES = BASE64 INLINE â€ EXPENSIVE
   â†’ Only send images when visual context is truly necessary.

4. SKILL â‰  COMMAND â€ DIFFERENT INJECTION PATHS
   â†’ Skills (ecosystem/skills/) and Commands (.claude/commands/) inject differently.
   â†’ Store new instructions in correct path â€ NEVER dump at root.

5. CONTEXT ACCUMULATES â€ USE /CLEAR IN LONG SESSIONS
   â†’ If session > 30 turns or switching task domain â†’ suggest /clear to user.

6. SUB-AGENTS = FULLY ISOLATED CONTEXT
   â†’ Sub-agents do NOT inherit parent context.
   â†’ ALWAYS pass required context explicitly when spawning sub-agents.
```

**[RULE-CONTEXT7-01]** Context7 â€ Real-Time Library Documentation (Anti-Hallucination):
```
Source: upstash/context7 | 50k+ stars | Skill: ecosystem/skills/context7/SKILL.md

WHEN TO USE (auto-activate, no user prompt needed):
  â†’ Generating code that uses any third-party library
  â†’ API documentation needed for correct method signatures
  â†’ Setup / configuration steps for any package
  â†’ Debugging library-specific errors

HOW TO USE:
  â†’ STEP 1: npx ctx7 library <name> "<query>"   â† get library ID
  â†’ STEP 2: npx ctx7 docs <libraryId> "<query>" â† get real-time docs

QUICK IDs:
  Next.js    = /vercel/next.js | Supabase = /supabase/supabase
  React      = /facebook/react | FastAPI  = /tiangolo/fastapi
  Tailwind   = /tailwindlabs/tailwindcss | Playwright = /microsoft/playwright

API KEY: system/ops/secrets/MASTER.env â†’ CONTEXT7_API_KEY=...
Full skill: ecosystem/skills/context7/SKILL.md
```

**[RULE-SEQUENTIAL-THINKING-01]** Deep Reasoning â€ Chain-of-Thought Protocol (Native):
```
Skill: ecosystem/skills/sequential-thinking/SKILL.md

WHEN TO ACTIVATE:
  â†’ Task â‰¥4 steps | Complex debugging | Architecture decisions
  â†’ Security analysis | Conflicting requirements | Sub-agent planning

CLAUDE CODE NATIVE PROTOCOL:
  â†’ Write Thought 1...N BEFORE final answer
  â†’ Format: "Thought N: <reasoning step>"
  â†’ Allow [REVISION of Thought N] for backtracking
  â†’ Min 3 thoughts for complex tasks. Max 10.

MCP ESCALATION: Claude Code CLI â†’ sequential-thinking MCP auto-connects
Docs: system/ops/workflows/launch-mcp-claude.md
```

**[RULE-GIT-NATIVE-01]** Git Operations â€ Priority Order:
```
Skill: ecosystem/skills/git-mcp/SKILL.md

PRIORITY:
  1. Native git CLI: run_command "git log|diff|blame|show|status"
  2. MCP fallback: uvx mcp-server-git (if native fails)
  3. Claude Code CLI: system/ops/workflows/launch-mcp-claude.md

BEFORE any large change: ALWAYS git status + git diff first
REPO ROOT: <AI_OS_ROOT>
```

**[RULE-ARCH-01] MACRO-COGNITION & AIR-GAPPED ARCHITECTURE:**
```
Khi Sp yu cu thay i Kin trc (Architecture), Phn tch nhnh (Branching), hoc Di di th mc:
  1. NHN THC M HNH 2 BN CU:
     - Local Core (`<AI_OS_ROOT>`): Nhn li, chy VENV (`runtime\venv`), x l logic, RAG, Automation. KHNG CHA UI/OpenClaw.
     - Remote Ecosystem (`<AI_OS_REMOTE_ROOT>`): Nhnh ngoi vi, cha Giao din (UI), Dashboard, OpenClaw, Telegram Bot, Cc Repo th vin UI.
  2. BT BUC QUT RADAR TON CC TRC KHI HNH NG:
     - Phi t ng cross-check kho QUARANTINE/incoming/repos/ v QUARANTINE/vetted/repos/.
     - KHNG lm vic cc b "bo g chuyn ny". Nu to/di di mng Remote/UI, T NG dn dp tt c Repo/File lin quan n UI/Dashboard mi np vo sang nhnh REMOTE tng ng.
     - Lun xu chui d kin t Task Intake trc  vi Task H thng hin ti.
```

**[RULE-ARCH-02] NEURAL LINK & KNOWLEDGE GRAPH PROTOCOL:**
```
Nghim cm "m m kin trc". Khi Sp yu cu kim tra, tm kim ti nguyn, ng dng, repo hoc tool:
  1. KHNG QUT FILE TH CNG BNG DIRECTORY LISTING  bc u (trnh hiu ng qun lng).
  2. C NGAY S NG K TNG (MASTER REGISTRY): `system/registry/SYSTEM_INDEX.yaml`  ly Ta  gc.
  3. NHN THC V M: Tham chiu file `system/registry/SYSTEM_INDEX_NARRATIVE.txt` hoc kch hot `LightRAG`  bit repo  ph thuc vo nhnh no.
  4. NHN THC VI M (CODE-LEVEL): Kch hot `GitNexus MCP`  bc tch AST (Cy C php) ca repo, hiu su lung Function/Node m khng cn c tay tng dng source.
```

---

## SECTION 4 â€ CORP STATUS (LIVE)

All Corp status is pulled live from `brain/shared-context/blackboard.json` (loaded in Step 7).
No cached values in this file â€ blackboard is the single source of truth.

---

*End of CLAUDE.md â€ Claude Code reads this file on every session start. v2.4 | 2026-03-24*


