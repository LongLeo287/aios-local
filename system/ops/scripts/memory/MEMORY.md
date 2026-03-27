# PROJECT MEMORY — Smart Bookmark Manager

> Persistent memory across sessions. Read this FIRST every session.
> Last updated: 2026-03-10

---

## PROJECT STATE

- **Phase**: Foundation Build (Day 1)
- **Existing Code**: popup.html, popup.css, popup.js, manifest.json (basic working extension)
- **Architecture**: Vanilla JS + Chrome APIs + Manifest V3
- **System Built**: 2026-03-10 — Full project structure created

## ARCHITECTURE DECISIONS

- **No Framework**: Pure Vanilla JS — keeps extension lightweight (<50KB)
- **Manifest V3**: Service Worker instead of background page
- **BEM CSS**: Consistent naming, no CSS-in-JS
- **DDD Structure**: src/core/ for domain logic, separated from UI
- **Plugin Registry**: plugins/ folder with PLUGIN_SPEC.md spec

## CURRENT CODE STATE

### popup.js
- Uses `DOMContentLoaded` event
- State: `currentData`, `currentEditItem`, `dialogMode`, `isEditingFolder`, `selectedParentId`
- Functions: `init()`, `loadBookmarks()`, `setupEventListeners()`, `handleSearch()`, `openDialog()`, `closeDialog()`, `saveDialog()`
- Context menu: `ctxEdit`, `ctxDelete`

### popup.html
- Header with search + add buttons
- Main bookmark tree area
- Dialog modal for add/edit
- Context menu

### manifest.json
- Permissions: `bookmarks`, `favicon`
- Action: popup → popup.html

## KEY PATTERNS

- Debounce on search input (300ms)
- Chrome bookmarks API for all CRUD
- Dynamic rendering (no virtual DOM)

## AGENT SYSTEM

5 agents defined in `.ai/agents/`:
- orchestrator, ux-agent, dev-agent, qa-agent, ai-tagger-agent
- Each has 9-file dossier: ROLE, OBJECTIVE, RULES, PROMPT, SKILL, WORKFLOW, MEMORY, COST_POLICY, SUBAGENTS

## PLUGIN SYSTEM

3 plugins planned:
1. `ai-tagger` — Auto-classify bookmarks with AI
2. `smart-search` — Semantic/vector search
3. `cloud-sync` — Backup to cloud

## NEXT SESSIONS TO DO

1. Refactor popup.js → DDD structure (src/core/)
2. Build UI component system (src/ui/components/)
3. Implement AI Tagger plugin
4. Setup MCP bridge
5. Write tests

## LESSONS LEARNED

- Extension ecosystem at D:\APP\Extension Ecosystem\ — has monorepo tooling to reuse
- LongLeo project at D:\APP\LongLeo\ — good governance patterns to borrow
- Github/ folder has curated repo references by category

## IMPORTANT FILES

```
CLAUDE.md              → Master rules (always read)
.system/config.json    → Global config
.rules/RULES.md        → Project rules
.ai/AGENTS.md          → Agent registry
plans/ROADMAP.md       → Product roadmap
docs/architecture/overview.md → Architecture
```

## REFERENCES (Github folder)

- BMAD-METHOD: Agile AI dev methodology
- Domain-Driven Hexagon: Architecture pattern
- openclaw/nanoclaw: Micro-worker patterns
- ui-ux-pro-max-skill: UI/UX skills reference
