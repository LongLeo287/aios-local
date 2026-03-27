# ðŸ¤– Agent Behavior & Responsibility Rules

## Description
A comprehensive rule set governing agent autonomy, resource awareness (SFUA loop), progress tracking, and Vietnamese-centric reporting standards for the project.

## 0. ðŸ§  Phase 11: Advanced Cognitive protocols (MANDATORY)

Agents operate under the **Cognitive Evolution** standard:

1.  **XML GROUNDING:** All instructions, task outputs, and decision-making logs **MUST** be bounded by XML tags (e.g., `<thought>`, `<plan>`, `<rules>`, `<fact>`). Non-compliant outputs are rejected.
2.  **MODE AWARENESS:** Agent must explicitly state its current mode in every report:

    ### `[PLANNING]` Mode
    - **Entry:** New task received, phase transition, or strategy reset.
    - **Activities:** Task decomposition (MECE), dependency mapping, resource verification, risk assessment.
    - **Output:** Structured `<plan>` with ordered steps, expected outcomes, and fallback paths.
    - **Exit:** Plan approved (self or HITL) and all dependencies verified.

    ### `[EXECUTION]` Mode
    - **Entry:** Approved plan exists, resources confirmed available.
    - **Activities:** Tool calls, code changes, file operations, test runs.
    - **Output:** Task receipts with status, artifacts produced, and blockers encountered.
    - **Exit:** All plan steps completed, or CIRCUIT BREAKER triggered (2 failures).

    ### `[REFLECTION]` Mode
    - **Entry:** Task completed (success or failure), phase boundary, or explicit trigger.
    - **Activities:** Outcome vs. plan comparison, fact extraction, lesson documentation, knowledge update.
    - **Output:** Reflection report with lessons learned, facts extracted to `memory/daily/`, knowledge updates.
    - **Exit:** Reflection documented, knowledge/ updated, next task identified.

    **Mode Transition Rules:**
    - `[PLANNING]` â†’ `[EXECUTION]`: Only after plan validation.
    - `[EXECUTION]` â†’ `[REFLECTION]`: Automatic on task completion or failure.
    - `[REFLECTION]` â†’ `[PLANNING]`: When next task is identified.
    - Emergency: Any mode â†’ `[PLANNING]` on CIRCUIT BREAKER activation.

3.  **SELF-DIAGNOSTICS:** Before calling a tool, the Agent must perform a "Dry Run" reasoning step within `<thought>` tags to predict success/failure and identify side effects.
4.  **HUMAN-IN-THE-LOOP (HITL) â€” Advanced Safety:**
    - **Tier 1 (Auto-Approve):** Read operations, search, local file edits within `.agents/`.
    - **Tier 2 (Dry-Run Required):** Code modifications, dependency changes â€” agent must output `<thought>` dry-run before execution.
    - **Tier 3 (User Confirmation):** File deletion, schema changes, deployment, git operations beyond local commits.
    - **Tier 4 (Simulated Dry-Run):** Infrastructure changes, external API calls â€” agent must simulate the full operation in `<thought>` tags, present expected outcomes, and wait for explicit approval.

---

## 1. Resource Awareness & Context Hub Protocol (SFUA)

Agents must move from "Static Prompting" to "Context Engineering" using the **SFUA Loop**:

1. **ðŸ” SEARCH**: At the start of any task, perform a **HYBRID SEARCH** (Keyword + Semantic) across `.agents/knowledge/`, `.agents/docs/`, and `.agents/memory/`. Do NOT rely on training data for internal project details.
2. **ðŸ“¥ FETCH**: Retrieve the full content of relevant skill manifests (`SKILL.md`), plans, or rules. Ensure you have the "Ground Truth" before planning execution.
3. **âš¡ USE**: Execute the task as per the [Strategy](../plans/implementation_plan.md).
4. **ðŸ“ ANNOTATE**: Use the [Smart Memory Skill](../skills/smart_memory/SKILL.md) to extract **Facts** (not logs). Update the `walkthrough_active.md` and annotate high-density lessons in `.agents/memory/daily/`.
5. **ðŸ”— CROSS-SESSION CONTINUITY**: When starting a new session or encountering an unknown context, you **MUST** review the `archive/` and previous `tasks/reports/` to ensure long-term continuity. Never start from zero.
6. **âš“ RE-ANCHOR**: At every phase transition, you **MUST** re-read `THESIS.md`, `.agents/tasks/task.md`, and **[ORCHESTRATION_SOP.md](ORCHESTRATION_SOP.md)**.
    - **RE-ANCHOR:** Every 30 minutes, re-read `CLAUDE.md`, `THESIS.md`, and the new **[SOUL.md](SOUL.md)**, **[AGENTS.md](AGENTS.md)**, **[WORKFLOW.md](WORKFLOW.md)**, **[ORCHESTRATION_SOP.md](ORCHESTRATION_SOP.md)**, and **[blackboard.json](../shared-context/blackboard.json)** to ensure behavioral alignment.
- **FRESHNESS:** Prioritize reading the latest files over cached knowledge.
- **REACT-GRAB ANCHOR:** For UI fixes, fetch the exact DOM fragment and source file first.
6. **â„ï¸ FRESHNESS**: Data about Live Build status, Git state, or current errors is "Volatile". You **MUST** run fresh search/status tools before acting on volatile data.
7. **ðŸ§  REFLECT**: After any major task completion, review the **Task Receipt** and trigger the [Cognitive Reflector](/reflect). Document the lesson learned in `.agents/docs/lessons_learned.md`.

- Agent **MUST** read `project_map.md` first when starting a session.
- If a task requires security, Agent **MUST** automatically apply `link_safety_rules.md`.
- If a task relates to UI, Agent **MUST** reference all UI-related plans in `archive/` if needed for context.

## 2. Progress Tracking

- **Task Update:** When completing a sub-task, Agent must update the `[x]` status in `.agents/tasks/task.md`.
- **New Task Detection:** If a new issue (Bug) or user request is detected, Agent must automatically add it to `Backlog` or `To-Do`.

## 3. Reporting & Brainstorming Standards (MANDATORY)

After finishing any assigned task or starting a brainstorm, the Agent **MUST** adhere to the **Visual-First Protocol**:

1.  **Visual Elements:** Use **Mermaid Mindmaps** for architecture/overview and **Carousel Slides** for comparing options or step-by-step progress.
2.  **Language:** Brainstorming, high-level reports for the USER, and `.resolved` output files **MUST** be in **<!--LANG-->Vietnamese<!--/LANG-->**. Technical docs remain in English.
3.  **NO AI IMAGES:** Do NOT generate images unless explicitly requested by the USER.
4.  **File Naming:** `REPORT_[TaskName]_[AgentID]`
5.  **Storage:** Brainstorms and Reports (the `.resolved` format) MUST be saved in the Agent's Native Artifact System (`C:\Users\%USERNAME%\.gemini\antigravity`) to support Rich UI rendering. All technical files, however, MUST remain in the local project directory.
6.  **Log & Document Aggregation (Archivist Rule):** All scattered `.md`, `.log`, and `.doc` files generated during execution must be stored in a dedicated folder (e.g., `.agents/archive/logs/`). When the file count grows, the Agent/Archivist MUST aggregate them into a single master summary file and delete the old scattered files to prevent clutter.

## 4. Resilience & Performance Rules

- **CIRCUIT BREAKER:** If a tool fails 2 times, you **MUST** stop and re-evaluate strategy. Do not enter an infinite loop.
- **PARALLELISM:** Proactively use parallel tool calls for independent file operations or searches to optimize runtime.
- **ADAPTIVE PATCHING:** If you find a rule in `agent_behavior.md` is causing repeated confusion, propose a "Patch" in `.agents/prompts/adaptive_patches/`.
- **GIT SAFETY:** Never `force-push`. Always verify changes with `git status` after execution.

## 5. Boundary & Cognitive Management

- **DO NOT** create metadata, logs, or plan files outside the `.agents/` directory.
- **ALWAYS** use absolute paths when manipulating system files.
- **REASONING PHASE:** Mandatory for architectural decisions or error recovery.
- **BIAS CHECK:** Scanning for the 12 cognitive biases (see `cognitive_biases.md`) is mandatory during planning.

