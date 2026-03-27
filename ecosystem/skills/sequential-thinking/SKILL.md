---
name: sequential-thinking
description: Dynamic and reflective problem-solving through thought sequences. Auto-activate for complex multi-step problems, debugging, system design decisions, and any task requiring deep reasoning. Anthropic official MCP server.
---

# Sequential Thinking — Dynamic Problem Solving

## What it Does
Guides the AI through a structured chain-of-thought process:
- Breaks complex problems into explicit reasoning steps
- Allows backtracking and revision of earlier thoughts
- Tracks reasoning confidence at each step
- Produces higher-quality outputs for hard problems

**Source:** Anthropic official MCP | `@modelcontextprotocol/server-sequential-thinking`

## When to Use (Auto-activate)
- Complex debugging (multi-root cause)
- System architecture decisions
- Multi-step planning (>4 steps)
- Security analysis (requires thorough reasoning)
- When initial approach seems uncertain

## How it Works
```
Tool: sequentialthinking
Input: {
  "thought": "Current reasoning step",
  "nextThoughtNeeded": true/false,
  "thoughtNumber": 1,
  "totalThoughts": 5,
  "isRevision": false
}
```

## Example Flow
```
Thought 1: "The bug could be in the auth middleware or the DB query"
Thought 2: "Checking middleware: token validation looks correct"
Thought 3: "Checking DB: found it — SQL injection in line 42"
Thought 4: [REVISION] "Actually, root cause is missing parameterization"
Thought 5: "Fix: use prepared statements, add input validation"
→ Final answer with full reasoning trace
```

## Integration
MCP Server running at: `npx @modelcontextprotocol/server-sequential-thinking`
Already added to: `~/.claude/claude_desktop_config.json` → `mcpServers.sequential-thinking`

## Notes
- Increases token usage but dramatically improves reasoning quality
- Best for P1/P2 tasks requiring high confidence
- Use with context7 for library-specific reasoning
