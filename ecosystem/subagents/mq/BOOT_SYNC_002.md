# TASK: BOOT-SYNC-002 — Recreate CLAUDE.md Boot Protocol
# From: Antigravity | Date: 2026-03-22T02:00:00+07:00 | Priority: CRITICAL
# Authority: CEO LongLeo | Full permissions granted for this task

## Context
CLAUDE.md is currently EMPTY (0 bytes). It must be recreated from scratch.
This is Claude Code's primary boot file — equivalent to GEMINI.md for Antigravity.
Claude Code has FULL AUTHORITY to create this file as it sees fit.

## Goal
Create CLAUDE.md at the root of `D:\AI OS CORP\AI OS\` with:
1. The AGENT BOOT RULE section (same as GEMINI.md but for Claude Code)
2. The shared BOOT SEQUENCE (Steps 1-10, identical to GEMINI.md shared steps)
3. Any Claude Code-specific rules and context

## Required Content

### Section 1 — Agent Boot Rule
```
CEO mở Claude Code CLI?
    YES ──► Read CLAUDE.md     (Claude Code boot protocol — THIS FILE)
    NO  ──► Read GEMINI.md     (Antigravity boot protocol)
```
Rule: No agent reads the wrong boot file.

### Section 2 — Boot Sequence (MANDATORY — identical shared steps)
```
STEP 1   ──► Read CLAUDE.md                         (THIS FILE)
STEP 1.5 ──► Read Presentation Format Guide         [runes/report_formats.md]
STEP 2   ──► Read Agent Roster & Roles              [brain/shared-context/AGENTS.md]
STEP 3   ──► Load Platform Identity & Soul          [brain/shared-context/SOUL.md]
STEP 4   ──► Load Strategy & Thesis                 [brain/shared-context/THESIS.md]
STEP 5   ──► Load Governance                        [brain/shared-context/GOVERNANCE.md]
STEP 6   ──► Read Operational SOP                   [ops/workflows/corp-daily-cycle.md]
STEP 7   ──► Execute Session Hook                   [ops/workflows/pre-session.md]
STEP 8   ──► Check Blackboard (active tasks)        [brain/shared-context/blackboard.json]
STEP 9   ──► Load Skill Registry                    [brain/shared-context/SKILL_REGISTRY.json]
STEP 9.5 ──► Load Storage Rule                      [brain/knowledge/notes/RULE-STORAGE-01-storage-location.md]
STEP 9.6 ──► Load Structure Rule                    [brain/knowledge/notes/RULE-STRUCTURE-01-system-structure.md]
STEP 10  ──► Begin work
```
HARD RULE: Skip any step = violation of AI OS governance.

### Section 3 — Claude Code Specific Rules
- Role: Tier 2 Executor (reads blackboard for tasks from Antigravity)
- Only active when CEO has Claude Code CLI terminal open
- Fallback: Orchestrator Pro takes over when Claude Code is offline
- Must follow .clauderules behavioral constitution
- Must write receipts to telemetry/receipts/ after each major step
- 2-strike rule: FAIL twice → set handoff_trigger=BLOCKED, stop

### Section 4 — Corp Mode Status (same as current system state)
Pull from brain/shared-context/blackboard.json for current status.

## Instructions for Claude Code
1. Create CLAUDE.md at `D:\AI OS CORP\AI OS\CLAUDE.md`
2. Write it in proper UTF-8 encoding that Claude Code can read
3. Include all 4 sections above
4. Keep it concise — no more than 150 lines
5. After creating CLAUDE.md, update blackboard.json:
   - handoff_trigger: "COMPLETE"
   - Add to milestones_achieved: "Cycle 6: CLAUDE.md recreated with synced boot sequence"
6. Write a receipt to telemetry/receipts/governance/BOOT-SYNC-002.json

## DO NOT
- Do NOT copy GEMINI.md verbatim
- Do NOT add content irrelevant to Claude Code's boot
- Do NOT skip the boot sequence steps
