---
id: notification_bridge
name: Notification Bridge
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Push notifications and multi-channel alerting (ccpoke Protocol).

accessible_by:
  - Orchestrator
  - User Experience

dependencies: []

exposed_functions:
  - name: send_alert
  - name: manage_subscriptions
  - name: push_to_channel

consumed_by:
  - orchestrator_pro
emits_events:
  - alert_sent
listens_to:
  - task_complete
  - task_failed
  - health_report_ready
---
# ðŸŒ‰ Notification Bridge Skill (Remote Connection)

This skill enables the AI OS to bridge with external communication channels (Telegram, Discord, Slack) inspired by the `ccpoke` protocol.

## ðŸ› ï¸ Core Functions:
1.  **Task Notifications (/notify):**
    - Send a push notification when a long-running task is complete.
    - Status updates: `[STARTING]`, `[IN_PROGRESS]`, `[COMPLETED]`, `[FAILED]`.
2.  **Remote Feedback Loop:**
    - Receive user approval/rejection for critical actions via remote chat.
3.  **Activity Reporting:**
    - Generate a "Summary Report" of the morning stack or night operations for mobile consumption.

## ðŸ“‹ Instructions:
- Use the `blackboard.json` to post signals for the Notification Bridge.
- Prioritize notifications for `[CRITICAL]` severity events.

## Principle:
*"Connected, yet controlled. Always present, never intrusive."*

