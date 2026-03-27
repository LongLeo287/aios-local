# Department: operations
---
description: Standard Operating Procedure for delegating tasks from Architect (Antigravity) to Executor (Claude Code). It defines the end-to-end lifecycle of a task from research to final reporting.
---

# 📋 Antigravity-to-Claude Delegation SOP

## Description
Standard Operating Procedure for delegating tasks from Architect (Antigravity) to Executor (Claude Code). It defines the end-to-end lifecycle of a task from research to final reporting.

## 🔄 Operational Cycle

1. **Research:** Antigravity analyzes links, images, and files in Vietnamese.
2. **Planning:** Brainstorming and Planning conducted in **<!--LANG-->Vietnamese<!--/LANG-->**. Technical plan files written in **<!--LANG-->Vietnamese<!--/LANG-->**.
3. **Decomposition & Anchoring:** Create [task.md](../tasks/task.md) (in English). 
   - **MANDATORY:** All relevant Rules, Skills, and Plugins **MUST** be linked in `task.md` for context anchoring.
4. **Automated Handoff (NEW):** 
   - Antigravity **MUST NOT** ask the user to manually run Claude Code.
   - Antigravity automatically uses the terminal to execute Claude Code CLI using the exact command defined in `workflows/automated_cli_handoff.md`.
5. **Execution:** Claude reads `task.md` in the background, including all linked resources, and auto-executes the plan.
6. **Organization:** Archivist sub-agent cleans up logs and indexes results.
7. **Verification & Reporting:**
   - **MANDATORY:** Claude generates a technical `report.md` in `tasks/reports/` upon completion.
   - Antigravity monitors the terminal, auto-detects completion, reads the report, and sends the final summary to the user in **<!--LANG-->Vietnamese<!--/LANG-->** as a UI Artifact (`.resolved`).

## 🚥 Control Points

- Project must be in a clean Git state or have a Snapshot before delegation.
- Archivist must ensure the library is searchable and updated after every major task.
