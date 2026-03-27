---
name: hitl_gateway_enforcer
display_name: HITL Gateway Enforcer
description: >
  Universal pattern to halt agent execution and require explicit human
  approval before committing high-risk or irreversible operations.
  Applicable to any project — not domain-specific.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: governance
domain: frontend
tags: [hitl, safety, approval, human-in-loop, governance, universal]
cost_tier: economy
accessible_by:
  - Claude Code
  - QA
  - Antigravity
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# HITL (Human-In-The-Loop) Gateway Enforcer

## When to Use
Activate this skill when an agent is about to execute an operation that:
- Is irreversible (deletes, production deployments, bulk mutations)
- Exceeds a defined risk threshold
- Involves external systems (APIs, email, payments)
- The user has not explicitly authorized in the current task

## Triggers (Default — Customize Per Project)

```
HIGH RISK (always require human approval):
- Bulk delete > 10 records
- Any production deploy
- Sending external messages (email, SMS, webhooks)
- Modifying authentication or security config

MEDIUM RISK (require human approval unless in task scope):
- Structural rename of files/tables
- Modifying shared config files
- Any operation on files outside current workspace
```

## Execution Flow

```
1. Agent identifies risky operation
2. Agent activates HITL skill
3. HITL writes to blackboard.json:
   {
     "hitl_requested": true,
     "operation": "<description>",
     "risk_level": "HIGH | MEDIUM",
     "requested_by": "<agent>",
     "timestamp": "<ISO 8601>"
   }
4. Agent calls notify_user:
   "⚠️ Cần duyệt: [mô tả operation]
    Risk: HIGH | MEDIUM
    Tôi sẽ dừng và chờ bạn xác nhận."
5. Agent STOPS and waits
6. On user approval → proceed
7. On user denial → abort, log to telemetry/receipts/HITL_DENIED_<timestamp>.json
```

## Integration with .clauderules

This skill complements the Circuit Breaker in `.clauderules`.
Circuit Breaker = tool failure protection.
HITL Gateway = human authorization protection.

## Customization Per Project

In your workspace's task_file.md, override triggers:
```
HITL_TRIGGERS:
  - operation: delete_user
    threshold: any
  - operation: deploy
    threshold: production_only
```
