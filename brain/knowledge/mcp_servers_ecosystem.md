---
source: https://github.com/punkpeye/awesome-mcp-servers
ingested_at: 2026-03-16T09:46:00+07:00
domain: AI|Architecture|Integration
trust_level: HIGH
vet_status: PASS
tags: [mcp, model-context-protocol, ai-tools, integration, llm]
---

# Awesome MCP Servers — Curated Knowledge

Danh sách curated các MCP (Model Context Protocol) server — giao thức mở cho phép LLM kết nối an toàn với các hệ thống bên ngoài.

**Repo:** https://github.com/punkpeye/awesome-mcp-servers  
**Author:** punkpeye  
**Trust:** Community-curated, high stars, active community

---

## MCP là gì?

Model Context Protocol (MCP) là một **giao thức mở** cho phép AI models tương tác an toàn với:
- Local resources (files, databases, system)
- Remote services (APIs, SaaS, cloud platforms)
- Development tools (GitHub, terminals, IDEs)

MCP server đóng vai trò **bridge** giữa LLM ↔ external system.

---

## 26 Categories (2026-03)

### 🔗 Aggregators
Một MCP server access nhiều app/tool cùng lúc qua single interface.

### 🎨 Art & Culture
Access art collections, cultural heritage, museum databases.

### 🌐 Browser Automation
Web scraping, content extraction, Puppeteer/Playwright automation.
- `agent-infra/mcp-server-browser` — Browser automation via Puppeteer (screenshots, scraping)
- `microsoft/playwright-mcp` — Official Microsoft Playwright MCP server
- `executeautomation/playwright-mcp-server` — Playwright-based automation server
- `merajmehrabi/puppeteer-mcp-server` — Puppeteer-based MCP server
- `chrome-devtools-mcp` — Puppeteer MCP for browser automation & debugging
- `aparajithn/agent-scraper-mcp` — Web scraping for AI agents

### ☁️ Cloud Platforms
AWS, GCP, Azure integrations.

### 💾 Cloud Storage
S3, GCS, Azure Blob và các cloud storage providers.

### 💻 Coding Environments
Generate, run, debug code — sandbox environments.

### 💬 Communication
Slack, Telegram, Discord và messaging platforms.
- Automate messaging và real-time notifications

### 📊 Customer Data Platforms
CRM và customer data integration.

### 🗄️ Databases
PostgreSQL, SQLite, MongoDB và các popular databases.
- `modelcontextprotocol/server-postgres` — Official PostgreSQL MCP (read-only + schema inspection)
- `Postgres MCP Pro` — Performance analysis, query optimization cho PostgreSQL
- `modelcontextprotocol/server-sqlite` — SQLite queries + visual data analysis
- MongoDB MCP — Atlas integration, collection management
- SQL query over 40+ apps từ 1 MCP server duy nhất
- Semantic search over database content

### 🛠️ Development Tools
IDE integration, code analysis, testing tools.
- VS Code integration
- Code review automation
- Test generation và execution

### 📁 File Systems
Local file access, read/write operations.
- `modelcontextprotocol/server-filesystem` — Official Anthropic filesystem server
- Secure sandboxed file operations (configurable root paths)
- Support read, write, list, move, search operations

### 💰 Financial Data
Real-time stock prices, market data, financial APIs.

### 🏦 Finance Servers
Breaking news, critical financial data, trading information.

### 🧠 Knowledge & Memory
Long-term storage, entity relationships, cross-session recall.
- `modelcontextprotocol/server-memory` — Entity-relation graph stored locally (JSON)
- Integrate với GitHub Copilot để cung cấp persistent context
- Knowledge graph: entities, relations, observations
- Perfect cho AI OS persistent memory layer

### 📍 Location Services
Geolocation, maps, POI data.

### 📣 Marketing
Marketing automation, analytics, campaign tools.

### 📈 Monitoring
System monitoring, alerts, observability.

### 📝 Note Taking
Obsidian, Notion, note management tools.

### 💳 Payment Processing
Stripe, payment gateway integrations.

### ⚡ Productivity Tools
Calendar, tasks, project management.

### 🧪 Sandbox & Virtualization
Secure code execution, isolated testing environments.

### 🔍 Search & Web
Web search, information retrieval for LLMs.
- Google Search, Bing, DuckDuckGo integrations
- Structured web data extraction

### 📱 Social Media
Twitter/X, LinkedIn, social platform automation.

### 🤖 System Automation
OS-level automation, shell commands, system control.

### 🔀 Version Control
GitHub, GitLab — repository management, PR handling, code analysis.
- `modelcontextprotocol/server-github` — Official GitHub MCP: repos, PRs, issues, code search
- GitLab MCP — merge requests, pipelines, issues
- Clone, commit, branch, PR, issue management via natural language
- Code search across repositories

### 💬 Communication
Slack, Discord và messaging platforms.
- Slack MCP — read messages, post content, manage channels, threaded discussions
- Automated notifications và workflow triggers
- Multi-workspace support

### 🔄 Workflow Automation
n8n, Zapier-style workflow automation via MCP.
- Trigger workflows từ AI
- Conditional logic và multi-step automation

---

## Key Actionable Patterns cho AI OS

### Pattern 1: MCP trong AI OS context
AI OS hiện có `mcp/config.json` — có thể add thêm MCP servers:
```json
{
  "mcpServers": {
    "filesystem": { "command": "node", "args": ["...server-filesystem/..."] },
    "github": { "command": "node", "args": ["...server-github/..."] },
    "memory": { "command": "node", "args": ["...server-memory/..."] }
  }
}
```

### Pattern 2: MCP servers phù hợp nhất cho AI OS
| Priority | Server | Lý do |
|----------|--------|-------|
| HIGH | `@modelcontextprotocol/server-filesystem` | File access cho skills |
| HIGH | `@modelcontextprotocol/server-memory` | Persistent agent memory |
| HIGH | `@modelcontextprotocol/server-github` | Code review, PR management |
| MEDIUM | `@modelcontextprotocol/server-postgres` | Database skills |
| MEDIUM | Browser automation MCP | Web research skills |
| LOW | Search MCP | Enhanced web search |

### Pattern 3: Install MCP servers
```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-github
```

---

## References
- [GitHub Repo](https://github.com/punkpeye/awesome-mcp-servers)
- [MCP Official Docs](https://modelcontextprotocol.io)
- [KDNuggets Overview](https://www.kdnuggets.com)
