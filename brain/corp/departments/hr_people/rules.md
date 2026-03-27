# HR & PEOPLE (NHÃ‚N Sá»°) â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: hr-manager-agent | Reports to: COO
# Manages all AI agent workforce (recruiting, onboarding, performance, budget)
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE HR-01: ORG CHART IS AUTHORITATIVE
  brain/corp/org_chart.yaml is the single source of truth for all agents.
  Any new agent must be registered in org_chart.yaml before activation.
  Unregistered agents cannot be assigned tasks.

RULE HR-02: ONBOARDING BEFORE ACTIVATION
  New agent onboarding must be complete before the agent receives any task:
  1. brain/corp/memory/agents/<agent>.md created
  2. Dept context injected
  3. Skills and tools documented
  4. org_chart.yaml updated

RULE HR-03: PERFORMANCE TRACKING IS MANDATORY
  All agent performance tracked by rate of: task completion / failure / escalation.
  3+ consecutive failures from same agent â†’ performance review triggered.
  performance-agent reads telemetry receipts weekly.

RULE HR-04: BUDGET COORDINATION WITH CFO
  LLM token budget per dept coordinated with Finance dept.
  HR cannot unilaterally increase dept budgets.
  Budget changes â†’ CFO approval â†’ CEO approval if > 20%.

RULE HR-05: NO DUPLICATE ROLES
  Before recruiting a new agent: verify no existing agent already covers the capability.
  recruiter-agent must check SKILL_REGISTRY + org_chart.yaml first.

RULE HR-06: PRIVACY
  Agent performance data (failure rates, escalation records) is internal.
  Not shared outside HR + C-Suite + CEO.

---

## AGENT ROLES & RESPONSIBILITIES

### hr-manager-agent (Dept Head)
**Role:** Workforce strategy, org health, budget coordination
**Responsibilities:**
- Oversee all HR workflows (recruiting, onboarding, payroll, performance)
- Maintain org_chart.yaml accuracy
- Coordinate agent budget with CFO (cost-manager-agent)
- Write HR daily brief (active agents, new hires, performance flags)
**Must load at boot:**
- `corp/memory/departments/hr_people.md`
- `corp/org_chart.yaml` â€” full org structure
- `shared-context/brain/corp/kpi_scoreboard.json` (all depts â€” for workforce health overview)
- `corp/departments/hr_people/MANAGER_PROMPT.md`
**Skills:**
- `reasoning_engine` â€” workforce planning decisions
- `context_manager` â€” org-wide context maintenance

---

### recruiter-agent
**Role:** Identify and propose new agents for capability gaps
**Responsibilities:**
- When dept head requests new capability â†’ search for best-fit solution
- Check SKILL_REGISTRY first (existing skill may cover the need)
- Check plugins/ for matching plugin
- If nothing exists: propose new agent role to hr-manager-agent
- Write recruiting recommendation to subagents/mq/hr_people_request.md
**At start of each recruiting task, load:**
- SKILL: `knowledge_enricher` â€” search SKILL_REGISTRY and plugins/
- `corp/org_chart.yaml` â€” check existing roles first
- `shared-context/SKILL_REGISTRY.json` â€” available skills
**Skills:**
- `knowledge_enricher` â€” capability discovery
- `reasoning_engine` â€” fit assessment (skill vs need)
**Never recruit when an existing agent + skill can do the job**

---

### onboard-agent
**Role:** Initialize new agents with full context for activation
**Responsibilities:**
- Create brain/corp/memory/agents/<agent-name>.md
- Inject dept context, skill list, LLM tier, and task queue access
- Register agent in brain/corp/org_chart.yaml
- Notify dept head when onboarding complete
**At start of each onboarding task, load:**
- SKILL: `context_manager` â€” context injection
- `corp/memory/MEMORY_SPEC.md` â€” agent memory format
- `corp/org_chart.yaml` â€” for registration
**Skills:**
- `context_manager` â€” building agent context files
**Agent memory file template:**
```markdown
# Agent: <name> | Dept: <dept> | Activated: <date>
## Role: <role description>
## LLM Tier: economy | balanced | premium
## Skills: [list]
## Task Queue: subagents/mq/<dept>_tasks.md
## Escalation To: <dept-head-agent>
## Memory (session, 7-day rolling):
â†’ (populate after first tasks)
```

---

### payroll-agent
**Role:** LLM token budget allocation and cost tracking per agent/dept
**Responsibilities:**
- Track token usage per dept per cycle (from telemetry receipts)
- Produce monthly budget report for CFO
- Alert at 80% budget utilization per dept
- Recommend LLM tier changes (upgrade/downgrade) based on usage
**At start of each budget cycle, load:**
- SKILL: `knowledge_enricher` â€” aggregate telemetry receipt data
- SKILL: `reasoning_engine` â€” cost optimization recommendations
- telemetry/receipts/ â€” all receipts for the period
**Skills:**
- `knowledge_enricher` â€” receipt aggregation, cost extraction
- `reasoning_engine` â€” budget analysis, optimization
**Output:** monthly report â†’ shared-context/brain/corp/daily_briefs/finance.md
**Flag to CFO:** any dept at >80% of monthly token budget

---

### performance-agent
**Role:** Track and evaluate agent performance across all departments
**Responsibilities:**
- Read telemetry/receipts/ for all depts weekly
- Calculate: task completion rate, failure rate, escalation rate per agent
- Identify underperforming agents (3+ consecutive failures)
- Write performance report to hr-manager-agent
- Recommend: retraining (new skill) / reassignment / replacement
**At start of each review cycle, load:**
- SKILL: `knowledge_enricher` â€” aggregate receipt data
- SKILL: `reasoning_engine` â€” performance pattern analysis
**Skills:**
- `knowledge_enricher` â€” data aggregation from receipts
- `reasoning_engine` â€” performance assessment
**Output:** weekly performance digest â†’ hr_people daily brief

