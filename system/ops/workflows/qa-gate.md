# Department: qa_testing
# qa-gate.md — QA Gate Protocol for AI OS Corp
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations)
# Executed by: QA Department (security-engineer-agent + superpowers-agent)

---

## Rule: Nothing Exits Without QA Sign-Off

Any output from Engineering department MUST pass QA Gate before:
- Being delivered to the user
- Being committed to a shared file
- Being deployed to any environment

Non-Engineering outputs (content, data reports, plans) use Light Review.

---

## Full QA Gate (Engineering Outputs)

```
[QA] Reviewing output: <TASK_ID>

Check 1 — CORRECTNESS
  Does the output do exactly what was specified?
  Test: run against spec or user requirement
  FAIL if: output misses any acceptance criterion

Check 2 — REGRESSION
  Does the output break any existing functionality?
  Test: against known-good baseline or existing tests
  FAIL if: any previously passing behavior now fails

Check 3 — COMPLETENESS
  Are all sub-requirements addressed?
  Test: checklist of all requirements
  FAIL if: any requirement is not addressed

Check 4 — QUALITY
  Does the output follow coding standards, style guides, and .clauderules?
  Test: manual review or automated lint
  FAIL if: major style violation or architectural anti-pattern

Check 5 — COMPLIANCE
  Does the output pass security and governance rules?
  Test: Strix scan (for new code), .clauderules check
  FAIL if: any Strix CRITICAL finding or .clauderules violation
```

**Outcome:**
- ALL 5 PASS → Write `[QA PASS] TASK_ID` to subagents/mq/qa_pass.md → delivery
- ANY FAIL → Write `[QA FAIL] TASK_ID: reason` to subagents/mq/qa_reject.md
  → Engineering worker receives failure note → fixes → re-submits

---

## Light QA Review (Non-Engineering Outputs)

```
Check A — COMPLETENESS: all requirements addressed?
Check B — COMPLIANCE: no policy violations?
```

**Outcome:**
- PASS → approved
- FAIL → send back with specific feedback

---

## QA Escalation

If QA finds a SYSTEMIC issue (same error in 3+ outputs from same agent):
1. Write escalation to `shared-context/corp/escalations.md`
2. Flag to Head of QA (security-engineer-agent)
3. Head of QA escalates to CTO if systemic

---

## QA Metrics (for daily brief)

Track and report in daily_briefs/qa.md:
- Total outputs reviewed: N
- Pass rate: X%
- Failure reasons: [list]
- Unresolved failures: N (must be 0 to report "on_track")

---

*"Quality is not a checkpoint. It is the final word before delivery."*
