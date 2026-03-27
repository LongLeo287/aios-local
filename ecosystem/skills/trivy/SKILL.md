---
name: trivy-security-scan
description: Run Trivy vulnerability scanner on containers, code repos, Kubernetes configs, and IaC files. Use whenever evaluating a new repo, container image, or infra config for security issues.
---

# Trivy Security Scanner — Dept 10 (Security GRC)

## When to Use
- Before integrating any new plugin or container into AI OS
- Scanning code repos for secrets, CVEs, misconfigurations
- Part of GATE_SECURITY in strix-scan pipeline

## Installation Check
```bash
trivy --version
# If not installed:
# Windows: winget install aquasecurity.trivy
# Or: choco install trivy
# Or download from: https://github.com/aquasecurity/trivy/releases
```

## Core Commands

### Scan a GitHub Repo (before cloning)
```bash
trivy repo https://github.com/owner/repo --scanners vuln,secret,misconfig
```

### Scan Local Directory
```bash
trivy fs . --scanners vuln,secret,misconfig --severity HIGH,CRITICAL
```

### Scan Container Image
```bash
trivy image python:3.12-slim
trivy image --severity CRITICAL,HIGH nginx:latest
```

### Scan Kubernetes Config
```bash
trivy config ./k8s/
```

### Generate JSON Report (for strix-scan pipeline)
```bash
trivy repo $REPO_URL \
  --format json \
  --output telemetry/qa_receipts/gate_security/trivy_$(date +%Y%m%d_%H%M%S).json \
  --scanners vuln,secret,misconfig \
  --severity HIGH,CRITICAL
```

### Quick Pass/Fail (exit code 1 if CRITICAL found)
```bash
trivy repo $REPO_URL --exit-code 1 --severity CRITICAL --quiet
```

## Strix Score Mapping
| Trivy Result | Strix Impact |
|-------------|--------------|
| CRITICAL CVEs | −30 pts |
| HIGH CVEs | −15 pts |
| Secrets found | −40 pts (BLOCK) |
| Misconfigs | −10 pts |
| Clean scan | +0 (no deduction) |

## Integration with Strix Pipeline
```python
import subprocess, json

def trivy_scan(repo_url: str) -> dict:
    result = subprocess.run(
        ["npx", "trivy", "repo", repo_url,
         "--format", "json", "--scanners", "vuln,secret,misconfig",
         "--severity", "HIGH,CRITICAL", "--quiet"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else {}
```

## Output Storage
All Trivy reports → `telemetry/qa_receipts/gate_security/`
Summary → `telemetry/qa_receipts/gate_security/batch_report_YYYY-MM-DD.md`

## Notes
- License: Apache 2.0 | 521 contributors | 85 releases
- Source: github.com/aquasecurity/trivy
- Owner: Dept 10 (Security GRC) — run before ANY Tier 2 plugin deploy
