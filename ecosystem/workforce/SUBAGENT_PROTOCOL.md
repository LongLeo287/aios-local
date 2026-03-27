# SUBAGENT_PROTOCOL.md -- AI OS Sub-Agent Operating Standard
# Version: 1.1 | Updated: 2026-03-17
# Authority: Tier 2 (Operations) | Allocation Map: corp/sops/RESOURCE_ALLOCATION_MAP.md
# Read by: Any agent operating as Developer, QA, or Researcher under Claude Code

---

## Department Assignment Map (v1.1)

> All 38 subagents assigned to owning departments. Call via on-demand activation.
> Full details: `corp/sops/RESOURCE_ALLOCATION_MAP.md` Section 2.

| Dept | Assigned Subagents |
|------|-------------------|
| **engineering** | `rapid-prototyper`, `code-reviewer`, `api-tester`, `devops-ops`, `git-workflow-master`, `mcp-builder`, `database-optimizer`, `ux-designer` |
| **qa_testing** | `performance-benchmarker`, `security-auditor`, `compliance-auditor` |
| **security_grc** | `incident-response-commander` |
| **marketing** | `growth-hacker`, `social-media-strategist`, `paid-media-specialist`, `image-prompt-engineer`, `sales-engineer`, `developer-advocate` |
| **support** | `support-analyst` |
| **content_review** | `doc-writer`, `brand-guardian` |
| **strategy** | `data-analyst`, `researcher`, `product-feedback-analyst` |
| **rd** | `scientific-researcher`, `academic-researcher`, `narrative-designer`, `blockchain-engineer`, `godot-engineer`, `roblox-developer`, `unity-engineer`, `unreal-engineer`, `xr-developer` |
| **hr_people** | `cultural-intelligence-analyst`, `chief-of-staff` |
| **od_learning** | `prompt-engineer` |
| **planning_pmo** | `project-shepherd` |
| **operations** | `mq` |

> **Note:** Subagents are on-demand blueprints, NOT persistent agents. Any dept may request a subagent via `od_learning` if not assigned.

---

## What Is a Sub-Agent?

A sub-agent is Claude Code operating in a **specific role** for a **specific step**.
Each step in task.md is executed by exactly ONE role at a time.

Sub-agents are NOT separate processes. They are **mental modes** that Claude Code
switches between explicitly, with a clear activation statement and role-specific
behavioral rules.

---

## Sub-Agent Startup Protocol (Every Role Switch)

Before beginning work in any role, the agent MUST:

```
1. Declare role activation:
   "[ROLE_NAME] Starting step <N>: <step_description>"

2. Load required skills from SKILL_REGISTRY.json:
   - Query registry for each skill the role needs
   - Verify access via accessible_by field
   - Read SKILL.md for each loaded skill
   - Announce: "Skills loaded: [list]"

3. Read task context:
   - Re-read the specific step in task.md
   - Read any output from the previous role (if handing off)
   - Check blackboard.json for any updates

4. Declare intent (XML grounding):
   <thought>
     Role: [DEVELOPER | QA | RESEARCHER]
     Step: [N of M]
     Intent: [what I will do]
     Input: [what I have to work with]
     Expected output: [what success looks like]
     Risk: [what could go wrong]
   </thought>
```

---

## DEVELOPER Sub-Agent

### Skill Library

Load from registry before starting:
| Skill | Why |
|-------|-----|
| `context_manager` | Token budget awareness |
| `reasoning_engine` | Logical implementation plan |
| `shell_assistant` | Execute commands safely |
| `resilience_engine` | Handle tool failures |

### Work Protocol

```
FOR EACH file to create/modify:

  STEP A -- Read first:
    [DEVELOPER] Reading: <file_path>
    [DEVELOPER] Current state: <brief description>

  STEP B -- Plan in thought:
    <thought>
      Change: [what line(s) will change]
      Reason: [why this change achieves the step goal]
      Rollback: [how to undo if wrong]
    </thought>

  STEP C -- Execute:
    Make the change

  STEP D -- Verify immediately:
    Read the file again
    Confirm the change took effect
    Run any relevant test/lint if applicable

  STEP E -- Write DEV receipt
```

### Developer Output Format (in receipt output_summary)

```
Modified: <file_path>
Change: <1-2 sentence description of what changed>
Verification: <how I confirmed it worked>
Lines changed: <approximate count>
```

---

## QA Sub-Agent

### Skill Library

Load from registry before starting:
| Skill | Why |
|-------|-----|
| `production_qa` | Adversarial review methodology |
| `reasoning_engine` | Logical analysis |
| `diagnostics_engine` | Quality scoring |

### QA Review Protocol

```
FOR EACH DEV output to review:

  1. Read the DEV receipt for this step
  2. Read the modified files
  3. Run the 5-point QA checklist:

     CHECK 1 -- Correctness:
       Does output match step requirement in task.md?
       [PASS / FAIL + reason]

     CHECK 2 -- Regression:
       Does change break any adjacent functionality?
       [PASS / FAIL + what breaks]

     CHECK 3 -- Completeness:
       Are edge cases handled? (null, empty, large input, concurrent)
       [PASS / PARTIAL + what's missing]

     CHECK 4 -- Quality:
       Is the code/file readable? Follows conventions?
       [PASS / FAIL + specifics]

     CHECK 5 -- Compliance:
       Follows SKILL_SPEC, .clauderules, language policy?
       [PASS / FAIL + violation]

  4. Verdict:
     ALL 5 PASS       -> verdict: PASS
     1-2 minor FAIL   -> verdict: PARTIAL (list issues)
     Any major FAIL   -> verdict: FAIL (list issues, return to DEVELOPER)

  5. Write QA receipt
```

### QA Failure Report Format (passed to DEVELOPER for fix)

```
QA ISSUES FOUND -- Step <N>:

Issue 1: [CHECK N] <description>
  Location: <file:line if applicable>
  Fix required: <specific action DEVELOPER must take>

Issue 2: ...

Priority: HIGH / MEDIUM / LOW
Return to: DEVELOPER for fix attempt <X>
```

---

## RESEARCHER Sub-Agent

### Skill Library

Load from registry before starting:
| Skill | Why |
|-------|-----|
| `web_intelligence` | External information gathering |
| `smart_memory` | Check if already known |
| `knowledge_enricher` | Enrich and link findings |

### Research Protocol

```
1. Check smart_memory FIRST:
   -> "Has this been researched before?"
   -> If yes: return cached findings, skip external search

2. Define research question precisely:
   <thought>
     Question: [exact question that blocks progress]
     Scope: [what sources to check]
     Success: [what answer would unblock the developer]
   </thought>

3. Research (in order of preference):
   a. Search existing workspace (skill docs, README files)
   b. Search SKILL_REGISTRY for relevant skills
   c. External search via web_intelligence (if allowed)

4. Synthesize findings:
   - Answer the specific question
   - Recommend concrete approach for DEVELOPER
   - Write to smart_memory for future recall

5. Write RESEARCH receipt + hand off to DEVELOPER
```

---

## Message Queue (MQ) Protocol

When a role needs to pass information to the next role:

```
Write file: subagents/mq/<event>_<step>_<timestamp>.json

Format:
{
  "from_role": "QA",
  "to_role": "DEVELOPER",
  "step_id": "<N>",
  "event": "qa_failed | research_complete | handoff",
  "payload": { ... },
  "timestamp": "<ISO 8601>"
}
```

Receiving role reads MQ on startup:
```powershell
$latest = Get-ChildItem "d:\Project\AI OS\subagents\mq\" |
          Where-Object { $_.Name -match "qa_failed_$stepId" } |
          Sort-Object LastWriteTime -Descending |
          Select-Object -First 1
$msg = Get-Content $latest.FullName | ConvertFrom-Json
```

---

## Receipt Writing (All Roles)

```
Path: <workspace_path>\telemetry\receipts\<ROLE>_<step>_<timestamp>.json

Schema:
{
  "task_id": "...",
  "step_id": "N",
  "step_description": "...",
  "role": "DEVELOPER | QA | RESEARCHER",
  "status": "PASS | FAIL | PARTIAL | BLOCKED",
  "attempt": 1,
  "files_modified": [],
  "output_summary": "English text",
  "issues_found": [],
  "skills_used": [],
  "timestamp": "ISO 8601",
  "next_action": "CONTINUE | RETRY | ESCALATE | BLOCKED"
}
```

**Rules:**
- Write receipt IMMEDIATELY after completing role action
- Never modify a previous receipt (append new attempt with attempt: 2, 3...)
- If workspace has no `telemetry/receipts/` folder: create it first

---

## Context Preservation Between Roles

After each role, update the working context in `<thought>` for the next role:

```xml
<context_handoff>
  Completed role: [ROLE]
  Step: [N]
  Status: [PASS/FAIL]
  Key output: [what was produced]
  Known issues: [anything the next role should know]
  Next role: [ROLE]
  Next role instruction: [specific guidance]
</context_handoff>
```

This ensures no context is lost between role switches even in long sessions.

---

*"Each role is a specialist. The manager ensures specialists talk to each other."*
