# KI: TEMM1E — Autonomous AI Agent Runtime (Rust)

## Metadata
- **Source:** https://github.com/temm1e-labs/temm1e
- **Category:** Agentic / Runtime
- **Priority:** 🟡 HIGH — Innovative architecture
- **Ingested:** 2026-03-21
- **Batch:** 03

## Tóm Tắt
TEMM1E là autonomous AI agent runtime viết bằng **Rust** — được mô tả là "SENTIENT and IMMORTAL" agent. Triển khai một lần, chạy mãi mãi. Giao tiếp qua Telegram, Discord, Slack, CLI.

## Architecture — "Tem's Mind"
```
[User Message]
    ↓
1. CLASSIFY (single LLM call — classifies AND responds + blueprint_hint)
    ↓
2. CONTEXT BUILD
   - System prompt + history + tools + blueprints + λ-Memory
   - Strict TOKEN BUDGET (e.g.: Used: 34,200 / Avail: 165,800)
    ↓
3. TOOL LOOP
   - LLM calls tool → Execute → Result+verification fed back
   - Loops until: reply / budget exhausted / user interrupt
   - No artificial iteration caps
    ↓
4. POST-TASK
   - Store λ-memories
   - Extract learnings
   - Author/refine Blueprint
   - Notify user
   - Checkpoint to task queue
```

## Tính Năng Nghiên Cứu (Tem's Lab)
- **λ-Memory** — Memory "fade" thay vì xóa hoàn toàn (graduated forgetting)
- **Tem's Mind v2.0** — Complexity-Aware Agentic Loop
- **Many Tems** — Swarm Intelligence (multi-agent)
- **Eigen-Tune** — Self-Tuning Knowledge Distillation
- **Tem Prowl** — Web-Native Browsing với OTK Authentication

## Tech Stack
- **Runtime:** Rust (cargo build)
- **TUI:** Interactive terminal UI
- **Channels:** Telegram, Discord, Slack, CLI
- **LLM Providers:** Multiple (configurable)

## Quick Start
```bash
git clone https://github.com/temm1e-labs/temm1e.git && cd temm1e
cargo build --release --features tui
./target/release/temm1e tui

# Server mode
export TELEGRAM_BOT_TOKEN="your-token"
./target/release/temm1e start
```

## Concepts Liên Quan AI OS
- **Token Budget Tracking** → AI OS nên implement budget monitoring
- **λ-Memory** → Inspire hot-cache expiry mechanism
- **Blueprint System** → Tương đồng với skill/workflow trong AI OS
- **Post-Task Checkpoint** → Tương đồng với `telemetry/receipts/`

## AI OS Action
```
STATUS: 🟡 HIGH — Học hỏi pattern, không deploy trực tiếp
RESEARCH: λ-Memory decay model cho hot-cache
RESEARCH: Token budget display trong pre-session workflow
```
