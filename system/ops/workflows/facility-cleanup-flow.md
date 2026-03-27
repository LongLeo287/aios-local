---
description: Workflow for Dept 22 (facility-agent) to autonomously sweep, compress, and delete AI OS artifact bloat, temporary logs, and orphaned repositories.
---

# Facility Cleanup Flow (Dept 22)

This workflow is executed by the `facility-agent` to ensure that AI OS does not succumb to file bloat caused by AI generation outputs and repository clone failures.

## Step 1: Execute Deep Cleaner Script
The core garbage collection logic is written in a Python maintenance script. You are authorized to run this script to scan for empty repositories, old logs, and orphaned markdown files.

```bash
python system/ops/scripts/aios_deep_cleaner.py --auto-delete --stale-days 14
```

### Script Targets:
1. `brain/knowledge/repos/*`: Scans for completely empty folders or failed clone states (missing `.git`) and deletes them immediately.
2. `system/security/QUARANTINE/`: Deletes `.log`, `.md`, `.txt` outputs that are older than 14 days.
3. `storage/vault/DATA/`: Deletes un-archived artifacts older than 14 days.
4. `$env:USERPROFILE\.gemini` (if accessible): Sweeps legacy AI generation trails.

## Step 2: Report Results
Review the console output of the cleaning script.
If the script recovered more than 50MB of space or deleted ghost repositories, generate a brief operations receipt (`system/telemetry/receipts/CLEANUP_<date>.md`).

## Step 3: Escalate Anomalies
If the scan encounters permission denied errors on massive folders (e.g. locked database indices), do not force delete. Report anomalies to the CEO in the Daily Brief.
