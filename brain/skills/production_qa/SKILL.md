---
id: production_qa
name: Production QA
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Adversarial QA reviews and cryptographically-auditable task receipts.

accessible_by:
  - QA
  - Architect

dependencies:
  - reasoning_engine

exposed_functions:
  - name: adversarial_review
  - name: generate_receipt
  - name: edge_case_hunt
  - name: regression_check

consumed_by:
  - orchestrator_pro
emits_events:
  - receipt_generated
  - qa_failed
listens_to:
  - task_complete
---
# ðŸ›¡ï¸ Production QA Skill (High-Fidelity Verification)

This skill mandates industrial-grade quality assurance, assuming all code is broken until proven correct.

## ðŸ› ï¸ Core Functions:
1.  **Adversarial Review (/review-full):**
    - Audit code for the [6 Boundary Safety Patterns].
    - Assume logic is incorrect. Force execution of tests or manual verification logs.
2.  **Receipt Generation (/receipt):**
    - Generate a JSON file in `.agents/telemetry/receipts/` summarizing the task's technical outcome and verification proof.
3.  **Self-Healing Gates:**
    - If a task is rejected/fails, use the [Circuit Breaker](file:///d:/APP/BookMark%20Extension/.agents/skills/resilience_engine/SKILL.md) to rework. Max 2 cycles before user notification.

## ðŸ“‹ Instructions:
Before declaring "[x] Task Complete":
1. Run `/review-full` on all modified files.
2. Generate the **Task Receipt**.
3. Re-verify artifact existence on disk.

## Principle:
*"Trust, but verify. Verify, then trust."*

