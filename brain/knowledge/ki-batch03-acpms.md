# KI: ACPMS — Agentic Coding Project Management System

## Metadata
- **Source:** https://github.com/thaonv7995/acpms
- **Category:** Agentic / Tools / Project Management
- **Priority:** 🟡 HIGH — Vietnamese developer project
- **Ingested:** 2026-03-21
- **Batch:** 03

## Tóm Tắt
Hệ thống quản lý project coding theo kiểu agentic — kết nối multi-agent (Claude Code, Codex, Gemini CLI, Cursor) với GitLab và OpenClaw. Single binary distribution.

## Tính Năng Chính
- **Contextual Awareness** — Agents làm Task link tới approved Requirements & Architecture
- **Full Lifecycle** — Plan → Code → Deploy → Fix với human-in-the-loop review
- **Multi-Agent Support** — Claude Code, OpenAI Codex, Gemini CLI, Cursor AI CLI
- **OpenClaw Gateway** — Quản lý project qua Telegram, Slack
- **GitLab Integration** — OAuth, MR creation, webhooks
- **Single Binary** — Backend + frontend + S3 proxy (self-hosting)

## Tech Stack
- Backend: Rust
- Frontend: Node.js 20+
- Database: PostgreSQL 16
- Storage: MinIO (S3)
- Container: Docker + Docker Compose

## Quick Install
```bash
# Option A: One-liner
bash -c "$(curl -sSL https://raw.githubusercontent.com/thaonv7995/acpms/main/install.sh)"

# Windows: WSL2 + Ubuntu/Debian
```

## Platforms
- Linux (x86_64, arm64)
- macOS (Intel, Apple Silicon)
- Windows via WSL2

## Liên Quan AI OS
- **OpenClaw Gateway** → Kết nối với awesome-openclaw-skills
- **Multi-agent support** → Tương đồng AI OS Tier 2-3 orchestration
- **Human-in-the-loop** → Tương đồng CEO approval gates trong AI OS
- **GitLab webhooks** → Tích hợp CI/CD pipeline AI OS

## AI OS Action
```
STATUS: 🟡 HIGH — Khả năng high nếu đang dùng GitLab
EVAL: Test ACPMS cho project management của AI OS Corp
NOTE: Vietnamese developer — community support tốt
```
