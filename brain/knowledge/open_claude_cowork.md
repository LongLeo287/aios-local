---
source: https://github.com/ComposioHQ/open-claude-cowork
ingested_at: 2026-03-16T10:26:00+07:00
domain: AI|Desktop|AgentApp|Integration
trust_level: HIGH
vet_status: PASS
tags: [composio, claude-agent-sdk, electron, desktop-app, 500-integrations, skills, clawdbot, mcp]
---

# open-claude-cowork — Desktop AI Assistant by ComposioHQ

**Repo:** https://github.com/ComposioHQ/open-claude-cowork  
**Type:** Open-source desktop chat application  
**By:** ComposioHQ (Composio — tool integration platform)

---

## Tổng quan

Desktop AI Assistant powered bởi **Claude Agent SDK** + **Composio Tool Router**.

**Value propositions:**
- 500+ app integrations (Gmail, Slack, GitHub, Google Drive...)
- Skills/plugins extensible
- Multi-platform messaging bot (WhatsApp, Telegram, Signal, iMessage)
- Full browser automation capability

---

## Tech Stack

```
┌─────────────────────────────────────────────┐
│  open-claude-cowork                         │
│                                             │
│  Desktop:  Electron.js                      │
│  Backend:  Node.js + Express                │
│  AI:       Claude Agent SDK + Opencode SDK  │
│  Tools:    Composio Tool Router + MCP       │
│  Stream:   Server-Sent Events (SSE)         │
└─────────────────────────────────────────────┘
```

### Project Structure
```
open-claude-cowork/
├── main.js              ← Electron main process
├── renderer/            ← Frontend UI (dark-themed)
├── server/
│   ├── backend logic
│   └── AI provider implementations (Claude/Opencode)
└── clawd/               ← Clawdbot components
    ├── adapters/
    │   ├── whatsapp.js
    │   ├── telegram.js
    │   ├── signal.js
    │   └── imessage.js
    └── claude-agent.js
```

---

## Features

### Desktop Chat App
- **Multi-provider:** Claude Agent SDK hoặc Opencode
- **Persistent sessions:** Context không mất giữa messages
- **Real-time streaming:** Token-by-token (SSE)
- **Tool visualization:** Xem tool inputs/outputs trong sidebar
- **Skills support:** Extend Claude với custom capabilities
- **Dark UI:** Modern, clean interface

### Composio Integration (Big Feature!)
Access **500+ application integrations** via Composio Tool Router:

| Category | Apps |
|----------|------|
| Email | Gmail, Outlook |
| Messaging | Slack, Teams |
| Code | GitHub, GitLab, Jira |
| Files | Google Drive, Dropbox, Notion |
| CRM | Salesforce, HubSpot |
| Calendar | Google Calendar, Outlook Calendar |
| + nhiều hơn | 490+ others |

```javascript
// Composio Tool Router — auto-route requests đến đúng app
const tools = await composio.getTools({
    apps: ["gmail", "slack", "github"],
    // → Automatically available as Claude tools
});
```

---

## Clawdbot — Personal AI Agent (Built-in)

Multi-platform messaging AI assistant trong cùng repo:

```
Users ─── WhatsApp ──┐
          Telegram ──┤→ Clawdbot → Claude Agent
          Signal  ──┤
          iMessage──┘
```

**Clawdbot capabilities:**
- **Persistent memory:** Nhớ context across conversations
- **Browser automation:** Navigate, click, fill forms, screenshots
- **Natural language scheduling:** "Remind me tomorrow at 9am" → cron job
- **Full tool access:** Via Composio 500+ integrations

---

## Claude Agent SDK (Core)

Đây là SDK chính thức của Anthropic để build agents:
```javascript
import { ClaudeAgent } from "@anthropic-ai/agent-sdk";

const agent = new ClaudeAgent({
    model: "claude-opus-4",
    tools: [...composioTools, ...mcpTools],
    skills: [...customSkills],
});

// Streaming response
for await (const chunk of agent.stream(userMessage)) {
    process.stdout.write(chunk.text);
}
```

---

## Patterns Học Được

### Pattern 1: Composio như Universal Tool Adapter
```
Thay vì code tích hợp từng app:
Gmail skill + Slack skill + GitHub skill...

→ Dùng Composio một lần → access 500+ apps
→ AI OS có thể tích hợp Composio Tool Router
   để có instant 500 tools
```

### Pattern 2: Sidebar Tool Visualization
```
Chat UI:
┌─────────────────────┐ ┌──────────────┐
│  Claude response... │ │ Tool calls:  │
│                     │ │ ├ gmail.read │
│                     │ │ ├ slack.post │
│                     │ │ └ github.pr  │
└─────────────────────┘ └──────────────┘
→ User thấy rõ agent đang làm gì
```

### Pattern 3: Multi-Platform Bot từ 1 Agent
```
1 Claude Agent → multiple interfaces
→ Desktop chat (Electron)
→ WhatsApp bot
→ Telegram bot
→ Signal bot
→ Cùng memory, cùng tools
```

### Pattern 4: SSE Streaming Architecture
```
Client ←── SSE ─── Express Server ←── Claude streaming API
→ Token-by-token display
→ No websocket needed
→ Simple, reliable
```

---

## Relevance cho AI OS

| Feature | AI OS Application |
|---------|-----------------|
| Composio 500+ tools | Thay thế viết nhiều skills riêng lẻ |
| Claude Agent SDK | Core engine cho AI OS agents |
| Skills support | Compatible với AI OS skill format |
| MCP integration | Tích hợp với AI OS MCP config |
| Clawdbot pattern | Multi-platform AI OS interface |

### Tích hợp tiềm năng
```
AI OS + Composio Tool Router:
→ "Send email về project status" → Gmail tool (auto)
→ "Create PR for this change" → GitHub tool (auto)
→ "Post update to #dev channel" → Slack tool (auto)
Không cần viết từng integration riêng
```

---

## Đánh giá

| Aspect | Assessment |
|--------|------------|
| **Relevance** | HIGH — Composio là game-changer cho AI OS tools |
| **Maturity** | Production-ready (ComposioHQ là funded startup) |
| **Adopt as-is** | Không — quá browser/Electron centric |
| **Adopt patterns** | YES — Composio integration, SSE, tool viz |
| **Key learning** | Composio Tool Router để skip custom integrations |

---

## Setup (Desktop App)

```bash
git clone https://github.com/ComposioHQ/open-claude-cowork
cd open-claude-cowork
npm install

# Configure
cp .env.example .env
# ANTHROPIC_API_KEY=...
# COMPOSIO_API_KEY=...

# Run
npm start  # Opens Electron app
```

---

## References
- [GitHub](https://github.com/ComposioHQ/open-claude-cowork)
- [Composio](https://composio.dev)
- [Claude Agent SDK](https://docs.anthropic.com/agent-sdk)
