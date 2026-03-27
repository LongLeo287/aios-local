# Department: hr_people
# agent-auto-create.md — Agent Auto-Creation Protocol
# Version: 2.0 | Updated: 2026-03-22 | Created: 2026-03-22
# Authority: Tier 2 (Operations) — CEO approval required for activation
# Agents: product-manager-agent (CSO) → hr-manager-agent → org-architect-agent
# Trigger: Called by knowledge-ingest.md Phase 5b when no agent covers new domain

---

## Overview

When new knowledge is ingested and no existing agent covers its domain, this protocol creates a new agent specification, proposes it to CEO, and (upon approval) integrates it into the org chart and system.

```
knowledge-ingest.md Phase 5b
    │
    ▼
[1] ASSESS       cognitive_reflector   — validate gap is real, not overlap
    │
    ▼
[2] DESIGN       product-manager-agent — draft agent spec from template
    │
    ▼
[3] SECURITY     strix-agent           — scan new agent's tool permissions
    │
    ▼
[4] PROPOSE      → CEO proposal (B5 format)
    │
    CEO APPROVES?
    ├── NO  → archive spec, close ticket
    └── YES ▼
[5] REGISTER     hr-manager-agent      — onboard agent into org_chart
    │
    ▼
[6] LINK         org-architect-agent   — link to dept, update shared-context
    │
    ▼
[7] ACTIVATE     registry-manager-agent — register skills in SKILL_REGISTRY
```

---

## Phase 1: Validate Gap (cognitive_reflector)

```
Input: { ki_id, domain_tags, knowledge_type, target_dept }

1. Search AGENTS.md for agents matching domain_tags
2. Search org_chart.yaml workers in target_dept
3. Search SKILL_REGISTRY.json for existing skills covering this domain

Verdict:
  GAP_CONFIRMED    → existing agents cannot cover this domain → proceed Phase 2
  OVERLAP_FOUND    → existing agent can be extended → stop, update agent memory instead
  PARTIAL_OVERLAP  → log gap, propose skill addition to existing agent
```

---

## Phase 2: Design Agent Spec (product-manager-agent)

```
Create: brain/agents/proposals/AGENT-PROPOSAL-<timestamp>-<domain>.md

Template:
---
proposal_id: <id>
status: DRAFT
created: <ISO8601>
knowledge_source: <KI-id>
---

# Agent Proposal: <Agent Name>

## Role
<1 sentence describing what this agent does>

## Why needed
<Gap identified: what knowledge no existing agent covers>
<Source: brain/knowledge/<domain>/<KI-id>.md>

## Proposed agent ID
<kebab-case-agent-id>

## Department
<target_dept> — reports to <dept_head>

## Skills required
- <skill_1> (exists in SKILL_REGISTRY: YES/NO)
- <skill_2> ...

## Tools / permissions needed
- [list of tools — will be reviewed by strix-agent]

## LLM tier
economy | balanced | performance

## Autonomy level
supervised | semi-autonomous | autonomous

## KPIs
- <measurable metric 1>
- <measurable metric 2>

## Sample tasks
1. <concrete task this agent would do>
2. <another task>

## Integration
- Reads from: [list of files/channels]
- Writes to:  [list of files/channels]
- Reports to: <dept_head>
```

---

## Phase 3: Security Review (strix-agent — GATE)

```
strix-agent reviews proposed agent's:
  □ Tool permissions — does it request more than needed?
  □ File write access — is scope appropriate?
  □ External connections — does it need internet access?
  □ Data access — does it touch sensitive knowledge?

Result:
  APPROVED  → add strix_approved: true to proposal
  CHANGES   → return to Phase 2 with required modifications
  REJECTED  → archive proposal, notify CEO of rejection reason
```

---

## Phase 4: CEO Proposal (B5 PROPOSAL format)

```
product-manager-agent writes to: shared-context/corp/proposals/PROPOSAL_<date>_new-agent-<id>.md

Format: B5 PROPOSAL
Content:
  - Summary: what new knowledge triggered this
  - Agent spec summary (from Phase 2)
  - Security review result (from Phase 3)
  - Estimated impact: what new capability this unlocks
  - Recommended: YES/NO + reasoning
  - Resource cost: LLM tier + approx token budget

Notification: notification_bridge → Telegram → CEO
```

**CEO DECISION REQUIRED — workflow pauses here.**

```
CEO response options:
  APPROVE   → "approve agent <id>"    → continue Phase 5
  REJECT    → "reject agent <id>"     → archive, close
  MODIFY    → "modify agent <id> ..."  → return to Phase 2
```

---

## Phase 5: Register Agent (hr-manager-agent)

### 5a — Create all required files (EVERY new agent)

```
On CEO APPROVE — hr-manager-agent creates ALL of the following:

1. AGENT.md — Full agent specification
   Path: brain/agents/<agent-id>/AGENT.md
   Template: brain/agents/_template/AGENT.md
   Required sections:
     - Identity (id, name, title, dept, reports_to, philosophy)
     - Role & Scope (primary function, responsibilities)
     - Decision Authority (what agent decides vs escalates)
     - Tool Stack & Skills (from SKILL_REGISTRY.json)
     - Workflow Integration (reads from / writes to)
     - KPIs (link to corp/kpi_targets.yaml)
     - Memory Format (MEMORY_SPEC.md Layer 4 schema)
     - Registration Metadata (JSON block)

2. Agent Short-term Memory
   Path: corp/memory/agents/<agent-id>.md
   Initial entry:
   ## [DATE] — Initialization
   Context: Agent created via agent-auto-create workflow
   Outcome: SUCCESS
   Key lesson: [pending first task]
   Current blockers: none

3. Onboarding receipt
   Path: telemetry/receipts/agent_onboard/<agent-id>.json
   Content: full audit trail JSON (see Full Audit Trail section)
```

### 5b — If NEW DEPARTMENT is also being created

```
If the agent belongs to a department that does NOT exist yet:

4. Create dept folder: corp/departments/<dept_name>/

5. MANAGER_PROMPT.md
   Path: corp/departments/<dept_name>/MANAGER_PROMPT.md
   Sections: mission, team, boot additions, task rules, workflow, brief format

6. WORKER_PROMPT.md
   Path: corp/departments/<dept_name>/WORKER_PROMPT.md
   Sections: role context, skill loading, task ownership, workflow protocol,
             receipt additions (dept-specific JSON)

7. rules.md
   Path: corp/departments/<dept_name>/rules.md
   Content: dept-specific constraints and operating rules

8. Dept memory
   Path: corp/memory/departments/<dept_name>.md
   Initial: MEMORY_SPEC.md Layer 3 schema, first cycle entry

9. Daily brief channel
   Path: brain/shared-context/corp/daily_briefs/<dept_name>.md
   Initial: header only, ready to receive first brief

10. Add to org_chart.yaml:
    departments:
      <dept_name>:
        head: <agent-id>
        workers: []
        prompts:
          manager: corp/departments/<dept_name>/MANAGER_PROMPT.md
          worker: corp/departments/<dept_name>/WORKER_PROMPT.md
        rules: corp/departments/<dept_name>/rules.md
        created_by: agent-auto-create
        created_at: <ISO8601>

11. Add to kpi_targets.yaml:
    Under departments: block, add new dept with daily/weekly targets
    Match the metrics referenced in WORKER_PROMPT.md

12. Add to kpi_scoreboard.json:
    Under departments: block, add:
    "<dept_name>": {
      "head": "<agent-id>",
      "daily_target_score": <N>,
      "completed_score": 0,
      "status": "idle",
      "metrics": { ... }
    }
    Update company_health.total_departments + 1
```

---

## Phase 6: Link to System (org-architect-agent)

```
1. Update corp/org_chart.yaml:
   Add to departments.<target_dept>.workers:
     - agent: <agent-id>
       role: "<role description>"
       prompt: "corp/departments/<target_dept>/WORKER_PROMPT.md"
       created_by: "agent-auto-create"
       knowledge_source: "<KI-id>"

2. Update brain/shared-context/AGENTS.md:
   Add agent entry in correct department section

3. Update shared-context/corp/daily_briefs/<target_dept>.md:
   Append: "New agent <agent-id> activated — covers <domain>"

4. Bump org_chart.yaml version + updated date
```

---

## Phase 7: Activate Skills (registry-manager-agent)

```
For each skill in agent spec that is NOT in SKILL_REGISTRY:
  → Trigger: skill registration proposal (mini knowledge-ingest for the skill itself)

For skills that EXIST in SKILL_REGISTRY:
  → Update SKILL_REGISTRY.json: add agent-id to accessible_by[]

Write activation receipt: telemetry/receipts/agent_activate/<agent-id>.json
Notify CEO: "Agent <agent-id> is now active in <dept>"
```

---

## Full Audit Trail

Every agent created by this protocol must have:

```json
{
  "agent_id": "<agent-id>",
  "created_by": "agent-auto-create",
  "trigger": "knowledge-ingest",
  "ki_source": "<KI-id>",
  "proposal_id": "<proposal-id>",
  "ceo_approved": true,
  "approved_at": "<ISO8601>",
  "strix_approved": true,
  "dept": "<target_dept>",
  "activation_date": "<ISO8601>"
}
```

Stored: `telemetry/receipts/agent_onboard/<agent-id>.json`

---

## What CEO needs to provide (at minimum)

When approving a new agent, CEO can optionally specify:
- Override LLM tier
- Additional skill restrictions
- Initial task assignment
- Budget cap (tokens/day)

If nothing specified → defaults from agent spec apply.

---

## Limits & Safeguards

- Max 3 new agents per cycle without explicit CEO budget review
- No agent can be created with `autonomy: autonomous` without separate CEO approval
- All auto-created agents start with `autonomy: supervised`
- Agents created by this protocol are tagged `auto_created: true` in org_chart.yaml

---

## AGENT ONBOARDING MASTER CHECKLIST

> Use this checklist for EVERY new agent — whether auto-created or manually created.
> Mark each item ✅ before declaring agent ACTIVE.

### For any new agent (worker or head)
- [ ] `brain/agents/<agent-id>/AGENT.md` — created from template, all sections filled
- [ ] `corp/memory/agents/<agent-id>.md` — initialized with creation entry
- [ ] AGENTS.md — agent entry added to roster under correct dept
- [ ] `corp/org_chart.yaml` — agent added to dept.workers (or dept.head if new head)
- [ ] SKILL_REGISTRY.json — skills assigned under agent ID's accessible_by[]
- [ ] Onboarding receipt written: `telemetry/receipts/agent_onboard/<agent-id>.json`

### Additional — if head agent (dept lead)
- [ ] `corp/memory/departments/<dept>.md` — dept memory initialized
- [ ] MANAGER_PROMPT.md — functional content (mission, workflow, brief format)
- [ ] WORKER_PROMPT.md — dept-specific (role context, skill loading, receipt format)
- [ ] `brain/shared-context/corp/daily_briefs/<dept>.md` — channel ready

### Additional — if NEW DEPARTMENT
- [ ] `corp/departments/<dept_name>/` — folder created
- [ ] `corp/departments/<dept_name>/rules.md` — dept rules written
- [ ] `corp/org_chart.yaml` — new dept block added
- [ ] `corp/kpi_targets.yaml` — dept KPI targets added
- [ ] `brain/shared-context/corp/kpi_scoreboard.json` — dept entry added, total_departments +1
- [ ] `blackboard.json` — corp_state.total_depts updated
- [ ] `corp-daily-cycle.md` — dept count in Phase 3 updated

### Verification (health-chief-agent — system_health dept)
- [ ] YAML valid: `corp/org_chart.yaml`
- [ ] JSON valid: `brain/shared-context/corp/kpi_scoreboard.json`, `blackboard.json`
- [ ] All file paths in AGENT.md exist on disk
- [ ] SKILL_REGISTRY.json valid JSON after update

---

*"A system that can grow its own team is a system that can face any challenge."*
