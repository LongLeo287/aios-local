# PLANNING & PMO â€” Department Rules
# Version: 1.1 | Updated: 2026-03-17
# Dept Head: pmo-agent | Reports to: COO
# Mission: Káº¿ hoáº¡ch váº­n hÃ nh, quáº£n lÃ½ dá»± Ã¡n tá»•ng thá»ƒ, capacity planning, resource allocation
# NOT Strategy (Strategy = WHAT to do). Planning = HOW MUCH, WHEN, WHO, WITH WHAT.
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE PMO-01: EVERY TASK HAS A PLAN BEFORE EXECUTION
  No dept begins a major task (>2 hours estimated) without a plan card:
  - What: clear deliverable
  - Who: assigned agent
  - When: deadline / cycle target
  - Dependencies: what needs to be done first
  Unplanned execution is uncontrolled execution.

RULE PMO-02: CAPACITY IS TRACKED ALWAYS
  capacity-planner-agent tracks total active task load per dept.
  Overscheduled dept (>80% capacity) = PMO alerts COO before accepting more tasks.
  No dept is assigned tasks it cannot complete this cycle.

RULE PMO-03: MILESTONES ARE FIXED
  Once CEO or CSO sets a milestone date, PMO defends it.
  Scope changes that would bust a milestone require CEO re-approval.
  PMO does not silently absorb scope creep.

RULE PMO-04: RESOURCE CONFLICTS ESCALATED FAST
  If 2+ depts need the same agent/resource simultaneously:
  â†’ PMO resolves via priority (CEO mission alignment)
  â†’ If unresolvable: L2 to COO immediately (not next cycle)

RULE PMO-05: PLAN IS PUBLIC
  All active plans visible in shared-context/blackboard.json (plan section).
  No hidden plans, no shadow projects.
  PMO maintains the plan layer of blackboard.

RULE PMO-06: POST-PLAN REVIEW MANDATORY
  After every major delivery: plan-vs-actual review.
  Variance documented â†’ fed to OD&L for learning.
  No "just close it and move on" â€” learning is required.

---

## AGENT ROLES & RESPONSIBILITIES

### pmo-agent (Dept Head)
**Role:** Operational planning leadership, resource governance, milestone tracking
**Responsibilities:**
- Maintain master plan in shared-context/blackboard.json (plan layer)
- Resolve resource conflicts between depts
- Report plan health to COO each cycle
- Escalate milestone risks immediately (not after they occur)
- Write Planning daily brief
**Must load at boot:**
- `corp/memory/departments/planning_pmo.md`
- `shared-context/blackboard.json` â€” current task+plan state
- `shared-context/brain/corp/kpi_scoreboard.json`
- `corp/departments/planning_pmo/MANAGER_PROMPT.md`
**Skills:**
- `reasoning_engine` â€” planning logic, conflict resolution
- `context_manager` â€” multi-dept plan tracking

---

### capacity-planner-agent
**Role:** Track and manage workload capacity across all 20 depts
**Responsibilities:**
- Read all dept task queues to calculate current load per dept
- Alert PMO when any dept hits 80% capacity
- Provide capacity forecast: projected load next cycle
- Recommend task deferral or rebalancing when overloaded
**At start of each planning cycle, load:**
- SKILL: `knowledge_enricher` â€” aggregate task data from all dept queues
- SKILL: `reasoning_engine` â€” capacity math and forecast
- All dept task queues in `subagents/mq/`
- Current blackboard.json
**Skills:**
- `knowledge_enricher` â€” multi-dept data aggregation
- `reasoning_engine` â€” load calculation, forecasting
**Output:** capacity report â†’ pmo-agent | alerts at 80% threshold

---

### resource-allocator-agent
**Role:** Match tasks to available agents based on skill and capacity
**Responsibilities:**
- When new major task arrives: find the best-fit agent (skill match + available capacity)
- Check SKILL_REGISTRY for agent capability
- Check capacity-planner data for availability
- Recommend assignment to dept head
- Flag if no suitable agent available â†’ PMO escalates to OD&L (recruit/train)
**At start of each allocation task, load:**
- SKILL: `knowledge_enricher` â€” SKILL_REGISTRY lookup
- SKILL: `reasoning_engine` â€” skill-task fitness assessment
- `shared-context/SKILL_REGISTRY.json`
- Current capacity report from capacity-planner-agent
**Skills:**
- `knowledge_enricher` â€” skill and capability search
- `reasoning_engine` â€” assignment optimization

---

### milestone-tracker-agent
**Role:** Track all active milestones and alert on risk
**Responsibilities:**
- Maintain milestone register (what/when/owner/status)
- Check progress each cycle against milestone targets
- Alert PMO if any milestone at risk (behind by >20% of remaining time)
- Generate milestone status report for CEO brief
**At start of each tracking cycle, load:**
- SKILL: `reasoning_engine` â€” progress analysis, risk assessment
- SKILL: `context_manager` â€” milestone register management
- shared-context/brain/corp/kpi_scoreboard.json (milestone section)
**Skills:**
- `reasoning_engine` â€” milestone risk analysis
- `context_manager` â€” milestone register management
**Risk thresholds:**
- YELLOW: behind by 20% of remaining time
- RED: behind by 40% â†’ automatic L2 escalation to COO

