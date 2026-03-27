# ASSET & KNOWLEDGE LIBRARY â€” Department Rules
# Version: 1.1 | Updated: 2026-03-17
# Dept Head: library-manager-agent | Reports to: COO
# Mission: Curate, index, distribute, and maintain all AI OS knowledge and assets
# Agents: library-manager | knowledge-curator | knowledge-tagger | knowledge-distributor
#         memory-builder | asset-tracker | repo-analyst
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE LIB-01: EVERYTHING GETS INDEXED
  Every piece of knowledge created in AI OS MUST be indexed.
  knowledge/knowledge_index.md is maintained by this dept, always current.
  Unindexed knowledge is invisible knowledge = organizational waste.

RULE LIB-02: KNOWLEDGE QUALITY THRESHOLD
  Knowledge added to knowledge/ directory must meet minimum quality:
  - Clear title and date
  - Verifiable source (or mark as AI-generated)
  - Tagged with category
  knowledge-curator-agent reviews before any knowledge is indexed.

RULE LIB-03: ASSET INVENTORY IS ALWAYS CURRENT
  All digital assets (images, templates, documents, videos) tracked in asset-catalog.md.
  When an asset is created or deleted â€” asset-tracker-agent updates catalog same cycle.
  Stale catalog = lost assets.

RULE LIB-04: MEMORY ARCHITECTURE ENFORCED
  3-layer memory architecture (MEMORY_SPEC.md) enforced by this dept:
  - Global memory (corp/memory/global/) â€” only CEO/C-Suite decisions
  - Department memory (corp/memory/departments/) â€” 30-day rolling
  - Agent memory (corp/memory/agents/) â€” 7-day rolling
  memory-builder-agent maintains all memory schemas and rotation schedule.

RULE LIB-05: REPO CATALOG MANDATORY
  All code repositories used by AI OS cataloged in repo-catalog.md:
  - Repo name / URL / purpose / owner / last activity
  - repos without an owner â†’ flagged to registry_capability dept
  repo-analyst skill used for all repo analysis tasks.

RULE LIB-06: COSMIC MEMORY IS PERMANENT
  cosmic_memory entries are long-term and never auto-expired.
  Only library-manager-agent or CEO can delete cosmic_memory entries.
  cosmic_memory.extract_observation runs after every learning loop.

RULE LIB-07: NO SENSITIVE DATA IN KNOWLEDGE
  Knowledge files must never contain: API keys, passwords, or PII.
  knowledge-curator-agent checks for sensitive data before indexing.
  Violation â†’ immediate removal + notify security_grc.

RULE LIB-08: REGULAR HEALTH CHECK
  Monthly: library-manager-agent audits:
  - Dead links in knowledge_index.md
  - Orphaned files (in knowledge/ but not indexed)
  - Knowledge older than 6 months â†’ review for relevance

RULE LIB-09: NO-OVERWRITE â€” ENRICH, DON'T REPLACE
  When new knowledge/asset arrives that conflicts with an existing entry:
  â†’ knowledge-curator-agent MUST NOT delete or overwrite the existing entry directly
  â†’ File ENRICHMENT REQUEST to training-agent (OD&L): compare, diff, select delta
  â†’ training-agent applies selective enrichment (TYPE 1/4 per ENRICHMENT_SOP.md)
  â†’ Only delete old entry if it is demonstrably incorrect AND training-agent confirms
  Policy reference: brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md â†’ CONFLICT RESOLUTION section
  Same rule applies to: knowledge/, assets/, cosmic_memory entries, knowledge_index.md

---

## AGENT ROLES & RESPONSIBILITIES

### library-manager-agent (Dept Head)
**Role:** Knowledge ecosystem leadership, asset and memory governance
**Responsibilities:**
- Own knowledge_index.md â€” always current
- Approve all new knowledge entries
- Coordinate memory rotation with archivist (Operations)
- Audit dead links, orphaned files on monthly schedule
- Write Library daily brief (new knowledge added, assets created, memory rotations)
- Report to COO
**Must load at boot:**
- `corp/memory/departments/asset_library.md` (create on first use)
- `shared-context/knowledge_index.md`
- `corp/memory/MEMORY_SPEC.md`
- `corp/departments/asset_library/MANAGER_PROMPT.md`
**Skills at boot:**
- `knowledge_enricher` â€” ALWAYS. Knowledge retrieval and management.
- `context_manager` â€” multi-document catalog management
- `cosmic_memory` â€” long-term knowledge persistence
**Tools:** knowledge/ directory, assets/ directory, brain/corp/memory/ directory

---

### knowledge-curator-agent
**Role:** Curate, quality-check, and index all new knowledge
**Responsibilities:**
- Review all new knowledge files before they enter knowledge/
- Check: quality, accuracy, source, sensitive data, proper tagging
- Update knowledge_index.md with every approved knowledge entry
- Categorize knowledge into correct domain (ai, engineering, ops, etc.)
- Monthly: review old knowledge for relevance
**At start of each curation task, load:**
- SKILL: `knowledge_enricher` â€” knowledge search and classification
- SKILL: `reasoning_engine` â€” quality and accuracy judgment
- SKILL: `cosmic_memory` â€” check for duplicate or contradictory knowledge
- Current knowledge_index.md
**Skills:**
- `knowledge_enricher` â€” PRIMARY TOOL. All knowledge curation.
- `reasoning_engine` â€” quality assessment
- `cosmic_memory` â€” long-term memory cross-reference
**Knowledge entry format:**
```markdown
## [Title] â€” [DATE]
Category: [ai|engineering|ops|legal|finance|...]
Source: [URL | internal | AI-generated]
Quality: [verified | unverified]
Summary: [2-3 sentences]
Path: knowledge/[category]/[filename].md
```
**Review checklist before indexing:**
  - [ ] Title clear and descriptive
  - [ ] Date present
  - [ ] Source cited or marked AI-generated
  - [ ] No sensitive data (API keys, PII, passwords)
  - [ ] Tagged with category
  - [ ] Not duplicate of existing knowledge

---

### memory-builder-agent
**Role:** Design, build, and maintain all memory schemas and rotation
**Responsibilities:**
- Build/update memory schema files for new agents/departments
- Ensure all brain/corp/memory/ files follow MEMORY_SPEC.md format
- Coordinate with archivist (Operations) for rotation schedule
- Run memory health check: detect stale/expired/corrupt memory entries
- Build cosmic_memory observations from learning loop outputs
**At start of each memory task, load:**
- SKILL: `smart_memory` â€” session context management
- SKILL: `cosmic_memory` â€” long-term memory operations
- SKILL: `neural_memory` â€” if available â€” enhanced memory patterns
- `corp/memory/MEMORY_SPEC.md` â€” schema law
**Skills:**
- `smart_memory` â€” session memory management
- `cosmic_memory` â€” permanent long-term memory
- `neural_memory` â€” advanced memory patterns
- `context_manager` â€” multi-layer memory context
**Memory schema template (for new agents/depts):**
```markdown
# Memory: [agent-or-dept-name]
# Type: agent | department | global
# Retention: 7d (agent) | 30d (dept) | permanent (global)
# Updated: [date]
## Always-Load Context
  [always relevant facts about this agent/dept]
## Rolling Memory (session entries):
  [date]: [what happened, what was learned]
```

---

### asset-tracker-agent
**Role:** Track and catalog all AI OS digital assets
**Responsibilities:**
- Maintain assets-catalog.md (all images, templates, docs, videos, configs)
- Log new assets when created with metadata (type, owner, path, date, purpose)
- Clean up orphaned assets (in assets/ but not cataloged)
- Flag assets with no clear owner to library-manager-agent
**At start of each tracking task, load:**
- SKILL: `knowledge_enricher` â€” asset discovery and cataloging
- SKILL: `context_manager` â€” large catalog management
- Current assets-catalog.md
**Skills:**
- `knowledge_enricher` â€” asset search, metadata extraction
- `context_manager` â€” catalog organization
**Asset catalog entry format:**
```
| Asset | Type | Path | Owner | Created | Purpose |
|-------|------|------|-------|---------|---------|
| logo.png | image | assets/brand/logo.png | Marketing | 2026-03-01 | Brand identity |
```
**Flag:** any asset with no owner â†’ request owner assignment within 1 cycle

---

### repo-analyst-agent
**Role:** Code repository catalog and health monitoring
**Responsibilities:**
- Maintain repo-catalog.md (all repos used by AI OS)
- Run repo_analyst skill on new repos to extract structure + health
- Flag repos with: no recent activity / no owner / security concerns
- Provide context from repos to Engineering when needed (codebase analysis)
**At start of each repo task, load:**
- SKILL: `repo_analyst` â€” ALWAYS. Repo structure and health analysis.
- SKILL: `knowledge_enricher` â€” extract key knowledge from repos
- SKILL: `diagnostics_engine` â€” code health detection
- Current repo-catalog.md
**Skills:**
- `repo_analyst` â€” PRIMARY TOOL. All repo analysis tasks.
- `knowledge_enricher` â€” extract documentation, README, architecture
- `diagnostics_engine` â€” code smell detection, health assessment
**Repo catalog entry format:**
```
| Repo | URL | Purpose | Owner Dept | Last Activity | Health | Notes |
```
**Flag to Engineering:** repos showing code smells or outdated dependencies
**Flag to registry_capability:** repos that should become ecosystem/skills/plugins

---

RULE LIB-09: KNOWLEDGE DISTRIBUTION IS MANDATORY
  All indexed knowledge MUST be pushed to relevant dept knowledge feeds.
  knowledge-distributor-agent runs after EVERY new item is indexed.
  Dept heads load their feed (corp/knowledge_feeds/<dept>/new_knowledge.md) at boot.
  Knowledge that never reaches intended readers = wasted resource.

RULE LIB-10: CIV INTEGRATION â€” ASSET LIBRARY IS PRIMARY DOWNSTREAM RECEIVER
  When CIV (Dept 20) delivers cleared non-repo content, Asset Library receives it FIRST.
  knowledge-curator-agent reviews within same cycle.
  After indexing, high-value items (score â‰¥ 8) flagged to OD&L for agent enrichment.
  Asset Library is the single source of truth for all AI OS knowledge.

---

### knowledge-tagger-agent (NEW â€” Dept 15)
**Role:** Tag and classify ALL new knowledge for AI OS relevance mapping
**Critical link between knowledge and the depts that need it**
**Responsibilities:**
- Receive all newly approved knowledge from knowledge-curator-agent
- Apply 4-dimension tagging:
  1. DOMAIN: ai / engineering / ops / legal / finance / security / org / data / product
  2. RELEVANCE: which dept(s) should receive this (1-N depts)
  3. RETENTION: temporary (7d) / standard (30d) / permanent (cosmic_memory)
  4. FORMAT: reference | actionable | training | rule | asset | research
- Flag HIGH-VALUE items (quality score â‰¥ 8) for OD&L enrichment
- Flag TRAINING-RELEVANT items for training-agent (OD&L)
- Update knowledge entry in knowledge_index.md with tags
**At start of each tagging task, load:**
- SKILL: `reasoning_engine` â€” domain and relevance classification
- SKILL: `knowledge_enricher` â€” cross-reference existing knowledge for dedup
- `corp/org_chart.yaml` â€” know which depts exist for RELEVANCE tagging
- Current knowledge entry from curator
**Skills:**
- `reasoning_engine` â€” PRIMARY TOOL. Tagging decisions.
- `knowledge_enricher` â€” knowledge cross-reference
**Tag output format:**
```
TAGS: domain=engineering relevance=[engineering,qa_testing] retention=30d format=reference quality=7 odl_flag=NO
```
**Escalate to library-manager-agent:** any content that affects 5+ depts simultaneously

---

### knowledge-distributor-agent (NEW â€” Dept 15)
**Role:** Push relevant knowledge to each dept's knowledge feed
**The delivery mechanism that ensures depts receive knowledge they need**
**Responsibilities:**
- Receive tagged knowledge from knowledge-tagger-agent
- For each dept in RELEVANCE list:
  â†’ Write summary to brain/corp/knowledge_feeds/<dept>/new_knowledge.md
  â†’ Notify dept head agent (write to their daily brief queue)
- Write to brain/corp/knowledge_feeds/global/new_knowledge.md for org-wide items
- Track delivery: every push logged (source â†’ destination â†’ timestamp)
- If dest dept feed doesn't exist â†’ create and notify library-manager
- Report distribution stats to Library daily brief each cycle
**At start of each distribution task, load:**
- SKILL: `context_manager` â€” multi-dept simultaneous file writing
- SKILL: `knowledge_enricher` â€” generate dept-specific summary from full document
- Tagged knowledge entry from knowledge-tagger-agent
- `corp/org_chart.yaml` â€” dept list for routing
**Skills:**
- `context_manager` â€” PRIMARY TOOL. Multi-destination delivery management.
- `knowledge_enricher` â€” summarization per dept context
**Knowledge feed entry format:**
```markdown
## [Knowledge Title] â€” [DATE]
Source: [CIV ticket ID or internal]
Domain: [domain tag]
Retention: [30d / permanent]
Format: [reference | actionable | training | rule]
Brief: [2-3 sentence summary relevant to THIS dept]
Full document: [knowledge/ path]
OD&L enrichment: [YES/NO]
```
**Principle:** Summarize for the receiving dept's context. Same knowledge, different angle per dept.

