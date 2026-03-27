# KI: karpathy/autoresearch — AI Agents chạy Research tự động

## Metadata
- **Source:** https://github.com/karpathy/autoresearch
- **Category:** Agentic / Research
- **Priority:** 🟡 HIGH — Karpathy's project, rất có giá trị
- **Ingested:** 2026-03-21
- **Batch:** 03

## Tóm Tắt
Dự án của Andrej Karpathy — cho phép AI agents tự động chạy research về GPT training trên single GPU. Thiết kế cực kỳ đơn giản: 3 files, 1 metric, 1 GPU, time-budget cố định 5 phút.

## How It Works
Ba files chính:
- **`prepare.py`** — Fixed constants, data prep, tokenizer (KHÔNG sửa)
- **`train.py`** — GPT model + Muon/AdamW optimizer (agent tự sửa)
- **`program.md`** — Instructions cho agent (human sửa rules)

**Metric:** `val_bpb` (validation bits per byte) — lower = better  
**Time budget:** 5 phút cố định per experiment  
**Speed:** ~12 experiments/hour, ~100 experiments overnight

## Cách Run
```bash
# Setup
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run prepare.py   # One-time: ~2 min

# Experiment
uv run train.py

# Autonomous mode
# Spin up Claude/Codex in repo → "Hi have a look at program.md!"
```

## Design Philosophy
- **Single file to modify** — Agent chỉ edit `train.py`. Diffs dễ review.
- **Fixed time budget** — Tất cả experiments comparable nhau (fair baseline)
- **Self-contained** — No distributed training, no complex configs
- `program.md` = "super lightweight skill"

## Requirements
- NVIDIA GPU (tested on H100)
- Python 3.10+
- uv package manager

## Concepts Áp Dụng Cho AI OS
- **program.md = lightweight skill** → Mỗi task AI OS nên có 1 instruction file rõ ràng
- **Time budget** → AI OS tasks nên có timeout/SLA definition
- **Single metric** → Mỗi AI OS experiment cần 1 measurable outcome
- **Agent modifies one file** → Scope isolation trong task design

## AI OS Action
```
STATUS: 🟡 RESEARCH VALUE — Học pattern, không cài trực tiếp
INSIGHT: program.md pattern = minimal skill design
Apply: Định nghĩa SLA/timeout cho AI OS tasks
```
