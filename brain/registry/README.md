# Registry — How It Works
# D:\Project\AI OS\registry\

## Purpose

This folder is the **single source of truth** for all repositories, tools, websites,
and resources that have been reviewed, ingested, or tracked for the AI OS.

## Files

| File | Purpose |
|---|---|
| `REPO_REGISTRY.md` | Master list of all repos + status |
| `README.md` | This file |

## Workflow

```
User provides new link
       ↓
Agent reviews repo
       ↓
Add to REPO_REGISTRY.md (correct section)
       ↓
Set STATUS: 📥 Queued / ✅ Ingested / 🔍 Watchlist / 📦 Plugin
       ↓
If ingesting: clone to plugins/ or knowledge/
       ↓
Extract skills → create SKILL.md files in agents/ or subagents/
       ↓
Update STATUS → ✅ Ingested or 📦 Plugin
```

## Status Codes

| Code | Meaning |
|---|---|
| ✅ Ingested | Content analyzed and incorporated into AI OS knowledge/agents |
| 📦 Plugin | Installed locally in `plugins/` folder |
| 📥 Queued | Approved for next ingestion cycle |
| 🔍 Watchlist | Tracked, not yet prioritized |
| ❌ Rejected | Reviewed, not useful for AI OS |
