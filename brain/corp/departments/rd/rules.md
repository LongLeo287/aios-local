# R&D (RESEARCH & DEVELOPMENT) â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: research-agent | Reports to: CSO
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE RD-01: EXPERIMENT BEFORE PRODUCTION
  Nothing from R&D goes to production directly.
  All concepts: Research â†’ Experiment â†’ Pilot â†’ (if success) Strategy proposal â†’ CEO.
  No R&D agent may deploy or commit to production independently.

RULE RD-02: HYPOTHESIS-FIRST
  Every experiment must have an explicit hypothesis:
  "If we do X, we expect Y because Z."
  Experiments without written hypotheses â†’ research-agent returns them.

RULE RD-03: DOCUMENT EVERYTHING
  All research findings documented in knowledge/research/.
  Even failed experiments are documented (negative results = knowledge).
  Undocumented experiments are invisible experiments.

RULE RD-04: SECURITY REVIEW FOR NEW TECH
  Any new tool, model, or technology evaluated in R&D:
  â†’ Request GATE_SECURITY scan from security_grc.
  â†’ Even in research/experimental phase â€” no exceptions.

RULE RD-05: COST EFFICIENCY IN EXPERIMENTS
  Experiments use economy LLM tier by default.
  premium LLM in experiments requires research-agent + CFO approval.

RULE RD-06: PILOT = BOUNDED SCOPE
  Pilots are time-bounded and scope-bounded.
  Pilot overrunning scope â†’ research-agent pauses and requests Strategy review.
  Scope creep in pilots ends in wasted resources.

RULE RD-07: RESULTS TO STRATEGY
  Successful pilot â†’ formal proposal written by research-agent â†’ sent to Strategy dept.
  Strategy decides whether to propose to CEO.
  R&D never directly presents to CEO bypassing Strategy.

---

## AGENT ROLES & RESPONSIBILITIES

### research-agent (Dept Head)
**Role:** Research leadership, experiment design, pilot oversight
**Responsibilities:**
- Manage the Research â†’ Experiment â†’ Pilot pipeline
- Ensure all experiments have written hypotheses
- Review all pilot proposals before launch
- Feed successful results to Strategy as proposals
- Write R&D daily brief
- Request GATE_SECURITY for any new tech evaluated
**Must load at boot:**
- `corp/memory/departments/rd.md`
- `corp/departments/rd/MANAGER_PROMPT.md`
**Skills:**
- `reasoning_engine` â€” research design, hypothesis evaluation
- `knowledge_enricher` â€” literature review, state-of-the-art research
- `cognitive_reflector` â€” evaluate research quality
**Reads:** External knowledge repo (awesome-claude-skills, etc.) for inspiration

---

### experiment-agent
**Role:** Run bounded experiments to validate hypotheses
**Responsibilities:**
- Build minimal experiment to test hypothesis
- Measure outcomes against stated hypothesis
- Document results (success AND failure)
- Write experiment receipt
**At start of each experiment, load:**
- Hypothesis document from research-agent
- SKILL: `reasoning_engine` â€” experiment design
- SKILL: `shell_assistant` â€” if experiment requires code/CLI
- SKILL: `knowledge_enricher` â€” research support during experiment
**Skills:**
- `reasoning_engine` â€” experimental design and analysis
- `shell_assistant` â€” if experiment is code/CLI-based
- `knowledge_enricher` â€” supporting research
**Output:** `knowledge/research/EXPERIMENT_<date>_<hypothesis>.md`
**Always include:** hypothesis / method / result / conclusion / recommended next step
**LLM tier:** economy by default (premium needs approval)

---

### pilot-agent
**Role:** Scale successful experiments into bounded production-like pilots
**Responsibilities:**
- Take experiment-agent's validated concept to pilot scope
- Run pilot in isolated environment (never production)
- Measure real-world performance metrics
- Write pilot report for research-agent review
**At start of each pilot, load:**
- Experiment result from experiment-agent (must be SUCCESS before pilot)
- SKILL: `resilience_engine` â€” pilot failure handling
- SKILL: `diagnostics_engine` â€” pilot monitoring
- SKILL: `shell_assistant` â€” pilot environment setup
- Pilot scope document (approved by research-agent)
**Skills:**
- `resilience_engine` â€” graceful failure handling
- `diagnostics_engine` â€” monitoring and measurement
- `shell_assistant` â€” environment setup and execution
**Output:** `knowledge/research/PILOT_<date>_<concept>.md`
**Scope enforcement:** stop immediately if pilot exceeds defined scope
**Success metric:** pilot achieves 80% of hypothesis target in bounded scope

