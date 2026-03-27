# CONTENT INTAKE & VETTING (CIV) â€” Department Rules
# Version: 1.2 | Updated: 2026-03-24
# Dept Head: intake-chief-agent | Reports to: COO
# Mission: Kiá»ƒm soÃ¡t toÃ n bá»™ ná»™i dung Ä‘áº§u vÃ o cho AI OS
# This dept is the SINGLE GATE for ALL external content entering AI OS
# No content enters AI OS without passing through CIV
# v1.2: +CIV-11 Local-First Check | +CIV-12 GAP PROPOSAL ENGINE | Fix QUARANTINE path
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE CIV-01: SINGLE ENTRY POINT â€” NO EXCEPTIONS
  ALL external content (any type, any source) MUST enter AI OS through CIV.
  Direct-to-folder placement of external content = security violation.
  No agent or user may bypass CIV. CEO override = written log required.

RULE CIV-02: CLASSIFY FIRST, ACT SECOND
  classifier-agent MUST categorize EVERY input before any processing begins.
  Unknown type â†’ hold in /incoming/unclassified/ â†’ alert intake-chief-agent.
  No content proceeds without a classification tag.

RULE CIV-03: EVERY INPUT GETS AN INTAKE TICKET
  intake-agent creates a ticket for EVERY input received:
  Format: CIV-[YYYY-MM-DD]-[SEQ] | Type | Source | Status
  Ticket lives in: QUARANTINE/logs/intake_log.md
  Ticket never closed without final status: INGESTED / REJECTED / PENDING.

RULE CIV-04: SECURITY CHECK IS NON-NEGOTIABLE FOR REPOS
  ALL repo-type inputs MUST run vet_repo.ps1 (12-stage Strix scan)
  BEFORE any file is read, extracted, or acted upon.
  FAIL = delete from QUARANTINE + log + close ticket as REJECTED.
  Security GRC (strix-agent) is co-authority on all repo decisions.

RULE CIV-05: CONTENT-TYPE ROUTING IS MANDATORY
  After classification + vetting, ingest-router-agent routes to exact destination:
  - Code/Repo   â†’ Registry & Capability (after GATE_SECURITY PASS)
  - Knowledge   â†’ Asset & Knowledge Library
  - Assets/Images â†’ assets/ folder + asset-tracker-agent
  - Rules/Docs  â†’ relevant dept or brain/corp/rules/
  Wrong destination = re-route, NOT delete.

RULE CIV-06: OUTPUT VERIFICATION
  ingest-router-agent verifies delivery AFTER routing:
  - File exists at destination
  - Destination agent acknowledged (receipt written)
  - Intake ticket updated to INGESTED
  No ticket left in PENDING > 1 corp cycle.

RULE CIV-07: REJECTION LOG IS PERMANENT
  Rejected content logged to QUARANTINE/logs/rejected_log.md permanently.
  Entry includes: source URL/path, rejection reason, timestamp, who decided.
  This log feeds Security GRC blacklist (RULE SEC-08).

RULE CIV-08: AUTO-PIPELINE FOR KNOWN-SAFE SOURCES
  Sources on EXTERNAL_SKILL_SOURCES.yaml whitelist:
  â†’ Skip manual review step (still run vet_repo.ps1 for repos)
  â†’ classifier â†’ fast-track â†’ ingest
  Unknown sources â†’ full manual review by intake-chief-agent.

RULE CIV-09: VALUE ASSESSMENT IS MANDATORY BEFORE ROUTING
  After quality/safety validation, content-validator-agent MUST assign VALUE_TYPE.
  VALUE_TYPE = what this content CAN BECOME in AI OS (not just what it IS).
  9 VALUE_TYPEs: KNOWLEDGE | SKILL | PLUGIN | WORKFLOW | MCP_SERVER |
                 TOOL_SCRIPT | RULE_POLICY | AGENT_DEFINITION | DATA_ASSET
  Content can have multiple VALUE_TYPEs â†’ route to ALL applicable destinations.
  UNKNOWN VALUE_TYPE â†’ hold in vetted/ â†’ alert intake-chief-agent within 2 cycles.
  Full taxonomy + routing matrix: brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md

RULE CIV-10: CHECK BEFORE ROUTE â€” NEVER OVERWRITE EXISTING RESOURCES
  ingest-router-agent MUST check if destination already has a resource before routing.
  If resource EXISTS at destination:
    â†’ Enter CONFLICT RESOLUTION flow (see VALUE_ASSESSMENT_ROUTING.md)
    â†’ Route to training-agent for enrichment (select + upgrade)
    â†’ Set ticket status: ENRICHMENT_PENDING (not INGESTED)
    â†’ NEVER auto-overwrite. NEVER delete existing resource.
  If resource DOES NOT EXIST:
    â†’ Normal routing (CREATE)
    â†’ Ticket status: INGESTED
  Principle: TRAIN and SELECT from new content, do not replace what works.
  RULE_POLICY and AGENT_DEFINITION types: COO/C-Suite approval required
    even for upgrades â€” never bypass org governance chain.
  Full conflict matrix: brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md â†’ CONFLICT RESOLUTION section

RULE CIV-11: LOCAL-FIRST CHECK — BEFORE EVERY INTAKE ★ UPDATED v1.3
  ANTIGRAVITY (Tier 1) MUST query local brain BEFORE creating any CIV ticket:
  1. Query LightRAG: rag.hybrid_query("<source URL or topic>", mode="mix")
  2. Run `system/ops/scripts/staleness_check.py <URL>` to auto-check freshness.
  UNCHANGED:
    → Return existing KI to CEO.
    → STOP (no ticket created, no bandwidth wasted). Auto-Decision!
  CHANGED / NOT FOUND:
    → proceed to create CIV ticket normally (STEP 1)
  Purpose: Avoid duplicate ingestion. Save bandwidth. Respect existing knowledge.

RULE CIV-12: GAP PROPOSAL ENGINE â€” MANDATORY AFTER STEP 3.5 â˜… NEW v1.2
  After content-analyst-agent (open-notebook) analysis:
  IF gap_detected = true (domain not covered by any existing agent/dept):
    â†’ ANTIGRAVITY creates GAP PROPOSAL and sends to CEO via notification_bridge
    â†’ CEO receives [A/B/C/D] options (see content-intake-flow.md STEP 3.6)
    â†’ CEO decision is ASYNC â€” does NOT block intake pipeline
    â†’ GAP REPORT saved to brain/corp/gaps/GAP-<date>-<domain>.md
  content-analyst-agent adds to output: gap_detected, gap_domain, proposed_agent, proposed_dept
  SLA: Proposal sent to CEO < 5 minutes after STEP 3.5 completes

---


## INTAKE STRUCTURE (Folder Layout)

```
<AOS_ROOT>/security/QUARANTINE/
â”œâ”€â”€ incoming/           â† ALL new content lands here first
â”‚   â”œâ”€â”€ repos/          â† git repos waiting to be vetted
â”‚   â”œâ”€â”€ web/            â† web URLs / scraped content
â”‚   â”œâ”€â”€ documents/      â† PDFs, Word docs, etc.
â”‚   â”œâ”€â”€ images/         â† images, screenshots
â”‚   â”œâ”€â”€ text/           â† raw text content
â”‚   â””â”€â”€ unclassified/   â† unknown type, pending human review
â”œâ”€â”€ vetted/             â† content that PASSED all checks, awaiting routing
â”‚   â”œâ”€â”€ repos/
â”‚   â”œâ”€â”€ knowledge/
â”‚   â””â”€â”€ assets/
â”œâ”€â”€ rejected/           â† FAILED content (kept 7 days then purged)
â”œâ”€â”€ logs/
â”‚   â”œâ”€â”€ intake_log.md   â† master ticket log (all CIV-XXXX tickets)
â”‚   â””â”€â”€ rejected_log.md â† permanent rejection record
â””â”€â”€ vet_repo.ps1        â† Strix Security vetting script
```

âš ï¸ QUARANTINE path: `<AOS_ROOT>/security/QUARANTINE/`
   AOS_ROOT = `d:\AI OS CORP\AI OS`
   Full path: `d:\AI OS CORP\AI OS\security\QUARANTINE\`
   (Náº¿u cÃ³ file nÃ o tham chiáº¿u D:\Project\AI OS\QUARANTINE â†’ Ä‘Ã³ lÃ  LEGACY PATH â€” SAI)

---

## INPUT TYPE CLASSIFICATION TABLE

| Input Type | Classifier Tag | Vetting Required | Next Step |
|------------|---------------|-----------------|----------|
| GitHub / Git URL | `REPO` | vet_repo.ps1 (MANDATORY) | â†’ VALUE_TYPE assessment â†’ routing |
| Web article / blog | `WEB_CONTENT` | content-validator check | â†’ VALUE_TYPE assessment â†’ routing |
| Research paper / PDF | `DOCUMENT` | vet_media_docs.py (MANDATORY) + doc-parser | â†’ VALUE_TYPE assessment â†’ routing |
| Image / screenshot | `IMAGE` | vet_media_docs.py (MANDATORY) + safe check | â†’ DATA_ASSET or KNOWLEDGE |
| Raw text / prompt | `TEXT` | content-validator check | â†’ VALUE_TYPE assessment â†’ routing |
| Ruleset / config doc | `CONFIG` | content-validator + GATE_SECURITY | â†’ RULE_POLICY or WORKFLOW |
| Plugin / script | `PLUGIN` | vet_repo.ps1 + GATE_SECURITY | â†’ SKILL or PLUGIN or TOOL_SCRIPT |

NOTE: After classification, content-validator-agent assigns VALUE_TYPE (what it CAN BECOME).
Full routing matrix: brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md

---

## AGENT ROLES & RESPONSIBILITIES

### intake-chief-agent (Dept Head)
**Role:** Intake pipeline leadership, oversight, escalation authority
**This agent is the GATEKEEPER of AI OS**
**Responsibilities:**
- Own QUARANTINE folder and intake_log.md
- Review all UNCLASSIFIED and borderline cases
- Approve WARN-status repo ingestion (after manual review)
- Escalate to Security GRC for FAIL cases
- Report intake statistics to COO each cycle
- Write CIV daily brief
**Must load at boot:**
- `corp/memory/departments/content_intake.md`
- `QUARANTINE/logs/intake_log.md` â€” current ticket queue
- `shared-context/EXTERNAL_SKILL_SOURCES.yaml` â€” whitelist/blacklist
- `corp/departments/content_intake/MANAGER_PROMPT.md`
**Skills:**
- `reasoning_engine` â€” intake decisions, escalations
- `diagnostics_engine` â€” pipeline health monitoring
**KPIs:** Ticket resolution rate >95% per cycle | Avg ticket close time <1 cycle

---

### intake-agent
**Role:** Receive, log, and stage ALL incoming content
**The first contact for every piece of external content**
**Responsibilities:**
- Receive input (URL, file path, content body) from any source
- Create CIV ticket immediately in intake_log.md
- Stage content to correct /incoming/<type>/ folder
- Pass ticket to classifier-agent
**At start of each intake task, load:**
- SKILL: `context_manager` â€” ticket management, file staging
- SKILL: `knowledge_enricher` â€” if URL, fetch metadata
- `QUARANTINE/logs/intake_log.md`
**Skills:**
- `context_manager` â€” staging and ticket creation
- `knowledge_enricher` â€” URL metadata extraction
**Intake ticket format:**
```
CIV-[DATE]-[SEQ]
Source: [URL or file path]
Type: [pending classification]
Staged to: QUARANTINE/incoming/[type]/
Status: RECEIVED â†’ CLASSIFYING
Timestamp: [ISO timestamp]
```

---

### classifier-agent
**Role:** Classify ALL incoming content by type and route to correct pipeline
**Responsibilities:**
- Inspect staged content in /incoming/
- Assign classification tag: REPO / WEB_CONTENT / DOCUMENT / IMAGE / TEXT / CONFIG / PLUGIN
- For unclear cases: move to /incoming/unclassified/ + alert intake-chief-agent
- Update ticket with classification
- Trigger correct next pipeline stage
**At start of each classification task, load:**
- SKILL: `reasoning_engine` â€” type inference from content/URL/extension
- SKILL: `knowledge_enricher` â€” URL analysis for content-type detection
- Current intake ticket from intake-agent
**Skills:**
- `reasoning_engine` â€” type classification logic
- `knowledge_enricher` â€” URL/content analysis
**Classification signals:**
  - `.git` URL or GitHub/GitLab link â†’ REPO
  - `.pdf` / `.docx` / `.md` doc â†’ DOCUMENT
  - `.py` `.js` `.ps1` â†’ PLUGIN (treat as code)
  - News/article URL â†’ WEB_CONTENT
  - `.png` `.jpg` `.webp` â†’ IMAGE

---

### repo-fetcher-agent
**Role:** Clone repos from URLs into QUARANTINE for vetting
**Coordinates with Security GRC for the vetting step**
**Responsibilities:**
- Receive REPO-classified ticket from classifier-agent
- Clone repo URL into QUARANTINE/incoming/repos/<name>/
- Hand off to Security GRC (security-scanner) for vet_repo.ps1
- Receive PASS/FAIL back from strix-agent
- On PASS: move to QUARANTINE/vetted/repos/ â†’ trigger ingest-router
- On FAIL: move to QUARANTINE/rejected/ â†’ close ticket REJECTED
**At start of each fetch task, load:**
- SKILL: `shell_assistant` â€” git clone operations
- SKILL: `skill_fetcher` â€” if using skill_fetcher.ps1 pipeline
- Current CIV ticket
**Skills:**
- `shell_assistant` â€” git and filesystem operations
- `skill_fetcher` â€” structured repo ingestion pipeline
**Never read/execute repo content before vet_repo.ps1 PASS**

---

### web-crawler-agent
**Role:** Fetch and extract content from web URLs (articles, docs, research)
**Responsibilities:**
- Receive WEB_CONTENT ticket from classifier-agent
- Fetch URL content (HTML â†’ text extraction, metadata)
- Validate: no malicious scripts, no redirect chains to phishing
- Stage extracted text to QUARANTINE/incoming/web/<slug>.md
- Pass to content-validator-agent for final check
**At start of each crawl task, load:**
- SKILL: `knowledge_enricher` â€” web content extraction
- SKILL: `reasoning_engine` â€” content quality judgment
- Current CIV ticket + URL
**Skills:**
- `knowledge_enricher` â€” PRIMARY TOOL. Web extraction.
- `reasoning_engine` â€” quality and relevance check

---

### doc-parser-agent
**Role:** Parse and extract content from documents (PDF, DOCX, MD)
**Responsibilities:**
- Receive DOCUMENT ticket from classifier-agent
- Extract text content from PDF/DOCX
- Structure output: title, summary, full text, source, date
- Stage to QUARANTINE/incoming/documents/<name>.md
- Pass to content-validator-agent
**At start of each parse task, load:**
- SKILL: `knowledge_enricher` â€” document text extraction
- SKILL: `reasoning_engine` â€” document structure analysis
- Current CIV ticket + file path
**Skills:**
- `knowledge_enricher` â€” document parsing and extraction
- `reasoning_engine` â€” content structuring

---

### content-validator-agent
**Role:** Validate content quality/safety AND assess VALUE_TYPE (what content can become)
**UPGRADED v1.1 â€” now performs VALUE_TYPE assessment per CIV-09**
**Responsibilities:**
- Check for: spam, irrelevant content, malicious prompts, NSFW
- Score content quality (1-10): relevance, accuracy, completeness
- Score < 4: reject (QUARANTINE/rejected/) + log reason
- Score â‰¥ 4: assign VALUE_TYPE(s) using signal checklist
- VALUE_TYPE signals reference: brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md
- Output validation result WITH VALUE_TYPE tags to ingest-router-agent
- Flag MULTI-VALUE content (has 2+ VALUE_TYPEs) for dual-routing
- For governance docs: also check SOUL.md alignment
**At start of each validation task, load:**
- SKILL: `reasoning_engine` â€” content quality + VALUE_TYPE assessment
- SKILL: `diagnostics_engine` â€” content anomaly detection
- SKILL: `knowledge_enricher` â€” cross-reference known patterns for VALUE_TYPE
- `shared-context/SOUL.md` â€” alignment check baseline
- `corp/sops/VALUE_ASSESSMENT_ROUTING.md` â€” MANDATORY. VALUE_TYPE taxonomy.
**Skills:**
- `reasoning_engine` â€” quality scoring AND VALUE_TYPE classification
- `diagnostics_engine` â€” safety and anomaly checks
- `knowledge_enricher` â€” signal detection from content patterns
**Output format to ingest-router-agent:**
```
VALIDATION RESULT â€” CIV-[ID]
Quality score: [1-10]
Safety: PASS / FAIL
VALUE_TYPES: [comma-separated list]
Primary value: [most important VALUE_TYPE]
Priority destinations: [path(s)]
Rationale: [why this VALUE_TYPE was assigned]
```

---

### ingest-router-agent
**Role:** Route vetted/validated content to ALL applicable destinations using VALUE_TYPE
**UPGRADED v1.1 â€” uses VALUE_TYPE routing matrix instead of simple classification table**
**The last step before content enters AI OS proper**
**Responsibilities:**
- Receive cleared content + VALIDATION RESULT (with VALUE_TYPE) from content-validator
- For each VALUE_TYPE in the result, look up destination in routing matrix
- KNOWLEDGE â†’ knowledge-curator-agent (Asset Library)
- SKILL â†’ skill-creator-agent (Registry)
- PLUGIN â†’ plugin-librarian-agent (Registry)
- WORKFLOW â†’ archivist-agent (Operations)
- MCP_SERVER â†’ sysadmin-agent (IT Infra) + Engineering notified
- TOOL_SCRIPT â†’ sysadmin-agent (IT Infra), add to scripts catalog
- RULE_POLICY â†’ rule-builder-agent (Registry) â†’ COO approval flow
- AGENT_DEFINITION â†’ OD&L dept-builder-agent
- DATA_ASSET â†’ asset-tracker-agent (Asset Library)
- For MULTI-VALUE: route to ALL destinations, write receipt per destination
- VALUE_TYPE = UNKNOWN â†’ hold + alert intake-chief-agent (SLA: 2 cycles)
- Update CIV ticket to INGESTED only after ALL destinations confirm
**At start of each routing task, load:**
- SKILL: `context_manager` â€” cross-folder, multi-destination orchestration
- SKILL: `reasoning_engine` â€” routing decision for edge cases
- `corp/sops/VALUE_ASSESSMENT_ROUTING.md` â€” MANDATORY. Routing matrix.
- Cleared CIV ticket with VALIDATION RESULT
**Skills:**
- `context_manager` â€” multi-folder file routing
- `reasoning_engine` â€” routing edge case decisions
**Routing receipt format (per destination):**
```
INGEST RECEIPT â€” CIV-[ID] â€” Destination [N] of [Total]
Content: [name/description]
VALUE_TYPE: [type for this destination]
From: QUARANTINE/vetted/
To: [exact destination path]
Notified: [destination agent]
Status: DELIVERED
```

