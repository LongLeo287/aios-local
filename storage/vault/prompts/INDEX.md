# KHO PROMPTS — Master Prompt Index
# Version: 1.0 | 2026-03-24 | Owner: Antigravity
# All prompts in one place — system, dept, agent level

---

## SYSTEM PROMPTS

| Prompt | File | Reads By | Tier |
|--------|------|---------|------|
| CEO Prompt | corp/prompts/CEO_PROMPT.md | CEO guidance | T0 |
| Master Prompt | corp/prompts/master_prompt.md | All agents | T0 |
| C-Suite Prompt | corp/prompts/CSUITE_PROMPT.md | CFO/COO/CMO/CTO | T1 |
| Manager Prompt (template) | corp/prompts/MANAGER_PROMPT.md | Dept heads | T2 |
| Worker Prompt (template) | corp/prompts/WORKER_PROMPT.md | Dept workers | T3 |
| QA Prompt | corp/prompts/QA_PROMPT.md | qa_testing | T2 |

## DEPT MANAGER PROMPTS (21)

| Dept | MANAGER_PROMPT | WORKER_PROMPT | Status |
|------|---------------|---------------|--------|
| asset_library | corp/departments/asset_library/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| client_reception | corp/departments/client_reception/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| content_intake | corp/departments/content_intake/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK v1.2 |
| content_review | corp/departments/content_review/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| engineering | corp/departments/engineering/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| finance | corp/departments/finance/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| hr_people | corp/departments/hr_people/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| it_infra | corp/departments/it_infra/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| legal | corp/departments/legal/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| marketing | corp/departments/marketing/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| monitoring_inspection | monitoring_inspection/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| od_learning | corp/departments/od_learning/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| operations | corp/departments/operations/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| planning_pmo | corp/departments/planning_pmo/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| qa_testing | corp/departments/qa_testing/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| rd | corp/departments/rd/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| registry_capability | registry_capability/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| security_grc | corp/departments/security_grc/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| strategy | corp/departments/strategy/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| support | corp/departments/support/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |
| system_health | corp/departments/system_health/MANAGER_PROMPT.md | WORKER_PROMPT.md | OK |

## BOOT PROMPTS

| Agent | Boot File | Location |
|-------|---------|---------|
| Antigravity | GEMINI.md | root |
| Claude Code | CLAUDE.md | root |
| Claude Code constitution | .clauderules | root |

## AGENT PROMPTS (brain/agents/)

brain/agents/ contains 48 agent definition files.
Key agents: intake-agent, classifier-agent, strix-agent, content-analyst-agent,
            content-validator, ingest-router, skill-creator, repo-fetcher...

## PROMPT RUNES

corp/prompts/runes/ — quick format selectors for CEO:
- report_formats.md

## HOW TO ADD A PROMPT

1. Create file in appropriate location (system → corp/prompts/, dept → corp/departments/<dept>/)
2. Add entry to this INDEX.md
3. If agent prompt: also add to brain/agents/<agent>.md
4. Register in kho/agents/ if new agent
