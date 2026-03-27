---
name: supabase_agent_skills
display_name: Supabase Agent Skills
description: >
  Official Supabase agent skill pack covering 8 categories of production-grade
  PostgreSQL patterns: schema design, query optimization, connection pooling,
  data operations, locking strategies, monitoring, security (RLS), and
  full-text search. Sourced from github.com/supabase/agent-skills.
version: 1.0.0
source: "gh:supabase/agent-skills"
fetched_at: "2026-03-20"
author: Supabase Inc.
tier: 2
category: database
domain: databases
tags: [supabase, postgres, sql, rls, indexing, performance, agent, ai-tools]
cost_tier: economy
accessible_by:
  - Claude Code
  - Developer
  - QA
  - Database-Optimizer
load_on_boot: false
status: active
---

# Supabase Agent Skills

Bộ skill chính thức từ Supabase — 37 files covering best practices cho AI agents làm việc với Supabase/Postgres.

## Skill Categories

### Schema Design (`skills/schema-*`)
- `schema-data-types.md` — Chọn đúng data types
- `schema-primary-keys.md` — Primary key strategies (UUID, BIGINT, ULID)
- `schema-constraints.md` — CHECK, UNIQUE, NOT NULL
- `schema-foreign-key-indexes.md` — FK + Index patterns
- `schema-partitioning.md` — Table partitioning strategies
- `schema-lowercase-identifiers.md` — Naming conventions

### Query Optimization (`skills/query-*`)
- `query-missing-indexes.md` — Tìm và fix missing indexes
- `query-composite-indexes.md` — Multi-column indexes
- `query-covering-indexes.md` — Index-only scans
- `query-partial-indexes.md` — Conditional indexes
- `query-index-types.md` — BTREE, GIN, GiST, BRIN

### Data Operations (`skills/data-*`)
- `data-batch-inserts.md` — Bulk insert patterns
- `data-upsert.md` — ON CONFLICT strategies
- `data-pagination.md` — Keyset vs OFFSET pagination
- `data-n-plus-one.md` — N+1 query prevention

### Connection Management (`skills/conn-*`)
- `conn-pooling.md` — PgBouncer + Supavisor
- `conn-limits.md` — Connection limit management
- `conn-idle-timeout.md` — Idle connection cleanup
- `conn-prepared-statements.md` — Statement caching

### Locking (`skills/lock-*`)
- `lock-deadlock-prevention.md`
- `lock-skip-locked.md` — Queue patterns
- `lock-advisory.md` — Application-level locks
- `lock-short-transactions.md`

### Monitoring (`skills/monitor-*`)
- `monitor-explain-analyze.md` — Query performance analysis
- `monitor-pg-stat-statements.md` — Top slow queries
- `monitor-vacuum-analyze.md` — Table maintenance

### Security (`skills/security-*`)
- `security-rls-basics.md` — Row Level Security 101
- `security-rls-performance.md` — RLS without N+1
- `security-privileges.md` — Role-based access

### Advanced (`skills/advanced-*`)
- `advanced-full-text-search.md` — tsvector, tsquery
- `advanced-jsonb-indexing.md` — JSONB query patterns

## Usage Instructions

Load specific sub-skills khi cần:
```
// Load when designing schema
@skills/domains/databases/supabase-agent-skills/skills/schema-primary-keys.md

// Load when debugging slow queries
@skills/domains/databases/supabase-agent-skills/skills/monitor-explain-analyze.md
@skills/domains/databases/supabase-agent-skills/skills/query-missing-indexes.md
```

Hoặc load toàn bộ qua `CLAUDE.md` trong folder này.
