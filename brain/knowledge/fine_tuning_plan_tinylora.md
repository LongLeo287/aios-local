# AI OS Corp — TinyLoRA Fine-Tuning Plan
# Version: 1.0 | Created: 2026-03-19
# Owner: rd department | Source: arxiv.org/abs/2602.04118
# Status: DRAFT — Awaiting R&D review

---

## MỤC TIÊU

Tận dụng TinyLoRA (13 parameters, RL-based) để fine-tune từng department agent trong AI OS Corp, tăng chất lượng reasoning mà không tăng infrastructure cost.

**Baseline model:** Qwen2.5-8B (đã chứng minh: 91% GSM8K với 13 params TinyLoRA)

---

## DANH SÁCH AGENTS ƯU TIÊN

### Priority 1 — Reasoning-Heavy (Implement ngay)

| Agent | Department | Domain Fine-Tune | Reasoning Task Type |
|-------|-----------|-----------------|---------------------|
| `finance-agent` | finance | Math/accounting | Multi-step financial calc, budget reasoning |
| `qa-testing-agent` | qa_testing | Systematic testing | Edge case detection, test scenario generation |
| `legal-agent` | legal | Legal argumentation | Rule-based deduction, contract analysis |
| `security-grc-agent` | security_grc | Threat analysis | Attack chain reasoning, risk scoring |
| `strategy-agent` | strategy | Strategic planning | Multi-factor decision, market analysis |

### Priority 2 — Knowledge-Intensive

| Agent | Department | Domain Fine-Tune | Reasoning Task Type |
|-------|-----------|-----------------|---------------------|
| `pmo-agent` | planning_pmo | Project management | Resource allocation, timeline estimation |
| `monitor-chief-agent` | monitoring_inspection | Compliance | Rule violation detection, metric analysis |
| `knowledge-curator-agent` | asset_library | Knowledge quality | Content evaluation, relevance scoring |
| `health-chief-agent` | system_health | Diagnostics | Symptom → root cause reasoning |
| `strix-agent` | security_grc | Security vetting | 12-stage repo analysis chains |

### Priority 3 — Content/Communication

| Agent | Department | Domain Fine-Tune |
|-------|-----------|-----------------|
| `content-validator-agent` | content_review | Content quality reasoning |
| `proposal-writer-agent` | client_reception | Proposal structure reasoning |
| `od-agent` | od_learning | Learning path design |

---

## TRAINING METHODOLOGY

### Dataset Requirements (per agent)
```
Minimum: 500 examples
Recommended: 1,000–2,000 examples
Format: (question, reasoning_chain, answer) triplets
Source: Existing AI OS workflows + synthetic generation
```

### Cấu trúc dataset theo department

**finance-agent dataset examples:**
```json
{
  "question": "Budget Q1: $50,000. Q1 actual spend: $42,500. Q2 needs $15,000 more than Q1 budget. What's total approved budget needed?",
  "chain_of_thought": "Q1 budget = 50000. Q2 needs = 50000 + 15000 = 65000. Total = 50000 + 65000 = 115000",
  "answer": "$115,000"
}
```

**qa-testing-agent dataset examples:**
```json
{
  "question": "API endpoint /api/tasks/add. What edge cases should you test?",
  "chain_of_thought": "1. Empty body → 400 expected. 2. Missing required fields → validate. 3. Duplicate task ID → check behavior. 4. Very long title (>10KB) → truncate or 400. 5. Special chars in title → encoding. 6. Concurrent add from 2 agents → race condition.",
  "answer": "6 edge cases: [...]"
}
```

### Training Config
```yaml
# tinylora_config.yaml
model: Qwen2.5-8B
method: TinyLoRA
  rank: 1               # or less — paper proves this works
  target: [q_proj, v_proj]
  init: random_small
training:
  algorithm: GRPO        # Group Relative Policy Optimization
  steps: 1000
  batch_size: 8
  lr: 1e-4
  reward: exact_match + format_score
output:
  format: bf16
  file: weights/{dept_name}_tinylora.bin  # < 100 bytes
```

---

## INFRASTRUCTURE

### Không cần hardware mới
- Qwen2.5-8B chạy được trên: RTX 3080 (10GB VRAM) với 4-bit quant
- TinyLoRA training: < 100MB VRAM thêm
- Inference: không đổi (weights negligibly small)

### Storage
```
weights/
├── finance_tinylora.bin          # ~26 bytes (13 params × bf16)
├── qa_testing_tinylora.bin
├── legal_tinylora.bin
├── security_grc_tinylora.bin
├── strategy_tinylora.bin
└── [16 more agents]...
Total: < 10KB cho tất cả 21 agents
```

### Integration với temm1e
```
temm1e runtime (15MB) 
  + Qwen2.5-8B (quantized, 4-bit: ~4GB)
  + TinyLoRA weights (< 10KB total)
= Full AI OS Corp agent layer với domain reasoning
```

---

## IMPLEMENTATION PLAN

### Phase 1 (Tuần 1-2): Research & Setup
- [ ] Reproduce TinyLoRA paper results (GSM8K 91%)
- [ ] Set up training environment (unsloth / trl / GRPO trainer)
- [ ] Create dataset generation pipeline từ AI OS Corp workflows

### Phase 2 (Tuần 3-4): Pilot
- [ ] Fine-tune `finance-agent` — math dataset (easiest to validate)
- [ ] Fine-tune `qa-testing-agent` — testing scenarios
- [ ] Evaluate: improvement vs baseline Qwen2.5-8B

### Phase 3 (Tháng 2): Priority 1 Rollout
- [ ] Fine-tune: legal, security_grc, strategy (3 agents)
- [ ] Create agent loading system: load TinyLoRA weights on agent init
- [ ] Integration test với ClawTask task briefings

### Phase 4 (Tháng 3): Full Rollout
- [ ] Fine-tune Priority 2 + 3 agents (11 agents còn lại)
- [ ] Benchmark: ClawTask completion quality trước/sau
- [ ] Publish internal report → asset_library knowledge base

---

## KPIs

| Metric | Baseline | Target After Fine-Tune |
|--------|----------|----------------------|
| finance-agent math accuracy | ~60% | ≥ 85% |
| qa-agent edge case detection | ~50% | ≥ 80% |
| legal-agent rule adherence | ~55% | ≥ 85% |
| security vetting accuracy | ~65% | ≥ 90% |
| Extra compute per agent call | 0ms | < 1ms (weights preloaded) |

---

## LINKS & REFERENCES

- TinyLoRA Paper: https://arxiv.org/abs/2602.04118
- Knowledge file: `knowledge/tinylora_reasoning_13params.md`
- temm1e runtime: `knowledge/repos/temm1e/knowledge.md`
- Owner dept: `rd` (Research & Development)
- Sponsor: CTO

---

*Cập nhật plan này sau mỗi phase hoàn thành. Chuyển status từ DRAFT → ACTIVE khi CTO approve.*
