# KI: claude-mem — Auto Memory cho Claude Code Sessions

## Metadata
- **Source:** https://github.com/thedotmack/claude-mem
- **Category:** Claw Variant / Memory / Plugin
- **Priority:** 🔴 CRITICAL — Giải quyết memory/context problem
- **Ingested:** 2026-03-21
- **Batch:** 03

## Tóm Tắt
Plugin Claude Code tự động **capture tất cả hành động** trong session, compress bằng AI (claude-agent-sdk), và inject lại relevant context vào future sessions. **215 Releases** — actively maintained.

## Cơ Chế Hoạt Động
1. **Capture** — Tự động ghi lại mọi thứ Claude làm trong session
2. **Compress** — Dùng AI để tóm tắt và nén thông tin
3. **Store** — Lưu memories theo project/context
4. **Inject** — Đưa relevant context vào session mới tự động

## Tính Năng
- Automatic capture (no manual effort)
- AI compression (claude-agent-sdk)
- MCP Search Tools — tìm memories từ session cũ
- Beta: Advanced memory retrieval
- Tích hợp với **OpenClaw Gateway** (🦞)
- Windows setup support

## Architecture
- Hook vào Claude Code session lifecycle
- Persistent memory store
- Semantic search qua MCP tools

## Liên Quan AI OS  
- **CRITICAL CONNECTION**: Giải quyết đúng vấn đề "mất context" giữa sessions
- Tương tự nhưng **tự động hơn** `brain/shared-context/blackboard.json`
- Kết hợp với `pre-session.md` → inject memory tự động
- Có thể thay thế/bổ sung cho manual `hot-cache.md` system

## Comparison với AI OS hiện tại
| Feature | AI OS (Manual) | claude-mem (Auto) |
|---------|---------------|-------------------|
| Session capture | Manual viết vào blackboard | Auto capture |
| Compression | Manual summarize | AI compressed |
| Injection | pre-session.md (manual read) | Auto inject |
| Search | Manual | MCP search tools |

## AI OS Action
```
STATUS: 🔴 CRITICAL — Evaluate và test cài vào Claude Code
COMMAND: npx @thedotmack/claude-mem (check actual install method)
BENEFIT: Giải quyết context loss giữa Claude sessions
```
