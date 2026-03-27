# PLUGIN_SPEC.md — AI OS Plugin Schema Standard
# Version: 2.0 | Updated: 2026-03-14
#
# SCOPE: AI OS-level plugins (d:\Project\AI OS\plugins\)
# This is NOT the BookMark Extension plugin spec.

## What Is a Plugin?

A **Plugin** extends the AI OS with capabilities that are:
- **Non-core** (not required for base OS operation)
- **Composable** (can depend on Skills but not on other plugins)
- **Isolable** (failure of a plugin must NOT crash the OS or other agents)

Plugins differ from Skills in that:
| Dimension | Skill | Plugin |
|-----------|-------|--------|
| Scope | Agent capability | System extension |
| Load | On-demand by role | Auto or manual |
| Dependencies | Skills only | Skills only |
| Failure mode | Fallback to base | Silent fail |
| State | Stateless | Can be stateful |

---

## Plugin Types

| Type | Description | Examples |
|------|-------------|---------|
| `cognitive` | Enhances agent reasoning or memory | `LightRAG`, `neural_memory` |
| `data` | Integrates external or local data sources | `langextract`, `eco-ingest` |
| `bridge` | Connects AI OS to external systems | `cloud-sync`, `notification_bridge` |
| `ui` | Provides dashboard or visual capabilities | `ai-os-viewer`, `ui-ux-pro-max` |

---

## Required Directory Structure

```
plugins/
└── <plugin_id>/
    ├── manifest.json     [REQUIRED] — Machine-readable metadata
    ├── PLUGIN.md         [REQUIRED] — Instructions & usage guide
    ├── README.md         [REQUIRED] — Human-readable overview
    ├── index.js          [OPTIONAL] — Entry point (if executable)
    └── tests/            [OPTIONAL] — Validation scripts
```

---

## manifest.json — Full Schema

```json
{
  "id": "<plugin_id>",
  "name": "<Human Readable Name>",
  "version": "<SemVer>",
  "type": "cognitive | data | bridge | ui",
  "status": "active | beta | deprecated | planned",
  "description": "<one-line description>",
  "author": "AI OS Core Team",
  "updated": "YYYY-MM-DD",

  "skill_dependencies": [
    "<skill_id_1>",
    "<skill_id_2>"
  ],

  "agent_hooks": {
    "onBoot": false,
    "onTaskStart": false,
    "onTaskComplete": false,
    "onReflection": false,
    "onHandoff": false,
    "onError": false
  },

  "auto_load": false,

  "config": {
    "<config_key>": "<default_value>"
  },

  "exposed_api": [
    {
      "name": "<function_name>",
      "description": "<what it does>",
      "input": "<type>",
      "output": "<type>"
    }
  ],

  "isolation": {
    "can_crash_os": false,
    "timeout_seconds": 30,
    "memory_limit_mb": 256
  }
}
```

---

## Agent Hooks Reference

| Hook | Trigger | Use Case |
|------|---------|---------|
| `onBoot` | OS starts | Preload data, warm caches |
| `onTaskStart` | Agent begins a new task | Context injection, resource setup |
| `onTaskComplete` | Agent finishes a task | Result archiving, metrics collection |
| `onReflection` | Agent enters [REFLECTION] mode | Lesson extraction, knowledge update |
| `onHandoff` | Agent hands off to another agent | Context packaging, receipt generation |
| `onError` | Any tool failure occurs | Error logging, fallback activation |

---

## Plugin Rules

1. Plugins **CANNOT** modify `Tier 0` or `Tier 1` files (`CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `THESIS.md`)
2. Plugins **CANNOT** depend on other plugins (only on Skills)
3. Plugins **MUST** declare `"can_crash_os": false` and handle all errors internally
4. Plugins **MUST** have a timeout — long-running plugins use async via `subagents/mq/`
5. Plugins **MUST** log to `telemetry/receipts/` when activated
6. Plugins with `auto_load: true` are started at boot — use sparingly

---

## Currently Registered Plugins

| Plugin ID | Type | Status | Description |
|-----------|------|--------|-------------|
| `LightRAG` | cognitive | planned | Graph-based RAG for knowledge retrieval |
| `ai-tagger` | cognitive | planned | Automatic semantic tagging of content |
| `smart-search` | cognitive | planned | Hybrid semantic + keyword search |
| `cloud-sync` | bridge | planned | Cloud backup and cross-machine sync |
| `langextract` | data | planned | Language/structure extraction from web |
| `ui-ux-pro-max` | ui | planned | Premium UI generation skill plugin |

---

## Plugin Lifecycle

```
[REGISTERED] ──► [LOADED] ──► [ACTIVE] ──► [IDLE] ──► [UNLOADED]
                                 │
                                 ▼
                            [ERROR] ──► [QUARANTINE]
```

- **REGISTERED:** Listed in `plugins/registry.json` but not yet loaded
- **LOADED:** `manifest.json` parsed, `skill_dependencies` verified
- **ACTIVE:** Currently running, hooks subscribed
- **IDLE:** Paused between tasks (preserves state)
- **QUARANTINE:** Failed 2+ times — disabled until reviewed by Antigravity

---

## Plugin Registry File

The master registry is at `d:\Project\AI OS\plugins\registry.json`.
Format:
```json
{
  "version": "2.0",
  "updated": "YYYY-MM-DD",
  "plugins": [
    {
      "id": "<plugin_id>",
      "path": "d:\\Project\\AI OS\\plugins\\<plugin_id>\\manifest.json",
      "status": "<status>",
      "auto_load": false
    }
  ]
}
```

---

*"A plugin adds power; a bad plugin adds chaos. Isolation is the price of extensibility."*
