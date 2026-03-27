# Department: operations
---
description: Repo On-Demand â€” how agents clone large repos when starting a project
---

# ðŸ—‚ï¸ Repo On-Demand Workflow

## Khi nÃ o trigger
Tá»± Ä‘á»™ng khi:
- Agent/dept báº¯t Ä‘áº§u project má»›i (phase 3: dispatch)
- CEO táº¡o brief cÃ³ tá»« khÃ³a liÃªn quan (frontend, security, analytics, etc.)
- `aos.py project init <name>` Ä‘Æ°á»£c gá»i
- Telegram: `/project <description>`

Manual khi:
- CEO paste yÃªu cáº§u dá»± Ã¡n â†’ Antigravity nháº­n diá»‡n

---

## Step 1 â€” Auto-Detect (repo_resolver.py)

```powershell
# Tá»« mÃ´ táº£ dá»± Ã¡n
python ops/scripts/repo_resolver.py "Build analytics dashboard with KPI charts"

# Tá»« phÃ²ng ban
python ops/scripts/repo_resolver.py --dept engineering

# Tá»« file proposal
python ops/scripts/repo_resolver.py --file brain/shared-context/corp/proposals/PROP_xyz.md

# Auto-clone ngay
python ops/scripts/repo_resolver.py "Build security scanner for CIV" --clone
```

---

## Step 2 â€” Clone On-Demand

```powershell
# Lá»‡nh clone cho tá»«ng repo (xem LARGE_REPOS_CATALOG.md Ä‘á»ƒ chá»n)
git clone --depth 1 <URL> "<AI_OS_ROOT>\plugins\github-repos\<REPO>"
```

---

## Step 3 â€” Notify CEO

Sau khi clone â†’ Antigravity gá»­i Telegram:
```
ðŸ“¥ REPO CLONED
Source: github.com/...
Project: <tÃªn dá»± Ã¡n>
Dept: <phÃ²ng ban>
Path: plugins/github-repos/<name>
Size: xxx MB
```

---

## Step 4 â€” Cleanup (tÃ¹y chá»n)

```powershell
# XÃ³a repo sau khi dá»± Ã¡n xong (náº¿u khÃ´ng cáº§n giá»¯)
Remove-Item -Recurse -Force "<AI_OS_ROOT>\plugins\github-repos\<REPO>"
```

---

## Tag Map (auto-detect keywords)

| Tag | Keywords | Repos |
|-----|----------|-------|
| FRONTEND | web app, ui, dashboard, react | next.js, anime |
| VISUALIZATION | chart, graph, kpi, plot | plotly.js |
| ANALYTICS | analytics, tracking, metrics | posthog |
| SECURITY | scan, vulnerability, audit, civ | trivy |
| AI-PATTERNS | llm, rag, prompt, research | openai-cookbook |
| TRAINING | training, onboard, roadmap | developer-roadmap, agents-course |
| INTEGRATION | api, external, webhook | public-apis |
| DIAGRAM | whiteboard, architecture, draw | excalidraw |
| TEMPLATE | gitignore, repo setup | gitignore |

---

## Dept Defaults

| Dept | Auto-resolve repos |
|------|--------------------|
| engineering | next.js, plotly.js, openai-cookbook |
| design | excalidraw, anime, next.js |
| rd | openai-cookbook, agents-course, public-apis |
| security | trivy |
| analytics | posthog, plotly.js |
| training | agents-course, developer-roadmap |
| devops | trivy, gitignore |
| product | next.js, excalidraw, posthog |

---

## Integration Points

- `ops/aos.py project init <name> --dept <dept>` â†’ runs repo_resolver
- `ops/scripts/brief_writer.py` â†’ appends repo suggestions per dept
- `infra/channels/bridge_router.py` â†’ `/project <desc>` Telegram command
- `brain/knowledge/notes/LARGE_REPOS_CATALOG.md` â†’ human-readable catalog

---

*Workflow v1.0 | 2026-03-25 | Owner: Antigravity*

