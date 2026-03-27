---
source: https://github.com/modelcontextprotocol/servers
ingested_at: 2026-03-16T10:05:00+07:00
domain: AI|Integration|MCP
trust_level: HIGH
vet_status: PASS
tags: [mcp, official-servers, reference-implementation, anthropic, npm]
---

# MCP Official Reference Servers

Repo chính thức: https://github.com/modelcontextprotocol/servers  
Đây là **reference implementations** — ví dụ giáo dục + production-ready cơ bản.

---

## Danh sách Official Servers

### 1. `@modelcontextprotocol/server-filesystem`
**Purpose:** Secure file operations với configurable access controls

**Tools cung cấp:**
- `read_file` — đọc file
- `write_file` — ghi file
- `create_directory` — tạo thư mục
- `list_directory` — liệt kê nội dung
- `move_file` — di chuyển/rename
- `search_files` — tìm kiếm file
- `get_file_info` — metadata

**Config trong `mcp/config.json`:**
```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y", "@modelcontextprotocol/server-filesystem",
      "/allowed/path/1",
      "/allowed/path/2"
    ]
  }
}
```
> ⚠️ Chỉ cho phép access vào các paths được chỉ định — sandboxed.

---

### 2. `@modelcontextprotocol/server-memory`
**Purpose:** Knowledge graph-based persistent memory

**Tools cung cấp:**
- `create_entities` — tạo entities mới
- `create_relations` — tạo quan hệ giữa entities
- `add_observations` — thêm observations
- `delete_entities` / `delete_relations`
- `search_nodes` — semantic search trong graph
- `read_graph` — đọc toàn bộ graph
- `open_nodes` — xem entities cụ thể

**Storage:** JSON file local (mặc định `~/memory.json`)

**Config:**
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  }
}
```

---

### 3. `@modelcontextprotocol/server-github`
**Purpose:** GitHub API integration đầy đủ

**Tools cung cấp:**
- Repository management (create, fork, search)
- File operations (read, create, update)
- Pull request handling (create, review, merge)
- Issue management (create, close, comment)
- Code search across repositories
- Branch management

**Config:**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>" }
  }
}
```

---

### 4. `@modelcontextprotocol/server-postgres`
**Purpose:** Read-only PostgreSQL access

**Khả năng:**
- Schema inspection (tables, columns, types)
- Read-only SQL query execution
- Database structure exploration

**Config:**
```json
{
  "postgres": {
    "command": "npx",
    "args": [
      "-y", "@modelcontextprotocol/server-postgres",
      "postgresql://user:pass@localhost/dbname"
    ]
  }
}
```

---

### 5. `@modelcontextprotocol/server-sqlite`
**Purpose:** SQLite database interaction + business intelligence

**Khả năng:**
- Read + Write SQLite databases
- Schema inspection
- Query execution + visualization
- Lightweight data analysis

**Config:**
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/db.sqlite"]
  }
}
```

---

### 6. `@modelcontextprotocol/server-brave-search`
**Purpose:** Web + local search via Brave Search API

**Khả năng:**
- Web search với pagination
- Local search (near me)
- Filtering + smart fallbacks
- Privacy-focused (không track)

**Yêu cầu:** BRAVE_API_KEY (free tier có sẵn)

**Config:**
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": { "BRAVE_API_KEY": "<your-key>" }
  }
}
```

---

### 7. `@modelcontextprotocol/server-fetch`
**Purpose:** Web content fetching + LLM-optimized conversion

**Khả năng:**
- Fetch URLs và convert sang Markdown
- Tối ưu output cho LLM consumption
- Bypass một số paywalls (public content)
- Xử lý redirects

**Config:**
```json
{
  "fetch": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-fetch"]
  }
}
```

---

### 8. `@modelcontextprotocol/server-everything`
**Purpose:** Test + demo server — tất cả MCP features

**Dùng để:** Testing MCP client implementations, không dùng production.

---

## Install tất cả một lần

```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-sqlite
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-fetch
```

Hoặc dùng `npx -y` trong config (auto-install khi chạy).

---

## Config đầy đủ cho AI OS (`mcp/config.json`)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "d:/Project"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "BSA..." }
    }
  }
}
```

> 💡 Tokens nhạy cảm nên để trong `.env`, không commit vào git.

---

## Ưu tiên tích hợp cho AI OS

| Priority | Server | Lý do |
|----------|--------|-------|
| 🔴 Ngay | `server-filesystem` | Skills cần đọc/ghi files |
| 🔴 Ngay | `server-memory` | Persistent agent memory thay `.ai-memory/` |
| 🟡 Sớm | `server-github` | Code management, PR automation |
| 🟡 Sớm | `server-fetch` | Thay thế khi browser offline |
| 🟢 Sau | `server-brave-search` | Web search capability |
| 🟢 Sau | `server-postgres` / `server-sqlite` | Data skills |

---

## References
- [Official Repo](https://github.com/modelcontextprotocol/servers)
- [npm: @modelcontextprotocol](https://www.npmjs.com/org/modelcontextprotocol)
- [Docs](https://modelcontextprotocol.io/docs/tools/debugging)
