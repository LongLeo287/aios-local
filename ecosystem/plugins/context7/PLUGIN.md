# PLUGIN.md — Context7
# AI OS Plugin | Tier 2 | Owner: Dept 4 Registry
# Version: latest | Installed: 2026-03-24
# RULE-AGENT-PLATFORM-01: Không độc quyền — setup cho ALL platforms

## Mô tả

Context7 là MCP server cung cấp documentation thư viện real-time cho LLM. Giải quyết hallucinated APIs và outdated code examples.

## Platform Support (KHÔNG ĐỘC QUYỀN)

| Platform | Cài đặt | Status |
|----------|---------|--------|
| Antigravity (Gemini/VS Code) | Thêm vào `mcp_config.json` | ✅ Active |
| Claude Code CLI | `npx ctx7 setup --claude` | ⏳ Chờ Claude CLI init |
| Cursor | `npx ctx7 setup --cursor` | ✅ Active |

## Cách dùng

Thêm `use context7` vào cuối prompt khi cần docs thư viện chính xác:

```
"Tạo Supabase Edge Function với JWT auth. use context7"
"Cài đặt Firecrawl v2 với custom scraper. use context7"  
"Next.js 15 App Router middleware. use context7"
```

## MCP Config (Antigravity/Cursor)

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp@latest"]
  }
}
```

## MCP Tools

- `resolve-library-id` — tìm ID thư viện từ tên
- `get-library-docs` — lấy docs theo version và topic

## Scope

ALL agents, ALL departments. Đặc biệt quan trọng cho: Engineering (Dept 1), Data (Dept 6), Backend skills.

## Rules

Xem: `GEMINI.md` → `[RULE-CONTEXT7-01]`
