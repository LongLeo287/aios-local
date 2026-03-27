# LLM Research Brief — March 2026
# Links: GLM-5 (z.ai), Kimi K2.5 (MoonshotAI), MiniMax-AI org, WorldVQA benchmark

---

## 1. GLM-5 — Z.AI / Zhipu AI
**Link:** https://z.ai/blog/glm-5
**Type:** Open-source LLM (Mixture-of-Experts)
**Released:** March 2026

### Key Stats
| Item | Value |
|------|-------|
| Total params | 744B |
| Active params/token | 40B |
| Pre-training tokens | 28.5T |
| Context window | 205K tokens |
| Max output | 128K tokens |
| Architecture | MoE + DeepSeek Sparse Attention (DSA) |
| RL infra | "Slime" (async RL) |

### Benchmark Highlights
- SWE-bench Verified: **77.8%** (new open-source SOTA, ≈ Claude Opus 4.5)
- Terminal Bench 2.0: **56.2%**
- BrowseComp (web retrieval): **62.0** (#1 open-source)
- AIME 2026 I: **92.7%**
- Artificial Analysis Intelligence Index: **50** (first open-weights to reach this)

### AI OS Relevance
- **Agentic**: optimized for long-horizon agentic tasks (coding, tool use, web browsing, multi-step)
- **Thinking modes**: multiple (instant vs extended reasoning)
- **Tool use**: powerful function-call capabilities
- **Consider**: integrate GLM-5 as an alternative LLM backend for ai-ml-agent

---

## 2. Kimi K2.5 — MoonshotAI
**Link:** https://www.kimi.com/blog/kimi-k2-5
**Repo:** https://github.com/MoonshotAI/WorldVQA (related research)
**Type:** Open-source native multimodal agentic model

### Key Features
| Item | Value |
|------|-------|
| Modes | Instant + Thinking |
| Vision | Native multimodal (vision+language) |
| Agent swarm | Up to **100 sub-agents** |
| Tool calls | Up to **1,500 per run** |
| Strengths | Coding from visual specs, UI generation, agent orchestration |

### Capabilities
- **Agent swarm**: Self-directs up to 100 sub-agents with parallel workflows
- **Visual coding**: Generate code from UI designs, diagrams, video frames
- **Frontend**: Translate conversations → complete frontend UIs with animations
- **Multi-step reasoning**: Logical, mathematical, multi-tool invocation

### AI OS Relevance
- **High**: Could be the AI backbone for creative/frontend engineering workers
- **Agent swarm** architecture: maps onto AI OS org chart naturally
- API: available via Kimi API platform

---

## 3. MiniMax-AI — Open Source Org
**Link:** https://github.com/orgs/MiniMax-AI/repositories

### Key Repos
| Repo | Description |
|------|-------------|
| MiniMax-01 | MiniMax-Text-01 + MiniMax-VL-01 (456B total params) |
| MiniMax-Text-01 | Language model, open-sourced Jan 2025 |
| MiniMax-VL-01 | Vision-language variant |

### AI OS Relevance
- Alternative LLM option (456B)
- Vision-language model available (VL-01)
- Open-source weights available on HuggingFace

---

## 4. WorldVQA — MoonshotAI Benchmark
**Repo:** https://github.com/MoonshotAI/WorldVQA
**Type:** Academic benchmark (not a tool)

### What It Is
- VQA benchmark for evaluating **visual world knowledge** in MLLMs
- 3,500 QA pairs across 9 categories
- Tests atomic visual knowledge (not reasoning — just entity recognition)
- Taxonomic precision required (must say "Bichon Frise" not just "dog")
- Used by MoonshotAI to benchmark Kimi K2.5

### AI OS Relevance
- Reference benchmark if testing vision capabilities of local models
- Not ingested as a plugin — kept as research reference

---

## Summary Recommendations

| Model | Best For | Status |
|-------|---------|--------|
| GLM-5 | Agentic coding, long-context tasks | 🔴 Monitor — could replace GPT-4o for coding workers |
| Kimi K2.5 | Vision + agent swarm tasks | 🟡 Interesting — test for frontend-agent and ui-ux-pro-max |
| MiniMax-01 | General LLM tasks | 🟢 Reference — available on HuggingFace |
| WorldVQA | Benchmark reference | 📚 Research only |
