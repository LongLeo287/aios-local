# KHO RULES — Master Rules Index
# Version: 1.0 | 2026-03-24 | Owner: Antigravity (Tier 1)
# Source of truth: GEMINI.md (core rules) + corp/departments/*/rules.md (dept rules)

---

## CORE RULES (from GEMINI.md)

| Rule ID | Name | File | Priority |
|---------|------|------|----------|
| RULE-STORAGE-01 | Storage Location | GEMINI.md#RULE-STORAGE-01 | P0 |
| RULE-CIV-01 | Auto CIV Pipeline | GEMINI.md#RULE-CIV-01 | P0 |
| RULE-NOTIFICATION-01 | Alert Routing | GEMINI.md#RULE-NOTIFICATION-01 | P0 |
| RULE-VERSION-01 | Dependency Pinning | GEMINI.md#RULE-VERSION-01 | P1 |
| RULE-PROCESS-01 | Deploy Process | GEMINI.md#RULE-PROCESS-01 | P1 |
| RULE-LANG-01 | Language Policy | GEMINI.md#RULE-LANG-01 | P1 |
| RULE-EXEC-01 | Execution Routing | GEMINI.md#RULE-EXEC-01 | P1 |
| RULE-CATALOG-01 | Plugin/Repo Tracking | GEMINI.md#RULE-CATALOG-01 | P1 |
| RULE-ACTIVATION-01 | Plugin Activation | GEMINI.md#RULE-ACTIVATION-01 | P1 |
| RULE-WEB-01 | Web Intelligence | GEMINI.md#RULE-WEB-01 | P2 |
| RULE-CONTEXT7-01 | Context7 Docs | GEMINI.md#RULE-CONTEXT7-01 | P2 |
| RULE-AGENT-PLATFORM-01 | No Platform Lock-in | GEMINI.md#RULE-AGENT-PLATFORM-01 | P2 |
| RULE-ECC-01 | Everything Claude Code | GEMINI.md#RULE-ECC-01 | P2 |
| RULE-RAG-01 | LightRAG First | GEMINI.md#RULE-RAG-01 | P2 |
| RULE-TIER-01 | 3-Tier Plugin Architecture | GEMINI.md#RULE-TIER-01 | P0 |
| RULE-AGENT-MECHANICS-01 | Agent Context | GEMINI.md#RULE-AGENT-MECHANICS-01 | P1 |
| RULE-SEQUENTIAL-THINKING-01 | Deep Reasoning | GEMINI.md#RULE-SEQUENTIAL-THINKING-01 | P2 |
| RULE-GIT-NATIVE-01 | Git Operations | GEMINI.md#RULE-GIT-NATIVE-01 | P2 |

## DEPT RULES (21 Departments)

| Dept | Rules File | Rule IDs |
|------|-----------|---------|
| content_intake | corp/departments/content_intake/rules.md | CIV-01 to CIV-12 |
| security_grc | corp/departments/security_grc/rules.md | SEC-* |
| engineering | corp/departments/engineering/rules.md | ENG-* |
| qa_testing | corp/departments/qa_testing/rules.md | QA-* |
| finance | corp/departments/finance/rules.md | FIN-* |
| hr_people | corp/departments/hr_people/rules.md | HR-* |
| legal | corp/departments/legal/rules.md | LEG-* |
| marketing | corp/departments/marketing/rules.md | MKT-* |
| rd | corp/departments/rd/rules.md | RD-* |
| registry_capability | corp/departments/registry_capability/rules.md | REG-* |
| *(other 11 depts)* | corp/departments/*/rules.md | DEPT-* |

## GOVERNANCE RULES

| Rule | Source | Scope |
|------|--------|-------|
| CEO authority | corp/rules/ceo_rules.md | All |
| C-Suite limits | corp/rules/csuite_rules.md | Tier 1 |
| Manager mandate | corp/rules/manager_rules.md | Tier 2 |
| Worker constraints | corp/rules/worker_rules.md | Tier 3 |
| Approval gates | corp/rules/APPROVAL_GATES.md | All |
| QA standards | corp/rules/qa_rules.md | QA |

## CLAUDE CODE RULES (.clauderules)

| Rule | Description |
|------|-------------|
| Circuit Breaker | 2-failure max, then BLOCKED |
| ABSOLUTE PROHIBITIONS | 9 hard stops (see .clauderules) |
| CIV prohibition | No bypass of CIV pipeline |
| Workspace boundary | d:\AI OS CORP\AI OS\ only |

## HOW TO ADD A NEW RULE

1. Write rule in source file (GEMINI.md for global, dept/rules.md for dept-specific)
2. Add entry to this INDEX.md
3. If global rule: also add to CLAUDE.md equivalent section
4. Notify CEO: `[NEW RULE] RULE-<ID>-<NAME>`
5. Update kho/rules/INDEX.md version header
