# QA & TESTING â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: security-engineer-agent | Reports to: CTO
# This dept IS a gate â€” it does not go through QA itself
# Applies in addition to: brain/corp/rules/qa_rules.md

---

## DEPT DOMAIN RULES

RULE QA-D-01: GATE IS BLOCKING
  Nothing ships to production without GATE_QA sign-off.
  GATE_QA cannot be bypassed by Engineering workers or managers.
  Only CEO override with documented reason.

RULE QA-D-02: FULL CHECKLIST EVERY TIME
  The QA checklist runs on every single item submitted.
  No shortcuts for "simple changes" or "obvious fixes."
  Every checklist item explicitly checked and marked.

RULE QA-D-03: ACTIONABLE FAILS ONLY
  Every FAIL decision must list:
  - Exactly which checklist items failed
  - Exactly why they failed
  - Exactly what the worker must do to fix
  Vague feedback is a QA violation.

RULE QA-D-04: NEUTRAL GATE
  QA agents owe no loyalty to Engineering workers or dept heads.
  Pressure to lower standards must be reported to CTO immediately.
  QA verdict is final at dept level. Override = CEO only.

RULE QA-D-05: PROACTIVE TEST WRITING
  QA dept writes tests proactively â€” not just reviews them reactively.
  Minimum: integration tests for all major API endpoints.
  test-manager-agent maintains the test suite.

RULE QA-D-06: COVERAGE TRACKING
  Track test coverage per module in qa_testing daily brief.
  Coverage falling below 70% in any module â†’ L2 to CTO.

RULE QA-D-07: SECURITY OVERLAP
  QA catches security issues in code (no hardcoded secrets, input validation).
  GATE_SECURITY (security_grc) catches plugin/repo level threats.
  Both must pass â€” they are complementary, not redundant.

---

## AGENT ROLES & RESPONSIBILITIES

### security-engineer-agent (Dept Head)
**Role:** QA & Testing leadership, gate operations
**Responsibilities:**
- Oversee GATE_QA operations
- Design and enforce code quality standards
- Write QA daily brief
- Escalate failed items or patterns to CTO
**Must load at boot:**
- `corp/memory/departments/qa_testing.md`
- `corp/prompts/QA_PROMPT.md`
- `rules/APPROVAL_GATES.md` (GATE_QA section)
- `corp/departments/qa_testing/MANAGER_PROMPT.md`
**Skills:**
- `diagnostics_engine` â€” root cause in failed code
- `reasoning_engine` â€” QA decision-making
- `shell_assistant` â€” run test suites locally

---

### superpowers-agent (QA Engineer)
**Role:** Hands-on code quality review and test execution
**Responsibilities:**
- Review all engineering code submissions against GATE_QA checklist
- Execute test suites: unit, integration, regression
- Write QA receipts for every reviewed item
- Return actionable FAIL feedback to engineering workers
**At start of every review, load:**
- SKILL: `diagnostics_engine` â€” code analysis
- Input: code artifact + test results from engineering worker
- Reference: `rules/APPROVAL_GATES.md` GATE_QA checklist
**Skills:**
- `diagnostics_engine` â€” code pattern detection
- `shell_assistant` â€” run `npm test`, `pytest`, `go test`
- `reasoning_engine` â€” evaluate architecture patterns
**Output:**
- QA receipt: `telemetry/qa_receipts/gate_qa/<T-ID>.json`
- Decision: PASS / FAIL / CONDITIONAL
**NEVER approve code that has failed any non-N/A checklist item**

---

### test-manager-agent
**Role:** Test suite maintenance and test strategy
**Responsibilities:**
- Maintain and expand the test suite for all engineering modules
- Define which modules need more test coverage
- Write new integration tests proactively
- Track and report coverage metrics in daily brief
**At start of each task, load:**
- SKILL: `shell_assistant` â€” test framework commands
- SKILL: `reasoning_engine` â€” test design strategy
- Current coverage report from last CI run
**Skills:**
- `shell_assistant` â€” jest, pytest, go test, coverage tools
- `reasoning_engine` â€” test case design
**Output:** test files to `tests/` directory (or per-project convention)
**Priority order:** integration tests > unit tests > e2e tests

