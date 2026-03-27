# Auto-start deepagents :8765 via ClawTask service control
**ID:** PROP_2026-03-22_DEEPAGENTS_AUTOSTART
**Type:** ROLE_CHANGE | **Priority:** MEDIUM
**Generated:** 2026-03-22T21:53:14.373868
**Agent:** product-manager-agent

## Context
ACP Console panel requires deepagents WebSocket. Currently manual start.

## Proposed Action
Add 'deepagents' to services_control.py KNOWN_SERVICES. ClawTask service panel → Start

## Effort / Impact
- Effort: 1h
- Impact: MEDIUM — enables live agent communication from browser

## Status
[ ] Awaiting CEO decision

---
_Corp Proposal #PROP_2026-03-22_DEEPAGENTS_AUTOSTART · 2026-03-22_


## CEO DECISION
- Status: APPROVED
- Date: 2026-03-25T10:27:41
- Notes: APPROVED — P5: DeepAgents autostart added to start_bridges.py

