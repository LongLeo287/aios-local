---
name: continuous-learning-v2
description: Structured self-improvement loop for AI agents. Captures lessons learned, identifies gaps, updates knowledge base, and evolves agent behavior over sessions.
---

# Continuous Learning v2 — Agent Self-Improvement Loop

## What it Does
Cherry-picked from `everything-claude-code` (affaan-m/everything-claude-code v1.8.0)
Structured loop for agents to learn from each session and improve over time.

## When to Use
- At end of each major task or session (post-session.md)
- When agent makes a mistake — capture lesson immediately
- Weekly retrospec cycle (corp-learning-loop.md)
- When discovering new patterns or better approaches

## The Learning Loop

### Step 1: Capture (During / After Task)
```
- What worked well?
- What failed or was suboptimal?
- What would I do differently?
- New pattern discovered?
```

### Step 2: Classify
```
LESSON_LEARNED    → Single session insight
PATTERN_UPDATE    → Recurring pattern worth codifying
RULE_CANDIDATE    → Should become a hard rule in GEMINI.md/CLAUDE.md
KNOWLEDGE_GAP     → Something I didn't know, now I do — write KI Note
```

### Step 3: Write
```bash
# Lesson → decisions_log.md
# Pattern → brain/knowledge/notes/KI-PATTERN-XX.md  
# Rule → Propose to CEO, then add to GEMINI.md
# KI Note → brain/knowledge/notes/KI-[TOPIC]-XX.md
```

### Step 4: Verify (Next Session)
```
- Was the lesson applied?
- Did the pattern hold?
- Is the rule working?
→ If yes: mark VALIDATED
→ If no: iterate
```

## Integration with AI OS Workflows
- `ops/workflows/post-session.md` — triggers this loop at session end
- `ops/workflows/corp-learning-loop.md` — weekly aggregate
- `brain/shared-context/corp/decisions_log.md` — permanent store

## Template: Lesson Entry
```markdown
## LESSON_[DATE]_[ID]
**Session:** Cycle X
**Context:** [What was happening]
**Issue:** [What went wrong or was suboptimal]
**Root Cause:** [Why]
**Fix Applied:** [What I changed]
**Status:** VALIDATED | PENDING | RECURRING
```

## Notes
- Source: github.com/affaan-m/everything-claude-code v1.8.0 (cherry-pick)
- This is a cognitive skill, not a tool — no CLI needed
- Already integrated with AI OS post-session workflow
- Owner: All agents — apply universally
