# Department: operations
---
description: AI OS notification routing — gửi alert qua Telegram, log hệ thống, CEO dashboard
---
# notification-bridge.md — Notification Bridge Protocol
# Version: 1.0 | Created: 2026-03-24
# Owner: Antigravity (Tier 1)
# Trigger: Bất kỳ agent nào cần gửi alert/notification

---

## Overview

notification-bridge là lớp trung gian nhận notification từ mọi agent và route đúng channel:

```
Agent → [notification-bridge] → Telegram (CEO)
                              ↘→ blackboard.json (system log)
                              ↘→ telemetry/receipts/ (audit trail)
                              ↘→ corp/escalations.md (nếu là escalation)
```

---

## Notification Types

| Type | Priority | Channel | Format |
|------|----------|---------|--------|
| `GAP_PROPOSAL` | HIGH | Telegram + blackboard | [A/B/C/D] options |
| `SECURITY_ALERT` | CRITICAL | Telegram + escalations.md | Immediate action needed |
| `CIV_COMPLETE` | NORMAL | blackboard only | Ticket status update |
| `CIV_REJECTED` | NORMAL | blackboard + Telegram | Reason + source |
| `SKILL_CREATED` | LOW | blackboard only | Skill name + path |
| `SYSTEM_ERROR` | HIGH | Telegram + escalations.md | Error context + fix suggestion |
| `CYCLE_COMPLETE` | NORMAL | blackboard | Phase 7 retro summary |
| `OPEN_ITEM_SLA` | HIGH | Telegram | Item ID + SLA breach |

---

## How Agents Send Notifications

### Format (any agent, any language):
```json
{
  "type": "GAP_PROPOSAL | SECURITY_ALERT | CIV_COMPLETE | ...",
  "priority": "CRITICAL | HIGH | NORMAL | LOW",
  "source_agent": "<agent-name>",
  "title": "<short title>",
  "body": "<message body>",
  "data": { "<extra context>" },
  "timestamp": "<ISO8601>"
}
```

### ANTIGRAVITY sends via:
- Telegram: `nullclaw_gateway` (start_nullclaw.ps1) → nullclaw bot message
- blackboard: Update `open_items[]` or `last_actions_this_cycle[]`

---

## Telegram Channel Setup

Config at: `ops/secrets/MASTER.env`
```
TELEGRAM_BOT_TOKEN=<bot token>
TELEGRAM_CHAT_ID=<CEO chat ID>
NULLCLAW_GATEWAY=http://localhost:<nullclaw-port>
```

Tool: `tools/core_intel/` — nullclaw messenger module
Script: `start_nullclaw.ps1` (launcher/)

### Test notification:
```powershell
# Test từ PowerShell
$body = @{
    type = "SYSTEM_ERROR"
    priority = "NORMAL"
    title = "Test notification"
    body = "AI OS notification-bridge working ✅"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:<nullclaw-port>/notify" -Method POST -Body $body -ContentType "application/json"
```

---

## GAP PROPOSAL Format (CEO nhận qua Telegram)

```
🆕 GAP PROPOSAL — [GAP-2026-03-24-DOMAIN]

DOMAIN: <chưa có agent/dept phụ trách X>
CONTENT: <tên repo/URL đã nhận>

Options:
[A] Tạo agent mới → agent-auto-create.md
[B] Assign vào dept gần nhất: <dept-name>
[C] Create new department → dept-builder-agent
[D] Skip — lưu reference, không tạo gì

Reply A/B/C/D trong 24h. Default: B nếu không reply.
GAP saved: corp/gaps/GAP-<date>-<domain>.md
```

---

## LightRAG Port Verification

LightRAG API: `http://localhost:9621`
```bash
# Test LightRAG (run in terminal):
curl http://localhost:9621/health
# Expected: {"status": "ok"}

# Start LightRAG (nếu DOWN):
cd tools/lightrag  # hoặc nơi cài lightrag
python -m lightrag.api --host 0.0.0.0 --port 9621 --working-dir brain/knowledge/lightrag_db
```

Config: `brain/lightrag_adapter.py` và `ops/scripts/index_skills_lightrag.py`

---

## open-notebook Port Verification

open-notebook API: `http://localhost:5055`
```bash
# Test open-notebook (run in terminal):
curl http://localhost:5055/health
# Expected: 200 OK

# Start open-notebook (nếu DOWN):
# Ref: skills/ hoặc plugins/openrag/ directory
```

---

## KPI / Escalations / Mission — Correct Paths

> **CANONICAL PATH:** `brain/shared-context/corp/`

| File | Correct Path |
|------|-------------|
| kpi_scoreboard.json | `brain/shared-context/corp/kpi_scoreboard.json` |
| escalations.md | `brain/shared-context/corp/escalations.md` |
| mission.md | `brain/shared-context/corp/mission.md` |
| proposals/ | `brain/shared-context/corp/proposals/` |
| daily_briefs/ | `brain/shared-context/corp/daily_briefs/` |

**corp/escalations.md** = redirect/alias. Real file = `brain/shared-context/corp/escalations.md`

GEMINI.md boot references should use `brain/shared-context/corp/` prefix.

---

*v1.0 | 2026-03-24 | notification-bridge covers ALL channels*
