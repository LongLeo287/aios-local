---
description: Evaluate whether to add Observability Layer (LangSmith / Langfuse) to AI OS
---

# PROPOSAL: Observability Layer for AI OS

**ID:** PROP_2026-03-23_OBSERVABILITY_LAYER
**Date:** 2026-03-23 | **Author:** Antigravity | **Status:** PENDING CEO

## Problem
AI OS hiện tại thiếu visibility vào:
- Mỗi LLM call tốn bao nhiêu tokens?
- Agent nào đang chậm / fail?
- Skill nào được gọi nhiều nhất?
- Errors xảy ra ở đâu trong pipeline?

From KI-AI-STACK-LANDSCAPE-01: **Observability = biggest gap** còn lại của AI OS so với enterprise tools.

## Options

### Option A: LangSmith (LangChain)
- Cloud-based, free tier
- Tích hợp ngay với CrewAI + LangChain
- Dashboard đẹp

### Option B: Langfuse (Self-hosted)
- Open source, MIT
- Self-hosted → data privacy
- Docker support
- **Recommended** cho AI OS (data stays local)

### Option C: Custom telemetry (current)
- `telemetry/` directory manual logging
- No real-time dashboard
- Good for simple cases, not scalable

## Recommendation
**Option B: Langfuse self-hosted**
- Privacy preserved
- Open source
- Docker compose trong 5 phút

```bash
# Langfuse Docker
git clone https://github.com/langfuse/langfuse
cd langfuse && docker compose up -d
# → Dashboard at localhost:3000
```

## Estimated Effort
1 session (Cycle 9): Docker deploy + instrument Tier 1 services

## CEO Decision
[ ] APPROVE Langfuse
[ ] APPROVE LangSmith  
[ ] DEFER to Cycle 10
[ ] REJECT
