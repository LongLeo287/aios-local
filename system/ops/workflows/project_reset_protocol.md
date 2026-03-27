# Department: operations
---
description: Standard Operating Procedure for archiving an old project and initializing a new one within the same AI OS instance. (Updated and Validated)
---

# 🔄 Project Reset & Archiving Protocol

## Objective
When the User commands to "Start a new project" or "Reset project", Antigravity (Architect) must automatically gather all data from the old project, package it into a ZIP archive for the User to persist, and clear the workspace to start the new project **WITHOUT damaging the Core Library (Rules, Skills, Workflows)**.

## Step 1: Data Classification (Engine vs Cargo)

The system rigidly separates 2 types of data:
*   **Core Library (Engine - KEEP UNTOUCHED):** `rules/`, `skills/`, `workflows/`, `CLAUDE.md`. This is the brain of the AI OS, shared across all projects.
*   **Old Project Data (Cargo - MUST ARCHIVE & WIPE):** All files located within `knowledge/`, `plans/`, `tasks/`, `archive/` (including the `media/` subfolder).

## Step 2: Automated Archiving (Zip & Save)

Antigravity **MUST** automatically execute a PowerShell script to compress all "Cargo" into a single ZIP file named after the Old Project (e.g., `OldProjectName_Archive.zip`) and save it outside the `.agents` directory (e.g., the project root folder).

Sample Script (PowerShell):
```powershell
$projectDir = "d:\APP\BookMark Extension\.agents"
$stagingDir = "d:\APP\Temp_Project_Archive"
$zipPath = "d:\APP\OldProject_Archive.zip"

# Copy Cargo to Staging
New-Item -ItemType Directory -Force -Path $stagingDir
Copy-Item "$projectDir\knowledge", "$projectDir\plans", "$projectDir\tasks", "$projectDir\archive" -Destination $stagingDir -Recurse -Force

# Compress and Cleanup Staging
Compress-Archive -Path "$stagingDir\*" -DestinationPath $zipPath -Force
Remove-Item -Path $stagingDir -Recurse -Force
```

## Step 3: Clean & Boot (Zero-Context Initialization)

1.  **Wipe Old Cargo:** Delete all contents within `knowledge/`, `plans/`, `tasks/`, `archive/` (keeping the empty directory structures intact).
2.  **Initialize New Anchors:** Create 2 essential starting files for the new project:
    *   `tasks/task.md` (An empty checklist with Anchoring links to `AGENTS.md` and `agent_behavior.md`).
    *   `knowledge/knowledge_index.md` (An empty index file linking back to The Rules).
3.  **UI Reporting:** Send a notification to the User (in Vietnamese) stating that "Packaging is complete, the ZIP file location, and the AI is ready to receive the new project objective."
