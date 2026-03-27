# Department: operations
---
description: Standard Operating Procedure (SOP) for new feature implementation
---

# Agent Workflow: Standard Task Execution

## Description
A technical workflow for AI agents, detailing the iterative cycle of preparation, implementation planning, execution, and verification within the AI OS ecosystem.

When assigned a complex task regarding the extension, follow these steps strictly:

### 1. Preparation & Context Mapping
- Verify you are operating within the `.agents` workspace.
- Review `.agents/docs/` and `.agents/rules/global_rules.md`.
- Ensure you have checked `.agents/docs/github_capabilities_registry.md` if the task requires new capabilities.

### 2. Planning Phase
- **Always** generate an `implementation_plan.md` using `write_to_file`.
- Group changes logically and ask the user for approval via `notify_user` with `BlockedOnUser: true`.

### 3. Execution Phase
- For UI Code: Load `.agents/plugins/ui-ux-pro-max/` parameters if adjusting design systems.
- Execute changes securely, using `replace_file_content` targeting the specific codebase (e.g., `extension/src/...`).

### 4. Verification & Validation
- Run linting or automated tests if available.
- Finalize the task by writing to `walkthrough.md` documenting the exact changes.
- Call `notify_user` to signal completion.
