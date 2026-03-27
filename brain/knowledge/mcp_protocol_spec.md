---
source: https://github.com/modelcontextprotocol/modelcontextprotocol
ingested_at: 2026-03-16T10:03:00+07:00
domain: AI|Architecture|Integration|Protocol
trust_level: HIGH
vet_status: PASS
tags: [mcp, protocol-spec, json-rpc, anthropic, official, sdk]
---

# Model Context Protocol (MCP) — Official Specification

Giao thức chính thức do Anthropic tạo ra, hiện được host bởi **The Linux Foundation**.  
Docs: https://modelcontextprotocol.io  
Schema: TypeScript + JSON Schema

---

## Tổng quan

MCP = **"USB cho AI integrations"** — chuẩn hóa cách AI apps kết nối với external tools/data.

**Vấn đề giải quyết:** Trước MCP, mỗi LLM app phải viết custom integration riêng cho từng tool. MCP chuẩn hóa interface này.

**Lấy cảm hứng từ:** Language Server Protocol (LSP) — áp dụng cùng pattern cho AI ↔ external systems.

---

## Architecture: Client-Host-Server Model

```
┌─────────────────────────────────────┐
│  MCP HOST (AI App)                  │
│  (Claude Desktop, Claude Code, IDE) │
│                                     │
│   ┌──────────┐   ┌──────────┐       │
│   │MCP Client│   │MCP Client│  ...  │
│   └────┬─────┘   └────┬─────┘       │
└────────┼──────────────┼─────────────┘
         │              │
    JSON-RPC 2.0   JSON-RPC 2.0
         │              │
   ┌─────▼─────┐  ┌─────▼─────┐
   │MCP Server │  │MCP Server │  ...
   │(Filesystem│  │(GitHub)   │
   │ Database) │  │           │
   └───────────┘  └───────────┘
```

- **Host:** AI app người dùng tương tác (Claude Desktop, Claude Code, chatbot, IDE)
- **Client:** Component trong host, quản lý 1 connection đến 1 server
- **Server:** External program bridge giữa AI và external system

### Nguyên tắc thiết kế
- **Simplicity:** Server chỉ làm 1 việc cụ thể, Host xử lý orchestration
- **Composability:** Mỗi server hoạt động độc lập
- **Security:** Server không thấy conversation context hay server khác
- **Progressive:** Core protocol tối giản, features thêm dần

---

## Protocol Layer

### Data Layer — JSON-RPC 2.0

**3 Server Primitives:**

| Primitive | Mô tả | Ví dụ |
|-----------|-------|-------|
| **Tools** | Executable functions AI có thể gọi | file operations, API calls, DB queries |
| **Resources** | Data sources cung cấp context | file contents, DB records, API responses |
| **Prompts** | Reusable templates | system prompts, few-shot examples |

**Client Features:**
- **Sampling** — server-initiated agentic behaviors
- **Roots** — server hỏi về filesystem boundaries
- **Elicitation** — server yêu cầu user input

**Discovery Pattern:**
```
tools/list   → liệt kê tools
tools/call   → gọi tool
resources/list → liệt kê resources
resources/read → đọc resource
prompts/list   → liệt kê prompts
prompts/get    → lấy prompt
```
Hỗ trợ real-time notifications khi tools thay đổi.

### Lifecycle
1. Connection initialization
2. Capability negotiation (client + server trao đổi supported features)
3. Active session
4. Connection termination

---

## Transport Layer

| Transport | Dùng khi | Giao thức |
|-----------|----------|-----------|
| **STDIO** | Local server (same machine) | stdin/stdout |
| **Streamable HTTP** | Remote server | HTTP + SSE |

Go SDK còn hỗ trợ: WebSocket, gRPC.

---

## Official SDKs (9 ngôn ngữ)

| Language | Package | Notes |
|----------|---------|-------|
| **TypeScript** | `@modelcontextprotocol/sdk` | Node.js, Bun, Deno |
| **Python** | `mcp` (PyPI) | Most popular |
| **Java** | Spring AI collaboration | Sync + Async |
| **Kotlin** | Official SDK | |
| **C#** | Official SDK | |
| **Go** | Google collaboration | STDIO, SSE, WS, gRPC |
| **Ruby** | Official SDK | JSON-RPC handling built-in |
| **Rust** | Tokio async runtime | High performance |
| **Swift** | Official SDK | iOS/macOS support |

---

## Security & Authorization

### Threats
- Token theft
- Server compromise
- **Prompt injection** (embedded trong content)
- Excessive permission scopes
- Tool metadata manipulation

### Authorization: OAuth 2.1
- **PKCE** (SHA-256) bắt buộc
- All endpoints phải HTTPS
- Token expiration + rotation
- OAuth 2.0 Authorization Server Metadata discovery
- Dynamic Client Registration Protocol

**STDIO transport:** API keys (OAuth không cần thiết cho local)  
**HTTP transport:** Full OAuth 2.1 flow

### Session Security
- Verify all inbound requests
- Không dùng session cho authentication
- Session IDs phải secure + non-deterministic
- Bind session ID đến user-specific info

---

## Quick Start — Build MCP Server

### TypeScript
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.tool("my_tool", "Mô tả tool", { param: z.string() }, async ({ param }) => {
  return { content: [{ type: "text", text: `Result: ${param}` }] };
});

await server.connect(new StdioServerTransport());
```

### Python
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Mô tả tool"""
    return f"Result: {param}"

mcp.run()
```

---

## Relevance cho AI OS

| Aspect | AI OS Application |
|--------|------------------|
| MCP Host | Claude Code / Antigravity = MCP Host |
| `mcp/config.json` | Cấu hình các MCP servers AI OS sử dụng |
| Tools | Skills trong AI OS có thể expose qua MCP |
| Resources | Knowledge files expose như MCP Resources |
| Memory server | Thay thế `.ai-memory/` bằng `server-memory` |

**Next step cho AI OS:** Tích hợp thêm:
- `@modelcontextprotocol/server-memory` → persistent agent memory
- `@modelcontextprotocol/server-github` → version control skills
- Custom MCP server cho AI OS skill registry

---

## References
- [Official Spec Repo](https://github.com/modelcontextprotocol/modelcontextprotocol)
- [Documentation](https://modelcontextprotocol.io)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
