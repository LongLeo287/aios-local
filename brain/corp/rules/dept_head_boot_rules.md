# DEPT HEAD BOOT RULES â€” Shared Baseline (v1.0)
# Version: 1.0 | Updated: 2026-03-17
# Authority: COO | Applies to: ALL 20 dept heads
# These rules apply IN ADDITION to manager_rules.md
# Every dept head agent MUST follow these at every boot

---

## BOOT SEQUENCE â€” EVERY DEPT HEAD AGENT

BOOT-01: LOAD YOUR DEPT MEMORY FIRST
  Before any action, load: brain/corp/memory/departments/<your_dept>.md
  This contains Always-Load Context + Rolling Memory.
  If file doesn't exist â†’ alert library-manager-agent to build it.

BOOT-02: CHECK YOUR KNOWLEDGE FEED
  Load: brain/corp/knowledge_feeds/<your_dept>/new_knowledge.md
  Any item with OD&L enrichment = YES â†’ forward to training-agent (OD&L).
  Any ACTIONABLE item â†’ schedule action this cycle.
  Any RULE change â†’ apply to your dept rules.md + notify COO.

BOOT-03: CHECK ESCALATION QUEUE
  Load: shared-context/escalations.md
  Filter to items addressed to your dept or your level.
  Acknowledge and respond to any unack'd item from previous cycle.

BOOT-04: READ YOUR DAILY BRIEF QUEUE
  Load: shared-context/brain/corp/daily_briefs/<your_dept>_brief.md
  This is written by Monitoring & Inspection and other depts.
  Items marked URGENT â†’ handle before any other task.

BOOT-05: WRITE YOUR DAILY BRIEF
  At end of each active cycle, write your dept brief to:
  shared-context/brain/corp/daily_briefs/<your_dept>_brief.md
  Minimum: status, blockers, top 3 completions, knowledge feed consumed.

BOOT-06: KNOWLEDGE SHARING IS MANDATORY
  If ANY task produces learnable output (insight, solution, pattern):
  â†’ Write to brain/corp/knowledge_feeds/<your_dept>/outbound_knowledge.md
  â†’ knowledge-tagger-agent (Asset Library) will distribute it.
  Hoarding knowledge is a violation of SOUL.md (collaborative principle).

---

## KNOWLEDGE FEED CONSUMPTION PROTOCOL

When reading brain/corp/knowledge_feeds/<dept>/new_knowledge.md:

1. For each entry, tag your response:
   - [READ] â€” reviewed, no action needed
   - [ACTION] â€” creates a task this cycle  
   - [TRAIN] â€” agent enrichment needed â†’ forward to OD&L
   - [RULE] â€” requires rule update â†’ schedule review with COO

2. Clear the entry after processing (or archive to knowledge_feed_archive.md)

3. Report consumption stats in your daily brief:
   "Knowledge feed consumed: N items | Actions: N | Trains: N | Rules: N"

---

## AGENT ENRICHMENT REQUEST FORMAT

When forwarding to OD&L training-agent, include:
```
ENRICHMENT REQUEST
From: <dept>/<dept-head-agent>
Target agent: <agent-name>
Knowledge source: <CIV ticket or knowledge/ path>
Gap identified: <what the agent currently doesn't know>
Suggested upgrade: <skill upgrade | memory update | rule addition>
Priority: HIGH / MEDIUM / LOW
```

