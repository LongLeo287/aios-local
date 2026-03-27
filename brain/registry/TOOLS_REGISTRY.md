# AI OS — Master Tools Registry
# Path: D:\Project\AI OS\registry\TOOLS_REGISTRY.md
# Updated: 2026-03-17
# Purpose: Inventory and categorize all tools in AI OS ecosystem

---

## 📊 Tools Summary

| Category | Count |
|---|---|
| **Automation Scripts** | 10 |
| **Memory Tools** | 2 |
| **Skill Tools** | 3 |
| **MCP Servers** | 2 |
| **Workflow Templates** | 4 |
| **Security Tools** | 1 |
| **Total Tools** | **22** |

---

## ⚙️ CATEGORY 1: Automation & Lifecycle Scripts

Located in `scripts/`

| Tool | File | Function |
|---|---|---|
| **Backup Project** | `backup-project.ps1` | Full project snapshot backup |
| **Backup Memory** | `Backup_Memory.bat` | Quick memory backup trigger |
| **WakeUp Memory** | `WakeUp_Memory.bat` | Restore memory on session start |
| **Wakeup Project** | `wakeup-project.ps1` | Load project context on boot |
| **Wakeup Session** | `wakeup.ps1` | General AI OS session init |
| **Backup Soul** | `scripts/memory/backup_soul.ps1` | Soul Sync — backup AI brain state |
| **Wake Soul** | `scripts/memory/wake_up.ps1` | Soul Sync — restore AI brain state |
| **Register Project** | `register_project.ps1` | Register new project in `registry.json` |
| **Handoff to Claude** | `handoff_to_claude_code.ps1` | Agent handoff protocol (full session state transfer) |
| **Migrate Skills** | `migrate_skill_frontmatter.ps1` | Bulk migrate SKILL.md frontmatter format |
| **Pre-Ingest Check** | `pre-ingest-check.ps1` | Pre-flight checks before repo ingestion |

---

## 🔐 CATEGORY 2: Security Tools

Located in `skills/security_shield/`

| Tool | File | Function |
|---|---|---|
| **Strix v2.0** | `skills/security_shield/vet_repo.ps1` | 12-stage security scan for repos — CVE, obfuscation, secrets, binary blobs, Unicode attacks |

**Strix Scan Stages:**
`HIDDEN_PAYLOAD` • `OBFUSCATION` • `SENSITIVE_ACCESS` • `NETWORK_EXFIL` • `CRYPTO_MINING` • `BINARY_BLOB` • `UNICODE_ATTACK` • `SHELL_INJECTION` • `DEPENDENCY_CONFUSION` • `GIT_HOOKS` • `ENV_LEAK` • `SUPPLY_CHAIN`

---

## 🎯 CATEGORY 3: Skill Tools

| Tool | Location | Function |
|---|---|---|
| **Skill Loader** | `scripts/skill_loader.ps1` | Load skills into active session context |
| **Skill Fetcher** | `scripts/skill_fetcher.ps1` | Fetch & cache skills from registry |
| **Skill Generator** | `tools/skill-generator/` + `plugins/skill-generator/` | 8-phase pipeline to create SKILL.md from any workflow |

---

## 🌐 CATEGORY 4: MCP Servers

Located in `mcp/`

| Tool | File | Function |
|---|---|---|
| **MCP Core Server** | `mcp/server.js` | Main MCP JSON-RPC server (10KB — full featured) |
| **MCP Bridge** | `mcp/mcp-server.js` | Lightweight MCP bridge layer |
| **Bookmark Server Config** | `mcp/servers/bookmark-server.config.json` | Smart Bookmark Reader config |
| **Native Messaging** | `mcp/servers/native-messaging-manifest.json` | Browser ↔ Claude Code native messaging |

**Active MCP Connections (from `mcp/config.json`):**
- `filesystem` — Access to BookMark Extension + Tiem Nuoc Nho workspace
- `github-bridges` — GitHub docs bridge

---

## 📋 CATEGORY 5: Workflow Templates

Located in `.agent/workflows/`

| Template | File | Function |
|---|---|---|
| **CLI Handoff** | `automated_cli_handoff.md` | SOP for automated CLI session handoff |
| **Delegation SOP** | `delegation_sop_boilerplate.md` | Boilerplate for agent delegation |
| **Export Template** | `export_ai_os_template.md` | Export AI OS config as portable template |
| **Recovery Protocol** | `recovery-protocol.md` | Emergency recovery steps when AI OS state is lost |

---

## 🔗 CATEGORY 6: Tool Integration Map

```
USER REQUEST
    │
    ├── New Session? → wakeup.ps1 → soul/wake_up.ps1 → load context
    │
    ├── New Project? → register_project.ps1 → registry.json
    │
    ├── New Repo? → vet_repo.ps1 (Strix) → pre-ingest-check.ps1 → skill_fetcher.ps1
    │
    ├── New Skill? → skill-generator (8-phase) → skill_loader.ps1
    │
    ├── Backup? → backup-project.ps1 → backup_soul.ps1
    │
    ├── Agent Handoff? → handoff_to_claude_code.ps1 → delegation_sop
    │
    └── AI Tool Call? → MCP Server (server.js) → filesystem/github-bridges
```

---

## 🏷️ Tool Tier Classification

| Tier | Tools |
|---|---|
| **T0 Core** | `vet_repo.ps1` (Strix), `wakeup.ps1`, `backup_soul.ps1`, `wake_up.ps1`, `handoff_to_claude_code.ps1`, `skill_loader.ps1`, MCP Core Server |
| **T1 Strategic** | `register_project.ps1`, `backup-project.ps1`, `skill_fetcher.ps1`, `skill-generator` |
| **T2 Operational** | `migrate_skill_frontmatter.ps1`, `pre-ingest-check.ps1`, Workflow Templates |
| **T3 Experimental** | Bookmark MCP Config, Native Messaging |

---

*Path: D:\Project\AI OS\registry\TOOLS_REGISTRY.md*
*Auto-update when new tools are added to scripts/, mcp/, or tools/*
