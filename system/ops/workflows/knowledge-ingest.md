# Department: registry_capability
# knowledge-ingest.md — Knowledge Ingestion Pipeline
# Version: 2.0 | Updated: 2026-03-22 | Created: 2026-03-22
# Authority: Tier 2 (Operations)
# Agents: intake-chief-agent → strix-agent → knowledge_navigator → knowledge_enricher → archivist
# Trigger: "aos ingest <source>" OR agent drops file into intake queue

---

## Overview

Every piece of external knowledge (URL, doc, repo, bug fix, research dump) passes through this pipeline before entering the AI OS brain.

```
SOURCE (URL / File / Repo / Bug Fix / Research)
    │
    ▼
[1] INTAKE       intake-chief-agent    — receive + queue
    │
    ▼
[2] SECURITY     strix-agent           — scan for threats/injections
    │
    ▼
[3] CLASSIFY     knowledge_navigator   — find target dept + domain
    │
    ▼
[4] ENRICH       knowledge_enricher    — metadata + cross-links
    │
    ▼
    ├── Agent exists for this domain? ──YES──► [5a] Link to agent memory
    └── No agent found?               ──NO───► [5b] → agent-auto-create workflow
    │
    ▼
[6] ARCHIVE      archivist             — persist to brain/knowledge/
    │
    ▼
[7] NOTIFY       notification_bridge   — alert CEO if significant new knowledge
```

---

## Supported Source Types

| Type | Input format | Trigger keyword |
|------|-------------|----------------|
| URL / webpage | `https://...` | `aos ingest url <url>` |
| Local file | `.md`, `.pdf`, `.txt` | `aos ingest file <path>` |
| Git repo | GitHub/GitLab URL | `aos ingest repo <url>` |
| Bug fix lesson | Task receipt + diff | Auto-trigger after task COMPLETE |
| Research dump | Free text | `aos ingest text "<content>"` |
| Web search | Query string | `aos ingest search "<query>"` |

---

## Phase 1: Intake (intake-chief-agent)

```
1. Receive source → create intake ticket:
   {
     "id": "KI-<timestamp>",
     "source_type": "url|file|repo|lesson|text|search",
     "source": "<value>",
     "submitted_by": "<agent_id>",
     "timestamp": "<ISO8601>",
     "status": "PENDING"
   }

2. If URL/repo: fetch content via **web_intelligence skill** (firecrawl_adapter):
   ```python
   from plugins.firecrawl.firecrawl_adapter import get_firecrawl
   fc = get_firecrawl()
   # Single URL:
   content = fc.research_url(source)
   # Full site/repo docs (limit=50):
   pages = fc.crawl_site(source, limit=50)
   ```
   → Fallback order: self-hosted (localhost:3002) → cloud → noop (log warning)
   → Rule: RULE-WEB-01: NEVER write custom HTTP code, always use firecrawl_adapter
3. If local file: read and extract text
4. If search: query web_intelligence.search("<query>"), collect top 3 results
5. Save raw content to: security/QUARANTINE/<KI-id>/ (temporary holding)
6. Update ticket status → "SECURITY_SCAN"
```

---

## Phase 2: Security Scan (strix-agent — GATE)

```
strix-agent reads from: security/QUARANTINE/<KI-id>/

Checks:
  □ Prompt injection patterns (forbidden instruction overrides)
  □ Malicious code snippets
  □ Credential/token exposure
  □ Known malware domains (if URL source)
  □ License conflicts (if repo source — GPL incompatibility)
  □ Binary/Macro inspection via `vet_media_docs.py` (if PDF/DOCX/Image)

Results:
  PASS → move to brain/knowledge/staging/<KI-id>/
         update ticket status → "CLASSIFYING"
  FAIL → move to security/QUARANTINE/REJECTED/<KI-id>/
         write ESCALATION_REPORT to shared-context/corp/escalations.md
         notify CEO via notification_bridge
         STOP — do not proceed further
```

---

## Phase 3: Classification (knowledge_navigator)

```
knowledge_navigator reads staged content and determines:

1. Domain tags (e.g., "backend", "ai-ml", "security", "marketing", "legal")
2. Target department (from org_chart.yaml departments list)
3. Knowledge type:
   - REFERENCE  → API docs, specs, standards
   - LESSON     → Bug fix insights, post-mortem lessons
   - RESEARCH   → New concepts, papers, patterns
   - TOOL       → New skill/plugin discovered
   - PATTERN    → Reusable architecture or code pattern
```

### Domain → Agent Matching Algorithm

```
STEP A: Extract domain tags from content
  → NLP-style keyword extraction on title, headings, summary
  → Map to standard domain vocabulary:
    "react", "vue", "html", "css"         → web_frontend
    "python", "api", "fastapi", "backend"  → backend
    "docker", "ci/cd", "devops", "k8s"    → devops
    "model", "llm", "rag", "embedding"    → ai_ml
    "security", "cve", "pentest", "owasp" → cybersecurity
    "gdpr", "contract", "legal", "ip"     → legal
    "seo", "content", "blog", "social"    → marketing
    "finance", "cost", "budget", "api_cost"→ finance
    "test", "qa", "coverage", "e2e"       → qa_testing
    "memory", "knowledge", "ki", "graph"  → knowledge_mgmt
    "agent", "skill", "register", "plugin"→ registry
    [unmatched]                            → general / CEO-escalate

  ⚡ SHORTCUT: Read brain/knowledge/CAPABILITY_MAP.md first!
     → Domain → Skill/Plugin lookup table (60+ entries, 12 domains)
     → Decision tree included
     → 90% accuracy WITHOUT LightRAG service running
     → 95%+ WITH LightRAG: python ops/scripts/index_skills_lightrag.py
        then query: aquery("what skill does X?", mode="mix")

STEP B: Identify relevant agents
  Source 1 — org_chart.yaml:
    → Find target_dept with matching domain
    → dept.head + dept.workers = candidate agents
  Source 2 — AGENTS.md:
    → Scan each agent's role description for domain keyword overlap
    → If overlap ≥ 1 term → add to relevant_agents
  Source 3 — SKILL_REGISTRY.json:
    → Find skills matching domain_tags
    → Skills → accessible_by[] → add those agents to relevant_agents

STEP C: Score confidence
  0.9+  → Clear match (domain term exact match in agent role/skills)
  0.7-0.89 → Strong match (domain cluster match in dept scope)
  0.5-0.69 → Weak match (only dept-level match, no specific agent)
  < 0.5 → Unknown domain → escalate to CEO with options

STEP D: Gap detection
  IF relevant_agents = [] AND knowledge_type IN [TOOL, RESEARCH]:
    → GAP_CONFIRMED: no agent covers this domain
    → Proceed to Phase 5b (agent-auto-create)
  IF relevant_agents = [] AND knowledge_type IN [REFERENCE, LESSON]:
    → Route to target_dept head as general knowledge
    → No new agent needed
  IF confidence < 0.5:
    → Escalate to CEO: show 3 options
      A) assign to <nearest dept>
      B) create new agent
      C) ignore (mark as LOW_PRIORITY archive)
```

```
4. Write classification result:
   brain/knowledge/staging/<KI-id>/classification.json:
   {
     "domain_tags": [...],
     "target_dept": "<dept_name>",
     "knowledge_type": "REFERENCE|LESSON|RESEARCH|TOOL|PATTERN",
     "relevant_agents": ["<agent_id>", ...],
     "confidence": 0.0-1.0,
     "gap_detected": true|false,
     "gap_reason": "<why no agent covers this>"
   }

5. If confidence < 0.5 → escalate to CEO with classification options
```

---

## Phase 4: Enrichment (knowledge_enricher)

```
knowledge_enricher processes classified content:

1. metadata_enrichment:
   - Add: source, date, domain_tags, knowledge_type, related_skills
   - Extract: key concepts, definitions, warnings, best practices

2. contextual_linking:
   - Cross-link to existing knowledge entries in brain/knowledge/
   - Link to relevant SKILL_REGISTRY.json entries
   - Link to relevant agent AGENT.md files

3. Create final knowledge entry:
   brain/knowledge/<domain>/<KI-id>.md:
   ---
   id: <KI-id>
   source: <url|file|agent>
   type: REFERENCE|LESSON|RESEARCH|TOOL|PATTERN
   domain: [tags]
   dept: <target_dept>
   agents: [relevant agent IDs]
   created: <ISO8601>
   ---
   [Extracted and structured content]
   [Cross-links]
   [Key takeaways]
```

---

## Phase 5: Agent Routing

### 5a. Agent Exists → Link to Memory

```
IF relevant_agents is not empty:
  For each agent in relevant_agents:
    Append to corp/memory/agents/<agent_id>.md:
    ## [DATE] — New Knowledge: <KI-id>
    Type: <knowledge_type>
    Summary: <1-2 sentence summary>
    Full entry: brain/knowledge/<domain>/<KI-id>.md
```

### 5b. No Agent → Trigger agent-auto-create

```
IF relevant_agents is empty AND knowledge_type = "TOOL" or "RESEARCH":
  → Invoke: ops/workflows/agent-auto-create.md
  Pass: { ki_id, domain_tags, knowledge_type, target_dept }

  Wait for agent-auto-create result (async — may span cycles):

  CASE: CEO APPROVES new agent
    → Update KI ticket: status = "AGENT_CREATED"
    → Link KI entry to new agent's AGENT.md once created
    → Proceed to Phase 6 (Archive) normally

  CASE: CEO REJECTS new agent
    → Update KI ticket: status = "NO_AGENT_ASSIGNED"
    → Route knowledge to nearest dept head as general reference:
       Append to corp/memory/agents/<target_dept_head>.md
    → Proceed to Phase 6 (Archive) — knowledge is NOT discarded

  CASE: CEO requests MODIFY (Phase 2 loop)
    → KI ticket stays in "PENDING_AGENT_CREATION" status
    → Phase 6 waits until agent-auto-create resolves
    → SLA: max 3 cycles — if unresolved → escalate to CSO

  CASE: agent-auto-create fails (strix REJECTED or system error)
    → Update KI ticket: status = "AGENT_CREATION_FAILED"
    → Route as "NO_AGENT_ASSIGNED" (see above)
    → Write reason to ticket for post-mortem
```

---

## Phase 6: Archive (archivist)

```
1. Move from staging → final location:
   brain/knowledge/staging/<KI-id>/ → brain/knowledge/<domain>/<KI-id>/

2. Update knowledge index:
   brain/knowledge/INDEX.md — append new entry

3. Update dept brief if significant:
   shared-context/corp/daily_briefs/<target_dept>.md

4. Write archivist receipt:
   telemetry/receipts/knowledge_ingest/<KI-id>_receipt.json

5. Clean staging: delete brain/knowledge/staging/<KI-id>/
```

---

## Phase 7: Notify CEO (if significant)

```
Conditions that trigger CEO notification:
  - knowledge_type = "TOOL" (new capability discovered)
  - knowledge_type = "RESEARCH" + confidence > 0.8
  - Security scan FAILED (always notify)
  - New agent was created via agent-auto-create

Notification format: B2 TASK_RECEIPT
Channel: notification_bridge → Telegram
```

---

## Integration Points

| System | How it connects |
|--------|----------------|
| `corp-learning-loop.md` | After each cycle retro → auto-trigger ingest for all LESSON-type findings |
| `SKILL_REGISTRY.json` | TOOL-type knowledge → propose new skill registration |
| `org_chart.yaml` | Target dept determined by classification; new agents linked here |
| `security/QUARANTINE/` | All raw content staged here first |
| `brain/knowledge/` | Final destination for all enriched knowledge |
| `blackboard.json` | Intake tickets tracked as tasks; agents pick up via blackboard |

---

## Triggers

```
Manual:    "aos ingest <source>"
Auto:      After any task COMPLETE receipt → extract LESSON
Auto:      After any bug fix → run with source_type=lesson
On-demand: "aos search <query>" → ingest + return summary to CEO
Weekly:    archivist runs backfill_knowledge to cross-link orphan entries
```

---

*"Knowledge that isn't ingested is knowledge that's lost. Every input is an opportunity to improve."*
