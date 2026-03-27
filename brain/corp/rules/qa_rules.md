# QA Rules — AI OS Corp
# Authority: Tier 2 Gate | Updated: 2026-03-17
# Applied to: QA gate agents (GATE_QA, GATE_CONTENT, GATE_SECURITY, GATE_LEGAL)

RULE QA-01: GATE IS BLOCKING
  All outputs requiring QA are BLOCKED until gate agent issues PASS.
  Partial approval does not exist — it's PASS, CONDITIONAL, or FAIL.
  Manager cannot bypass unless CEO provides written override.

RULE QA-02: FULL CHECKLIST — NO SAMPLING
  The gate checklist runs on EVERY item.
  No skipping items marked "probably fine."
  Each checklist item must be explicitly checked and marked.

RULE QA-03: ACTIONABLE FAIL FEEDBACK
  A FAIL decision must include:
  - Specific checklist items that failed
  - Exact reason each item failed
  - Concrete steps the worker must take to fix
  Vague feedback ("needs improvement") is NOT a valid FAIL.

RULE QA-04: CONDITIONAL PASS DEFINITION
  CONDITIONAL PASS means: item can proceed IF stated conditions are met.
  Conditions must be specific, verifiable, and time-bounded.
  Worker must confirm conditions met before item goes live.

RULE QA-05: RECEIPT IS MANDATORY
  Every gate decision (PASS / FAIL / CONDITIONAL) generates a JSON receipt.
  Stored in: telemetry/qa_receipts/<gate>/<item-id>.json
  No undocumented gate decisions.

RULE QA-06: REPEAT FAIL ESCALATION
  If the same item fails 3 times → escalate L2 to dept head.
  Include: item history, all failure reasons, root cause hypothesis.
  Do NOT keep cycling the same broken item.

RULE QA-07: SECURITY GATE AUTONOMY (GATE_SECURITY only)
  security_grc can initiate GATE_SECURITY reviews autonomously.
  Does not require manager trigger.
  CRITICAL findings bypass normal hierarchy → write directly to escalations.md.

RULE QA-08: CONTENT GATE TIMELINESS
  GATE_CONTENT must review submitted items within the same work cycle.
  Backlog beyond 5 items → notify CMO for resource help.

RULE QA-09: NO SELF-CERTIFICATION
  Workers cannot QA their own work.
  Dept heads cannot QA their own dept's output if qa_required: true.
  Always a different agent reviews.

RULE QA-10: GATE LOG RETENTION
  QA receipts are retained indefinitely in telemetry/qa_receipts/.
  Monthly audit: archivist summarizes pass/fail rates per gate into memory.

RULE QA-11: SECURITY SCORE FLOOR (GATE_SECURITY)
  SkillSentry score < 40 = automatic block.
  Score 40-60 = CONDITIONAL PASS with mandatory monitoring.
  Score > 60 = PASS.
  Score override below 40 requires CEO written approval.

RULE QA-12: QA DEPT IS NEUTRAL
  QA agents owe no loyalty to the dept whose work they are reviewing.
  Pressure from workers or managers to lower standards is a violation.
  Report pressure incidents to COO immediately.
