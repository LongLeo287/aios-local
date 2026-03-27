---
description: GitHub integration stub — placeholder cho future GitHub webhook + PR review
---
# ops/integrations/github/README.md
# Version: stub-1.0 | 2026-03-25
# Status: PLACEHOLDER — wired và sẵn sàng, chưa activate
# Activate khi: CEO muốn gắn GitHub repo vào AI OS

---

## Planned Integration: GitHub → AI OS

### Use Cases (Future)

1. **PR Auto-Review**: PR mới → CIV pipeline đánh giá → comment trên GitHub
2. **Issue → Task**: GitHub Issue → auto-create task trong task_backlog.json
3. **Release → Notify**: New release → Telegram notify CEO
4. **Repo Intake**: CEO paste GitHub URL → CIV pipeline clone + analyze

---

## Architecture (Planned)

```
GitHub Webhook → infra/channels/github_bridge.py
    │
    ▼
bridge_router.py (handle_github_event)
    │
    ├─ PR event → CIV pipeline → review comment → GitHub API
    ├─ Issue event → task_backlog.json (append)
    └─ Push event → Telegram notify (@aios_corp_bot)
```

---

## Prerequisites (to activate)

1. **GitHub App / Webhook**: GitHub repo settings → Webhooks → point to ngrok/public URL
2. **GITHUB_TOKEN** in .env:
   ```
   GITHUB_TOKEN=ghp_xxxx       # Personal Access Token hoặc GitHub App token
   GITHUB_REPO=owner/repo
   GITHUB_WEBHOOK_SECRET=xxxx
   ```
3. **Bridge file**: `infra/channels/github_bridge.py` (create when activating)
4. **Public URL**: ngrok hoặc Cloudflare Tunnel để nhận webhook

---

## Activate When Ready

```powershell
# 1. Add to .env:
Add-Content ".env" "GITHUB_TOKEN=ghp_your_token"
Add-Content ".env" "GITHUB_REPO=your/repo"

# 2. Create bridge:
python ops/scripts/generate_github_bridge.py  # (to be built)

# 3. Register in start_bridges.py:
# Add: "github": ("github_bridge.py", bool(GITHUB_TOKEN))

# 4. Start:
python infra/channels/start_bridges.py github
```

---

## .env Placeholder (already added)
```
# GitHub (activate when ready)
GITHUB_TOKEN=
GITHUB_REPO=
GITHUB_WEBHOOK_SECRET=
```

---

*Stub v1.0 | 2026-03-25 | Activate: CEO says "gắn GitHub vào"*
