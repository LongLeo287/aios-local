---
name: channel_manager
version: 1.0
tier: 3
category: channels
description: Control and monitor all remote bridge channels (Telegram/Zalo/Discord/FB)
exposed_functions:
  - start_bridge
  - stop_bridge
  - get_bridge_status
  - broadcast
  - send_to_user
dependencies:
  - notification_bridge
---

# Channel Manager Skill

## Purpose
Provides a unified skill interface to the `channels/` remote bridge module.
Any agent can call these functions to interact with messaging platforms.

## Exposed Functions

### start_bridge(channel: str) → bool
```
channel: "telegram" | "zalo" | "messenger" | "discord" | "all"
Action: Starts the specified bridge process
Returns: True if started successfully
Command: python channels/<channel>_bridge.py
         or python channels/start_bridges.py (for "all")
```

### stop_bridge(channel: str) → bool
```
Terminates the bridge process gracefully
```

### get_bridge_status() → dict
```
Returns: {
  "telegram":  {"running": bool, "active_users": N},
  "zalo":      {"running": bool, "active_users": N},
  "messenger": {"running": bool, "active_users": N},
  "discord":   {"running": bool, "active_users": N},
  "port": 5001
}
```

### send_to_user(channel: str, user_id: str, message: str) → bool
```
Send a proactive message to a specific user on a channel
Requires: credentials configured in .env
```

### broadcast(message: str) → dict
```
Send message to ALL active channel users
Returns: {"sent": N, "failed": N}
```

### get_today_stats() → dict
```
Reads telemetry/channels/<today>/*.jsonl
Returns: {
  "total_messages": N,
  "unique_users": N,
  "blocked_messages": N,
  "channels_active": [...]
}
```

## Prerequisites
- `.env` tokens configured (TELEGRAM_BOT_TOKEN, etc.)
- `pip install -r channels/requirements.txt` completed

## HITL Safety
- Tier 1: Reading bridge status → Auto-approve
- Tier 2: Starting/stopping bridges → Dry-run first
- Tier 3: Broadcasting to all users → User confirmation required

## Governance
All operations subject to `rules/CHANNEL_RULES.md`.
