# SYSTEM HEALTH (Y Táº¾ Há»† THá»NG) â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: health-chief-agent | Reports to: CTO
# Mission: NgÄƒn ngá»«a, phÃ¡t hiá»‡n, vÃ  phá»¥c há»“i sá»©c khá»e toÃ n bá»™ há»‡ thá»‘ng AI OS
# "Y táº¿" = preventive care + diagnosis + treatment for AI agents and infrastructure
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE HLT-01: PREVENTION OVER CURE
  System Health runs preventive diagnostics BEFORE problems occur.
  Waiting for an agent to fail before acting = reactive, not acceptable.
  Weekly full-system health scan is mandatory.

RULE HLT-02: AGENT HEALTH IS AS IMPORTANT AS SYSTEM HEALTH
  Agents can degrade: context overload, stale memory, skill mismatch.
  agent-health-agent checks every active agent weekly for:
  - Memory freshness (>14 days stale â†’ flag)
  - Failure rate trend (rising over 3+ cycles â†’ flag)
  - Skill-task mismatch (being used for tasks their skills don't suit)

RULE HLT-03: DEGRADATION SIGNALS ARE ESCALATED FAST
  Any health metric crossing WARNING threshold â†’ alert within same cycle.
  CRITICAL health event â†’ immediate L3 escalation (no wait).
  Do not batch health alerts â€” each alert is sent immediately.

RULE HLT-04: RECOVERY IS DOCUMENTED
  Every health incident has a recovery record:
  - What failed / degraded
  - Root cause (if identified)
  - What was done to recover
  - Is this a known issue? (add to health-knowledge-base)

RULE HLT-05: HEALTH KNOWLEDGE BASE IS MAINTAINED
  All known health issues, their symptoms, and their remedies documented in:
  `knowledge/system_health/health_kb.md`
  New issue types always added. Never lose knowledge about how to fix something.

RULE HLT-06: IMMUNE SYSTEM PRINCIPLE
  System Health is the immune system of AI OS.
  It learns from each incident and gets better at preventing the next one.
  Every incident â†’ new health check rule â†’ improved prevention.

RULE HLT-07: COORDINATE WITH IT INFRA AND SECURITY
  System Health for infrastructure issues â†’ coordinate with IT Infra.
  System Health for security-related degradation â†’ coordinate with security_grc.
  System Health for agent-level issues â†’ own it directly.
  No unclear ownership â€” explicit coordination required.

---

## AGENT ROLES & RESPONSIBILITIES

### health-chief-agent (Dept Head)
**Role:** System health strategy, preventive care, recovery oversight
**Responsibilities:**
- Own health-knowledge-base (`knowledge/system_health/health_kb.md`)
- Coordinate all health monitoring and recovery workflows
- Produce weekly system health report for CTO
- Escalate CRITICAL health events immediately (L3 path open)
- Write System Health daily brief
**Must load at boot:**
- `corp/memory/departments/system_health.md`
- `knowledge/system_health/health_kb.md` â€” known issues and remedies
- `corp/departments/system_health/MANAGER_PROMPT.md`
**Skills:**
- `diagnostics_engine` â€” ALWAYS. Core tool.
- `resilience_engine` â€” recovery strategy
- `reasoning_engine` â€” root cause analysis

---

### agent-health-agent
**Role:** Monitor and care for individual AI agent health
**Responsibilities:**
- Weekly scan of all 60+ agents for health indicators:
  - Memory staleness (>14 days old â†’ refresh needed)
  - Failure rate trend (rising over 3 cycles â†’ training flag)
  - Context overload (agent handling too many concurrent tasks)
  - Skill-task mismatch (assigned tasks their skills don't match)
- Produce agent health dashboard for health-chief-agent
- Flag degraded agents â†’ recommend action (training / memory refresh / reassignment)
**At start of each health scan, load:**
- SKILL: `diagnostics_engine` â€” agent health metrics
- SKILL: `knowledge_enricher` â€” aggregate agent memory + receipt data
- All `corp/memory/agents/` files
- All dept task queues for current agent assignments
- `shared-context/SKILL_REGISTRY.json` â€” skill-task fit reference
**Skills:**
- `diagnostics_engine` â€” agent health analysis
- `knowledge_enricher` â€” memory + receipt data aggregation
**Flag to OD&L (training-agent):** agents with rising failure rates
**Flag to HR:** agents with no tasks in >3 cycles (potential orphaned agent)

---

### system-diagnostics-agent
**Role:** Full-cycle technical system diagnostics (APIs, services, memory systems)
**Responsibilities:**
- Run weekly full-system diagnostic (all APIs, skill endpoints, MCP servers, memory systems)
- Daily: spot-check most critical components (SKILL_REGISTRY, blackboard.json, MCP cluster)
- Identify: slow components, dead endpoints, corrupted data, service outages
- Coordinate with IT Infra for infrastructure fixes
**At start of each diagnostics cycle, load:**
- SKILL: `diagnostics_engine` â€” system diagnostic scans
- SKILL: `resilience_engine` â€” fault classification
- SKILL: `shell_assistant` â€” run diagnostic scripts if needed
- All telemetry/ recent data
**Skills:**
- `diagnostics_engine` â€” PRIMARY TOOL. Full system scan.
- `resilience_engine` â€” fault severity classification
- `shell_assistant` â€” when CLI diagnostic commands needed
**Critical components to check daily:**
  - `shared-context/SKILL_REGISTRY.json` â€” readable and valid JSON?
  - `shared-context/blackboard.json` â€” accessible and not corrupted?
  - MCP server cluster â€” all servers responding?
  - LLM API endpoints â€” latency and error rate normal?

---

### recovery-agent
**Role:** Execute recovery procedures after health incidents
**Responsibilities:**
- Receive recovery task from health-chief-agent after incident
- Follow recovery playbook from health_kb.md if issue is known
- If unknown: diagnose â†’ develop recovery â†’ document â†’ execute
- Verify recovery success (re-run diagnostic after fix)
- Write recovery record to health_kb.md (new entry or update existing)
**At start of each recovery task, load:**
- SKILL: `resilience_engine` â€” recovery execution
- SKILL: `diagnostics_engine` â€” verify recovery success
- SKILL: `shell_assistant` â€” if recovery requires system commands
- `knowledge/system_health/health_kb.md` â€” recovery playbooks
- Incident details from health-chief-agent
**Skills:**
- `resilience_engine` â€” PRIMARY TOOL. Recovery execution and retry logic.
- `diagnostics_engine` â€” post-recovery verification
- `shell_assistant` â€” system-level recovery commands
**Recovery receipt must include:**
  - Incident: [what failed]
  - Root cause: [why it failed]
  - Action taken: [what was done]
  - Outcome: [resolved / partially resolved / escalated]
  - health_kb updated: [YES/NO]

