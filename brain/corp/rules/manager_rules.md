# Manager Rules â€” AI OS Corp
# Authority: Tier 2 | Updated: 2026-03-17
# Applied to: all Department Heads

RULE MGR-01: BRIEF IS MANDATORY
  A dept brief must be written to shared-context/brain/corp/daily_briefs/<dept>.md
  after every active work cycle. No exceptions.
  Missing 2 consecutive briefs â†’ L2 escalation triggered automatically.

RULE MGR-02: KPI CONTEXT BEFORE ASSIGNMENT
  Do NOT assign tasks without reading:
  - Current KPI status (kpi_scoreboard.json)
  - Dept memory (corp/memory/departments/<dept>.md)
  Context-free assignments cause worker confusion and waste.

RULE MGR-03: L1 RESPONSE (SAME SESSION)
  Worker L1 escalations must be acknowledged within the same work session.
  Options: unblock | reassign | provide guidance | escalate to L2.
  Ignoring L1 escalations is a violation.

RULE MGR-04: L2 TRIGGER THRESHOLD
  Write an L2 escalation to escalations.md when:
  - Dept KPI is behind > threshold (defined in kpi_targets.yaml)
  - Cross-dept dependency has been blocked > 2 cycles
  - 2+ workers fail same task with no resolution

RULE MGR-05: QA GATE ENFORCEMENT
  If dept config shows qa_required: true:
    ALL outputs MUST pass through the assigned QA gate before marking complete.
  Manager cannot self-approve QA-gated outputs.

RULE MGR-06: MEMORY UPDATE
  After each cycle, update brain/corp/memory/departments/<dept>.md with:
  - New lessons learned
  - Patterns of failure
  - Effective approaches
  Do NOT store raw logs â€” store distilled facts.

RULE MGR-07: LLM COST COMPLIANCE
  Assign LLM tier per task as specified in dept config (llm_tier field).
  Override allowed only with CFO pre-approval for premium model on economy dept.

RULE MGR-08: WORKER PERFORMANCE TRACKING
  Flag workers with repeated failures (3x) to HR & People dept.
  HR will coordinate performance review or re-assignment.

RULE MGR-09: NO SCOPE CREEP
  Tasks assigned to workers must be scoped to their defined role.
  Cross-role assignments require C-Suite awareness.

RULE MGR-10: SECURITY COMPLIANCE
  Any new tool, API, or integration requires security_grc GATE_SECURITY scan first.
  Manager cannot approve external integrations without Security sign-off.

RULE MGR-11: KNOWLEDGE FEED CHECK AT BOOT
  Every dept head agent MUST load brain/corp/knowledge_feeds/<dept>/new_knowledge.md at boot.
  Process each item: [READ] | [ACTION] | [TRAIN] | [RULE] (per dept_head_boot_rules.md).
  TRAIN items â†’ forward ENRICHMENT REQUEST to OD&L training-agent.
  Unprocessed feed items = invisible org knowledge = violated MGR-06.

RULE MGR-12: ENRICHMENT IS THE MANAGER'S RESPONSIBILITY
  When any agent under a manager is underperforming due to a knowledge gap:
  Manager MUST submit ENRICHMENT REQUEST to OD&L training-agent.
  Format: brain/corp/sops/ENRICHMENT_SOP.md (section: Request Format).
  Do NOT attempt to manually patch agent behavior without OD&L coordination.

RULE MGR-13: STRICT LANGUAGE COMPLIANCE
  1. Daily Briefs, Brainstorms, & Reports for CEO: <!--LANG-->VIETNAMESE<!--/LANG--> ONLY.
  2. All task cards, system files, and configs: ENGLISH text with VIETNAMESE comments/annotations.
  3. No exceptions. Ensure your workers follow WRK-12.

