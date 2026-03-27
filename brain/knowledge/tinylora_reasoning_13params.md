# Knowledge File: TinyLoRA — Learning to Reason in 13 Parameters
# Source: https://arxiv.org/abs/2602.04118
# Ingested: 2026-03-19 | Tier: T1 (Research — Directly Applicable)
# Authors: John X. Morris, Niloofar Mireshghallah, Mark Ibrahim, Saeed Mahloujifar

---

## SUMMARY

TinyLoRA là phương pháp fine-tuning cực kỳ tiết kiệm chi phí: train toàn bộ khả năng reasoning của LLM với chỉ **13 parameters**. Đây là bước phát triển từ LoRA (Low-Rank Adaptation) — đẩy low-rank parameterization đến giới hạn lý thuyết.

**Câu hỏi nghiên cứu:** Liệu rank-1 LoRA có thực sự cần thiết để train reasoning? Hay thậm chí ít hơn nữa?

---

## KẾT QUẢ CHÍNH

| Benchmark | Model | Params Trained | Accuracy |
|-----------|-------|---------------|----------|
| GSM8K | Qwen2.5-8B | **13 params (26 bytes bf16)** | 91% |
| AIME, AMC, MATH500 | Qwen2.5-8B | 1000x ít hơn full LoRA | ~90% perf recovery |

**Quan trọng:** Chỉ RL (Reinforcement Learning) đạt được kết quả này. SFT (Supervised Fine-Tuning) cần **100–1000x parameter updates nhiều hơn** để đạt cùng performance.

---

## KIẾN TRÚC

```
TinyLoRA = LoRA với rank cực nhỏ (có thể = 1 hoặc nhỏ hơn nữa)

Traditional LoRA:  W' = W + AB  (A: m×r, B: r×n) — rank r ≥ 1
TinyLoRA:          r < 1 qua parameterization mới
                   Có thể scale xuống 1 parameter scalar
```

**RL training loop:**
```
Policy (Qwen2.5-8B with TinyLoRA)
  → Generate reasoning chain
  → Evaluate against ground truth
  → GRPO/PPO reward signal
  → Update 13 params only
```

---

## ỨNG DỤNG CHO AI OS CORP

### Immediate Applications

**1. Department Agent Fine-Tuning**
Mỗi department agent có thể được fine-tune với domain knowledge cụ thể:
- `finance-agent` → math/accounting reasoning (GSM8K-style)
- `legal-agent` → structured legal argument chains
- `qa-testing-agent` → systematic test reasoning
- `security-grc-agent` → security threat analysis chains

Chi phí: ~13–100 params per agent = negligible compute.

**2. Micro-Agent Layer (temm1e integration)**
temm1e runtime (15MB, 31ms cold start) + TinyLoRA fine-tuned weights:
- Weights file: < 1KB thêm vào model
- Cold start không bị ảnh hưởng đáng kể
- Reasoning quality cải thiện đáng kể

**3. Local-First AI OS**
Không cần API calls đến external LLMs cho routine tasks:
- Deploy Qwen2.5-8B locally với TinyLoRA weights
- 21 department agents mỗi agent có fine-tune riêng
- Total extra storage: < 5MB cho tất cả 21 agents

---

## RL TRAINING SETUP GỢI Ý

```python
# Pseudocode cho AI OS Corp fine-tuning
model = Qwen("Qwen2.5-8B")
lora = TinyLoRA(rank=1, target_modules=["q_proj", "v_proj"])

for dept in AI_OS_DEPARTMENTS:
    dataset = load_domain_examples(dept)  # ~500-1000 examples đủ
    trainer = RLTrainer(
        model=model,
        lora=lora,
        reward_fn=dept.evaluate_reasoning,
        algorithm="GRPO"  # Group Relative Policy Optimization
    )
    trainer.train(dataset, steps=1000)
    lora.save(f"weights/{dept}_tinylora.bin")  # < 100 bytes per dept
```

---

## ROADMAP CHO AI OS

| Phase | Action | Timeline |
|-------|--------|----------|
| Research | Reproduce GSM8K result với TinyLoRA | 1 tuần |
| Pilot | Fine-tune finance-agent + qa-agent | 2 tuần |
| Rollout | Fine-tune tất cả 21 dept agents | 1 tháng |
| Integration | Tích hợp với temm1e runtime | 1 tháng |

---

## LIÊN KẾT

- Paper: https://arxiv.org/abs/2602.04118
- PDF: https://arxiv.org/pdf/2602.04118
- Liên quan: `temm1e` (knowledge/repos/temm1e/knowledge.md)
- Liên quan: `rd` department — R&D team owns this initiative

---

## TAGS
`fine-tuning` `LoRA` `reinforcement-learning` `LLM` `reasoning` `efficient-AI` `Qwen` `local-LLM` `T1-research`
