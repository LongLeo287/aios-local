# Department: monitoring_inspection
---
description: AI OS Bot Reporting Protocol â€” how to report status, tasks, and alerts via Telegram bot
---

# AI OS Bot Reporting Protocol

## Quy táº¯c chung
// turbo-all

Má»i káº¿t quáº£ audit, task completion, alert Ä‘á»u PHáº¢I push lÃªn bot trÆ°á»›c khi bÃ¡o cÃ¡o vá»›i user.

---

## 1. Gá»­i report lÃªn bot

```python
# turbo
python -c "
import urllib.request, json
TOKEN = '[REDACTED_TELEGRAM_TOKEN]'
CHAT  = '646106732'
msg = '''[TITLE]
[CONTENT]'''
body = json.dumps({'chat_id': CHAT, 'text': msg}).encode()
req = urllib.request.Request(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=body, headers={'Content-Type': 'application/json'})
r = json.loads(urllib.request.urlopen(req, timeout=8).read())
print('Sent:', r.get('ok'), 'msg_id:', r.get('result',{}).get('message_id'))
"
```

---

## 2. CÃ¡c loáº¡i message chuáº©n

### Task Completion Report
```
âœ… [TASK_ID] COMPLETE â€” [date]

Done:
- item 1
- item 2

Pending:
- item X

Next: [next action]
```

### Audit / Status Report
```
AI OS Status [time]

=== [AREA] ===
[item]: [status]
...

=== NEXT PRIORITIES ===
1. [priority 1]
2. [priority 2]
```

### Alert / Issue Found
```
âš ï¸ ISSUE FOUND â€” [severity]
Area: [file/service]
Issue: [description]
Impact: [impact]
Fix: [proposed fix]
```

### Brainstorm / Idea
```
ðŸ’¡ BRAINSTORM â€” [topic]
Context: [why now]
Ideas:
1. [idea 1]
2. [idea 2]
Recommended: [best option]
```

---

## 3. Khi nÃ o push lÃªn bot

| Trigger | Action |
|---------|--------|
| HoÃ n thÃ nh 1 Sprint/Phase | Push full completion report |
| PhÃ¡t hiá»‡n critical bug/issue | Push alert ngay |
| Báº¯t Ä‘áº§u session má»›i | Push context summary |
| Káº¿t thÃºc session | Push pending tasks summary |
| Brainstorm xong | Push ideas list |
| Task list thay Ä‘á»•i | Push updated task status |

---

## 4. Blackboard Protocol (Antigravity â†’ Bot)

Khi Antigravity muá»‘n tráº£ lá»i message tá»« user qua bot:

```python
# Write to telegram_outbox trong blackboard.json
bb["telegram_outbox"] = {
    "user_id": "646106732",
    "reply": "[message content]",
    "ts": datetime.now().isoformat()
}
```

Bot sáº½ tá»± Ä‘á»™ng pick up trong vÃ²ng <3 giÃ¢y vÃ  gá»­i cho user.

---

## 5. MQ Task Queue (Long-running tasks)

```bash
# Bot nháº­n message â†’ viáº¿t vÃ o subagents/mq/tg_<id>.json
# Antigravity Ä‘á»c â†’ xá»­ lÃ½ â†’ viáº¿t reply vÃ o task["reply"]
# Bot poll â†’ gá»­i reply vá» user (timeout 2.5s)
```

Vá»›i task phá»©c táº¡p: Antigravity Ä‘á»c _BB_PATH.telegram_inbox vÃ  reply qua telegram_outbox.

