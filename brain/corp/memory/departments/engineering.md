# engineering â€” Department Memory
# Owner: Dept Head | Retention: 30-day rolling | Layer: Department
# Updated: 2026-03-20 | Format: see brain/corp/memory/MEMORY_SPEC.md

## Always-Load Context
Dept: engineering
Escalation path: â†’ CTO â†’ CEO
LLM tier: economy (balanced for complex architecture)
Primary skills: backend, database, docker, supabase, api-design

---

## Sprint 1 â€” 2026-03-17 (Initial)

### Architecture Decisions
- Dept created as part of AI OS Corp v2.0 restructure

### Lessons Learned
- (populate after first active sprint)

### Known Patterns
- (populate after first active sprint)

### Cross-Dept Dependencies
- (populate as discovered)

---

## Cycle 1 â€” 2026-03-20 (First Execution)

### Tasks Completed
- **ENG-01-001** [DONE]: Fixed Supabase `tasks` table schema
  - Applied ALTER TABLE: added `agent_id`, `blockers`, `notes` columns
  - Migration ran via Supabase MCP successfully
  - ClawTask API can now store tasks with agent_id field

### Architecture Decisions
- Supabase chosen as primary DB for ClawTask (JSON as fallback)
- Migration approach: `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` (safe, idempotent)

### Lessons Learned
- ClawTask .env must have SUPABASE_URL + SUPABASE_KEY for backend to switch from json â†’ supabase
- Supabase MCP migration tool works reliably for DDL changes

### Known Issues
- ClawTask still shows backend: "json" â€” need to verify .env vars inside Docker container
- Root cause: .env file may not have the correct SUPABASE vars, or variables not loaded at container startup

### Cross-Dept Dependencies
- Operations: provides ClawTask API infrastructure
- System Health: monitors Supabase connectivity

---
*Append new cycles below. Archivist rotates entries older than 30 days.*

