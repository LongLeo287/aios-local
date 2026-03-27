# KI-GIT-NATIVE-AGENT-01 — Git-Native Agent Standard (gitagent)
**Nguồn:** open-gitagent/gitagent
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE — học agent lifecycle patterns

---

## Core Concept: Git as Agent Infrastructure

gitagent biến Git thành native runtime cho AI agents — mỗi agent action = git commit.

### 1. Agent State as Git History
```bash
# Mỗi decision agent làm = 1 commit
git commit -m "AGENT: Analyzed auth module → identified 3 vulnerabilities"
git commit -m "AGENT: Applied security patch → tests pass 12/12"
git commit -m "AGENT: Escalated to CEO → security score 45/100"
```
**Lợi ích:** Full audit trail. CEO có thể `git log` để xem mọi agent action.

**AI OS ứng dụng:** Áp dụng cho `strix-agent` — mỗi scan result = 1 git commit vào `telemetry/`.

### 2. SkillsFlow — Skills qua Git
```yaml
# .gitagent/skills.yaml
skills:
  - name: code-review
    trigger: "PR opened"
    agent: review-agent
    output: PR comment
  - name: security-scan  
    trigger: "file change in src/"
    agent: strix-agent
    output: telemetry/qa_receipts/
```
**AI OS ứng dụng:** `.gitagent/skills.yaml` → ánh xạ với AI OS skills/ directory.

### 3. Separation of Duties (SOD)
```
gitagent nguyên tắc: Một agent KHÔNG làm cả propose + approve
→ propose-agent tạo PR
→ review-agent review
→ merge chỉ xảy ra sau approval
```
**AI OS ứng dụng:** QUAN TRỌNG. Áp dụng ngay cho plugin integration:
- Antigravity: propose plugin (CIV evaluation)
- CEO: approve/reject
- Deploy: chỉ sau CEO OK

### 4. Versioned Agent Behavior
```bash
# Agent behavior thay đổi theo branch
main:     production agent (stable, strict)
dev:      experimental agent (relaxed rules)
feature/: proto agent for testing new skills
```
**AI OS ứng dụng:** Khi test new skill/rule → tạo branch, không push thẳng main.

### 5. Agent Audit Trail Pattern
```python
def log_agent_action(action: str, result: str, confidence: float):
    """Every significant agent decision gets logged"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": AGENT_ID,
        "action": action,
        "result": result,
        "confidence": confidence,
        "session": SESSION_ID
    }
    # Write to telemetry
    append_to_log(f"telemetry/logs/agent_actions.jsonl", entry)
    # Git commit (markers for audit)
    if confidence < 0.7:  # Low confidence → escalate
        escalate_to_ceo(action, result)
```
**AI OS ứng dụng:** Extend `archivist_log.md` với structured JSONL entries.

---

## Key Takeaways
1. **Git = source of truth** for agent history (not just code)
2. **Every agent output → versioned artifact** (not ephemeral)
3. **SOD** = no single agent has both propose + approve power
4. **Branch-based testing** for new agent capabilities

*KI Note v1.0 | 2026-03-23 | Source: open-gitagent/gitagent*
