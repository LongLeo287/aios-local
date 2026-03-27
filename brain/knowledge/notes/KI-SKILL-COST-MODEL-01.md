# KI-SKILL-COST-MODEL-01 — 5-Layer Skill Cost Intelligence (rune)
**Nguồn:** rune-kit/rune
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE — học skill architecture

---

## 5-Layer Skill Framework (rune model)

rune mở rộng model skill standard với focus vào cost intelligence và mesh resilience.

### Layer 1: Intent
```yaml
intent:
  purpose: "What this skill does in one sentence"
  triggers:  ["when user asks about X", "when detecting pattern Y"]
  not_for:   ["when Z is needed instead — use skill-Y"]
```
**Khác với AI OS hiện tại:** AI OS skills chỉ có `description` trong YAML. Thêm `triggers` và `not_for` giúp agent CHỌN ĐÚNG skill hơn.

### Layer 2: Knowledge  
```yaml
knowledge:
  domain: "security | engineering | finance | ..."
  requires: ["tool-A", "api-B"]
  context_budget: 2000   # Max tokens to load for this skill
```
**Áp dụng:** `context_budget` trong skill YAML → agent biết cost trước khi load.

### Layer 3: Execution
```yaml
execution:
  steps:
    - validate_input
    - fetch_context     # May use context7
    - apply_logic
    - verify_output
  timeout: 30s
  retries: 3
```

### Layer 4: Verification (4C Model)
| Gate | Kiểm tra |
|------|---------|
| **Correctness** | Output đúng về mặt logic/fact |
| **Completeness** | Không thiếu step quan trọng |
| **Context-fit** | Phù hợp với ngữ cảnh cụ thể |
| **Consequence** | Không gây side-effect nguy hiểm |

**AI OS hiện tại:** Chưa có 4C verification. Apply cho critical skills (Dept 10 security, Dept 15 finance).

### Layer 5: Evolution
```yaml
evolution:
  version: "1.2.0"
  changelog:
    - "1.2.0: Added context7 integration"
    - "1.1.0: Fixed timeout handling"
  next_review: "2026-06-23"
  owner: "Dept 1"
```

---

## Cost Intelligence Patterns

### Skill Token Cost Estimation
```python
SKILL_COSTS = {
    "context7": 500,           # Variable — depends on docs fetched
    "trivy-security-scan": 200,
    "understand-anything": 1500,  # Heavy — loads full codebase graph
    "framework-standards": 800,
    "agent-shield": 600,
}

def estimate_session_cost(skills_used: list[str]) -> int:
    return sum(SKILL_COSTS.get(s, 300) for s in skills_used)
```
**AI OS ứng dụng:** Add `context_budget` field vào mỗi SKILL.md, track trong `budget.json`.

### Mesh Resilience: Skill Fallback Chain
```yaml
# If primary skill fails → try fallback
fallback_chain:
  - primary: trivy-security-scan
  - fallback: agent-shield        # Manual audit if trivy unavailable
  - last_resort: manual_checklist # If both fail
```
**AI OS ứng dụng:** Strix pipeline — nếu trivy down → AgentShield → manual.

---

## Immediate AI OS Upgrades

1. **Add `triggers` + `not_for` to SKILL.md** — giúp agent chọn skill đúng
2. **Add `context_budget` field** — track cost per skill
3. **4C Verification gates** cho critical skills
4. **Fallback chains** cho security và critical pipeline skills

*KI Note v1.0 | 2026-03-23 | Source: rune-kit/rune*
