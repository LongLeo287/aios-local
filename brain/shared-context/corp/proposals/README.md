# AI OS Corp — Proposals Directory
# Written by: Strategy dept (product-manager-agent, cognitive_reflector)
# Read by: CEO via corp_orchestrator.approve_proposal

---

## How Proposals Work

1. Strategy dept writes proposal here after daily retro
2. corp_orchestrator surfaces it to CEO in next session
3. CEO approves/rejects/modifies via Antigravity
4. Decision logged to: `shared-context/corp/decisions/log.md`

## Proposal Filename Convention

```
PROPOSAL_YYYY-MM-DD_<type>_<topic>.md
ESCALATION_YYYY-MM-DD_<dept>_<topic>.md
RETRO_YYYY-MM-DD.md
```

Types: `NEW_SKILL` | `KPI_REVISION` | `WORKFLOW_CHANGE` | `ROLE_CHANGE` | `STRATEGIC_ESCALATION`

## Proposal Template

```markdown
# Proposal: <title>

**Date:** YYYY-MM-DD  
**Type:** NEW_SKILL | KPI_REVISION | WORKFLOW_CHANGE | STRATEGIC_ESCALATION  
**Dept:** <department>  
**Author:** <agent_name>  
**CEO Decision Required:** YES | NO  

## Evidence

<!-- Reference daily_briefs or retro findings -->
-

## Proposed Action

<!-- Concrete next step -->

## Impact

<!-- Which depts / metrics affected -->

## Options

A. <option>  
B. <option>  

**Recommended:** A

---
**CEO Response:** _pending_
```

---

*Proposals are the mechanism by which agents influence strategy.*
*CEO is the final decision maker on all YES items.*
