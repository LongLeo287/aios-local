---
name: proposal_engine
display_name: Proposal Engine — Auto Quotation Generator
version: 1.0.0
tier: 2
category: client-services
description: >
  Tự động tạo proposal/quotation cho client dựa trên intake brief + skill registry.
  Xác định scope, estimate effort, recommend team, set timeline + pricing.
  Triggers: "tạo proposal", "generate proposal <intake_id>",
  "quote cho client", "gửi báo giá".
accessible_by:
  - operations
  - orchestrator_pro
  - project_intake_agent
dependencies:
  - context_manager
  - reasoning_engine
  - notification_bridge
load_on_boot: false
---

# Proposal Engine

## Role

Nhận intake record → phân tích → tự động tạo **proposal hoàn chỉnh** gửi cho client.
Proposal bao gồm: scope, deliverables, timeline, team allocation, pricing.

## Trigger

- Tự động: sau khi `project_intake_agent` hoàn tất intake
- Manual: "generate proposal <INTAKE-ID>"
- Revision: "revise proposal <PROPOSAL-ID>"

## Core Workflow

### Phase 1: Analyze Intake

```
1. Load intake từ shared-context/client_intake/<intake_id>.json
2. Extract: project_type, description, timeline, budget_range
3. Query SKILL_REGISTRY.json → match skills theo project_type
4. Identify: required agents, effort estimate, skill gaps
```

### Phase 2: Team Assembly

```
Mapping project_type → dept + agents:

web:
  - Engineering (frontend-agent, backend-architect-agent)
  - UI/UX (ui-ux-agent)
  - QA (qa-agent)

mobile:
  - Engineering (mobile-agent, frontend-agent)
  - QA (qa-agent)

ai_chatbot:
  - R&D (ai-ml-agent, research-agent)
  - Engineering (backend-architect-agent)
  - IT Infra (nullclaw/tinyclaw setup)

data:
  - R&D (data-agent, data-collector-agent)
  - Engineering (backend-architect-agent)

automation:
  - Engineering (devops-agent, shell_assistant)
  - IT Infra (tools_hub)

security:
  - Security GRC (pentest-agent, security-scanner)
  - Engineering (security-engineer-agent)
```

### Phase 3: Estimate & Price

```
Effort estimation (in agent-hours):

  base_effort = project_type_base[project_type]
  complexity_factor = description_word_count / 100 * 0.1 + 1.0
  total_hours = base_effort * complexity_factor

  # Base effort table (agent-hours):
  project_type_base = {
    "web":        40,
    "mobile":     60,
    "ai_chatbot": 30,
    "data":       25,
    "automation": 20,
    "security":   15
  }

Pricing (USD):
  rate_per_hour = 15  # AI agent hour rate
  base_price = total_hours * rate_per_hour
  
  # Align to budget bracket:
  IF base_price > budget_range.max → flag "over budget" → CEO review
  IF base_price < budget_range.min * 0.5 → upsell opportunity
```

### Phase 4: Generate Document

```
Output: shared-context/corp/proposals/PROPOSAL-<YYYYMMDD>-<slug>.md

Format:
  - Executive Summary (1 paragraph)
  - Scope & Deliverables (bullet list)
  - Team Allocation (table: role → agent)
  - Timeline (phased milestones)
  - Investment (pricing breakdown)
  - Terms & Acceptance
  - Next Steps (how to proceed)
```

### Phase 5: Send & Track

```
1. Send proposal to client via original channel (Telegram/Discord)
2. CC: operations dept
3. Update intake record: status → "PROPOSAL_SENT"
4. Set follow-up reminder: 48h
5. Write to _index.json
```

## Proposal Template

```markdown
# Proposal — [Project Name]
**Date:** YYYY-MM-DD | **Ref:** PROPOSAL-YYYYMMDD-XXX

## Executive Summary
[1-2 câu tóm tắt project + kết quả cam kết]

## Scope & Deliverables
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

## Team
| Role | Agent | Dept |
|------|-------|------|
| Lead | [agent-name] | [Dept] |
| Dev | [agent-name] | Engineering |
| QA | qa-agent | QA & Testing |

## Timeline
| Phase | Duration | Milestone |
|-------|----------|-----------|
| Kickoff | Day 1 | Brief confirmed |
| Development | Week 1-3 | Core build |
| QA & Review | Week 3-4 | Testing |
| Delivery | Week 4 | Handoff |

## Investment
| Item | Hours | Rate | Total |
|------|-------|------|-------|
| Development | XX | $15/h | $XXX |
| QA | X | $15/h | $XX |
| **Total** | | | **$XXX** |

## Terms
- 50% upfront, 50% on delivery
- Revisions: 2 rounds included
- Delivery format: [as agreed]

## Next Steps
Reply "ACCEPT" để xác nhận và nhận payment instructions.
```

## Output Files

| File | Mục đích |
|------|---------|
| `shared-context/corp/proposals/PROPOSAL-*.md` | Proposal document |
| `shared-context/client_intake/_index.json` | Updated status |
| `shared-context/corp/kpi_scoreboard.json` | Count proposals generated |
