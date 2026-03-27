# Department: operations
---
description: Khi nÃ o vÃ  cÃ¡ch khá»Ÿi Ä‘á»™ng Claude Code CLI Ä‘á»ƒ dÃ¹ng MCP servers trong AI OS â€” Hybrid MCP Strategy
---

# Workflow: Launch MCP via Claude Code CLI

## Má»¥c Ä‘Ã­ch
Khi task cáº§n dÃ¹ng MCP server mÃ  Antigravity khÃ´ng Ä‘á»§:
- Sequential Thinking MCP (cho reasoning chains phá»©c táº¡p)
- Git MCP (cho git operations nÃ¢ng cao)
- Filesystem MCP (vá»›i access control granular)

> **Æ¯u tiÃªn:** DÃ¹ng Antigravity native trÆ°á»›c â†’ chá»‰ escalate khi cáº§n.

---

## Decision Matrix â€” Khi nÃ o dÃ¹ng gÃ¬

| Scenario | DÃ¹ng gÃ¬ |
|----------|---------|
| Git log/diff/blame Ä‘Æ¡n giáº£n | Antigravity `run_command` (native) |
| Complex reasoning, debugging | Antigravity Thought N: pattern (native) |
| Deep git history traversal, multi-file blame | Python `mcp_client.py call_mcp("git", ...)` |
| Extended sequential reasoning session | Claude Code CLI vá»›i MCP server |
| Cáº§n nhiá»u MCP tools liÃªn tá»¥c | Claude Code CLI |

---

## CÃ¡ch 1 â€” Python MCP Client (KhÃ´ng cáº§n Claude Code CLI)

```python
# Gá»i tá»« báº¥t ká»³ skill/adapter trong AI OS
from plugins.mcp_client.mcp_client import call_mcp, AI_OS_ROOT

# Git: xem history
history = call_mcp("git", "git_log", {
    "repo_path": AI_OS_ROOT,
    "max_count": 20
})

# Sequential Thinking: má»™t thought step
thought = call_mcp("sequential-thinking", "sequentialthinking", {
    "thought": "Analyzing the root cause of this bug...",
    "thoughtNumber": 1,
    "totalThoughts": 4,
    "nextThoughtNeeded": True
})

# Filesystem: list directory
files = call_mcp("filesystem", "list_directory", {
    "path": f"{AI_OS_ROOT}/skills"
})
```

```bash
# CLI mode
python plugins/mcp-client/mcp_client.py git git_log '{"repo_path": "<AI_OS_ROOT>", "max_count": 10}'
```

---

## CÃ¡ch 2 â€” Claude Code CLI Launch (Khi cáº§n full MCP session)

### BÆ°á»›c 1: Má»Ÿ terminal má»›i
```powershell
# Tá»« AI OS root
cd "<AI_OS_ROOT>"
```

### BÆ°á»›c 2: Äáº£m báº£o claude_desktop_config.json Ä‘Ã£ cÃ³ MCP servers
File: `<USER_PROFILE>\AppData\Roaming\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "sequential-thinking": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"] },
    "git": { "command": "uvx", "args": ["mcp-server-git", "--repository", "<AI_OS_ROOT>"] },
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "d:\\AI OS CORP"] }
  }
}
```

### BÆ°á»›c 3: Khá»Ÿi Ä‘á»™ng Claude Code CLI
```powershell
claude  # hoáº·c: claude --mcp-debug (Ä‘á»ƒ debug MCP connections)
```

### BÆ°á»›c 4: Trong Claude Code session, verify MCPs connected
```
/mcp         # list connected MCP servers
/tools       # list all available tools including MCP tools
```

### BÆ°á»›c 5: DÃ¹ng MCP tools tá»± nhiÃªn
Claude Code tá»± detect vÃ  dÃ¹ng MCP tools khi phÃ¹ há»£p.
Hoáº·c explicit: "Use the sequential-thinking MCP to analyze this bug"

### BÆ°á»›c 6: Sau khi xong â€” output vá» Antigravity
Copy káº¿t quáº£ / files Ä‘Ã£ táº¡o â†’ tiáº¿p tá»¥c trong Antigravity

---

## MCPs trong AI OS â€” Danh sÃ¡ch Ä‘áº§y Ä‘á»§

| MCP Server | Package | Tier | Skill |
|-----------|---------|------|-------|
| sequential-thinking | `@modelcontextprotocol/server-sequential-thinking` | 1 | skills/sequential-thinking/SKILL.md |
| git | `mcp-server-git` (uvx) | 1 | skills/git-mcp/SKILL.md |
| filesystem | `@modelcontextprotocol/server-filesystem` | 1 | Built-in |
| context7 | `@upstash/context7` (CLI npx ctx7) | 1 | skills/context7/SKILL.md |

> **Note:** context7 dÃ¹ng CLI mode (`npx ctx7`) â€” khÃ´ng cáº§n MCP session.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `uvx: not found` | `$env:Path = "<USER_PROFILE>\.local\bin;$env:Path"` |
| MCP server khÃ´ng connect | `claude --mcp-debug` Ä‘á»ƒ xem log |
| `claude: not found` | Install: `npm install -g @anthropic-ai/claude-code` |
| Port/pipe error | Restart Claude Code CLI |

*Workflow v1.0 | 2026-03-24 | Owner: Dept 1 (Engineering)*

