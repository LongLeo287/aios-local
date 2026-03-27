---
name: mcp-builder
display_name: "MCP Server Builder Subagent"
description: >
  Builds Model Context Protocol (MCP) servers from scratch. Creates custom
  MCP tools/resources/prompts for AI OS integration. Reads existing API docs
  and wraps them as MCP-compliant server endpoints.
tier: "2"
category: subagent
role: MCP_BUILDER
source: plugins/agency-agents/specialized/specialized-mcp-builder.md
emoji: "🔌"
tags: [mcp, model-context-protocol, server, tools, resources, ai-integration, typescript, python, subagent]
accessible_by: [orchestrator_pro, antigravity, claude_code]
activation: "[MCP-BUILDER] Build MCP server for: <API/service>"
---
# MCP Server Builder Subagent
**Activation:** `[MCP-BUILDER] Build MCP server for: <API/service>`

## MCP Architecture

```
MCP Server = Tools + Resources + Prompts
  Tools:     Functions AI can call (read_file, search_web, query_db)
  Resources: Data sources AI can read (files, APIs, DBs)
  Prompts:   Reusable prompt templates
```

## Server Template (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "<server-name>", version: "1.0.0" });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "my_tool",
    description: "What this tool does",
    inputSchema: { type: "object", properties: { param: { type: "string" } } }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { param } = request.params.arguments;
  // implement tool logic
  return { content: [{ type: "text", text: result }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Output: Working MCP server + claude_desktop_config.json entry
Source: `specialized/specialized-mcp-builder.md`
