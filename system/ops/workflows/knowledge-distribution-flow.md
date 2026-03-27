# Department: content_review
# Knowledge Distribution & Enrichment Workflow
# Version: 1.0 | Updated: 2026-03-17
# Triggered by: ingest-router-agent (Dept 20 CIV) after content PASSES
# Primary dept: Asset & Knowledge Library (Dept 15)
# Support dept: OD&L (Dept 16)

---

## THE DOWNSTREAM MAP — After CIV Clears Content

```
╔═══════════════════════════════════════════════════════════════╗
║          KNOWLEDGE DISTRIBUTION & ENRICHMENT PIPELINE         ║
╚═══════════════════════════════════════════════════════════════╝

CIV ingest-router-agent delivers cleared content
(content PASSED all vetting/validation gates)
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│              ASSET & KNOWLEDGE LIBRARY (Dept 15)          │
│                                                           │
│  Step 1: knowledge-curator-agent receives + evaluates     │
│  Step 2: knowledge-tagger-agent tags categories + dept    │
│  Step 3: knowledge-distributor-agent pushes to correct    │
│          dept knowledge feed                              │
│  Step 4: library-manager-agent indexes in knowledge_index │
└────────────────────────────┬──────────────────────────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
       For AGENTS        For DEPTS      For SYSTEM
       or SKILLS         knowledge     configuration
             │               │               │
             ▼               ▼               ▼
    OD&L training     Dept knowledge    Registry &
    -agent            feeds             Capability
    upgrades agent    updated           ingests new
    rules/memory      (dept memory +    skills/plugins
                      knowledge/)
             │
             ▼
    memory-builder-agent (Asset Library)
    updates agent memory schemas
    if new knowledge is structural
```

---

## INPUT TYPES AND THEIR DOWNSTREAM DESTINATIONS

| Source Type | From CIV | Received By | Classified To | Distributed To |
|-------------|----------|-------------|---------------|----------------|
| REPO/Plugin (PASS) | Registry & Capability | registry-manager | Code/Skill | plugins/ or skills/ |
| Research/Article | Asset Library | knowledge-curator | Domain knowledge | Relevant dept feed |
| PDF/Doc (External) | Asset Library | knowledge-curator | Reference doc | knowledge/docs/ |
| Training material | Asset Library → OD&L | knowledge-curator → training-agent | Agent skill | Agent rules.md upgrade |
| Rule/Policy doc | Relevant dept | knowledge-distributor | Governance | corp/rules/ or dept/rules.md |
| Image/Asset | Asset Library | asset-tracker | Digital asset | assets/ + catalog |
| Raw knowledge/text | Asset Library | knowledge-curator | Tagged content | knowledge/<category>/ |

---

## WORKFLOW STEPS (POST-CIV)

### STEP D1 — Receipt & Assessment
Trigger: ingest-router-agent (CIV) writes receipt to:
  - `subagents/mq/asset_library_ingest.md`   ← WEB/DOCUMENT/TEXT content
  - `subagents/mq/registry_ingest.md`         ← REPO/PLUGIN content
Agent: knowledge-curator-agent (Asset Library)
For REPO: registry-manager-agent (Registry & Capability)

Receipt format (written by ingest-router):
```json
{ "civ_ticket": "CIV-2026-03-22-001",
  "content_type": "WEB_CONTENT|DOCUMENT|TEXT|REPO|PLUGIN",
  "destination_path": "<AOS_ROOT>/brain/knowledge/...",
  "quality_score": 7,
  "tags": [],
  "source_url": "..." }
```

Actions:
- Read CIV intake receipt (what was cleared, what type, source)
- Review quality (even cleared content may need library standards check)
- Route to knowledge-tagger-agent for tagging

SLA: < 1 corp cycle after delivery

---

### STEP D2 — Tag & Classify (in AI OS context)
Trigger: knowledge-curator-agent hands off to knowledge-tagger-agent
Agent: knowledge-tagger-agent (NEW — Asset Library)

Tagging dimensions:
1. DOMAIN: ai / engineering / ops / legal / finance / security / org / data
2. RELEVANCE: which dept(s) should know about this
3. RETENTION: temporary (7d) / standard (30d) / permanent (cosmic_memory)
4. FORMAT: reference | actionable | training | rule | asset

Output: tagged knowledge entry for knowledge_index.md

SLA: Immediate (per item)

---

### STEP D3 — Distribute to Dept Feeds
Trigger: knowledge-tagger-agent completes tagging with RELEVANCE dept list
Agent: knowledge-distributor-agent (NEW — Asset Library)

Actions:
- Push knowledge summary to each relevant dept's knowledge feed
- Write to: corp/knowledge_feeds/<dept_name>/new_knowledge.md
- Notify dept head agent that new knowledge is available
- Flag HIGH-VALUE items (quality ≥ 8) for OD&L enrichment

SLA: < 1 corp cycle after tagging

---

### STEP D4 — Index in Master Catalog
Trigger: knowledge-distributor-agent completes distribution
Agent: library-manager-agent (Asset Library)

Actions:
- Update knowledge_index.md with new entry
- Archive CIV intake ticket (link intake_log → knowledge_index)
- If PERMANENT: extract to cosmic_memory (run cosmic_memory.extract_observation)

---

### STEP D5 — Agent/Dept Enrichment (if training-relevant)
Trigger: knowledge-distributor-agent flags HIGH-VALUE or TRAINING-RELEVANT items
Agent: training-agent (OD&L)

Actions:
- Assess: is this new knowledge that changes how an agent should work?
- YES: propose skill/rule update to affected agent's rules.md
- YES + new skill needed: coordinate with skill-creator-agent (Registry)
- Update agent memory schema if needed (memory-builder-agent)
- Validate enrichment by reviewing agent's next task output

Example triggers:
  - New security technique  → update security-scanner's knowledge
  - New AI framework docs   → update Engineering dept feed
  - New business rule doc   → update relevant dept rules.md
  - New skill/plugin added  → update Registry + notify Engineering

SLA: Within 2 corp cycles of knowledge flagging

---

## DEPT KNOWLEDGE FEED STRUCTURE

Each dept has a knowledge feed updated by knowledge-distributor-agent:

```
corp/knowledge_feeds/
├── engineering/           └── new_knowledge.md
├── qa_testing/            └── new_knowledge.md
├── it_infra/              └── new_knowledge.md
├── marketing/             └── new_knowledge.md
├── support/               └── new_knowledge.md
├── content_review/        └── new_knowledge.md
├── operations/            └── new_knowledge.md
├── hr_people/             └── new_knowledge.md
├── security_grc/          └── new_knowledge.md   ← threat intel priority
├── finance/               └── new_knowledge.md
├── strategy/              └── new_knowledge.md
├── legal/                 └── new_knowledge.md
├── rd/                    └── new_knowledge.md
├── registry_capability/   └── new_knowledge.md
├── asset_library/         └── new_knowledge.md
├── od_learning/           └── new_knowledge.md   ← training input feed
├── planning_pmo/          └── new_knowledge.md
├── monitoring_inspection/ └── new_knowledge.md
├── system_health/         └── new_knowledge.md
├── content_intake/        └── new_knowledge.md
├── client_reception/      └── new_knowledge.md
└── global/
    └── new_knowledge.md     ← org-wide knowledge, read by ALL 21 dept heads
```

Dept head agent loads their feed at boot (add to rules.md boot checklist).
Feed format: latest item appended at top. Agents read top 5 entries max per boot.

---

## KNOWLEDGE ENRICHMENT — Who Gets What

| Knowledge Type | Primary Recipient | OD&L Role | Memory Update |
|----------------|------------------|-----------|---------------|
| AI technique/model | R&D + Engineering | training-agent loads into eng feed | Optional |
| Security threat intel | Security GRC | training-agent updates scanner rules | Security GRC memory |
| Process improvement | Operations + Planning PMO | org-analyst reviews for OD-04 | Planning PMO memory |
| Legal/compliance update | Legal + Security GRC | compliance-agent gets updated rules | Compliance memory |
| New skill/plugin | Registry + All depts | training-agent proposes skill adoption | SKILL_REGISTRY.json |
| Org learning (retro) | OD&L | learning-curator archives | cosmic_memory |
| Tool/framework doc | Engineering + QA | training-agent updates agent specs | Engineering memory |
| Business/domain knowledge | Strategy + CSO | CSO brief | Strategy memory |

---

## COLLABORATION MAP

```
CIV (Dept 20)
    ↓ delivers
Asset & Knowledge Library (Dept 15) ← MAIN HUB
    ↓ distributes
├── All 20 dept knowledge feeds
├── Registry & Capability (code/skills)
└── OD&L (Dept 16) ← ENRICHMENT
         ↓ trains
         All agents (via rules.md + memory updates)
```
