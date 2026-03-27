# KI-MCP-OFFICIAL-SERVERS-01 — Official MCP Server Registry
**Nguồn:** modelcontextprotocol/servers (Anthropic official)
**Stats:** 907 contributors | 24 releases | MIT | 50k+ stars
**Ngày:** 2026-03-23 | **Verdict:** APPROVE — MASTER INDEX, supersedes punkpeye/awesome-mcp-servers

---

## Tại sao repo này quan trọng hơn awesome-mcp-servers
- **Maintained by Anthropic** — chính thức, luôn cập nhật với MCP spec
- **907 contributors** — cộng đồng lớn hơn
- Có **Reference Servers** do Anthropic viết = gold standard implementation
- **Quality gate** — servers phải đáp ứng standard trước khi được list

---

## 1. Reference Servers (Anthropic Official — Install ngay)

| Server | Chức năng | Install |
|--------|-----------|---------|
| **Fetch** | Web content fetching → markdown cho LLM | `npx @modelcontextprotocol/server-fetch` |
| **Filesystem** | Secure file operations + access control | `npx @modelcontextprotocol/server-filesystem` |
| **Git** | Read, search, manipulate Git repos | `npx @modelcontextprotocol/server-git` |
| **Memory** | Knowledge graph-based persistent memory | `npx @modelcontextprotocol/server-memory` |
| **Sequential Thinking** | Dynamic reflective problem-solving | `npx @modelcontextprotocol/server-sequentialthinking` |
| **Time** | Time and timezone conversion | `npx @modelcontextprotocol/server-time` |

### AI OS Status:
- ✅ **Filesystem** — đã có (infra/mcp/MCP_REGISTRY.md server #4)
- ✅ **Fetch** — Firecrawl cover use case tốt hơn (self-hosted)
- ✅ **Memory** — Mem0 cover tốt hơn (vector store)
- ⭐ **Git** — CHƯA CÓ → **INSTALL NGAY** (Dept 1: code review, PR management)
- ⭐ **Sequential Thinking** — CHƯA CÓ → **INSTALL** (reasoning enhancement)
- ⭐ **Time** — Minor utility, low priority

### Install Git + Sequential Thinking (Claude Code):
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "d:\\AI OS CORP"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequentialthinking"]
    }
  }
}
```

---

## 2. Official Integrations — Top Picks cho AI OS

### Productivity & Communication
| Server | Provider | AI OS Use |
|--------|----------|-----------|
| **Slack** | Slack | Dept comms, CEO notifications |
| **Google Drive** | Google | Document storage |
| **Gmail** | Google | Email automation |
| **Linear** | Linear | Project management |
| **Notion** | Notion | Knowledge base |
| **Jira** | Atlassian | Issue tracking |

### Developer Tools
| Server | Provider | AI OS Use |
|--------|----------|-----------|
| **GitHub** (official) | GitHub | PR management, code review, repo ops |
| **Supabase** | Supabase | Direct DB queries |
| **Sentry** | Sentry | Error tracking from AI OS |
| **Cloudflare** | Cloudflare | Edge functions, DNS |

### Data & Analytics
| Server | Provider | AI OS Use |
|--------|----------|-----------|
| **AgentQL** | TinyFish | Structured web extraction (AI OS đã có skill) |
| **AgentOps** | AgentOps | Agent observability alternative (vs Langfuse) |
| **Algolia** | Algolia | Semantic search |
| **Snowflake** | Snowflake | Analytics DB |

### Security & Infrastructure
| Server | Provider | AI OS Use |
|--------|----------|-----------|
| **AWS** (official) | AWS | Cloud infrastructure |
| **GCP** | Google | Cloud infrastructure |
| **Azure** | Microsoft | Cloud infrastructure |
| **HashiCorp Vault** | HashiCorp | Secret management |

---

## 3. Frameworks (MCP Server Building)

### For Servers
- **FastMCP** (Python) — build MCP servers nhanh với Python
- **MCP Framework** (TypeScript) — official TypeScript SDK
- **Anthropic Server SDK** — used in Reference Servers

### AI OS ứng dụng
Khi build MCP servers mới cho AI OS (corp-data, skill-registry, aos-workspace):
```python
# Use FastMCP pattern (simpler than raw SDK)
from fastmcp import FastMCP

mcp = FastMCP("aos-workspace")

@mcp.tool()
def list_skills() -> list[str]:
    """List all installed AI OS skills"""
    return [d.name for d in Path("skills/").iterdir() if d.is_dir()]
```

---

## 4. AI OS Action Items (Priority)

| # | Action | Priority | Owner |
|---|--------|----------|-------|
| 1 | Install `server-git` MCP | P1 | Dept 1 |
| 2 | Install `server-sequentialthinking` MCP | P1 | All agents |
| 3 | Evaluate GitHub official MCP (replace github-bridges) | P2 | Dept 4 |
| 4 | Evaluate Supabase MCP (complement database-js) | P2 | Dept 1 |
| 5 | Evaluate Slack MCP for CEO notifications | P3 | Dept 1 |
| 6 | Update aos-workspace MCP server dùng FastMCP pattern | P3 | Dept 1 |

---

## 5. Relationship với KI-MCP-SERVER-INDEX-01
KI-MCP-SERVER-INDEX-01 = punkpeye/awesome-mcp-servers (community curated)
KI-MCP-OFFICIAL-SERVERS-01 = modelcontextprotocol/servers (Anthropic official)

**Use case:**
- Cần server chắc chắn stable → CHECK đây trước
- Niche/specialized server → check awesome-mcp-servers

*KI Note v1.0 | 2026-03-23 | Source: modelcontextprotocol/servers | 907 contributors | MIT*
*Owner: Dept 4 (Registry) — review quarterly với MCP spec updates*
