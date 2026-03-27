# CI/CD Pipeline: Intake
# Trigger: CIV STEP 3A (repo received) | Owner: content_intake
# Purpose: Auto-check integrity before vet_repo.ps1 runs

## Steps

- [ ] Step 1: Verify QUARANTINE path exists
      Check: security/QUARANTINE/incoming/<type>/ present
- [ ] Step 2: Run gitingest summary
      Command: gitingest <repo_path> --output _DIGEST.md
- [ ] Step 3: File count + size check
      Reject if: >50MB or >10,000 files (flag for manual review)
- [ ] Step 4: Quick secret scan (pre-scan)
      Pattern match: API keys, tokens, passwords in README
- [ ] Step 5: Trigger vet_repo.ps1
      Command: powershell security/QUARANTINE/vet_repo.ps1 -RepoPath <path>
- [ ] Step 6: Write receipt
      File: telemetry/receipts/content_intake/INTAKE_<id>_<ts>.json

## On Failure
- Write: security/QUARANTINE/rejected/<id>_REASON.md
- Notify: notification-bridge (SECURITY_ALERT or CIV_REJECTED)
