# Expanded Cowork Session Templates
# Extends: cowork/COWORK_PROTOCOL.md
# Updated: 2026-03-17

---

## Template 5: Engineering Squad Cowork

Full backend + frontend + DevOps team simulation.

```
ARCHITECT (Claude/backend-architect-agent):
  - Design system architecture + database schema
  - Output: architecture_doc.md + ERD

FRONTEND (Claude Code/frontend-agent):
  - Implement UI components from ui-ux-agent design
  - Output: React components + test coverage

DEVOPS (GPT-4o/devops-agent):
  - Setup CI/CD + Docker + health monitoring
  - Output: docker-compose.yml + GitHub Actions YAML

QA (subagent/api-tester):
  - API test suite: functional + security + performance
  - Output: test report + Go/No-Go verdict

Coordination: orchestrator_pro
Context file: cowork/sessions/engineering-squad/context.md
Handoff order: ARCH → FRONTEND + DEVOPS (parallel) → QA
```

---

## Template 6: Full Product Team (BMAD Sprint)

Complete agile product sprint with BMAD agents.

```
PM (product-manager-agent):
  - Create PRD → user stories → acceptance criteria
  - Duration: 1-2 hours / Output: PRD + story backlog

ARCHITECT (backend-architect-agent):
  - Technical feasibility + system design
  - Output: ADR + database schema

SCRUM MASTER (scrum-master-agent):
  - Sprint planning → story sizing → sprint goal
  - Output: Sprint backlog + capacity plan

DEVELOPER (Claude Code):
  - Story implementation per AC
  - Output: code diff + implementation notes

QA (code-reviewer + api-tester subagents):
  - Code review + API validation
  - Output: review report + Go/No-Go

WRITER (doc-writer subagent):
  - README + API docs update
  - Output: documentation PR

Coordination: scrum-master-agent
Session duration: 1 sprint (1-2 weeks simulation)
```

---

## Template 7: Growth Team Cowork

Acquisition + content + analytics collaboration.

```
GROWTH (growth-agent):
  - Identify growth lever + design 3 experiments (ICE-scored)
  - Output: experiment backlog + priority ranking

CONTENT (content-agent):
  - Write content for top experiment (blog/email/social)
  - Output: content pack (copy + SEO metadata)

ANALYST (data-agent):
  - Define KPIs + measurement plan + baseline metrics
  - Output: analytics spec + dashboard config

AFFILIATE (growth-hacker + sales-engineer subagents):
  - Affiliate angle + POC scope for partnership approach
  - Output: affiliate brief + partner pitch

Coordination: orchestrator_pro
Context file: cowork/sessions/growth-team/context.md
```

---

## Template 8: AI System Design Cowork

Designing an AI-powered feature with safety + memory.

```
AI ARCHITECT (ai-ml-agent):
  - Select model approach: RAG vs fine-tuning vs prompt
  - Design inference pipeline + memory strategy (Cognee)
  - Output: AI system design doc

BACKEND (backend-architect-agent):
  - API design for AI feature
  - Output: OpenAPI spec + database schema for AI data

SECURITY (security-auditor subagent):
  - LLM security review: prompt injection, data leakage
  - Output: AI-specific security report

PROMPT ENGINEER (prompt-engineer subagent):
  - Optimize system prompts + create eval test cases
  - Output: versioned prompt library + eval results

Coordination: orchestrator_pro
Context file: cowork/sessions/ai-system-design/context.md
```

---

## Template 9: Research-to-Content Pipeline

High-quality long-form content via multi-agent pipeline.

```
RESEARCHER (researcher subagent):
  - Deep research: competitor analysis, expert sources, data
  - Output: structured research doc + source list

SEO ANALYST (data-agent):
  - Keyword research + search intent analysis + AEO opportunities
  - Output: SEO brief + target keywords

WRITER (content-agent):
  - Write using research + SEO brief
  - Output: long-form article (2000-5000 words)

EDITOR (doc-writer subagent):
  - Grammar, structure, readability, brand voice review
  - Output: edited final draft + meta title/description

QA (prompt-engineer subagent):
  - AEO validation: does content answer AI search queries?
  - Output: AEO score + improvement suggestions

Coordination: content-agent (lead)
Output: publication-ready article + metadata
```
