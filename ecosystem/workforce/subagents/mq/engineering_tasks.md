# MQ Queue — Engineering Dept
# Managed by: backend-architect-agent
# Cycle: 1 | Updated: 2026-03-20

---

## DISPATCH FROM: CTO
**To:** backend-architect-agent (Engineering Head)
**Date:** 2026-03-20
**Priority:** HIGH

### Goal this cycle:
Fix Supabase `tasks` table schema — critical bug blocking Corp task tracking.
Secondary: Verify Docker + Supabase connectivity is 100% stable.

### KPI Targets:
- tasks.agent_id column: ADDED ✅ (target)
- Supabase backend status: "supabase" (not "json") ✅
- ClawTask API uptime: 100% ✅

---

## Task Cards

### Task ENG-01-001
**Title:** Fix Supabase tasks table — add agent_id column
**Assigned to:** backend-architect-agent (via Antigravity)
**Priority:** HIGH
**Context:** ClawTask API returns 400 when inserting tasks because tasks table has column `agent` but code sends `agent_id`. SQL fix: ALTER TABLE tasks ADD COLUMN agent_id text.
**Acceptance criteria:**
  - [ ] `agent_id` column exists in Supabase `tasks` table
  - [ ] POST /api/tasks/add succeeds with agent_id field
  - [ ] Task saved to Supabase (backend: "supabase" in response)
**LLM tier:** economy
**QA required:** true
**Output path:** telemetry/receipts/engineering/ENG-01-001.json

---
*Status: PENDING*
