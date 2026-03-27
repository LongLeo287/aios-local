# LEARNING_CYCLE_PROTOCOL.md — AI OS Self-Improvement Loop
# Version: 1.0 | Updated: 2026-03-14
# Authority: Tier 2 (Operations)
# Adapted from: LongLeo learning-agent.md (weekly cycle concept)
# Executed by: cognitive_evolver + cognitive_reflector skills

---

## Purpose

The learning cycle ensures AI OS improves its skill library over time.
Instead of static skills, the system analyzes its own performance and
proposes new skills when it encounters repeated patterns.

---

## When to Run

Run on ANY of these triggers (not fixed schedule):
- After completing 5+ tasks in a project  
- When `cognitive_reflector` identifies a repeated gap in skills
- When user explicitly requests: "review what we've learned"
- End of major project phase

---

## The 5-Step Learning Cycle

### Step 1: Load Session Evidence
```
Source: telemetry/receipts/ (filter by last N tasks)
Extract:
  - Steps that had FAIL or PARTIAL status
  - Steps where RESEARCHER role was needed (= skill gap)
  - Steps where same action was repeated > 3 times
  - BLOCKED states and their failure reasons
```

### Step 2: Pattern Analysis
```
For each extracted pattern:
  Q1: Is this a general pattern or project-specific?
       General → candidate for core skill
       Specific → candidate for domain skill

  Q2: Has this been solved before?
       Check SKILL_REGISTRY.json for existing related skills
       If exists: consider updating existing skill (not creating new)

  Q3: Would a skill file solve this?
       Skill = a set of instructions an agent can follow
       If the solution is "call an API" or "write code" → it's a skill
       If the solution is "redesign the system" → it's a plan, not a skill
```

### Step 3: Propose New Skills
```
For each validated candidate, create a proposal in skills/experimental/:

File: skills/experimental/PROPOSAL_<skill_name>_<date>.md
Format:
  ---
  status: PROPOSAL
  proposed_by: cognitive_evolver
  proposed_at: ISO 8601
  evidence: [receipt IDs that triggered this]
  problem_statement: [what gap does this fill?]
  domain: core | google-workspace | databases | finance | pos | frontend | ...
  ---

  # Skill Proposal: [Name]
  ## Problem it solves
  ## Proposed approach
  ## Example usage
  ## Risk if not created
```

### Step 4: Review and Promote
```
Antigravity presents proposals to user:
  "Tôi đề xuất [N] skill mới dựa trên phân tích [X] task gần đây.
   Bạn muốn review không?"

For each proposal:
  User APPROVE → Convert to full SKILL.md with frontmatter
                 → Move to skills/core/ or skills/domains/<domain>/
                 → Run skill_loader.ps1

  User REJECT  → Archive to skills/experimental/rejected/
                 → Note reason in cognitive_evolver memory

  User MODIFY  → Update proposal, return to Step 3
```

### Step 5: Update and Report
```
After promotions:
  Run: skill_loader.ps1                    [rebuild registry]
  Update: shared-context/SKILL_REGISTRY.json
  Write: cosmic_memory entry for this cycle
  Report to user (Vietnamese):
    "✅ Chu kỳ học tập hoàn thành.
     - Phân tích: [N] tasks
     - Đề xuất: [M] skills mới
     - Đã duyệt: [X] skills → promoted
     - Registry: [total] skills active"
```

---

## Cost Optimization via Learning

Track token usage patterns across tasks:
```
Patterns to identify:
  - Which skill reduces tokens when loaded? → Promote to eager (Tier 1)
  - Which skill is rarely used? → Demote to manual (Tier 3)
  - Which RESEARCHER queries are repeated? → Create a skill from the answer

Goal: Reduce average tokens per task by 15% per quarter
```

---

## Learning Cycle Output Files

```
skills/experimental/
├── PROPOSAL_<name>_<date>.md    ← new proposals
└── rejected/
    └── REJECTED_<name>_<date>.md

telemetry/
└── learning_report_<date>.json  ← cycle summary
```

---

*"Every failure is a skill not yet written. Every repeated action is a skill waiting to exist."*
