# Batch-add tier metadata to 2618 SKILL.md files
**ID:** PROP_2026-03-22_SKILL_TIER_BATCH
**Type:** NEW_SKILL | **Priority:** HIGH
**Generated:** 2026-03-22T21:53:14.373868
**Agent:** product-manager-agent

## Context
FAST_INDEX rebuild found 2618/2795 skills have no tier set in frontmatter. This breaks tier-based routing.

## Proposed Action
Create script: brain/shared-context/fix_skill_tiers.py — auto-assign tier based on category+dept

## Effort / Impact
- Effort: 2h
- Impact: HIGH — enables tier-based agent boot optimization

## Status
[ ] Awaiting CEO decision

---
_Corp Proposal #PROP_2026-03-22_SKILL_TIER_BATCH · 2026-03-22_


## CEO DECISION
- Status: APPROVED
- Date: 2026-03-25T10:27:41
- Notes: APPROVED — P2: fix_skill_tiers.py ready, run with --write to apply

