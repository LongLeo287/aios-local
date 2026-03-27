# KI-MCP-SERVER-INDEX-01 — MCP Server Index (awesome-mcp-servers)
**Nguồn:** punkpeye/awesome-mcp-servers (140+ chunks, 40+ categories)
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE INDEX — tham khảo khi cần MCP server mới

---

## Mục đích
Index tham khảo khi AI OS cần thêm khả năng mới qua MCP.
**QUY TẮC:** Trước khi tự build MCP server mới → CHECK INDEX NÀY TRƯỚC.

## Categories có sẵn (40+)

| Category | Dùng khi AI OS cần... |
|----------|----------------------|
| 🔌 Aggregators | Quản lý nhiều MCP servers |
| 📂 Browser Automation | Điều khiển browser, test UI |
| ☁️ Cloud Platforms | AWS/GCP/Azure actions |
| 👨‍💻 Code Execution | Chạy code an toàn (sandbox) |
| 🤖 Coding Agents | Sub-agents cho coding tasks |
| 💬 Communication | Slack, Email, Discord integration |
| 🗄️ Databases | Query DB bằng natural language |
| 💻 Developer Tools | Git, CI/CD, IDE integration |
| 💰 Finance & Fintech | Crypto, stocks, banking APIs |
| 📂 File Systems | File read/write với access control |
| 🎮 Gaming | Game data APIs |
| 🧠 Knowledge & Memory | Vector stores, knowledge graphs |
| 🗺️ Location Services | Maps, geocoding |
| 🎯 Marketing | SEO, analytics, ad platforms |
| 📊 Monitoring | Metrics, alerts, dashboards |
| 🔬 Research | Academic papers, web search |
| 🔎 Search & Data Extraction | Web scraping, search APIs |
| 🔒 Security | Vulnerability scanning, secret management |
| 🌐 Social Media | Twitter/X, LinkedIn, Reddit |
| 🔄 Version Control | Git advanced operations |
| 🏢 Workplace & Productivity | Calendar, tasks, docs |

## Top Picks cho AI OS tiếp theo

### Knowledge & Memory (Priority cho AI OS)
- **mem0** MCP — AI OS đã có adapter, thêm MCP mode
- **Zep** — long-term memory với graph
- **Chroma** — vector store MCP

### Security (Dept 10)
- **Trivy** MCP — AI OS đã có skill, thêm MCP mode
- **Semgrep** — code security analysis
- **Vault** (HashiCorp) — secret management

### Developer Tools (Dept 1)
- **GitHub** official MCP — PR management, code review
- **Linear** — project management
- **Sentry** MCP — error tracking

### Search & Data (Firecrawl complement)
- **Brave Search** MCP — web search
- **Tavily** — research-optimized search
- **Arxiv** — academic papers

### Databases
- **Supabase** MCP — query, manage
- **PlanetScale** MCP (defer: database-js)
- **ClickHouse** — analytics

## How to Use This Index
```bash
# Query online
# https://github.com/punkpeye/awesome-mcp-servers#category-name

# When AI OS needs new capability:
# 1. Check category above
# 2. Find MCP server
# 3. Run trivy scan on it
# 4. If PASS → add to infra/mcp/MCP_REGISTRY.md
# 5. Dept 4 (Registry) approves
```

## Install Pattern (Claude Code)
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@server/package-name"]
    }
  }
}
```

*KI Note v1.0 | 2026-03-23 | Source: punkpeye/awesome-mcp-servers*
*Owner: Dept 4 (Registry) — update quarterly*
