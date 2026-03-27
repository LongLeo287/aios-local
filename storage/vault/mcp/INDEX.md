# KHO MCP — Index
# Config: .mcp.json (root)
# Registry: kho/mcp/registry.json

## ACTIVE MCP SERVERS (5)
- context7           npx @upstash/context7-mcp     [RULE-CONTEXT7-01]
- sequential-thinking npx @modelcontextprotocol/... [RULE-SEQUENTIAL-THINKING-01]
- git-mcp            uvx mcp-server-git             [RULE-GIT-NATIVE-01 fallback]
- aos-workspace      node infra/mcp/servers/        [Custom]
- supabase           npx @supabase/mcp-server-*     [ClawTask backend]

See: kho/mcp/registry.json for full details
