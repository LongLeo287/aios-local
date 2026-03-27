# Department: operations
---
description: AI OS V3.1 Central Workflow Orchestrator — route tasks to agents, update HUD, notify Telegram
---

# AI OS Workflow Orchestrator — V3.1
**Script:** `system/ops/aios_orchestrator.py`
**Telegram:** `system/ops/telegram_dispatch.py`
**Owner:** Antigravity (Master Orchestrator)

---

## Architecture

```
                        ┌────────────────────────────┐
                        │   BLACKBOARD.JSON           │
                        │   (Task Queue & State)      │
                        └───────────────┬────────────┘
                                        │ read
                        ┌───────────────▼────────────┐
                        │   AIOS ORCHESTRATOR         │
                        │   aios_orchestrator.py      │
                        └──┬────────────┬──────────┬─┘
                           │route       │update    │notify
              ┌────────────▼──┐  ┌──────▼──────┐  ┌▼──────────────┐
              │ AGENT ROUTER  │  │ HUD STATUS  │  │ TELEGRAM BOT  │
              │ domain→agent  │  │ STATUS.json │  │ @aios_corp_bot│
              └──────────┬────┘  └─────────────┘  └───────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   devops-agent   knowledge_agent   security-agent
   (gcp_deploy)  (knowledge_nav)   (agent-shield)
```

---

## Chạy Orchestrator

```bash
# Chạy 1 lần (kiểm tra + update HUD)
python system/ops/aios_orchestrator.py once

# Chạy liên tục (poll mỗi 30 giây)
python system/ops/aios_orchestrator.py watch 30

# Gửi Telegram status
python system/ops/telegram_dispatch.py status

# Test Telegram connection
python system/ops/telegram_dispatch.py test
```

---

## Agent Routing Table

| Domain | Agent | Primary Skill |
|--------|-------|---------------|
| `engineering` | `backend-architect-agent` | `reasoning_engine` |
| `devops` | `devops-agent` | `shell_assistant` |
| `security` | `security-engineer-agent` | `agent-shield` |
| `knowledge` | `knowledge_agent` | `knowledge_navigator` |
| `research` | `knowledge_agent` | `web_intelligence` |
| `data` | `data-agent` | `reasoning_engine` |
| `content` | `content-agent` | `reasoning_engine` |
| `marketing` | `growth-agent` | `web_intelligence` |
| `comms` | `channel_agent` | `channel_manager` |
| `cloud` | `devops-agent` | `gcp_deploy_skill` |

---

## Telegram Dispatch Commands

```python
from system.ops.telegram_dispatch import notify, alert_task_blocked, send_system_status

# Gửi notification
notify("Title", "Body", priority="INFO")

# Alert blocked task
alert_task_blocked("TASK-001", "devops-agent", "gcloud auth required")

# Daily digest
send_system_status()
```

---

## Cấu Hình Telegram

Thêm vào `.env`:
```
TELEGRAM_BOT_TOKEN=<bot token từ @BotFather>
TELEGRAM_CHAT_ID=<CEO's Telegram chat ID>
```

---

## Receipts & Audit Trail

Mọi dispatch được ghi vào:
`system/telemetry/receipts/<agent_id>/<task_id>.json`

Notifications (khi MCP offline):
`system/telemetry/notifications/notif_<timestamp>.json`

---
*AI OS V3.1 | Workflow Orchestrator | 2026-03-26*
