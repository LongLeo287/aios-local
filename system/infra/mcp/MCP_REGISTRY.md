# AI OS â€” MCP Server Registry
_Cáº­p nháº­t: 2026-03-17_

Táº¥t cáº£ MCP servers trong há»‡ thá»‘ng. Claude Code Ä‘á»c tá»« `mcp/config.json`.

## CÃ¡ch thÃªm vÃ o Claude Code

1. Má»Ÿ Claude Code settings â†’ MCP
2. Trá» Ä‘áº¿n `<AI_OS_ROOT>\mcp\config.json`
3. Hoáº·c copy ná»™i dung vÃ o `~/.claude/mcp.json`

---

## Servers

### 1. aos-workspace â­
- **File:** `mcp/servers/aos-workspace/index.js`
- **DÃ¹ng cho:** Duyá»‡t AI OS workspace, Ä‘á»c skills, plugins, blackboard
- **Tools:** `list_dir`, `read_file`, `search_skills`, `read_blackboard`, `read_context`, `list_plugins`
- **Start test:** `node mcp/servers/aos-workspace/index.js --test`

### 2. skill-registry
- **File:** `mcp/servers/skill-registry/index.js`
- **DÃ¹ng cho:** Query SKILL_REGISTRY.json â€” list, get, health check
- **Tools:** `list_skills`, `get_skill`, `check_health`, `get_registry_summary`
- **Start test:** `node mcp/servers/skill-registry/index.js --test`

### 3. corp-data
- **File:** `mcp/servers/corp-data/index.js`
- **DÃ¹ng cho:** KPI, escalations, proposals, org chart, mission
- **Tools:** `get_kpi_board`, `update_kpi`, `list_escalations`, `add_escalation`, `get_proposals`, `get_mission`, `get_org_chart`
- **Start test:** `node mcp/servers/corp-data/index.js --test`

### 4. filesystem (existing)
- **Loáº¡i:** `@modelcontextprotocol/server-filesystem` (official MCP package)
- **DÃ¹ng cho:** General file access â€” AI OS root + BookMark + POS

### 5. github-bridges (existing)
- **DÃ¹ng cho:** GitHub docs bridge

---

## Servers KHÃ”NG dÃ¹ng MCP (HTTP thay tháº¿)

> DÃ nh cho ChatGPT, Gemini, AI Studio

| Platform | CÃ¡ch truy cáº­p |
|----------|--------------|
| ChatGPT Education | GPT Actions â†’ `api/openapi.json` |
| Gemini Pro | REST API: `http://localhost:7000/api/*` |
| Google AI Studio | REST API: `http://localhost:7000/api/*` |
| Má»i HTTP client | `GET /api/skills`, `POST /api/corp/escalate`, ... |

**Start REST API:** `node api/server.js` hoáº·c `.\cli\aos.ps1 api start`

---

## CÃ i dependencies

```bash
# Cho MCP servers (Node.js >= 18)
cd mcp/servers/aos-workspace && npm init -y && npm install @modelcontextprotocol/sdk
cd ../skill-registry && npm init -y && npm install @modelcontextprotocol/sdk
cd ../corp-data && npm init -y && npm install @modelcontextprotocol/sdk

# Test táº¥t cáº£
.\cli\aos.ps1 mcp test all
```

---

## Servers Added Cycle 8 — 2026-03-23

### 6. sequential-thinking (Official MCP)
- **Package:** @modelcontextprotocol/server-sequential-thinking
- **Version:** v1.21.5 (2026-03-17)
- **Dùng cho:** Dynamic reflective problem-solving — agent tu duy theo chu?i steps
- **Start:** 
px @modelcontextprotocol/server-sequential-thinking
- **Source:** modelcontextprotocol/servers (Anthropic official)

### 7. mcp-git (Official — via uvx, Python)
- **Package:** mcp-server-git (Python, dùng uvx)
- **Dùng cho:** Read, search, manipulate Git repos — code review, PR ops
- **Start:** uvx mcp-server-git --repository d:\AI OS CORP
- **Note:** Requires Python + uvx. Alternative: use GitHub official MCP for cloud ops.
- **Source:** modelcontextprotocol/servers (Anthropic official)

### Source: modelcontextprotocol/servers
- 907 contributors | 24 releases | MIT
- **MASTER MCP INDEX** — supersedes punkpeye/awesome-mcp-servers
- KI Note: brain/knowledge/notes/KI-MCP-OFFICIAL-SERVERS-01.md

