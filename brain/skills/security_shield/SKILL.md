---
id: security_shield
name: Security Shield
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Defensive security auditing, vulnerability scanning and auto-remediation.

accessible_by:
  - QA
  - DevOps

dependencies:
  - reasoning_engine

exposed_functions:
  - name: vulnerability_scan
  - name: auto_remediate
  - name: compliance_check
  - name: threat_model

consumed_by: []
emits_events:
  - vulnerability_found
  - compliance_passed
listens_to: []
---
# ðŸ›¡ï¸ Security Shield Skill (Strix Protocol)

## Description
This skill provides the AI OS with "Hacker Instincts" â€” pre-clone repo vetting, vulnerability scanning, and auto-remediation. Protects the ecosystem from supply chain attacks, malware, and data exfiltration.

## ðŸ› ï¸ Core Functions

1. **Pre-Clone Vetting (/vet-repo):** â† NEW
   - Run `vet_repo.ps1` on a quarantined repo BEFORE any content enters AI OS.
   - Scans: git hooks, npm postinstall scripts, network calls, sensitive data access, obfuscation, hardcoded secrets, suspicious binaries.
   - Generates `_VET_REPORT.md` with PASS / WARN / FAIL verdict.
   - Usage: `.\vet_repo.ps1 -RepoPath "D:\APP\QUARANTINE\repo-name" -Verbose`

2. **Vulnerability Scan (/scan):**
   - Static analysis on existing AI OS code and any newly added files.
   - Search for: Hardcoded secrets, insecure API usage, open permissions, injection points.

3. **Proof-of-Impact (/exploit-test):**
   - Safe, sandboxed tests to verify if a suspected vulnerability is real.

4. **Auto-Remediation (/secure-patch):**
   - Propose and apply security patches automatically.

## ðŸ“‹ Standard Operating Procedure

### For External Repos (MANDATORY)
1. Clone into `D:\APP\QUARANTINE\<repo-name>` with `--depth=1`
2. Delete `.git\hooks\` non-.sample files
3. Run `/vet-repo` â†’ wait for PASS
4. Extract ONLY needed files into AI OS
5. Run `/scan` on newly added files
6. Delete QUARANTINE folder

See full protocol: `D:\APP\AI OS\rules\clone_security_protocol.md`

### For Code Changes (Before Commit)
1. Run `/scan` on changed files
2. If vulnerabilities found â†’ trigger `/secure-patch`
3. Document "Security Receipt" in task telemetry

## ðŸ“š Knowledge Base
- Protocol: [clone_security_protocol.md](../rules/clone_security_protocol.md)
- Knowledge: [repo_vetting_knowledge.md](../knowledge/repo_vetting_knowledge.md)
- Script: [vet_repo.ps1](./vet_repo.ps1)

## Principle
*"Trust no external input. Verify before you ingest."*

