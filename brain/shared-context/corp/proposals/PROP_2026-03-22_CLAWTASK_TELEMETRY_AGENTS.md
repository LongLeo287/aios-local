# Add /api/telemetry/agents live heartbeat endpoint
**ID:** PROP_2026-03-22_CLAWTASK_TELEMETRY_AGENTS
**Type:** NEW_SKILL | **Priority:** MEDIUM
**Generated:** 2026-03-22T21:53:14.373868
**Agent:** product-manager-agent

## Context
Telemetry panel in ClawTask shows receipts but not live agent status.

## Proposed Action
Add GET /api/telemetry/agents to clawtask_api.py — reads agents.json + last heartbeat time

## Effort / Impact
- Effort: 1h
- Impact: MEDIUM — real-time agent status in dashboard

## Status
[ ] Awaiting CEO decision

---
_Corp Proposal #PROP_2026-03-22_CLAWTASK_TELEMETRY_AGENTS · 2026-03-22_


## CEO DECISION
- Status: APPROVED
- Date: 2026-03-25T10:28:01
- Notes: APPROVED — P4: ClawTask events→Telegram watcher added to start_bridges.py (clawtask_watcher, polls :7474 every 15s)

