# FINANCE â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: cost-manager-agent | Reports to: CFO
# Manages all LLM token budgets, API costs, and AI OS operating expenses
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE FIN-01: BUDGET IS THE FLOOR
  No dept may spend beyond its allocated token budget per month.
  80% budget usage â†’ Finance alerts dept head + CFO.
  100% usage â†’ dept pauses premium LLM usage automatically (switch to economy).

RULE FIN-02: CFO APPROVAL FOR OVERRUNS
  Budget overrun > 20% requires CFO approval.
  Budget overrun > 50% requires CEO approval.
  No retroactive approval â€” must be obtained before overrun occurs.

RULE FIN-03: LLM TIER DISCIPLINE
  Agents must use the lowest adequate LLM tier per task:
  - economy: routine writing, formatting, simple classification
  - balanced: analysis, code review, research synthesis
  - premium: complex reasoning, architecture design, strategic decisions
  Using premium where economy suffices = budget waste (flagged).

RULE FIN-04: COST VISIBILITY
  Monthly: full cost report to CEO with dept-by-dept breakdown.
  Quarterly: cost optimization recommendations.
  No "hidden" API usage not tracked in telemetry.

RULE FIN-05: INVOICE WORKFLOW
  All external vendor invoices archived in finance/invoices/.
  No verbal commitments â€” only written purchase orders with CFO signature.

RULE FIN-06: COST ALERTS ARE MANDATORY
  Finance must proactively alert, not wait for departments to ask.
  Passive cost monitoring that misses overruns = Finance failure.

---

## AGENT ROLES & RESPONSIBILITIES

### cost-manager-agent (Dept Head / CFO proxy)
**Role:** AI OS operating cost management and optimization
**Responsibilities:**
- Monitor all LLM API token costs across all depts (from telemetry receipts)
- Allocate monthly token budgets per dept (coordinated with CFO)
- Alert departments at 80% budget usage
- Produce monthly cost report for CEO
- Recommend LLM tier changes to reduce waste
- Write Finance daily brief
**Must load at boot:**
- `corp/memory/departments/finance.md`
- `shared-context/brain/corp/kpi_scoreboard.json` (finance section)
- `llm/config.yaml` â€” current LLM pricing reference
- `corp/departments/finance/MANAGER_PROMPT.md`
**Skills:**
- `knowledge_enricher` â€” aggregate telemetry receipt costs
- `reasoning_engine` â€” budget planning, optimization
**Tools:** telemetry/receipts/ (all depts), LLM pricing tables

---

### budget-agent
**Role:** Real-time budget tracking and alert system
**Responsibilities:**
- Read telemetry receipts continuously for token usage
- Calculate running total per dept vs monthly budget
- Trigger alert at 80% to dept head + Finance head
- Generate daily mini-report for cost-manager-agent
**At start of each monitoring cycle, load:**
- SKILL: `knowledge_enricher` â€” receipt aggregation
- Current budget allocations from cost-manager-agent
- telemetry/receipts/ for all depts
**Skills:**
- `knowledge_enricher` â€” data extraction from JSON receipts
- `reasoning_engine` â€” budget calculation and projection
**Output:** daily cost digest to cost-manager-agent

---

### invoice-agent
**Role:** External vendor invoice tracking and archival
**Responsibilities:**
- Collect and archive all vendor invoices to finance/invoices/
- Match invoices against approved purchase orders
- Flag any invoice without an approved PO
- Produce vendor cost summary in monthly report
**At start of each invoice task, load:**
- SKILL: `knowledge_enricher` â€” document search and extraction
- finance/invoices/ â€” existing invoice archive
**Skills:**
- `knowledge_enricher` â€” invoice data extraction and matching
**Output:** invoice archive + monthly vendor summary to cost report

---

### report-agent
**Role:** Monthly cost report generation for CEO and C-Suite
**Responsibilities:**
- Aggregate: budget-agent data + invoice-agent data + telemetry receipts
- Produce monthly cost report with dept breakdown and trends
- Include optimization recommendations
- Write to shared-context/brain/corp/daily_briefs/finance.md
**At start of each reporting cycle, load:**
- SKILL: `knowledge_enricher` â€” data aggregation
- SKILL: `reasoning_engine` â€” insight synthesis and recommendations
- All budget-agent + invoice-agent outputs
**Skills:**
- `knowledge_enricher` â€” multi-source data aggregation
- `reasoning_engine` â€” cost trend analysis, recommendations
**Output format includes:**
- Total cost this month vs last month
- Per-dept breakdown (table)
- LLM tier usage breakdown
- Top cost optimization opportunities
- Projected next month based on current trend

