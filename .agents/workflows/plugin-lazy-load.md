---
description: How agents select and trigger Tier 2 Plugins via Lazy-Load Protocol
---
# 3-Tier Plugin Protocol (Lazy-Load Workflow)

When an Agent needs to use an external tool from the `plugins/` directory, it MUST follow this workflow.

## Step 1: Tool Tier Verification
1. Read `shared-context/SKILL_REGISTRY.json`
2. Identify the tool's tier.
   - If **Tier 1 (Core Infra)**: Proceed using standard REST API (Mem0, Firecrawl, CrewAI, etc.).
   - If **Tier 3 (Blacklisted/Conflict)**: Abort immediately and escalate.
   - If **Tier 2 (Specialized/Lazy-Load)**: Proceed to Step 2.

## Step 2: Sandbox Initialization (Lazy-Load)
Do NOT install Tier 2 dependencies globally or mix them with AI OS core. Use a temporary sandbox.
Run the following initialization commands:
// turbo
```powershell
Write-Host "[LAZY-LOAD] Initializing Sandbox..."
New-Item -ItemType Directory -Force -Path "_temp_sandbox" | Out-Null
cd _temp_sandbox
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Step 3: Tool Execution
Install the specific Tier 2 tool dependencies and execute the required task within the sandbox.
```powershell
# Example standard execution:
# pip install -r ../plugins/<tool-dir>/requirements.txt
# python ../plugins/<tool-dir>/run.py > output.json
```
Ensure output is written to `telemetry/receipts/` or parsed back directly to the Agent.

## Step 4: Teardown & Cleanup
Once the task is complete, the sandbox MUST be destroyed to prevent System Bloatware.
// turbo
```powershell
Write-Host "[LAZY-LOAD] Tearing down Sandbox..."
deactivate
cd ..
Remove-Item -Recurse -Force _temp_sandbox
```

## Step 5: Mission Logging (Handoff)
Log the usage of the Tier 2 tool to `shared-context/blackboard.json` adhering to the system rules format.
```json
{
  "handoff_trigger": "COMPLETE",
  "target_agent": "Antigravity",
  "completed_by": "[Current Agent Name]",
  "summary": "Successfully lazy-loaded and executed Tier 2 tool",
  "files_modified": [],
  "outcome": "SUCCESS",
  "notes": "Sandbox was properly destroyed."
}
```
