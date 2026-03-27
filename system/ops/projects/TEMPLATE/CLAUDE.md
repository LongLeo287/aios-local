# Project: [PROJECT_NAME] â€” AI OS Connected
# PRJ-ID: PRJ-XXX
# Status: active
# Updated: [DATE]

> **Satellite project of AI OS.**  
> Skills, knowledge, and agents from AI OS are available here.
> See: `<AI_OS_ROOT>\CLAUDE.md` for full governance.

---

## ðŸ§­ Identity

- **Project name:** [PROJECT_NAME]
- **Path:** [PROJECT_PATH]
- **Tech stack:** [e.g., React + TypeScript, Python, GAS]
- **Domain:** [e.g., POS, Web App, Data Pipeline]

---

## ðŸ› ï¸ Skills Loaded

<!-- List the AI OS skills relevant to this project -->

```
LOAD: <AI_OS_ROOT>\skills\[skill-name]\SKILL.md
```

Common options:
- `ui-ux-pro-max` â€” Premium UI/UX design
- `pos-event-sourcing` â€” POS audit & event tracing
- `gas-sheets-optimizer` â€” Google Apps Script & Sheets
- `knowledge_navigator` â€” Query AI OS knowledge base

---

## ðŸ“ Project Structure

```
[PROJECT_PATH]/
â”œâ”€â”€ [src or main code dir]/
â”œâ”€â”€ [config files]
â”œâ”€â”€ .agent/
â”‚   â””â”€â”€ CLAUDE.md          â† this file (or in .clauderules)
â””â”€â”€ DATA/ or docs/
```

---

## âš¡ Quick Commands

```bash
# Dev server
[dev command, e.g.: npm run dev]

# Build
[build command]

# Type check
[type check command, e.g.: npx tsc --noEmit]
```

---

## ðŸ”— AI OS Resources

| Resource | Path |
|----------|------|
| Master Entry | `<AI_OS_ROOT>\CLAUDE.md` |
| Skill Registry | `<AI_OS_ROOT>\shared-context\SKILL_REGISTRY.json` |
| Knowledge Base | `<AI_OS_ROOT>\knowledge\` |
| Blackboard | `<AI_OS_ROOT>\shared-context\blackboard.json` |
| Handoff Workflow | `<AI_OS_ROOT>\workflows\claude_code_handoff.md` |

---

## ðŸ”‘ Key Business Rules

<!-- Fill in project-specific rules here -->
1. [Rule 1]
2. [Rule 2]

---

## âš ï¸ Safe vs Prohibited Actions

**Safe (auto-approve):**
- Reading files, running dev server, type checking

**Require confirmation:**
- Deleting files, deploying to production, modifying config

**Never:**
- Touching AI OS core files from this workspace

