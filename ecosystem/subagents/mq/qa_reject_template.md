# qa_reject_template.md — QA Gate Rejection Message Format
# Usage: QA agent copies this template → saves as subagents/mq/<dept>_qa_reject.md
# Read by: worker agent after GATE_QA FAIL
# Ref: corp-gate-flow.md GATE_QA Operation

---

## QA REJECTION — [T-ID]-r[N] — [DATETIME]

From: test-manager-agent (qa_testing)
To: <worker-agent>
Dept: <engineering | other>
Task: [T-ID] — [task title]
Attempt: r[N] (e.g., r1 = first fail, r2 = second fail)

### Failed Checklist Items:
<!-- List ONLY the items that failed — be specific -->

- [ ] **Q[N]** — [Criterion name]
  Issue: [exact problem found]
  Location: [file:line or component]
  Required fix: [what must be done]

<!-- Add more failed items as needed -->

### Passed Items (for reference):
- [x] Q1 — Tests pass
- [x] Q3 — No hardcoded secrets
<!-- etc -->

### Instructions for Worker:
1. Fix ONLY the listed failed items — do not change passing items
2. Re-run tests after fix
3. Re-submit with task ID suffix: [T-ID]-r[N+1]
4. Include this rejection ref in your re-submission notes

<!-- If this is r3 (3rd failure): -->
<!-- 3RD FAIL — This triggers L2 escalation to CTO. Worker: stop and wait. -->

QA Receipt: telemetry/qa_receipts/gate_qa/[T-ID]-r[N].json
