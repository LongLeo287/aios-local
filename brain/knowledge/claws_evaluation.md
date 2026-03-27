# Claws Evaluation — AI OS Plugin Assessment
# Updated: 2026-03-16
# Purpose: Choose the best claw variant(s) to use for AI OS channel management

---

## Candidates Reviewed (Top 3 of 15)

### 1. ZeroClaw 🦀 (Rust — RECOMMENDED for infrastructure)

| Metric | Value |
|--------|-------|
| Language | Rust |
| RAM | < 5MB |
| Startup | < 10ms |
| Binary | ~8.8MB (self-contained) |
| License | MIT OR Apache 2.0 |

**Strengths:**
- Zero overhead, zero runtime deps — runs anywhere
- Trait-based architecture: swap providers, channels, tools, memory
- Built-in auth management (Claude Code OAuth, OpenAI Codex)
- `zeroclaw daemon` = 24/7 autonomous agent runtime
- `zeroclaw channel bind-telegram / doctor` = dedicated channel health
- Windows x86_64 pre-built binary available

**Verdict:** Best for always-on AI OS daemon with minimal resource footprint.

---

### 2. TinyClaw 🦞 (Node.js — BEST for multi-agent teams)

| Metric | Value |
|--------|-------|
| Language | Node.js |
| Channels | Discord, WhatsApp, Telegram |
| Queue | SQLite + retry logic |
| UI | TinyOffice (Next.js) on port 3777/3000 |

**Strengths:**
- Multi-agent + multi-team architecture (agents hand off work via `@agent_id`)
- SQLite task queue with dead-letter management
- TinyOffice: Kanban board, chatrooms, org chart, real-time logs
- Parallel agent processing with isolated workspaces
- CLI: `tinyclaw start/status/logs/agent list`

**Verdict:** Best for orchestrating multiple Claude Code workers in parallel teams.

---

### 3. PicoClaw 🦐 (Go — BEST channel coverage)

| Metric | Value |
|--------|-------|
| Language | Go |
| RAM | < 10MB |
| Startup | < 1s |
| Channels | Telegram, Discord, WhatsApp, Matrix, QQ, DingTalk, LINE, WeCom |
| Docker | Yes (Docker Compose included) |

**Strengths:**
- 8+ channels including Asian platforms (QQ, DingTalk, WeCom, LINE)
- Single binary for all platforms
- `picoclaw gateway` = unified webhook for all channels port 18790
- Skill system (`~/.picoclaw/workspace/skills/`)
- Plugin config in JSON (`config.json`)

**Verdict:** Best when needing more channels than just Telegram/Discord.

---

## Recommendation for AI OS

| Use Case | Best Claw |
|----------|-----------|
| Always-on lightweight daemon | **ZeroClaw** |
| Multi-agent team orchestration | **TinyClaw** |
| Multi-channel (especially Vietnamese/Asian) | **PicoClaw** |
| Current AI OS (4 channels, Python bridges) | **Keep current** + PicoClaw as upgrade path |

## Immediate Action

**Status: No action needed now.**  
AI OS already has Python-based bridges for Telegram/Zalo/Discord/Messenger.
These claws are **archived as plugin options** for when:
- Need to scale to 24/7 daemon → use ZeroClaw
- Need multi-agent teams UI → use TinyClaw
- Need QQ/LINE/WeChat channels → use PicoClaw

## To Activate Later

```powershell
# ZeroClaw (Windows pre-built)
# Download from: https://github.com/zeroclaw-labs/zeroclaw/releases/latest
# Then: zeroclaw onboard

# TinyClaw (Node.js)
# curl -fsSL .../remote-install.sh | bash
# tinyclaw start

# PicoClaw (Go)
# Download from: https://github.com/sipeed/picoclaw/releases
# picoclaw onboard
```
