---
name: agentune
description: Background music player MCP for agents during coding sessions. Plays ambient soundscapes to improve focus. Low-distraction, browser-dashboard controlled.
---

# Agentune — Agent Music Player (MCP)

## What it Does
Plays background music/ambient sound during coding sessions via MCP connection.
Controlled via browser dashboard. Non-intrusive — runs in background.

## Quick Start
```bash
# Install
npx agentune install

# Connect to MCP client (add to MCP config)
{
  "mcpServers": {
    "agentune": {
      "command": "npx",
      "args": ["agentune", "mcp"]
    }
  }
}

# Open browser dashboard
npx agentune dashboard
# → opens at http://localhost:PORT
```

## MCP Commands (via agent)
```
play lofi          # Play lofi hip-hop
play focus         # Play focus/deep work sounds
play nature        # Play nature ambient
pause              # Pause current track
volume 70          # Set volume (0-100)
status             # Current playback status
```

## Notes
- Source: github.com/tqdat410/agentune | VN developer
- Requires: Node.js
- Platform: Windows/Mac/Linux
- Risk: LOW — no data access, no network calls to AI
- Owner: Dept 1 (Engineering) utility
