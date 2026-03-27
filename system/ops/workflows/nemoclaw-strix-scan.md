---
description: NemoClaw automated Strix security scan pipeline for AI OS Corp plugins
---

# NemoClaw Strix Automation Workflow

## Purpose

Automate the Strix v2.0 security vetting process using NVIDIA NemoClaw as the agentic runtime. Replaces manual per-repo Strix scanning.

---

## Prerequisites

- NemoClaw ingested in EXTERNAL_SKILL_SOURCES.yaml âœ…
- GATE_SECURITY protocol defined (security_grc.md) âœ…
- strix-agent available in agent roster âœ…

---

## Step 1: Trigger Conditions

This pipeline triggers when:
1. A new repo is added to `EXTERNAL_SKILL_SOURCES.yaml` (status: pending)
2. Manual request from Security dept head
3. Session boot scan (via `antigravity-boot.md`)

---

## Step 2: Collect Scan Targets

```python
# Auto-collect from EXTERNAL_SKILL_SOURCES.yaml
import yaml

with open("shared-context/EXTERNAL_SKILL_SOURCES.yaml") as f:
    sources = yaml.safe_load(f)

pending = [s for s in sources if s.get("status") == "pending"]
# Also scan any with status: trusted but no scan_score recorded
unscanned = [s for s in sources if not s.get("scan_score")]
```

---

## Step 3: Strix Score Matrix

For each repo, NemoClaw evaluates:

| Criterion | Weight | Pass Threshold |
|-----------|--------|---------------|
| License clarity | 20 | MIT/Apache2 = 20, GPL = 10, None = 0 |
| Network access | 15 | Declared + controlled = 15, Undeclared = 0 |
| Code provenance | 20 | Known org (NVIDIA, Microsoft) = 20, Unknown = 5 |
| README/docs quality | 15 | Complete = 15, Minimal = 7 |
| Dependency hygiene | 15 | <10 deps or all known = 15 |
| Data handling | 15 | No PII, stateless = 15 |

**Minimum passing score: 60/100**

---

## Step 4: NemoClaw Execution

```bash
# NemoClaw runs as sandboxed agent â€” policy-based execution
nemoclaw run strix-scan \
  --repo-url $REPO_URL \
  --policy security/strix_policy.yaml \
  --output telemetry/qa_receipts/gate_security/$SCAN_ID.json
```

**Output schema:**
```json
{
  "repo_url": "https://github.com/...",
  "scan_id": "STRIX-2026-03-20-001",
  "score": 94,
  "decision": "PASS|CONDITIONAL|BLOCK",
  "criteria": {...},
  "timestamp": "2026-03-20T11:00:00+07:00",
  "agent": "strix-agent (NemoClaw runtime)"
}
```

---

## Step 5: Decision Routing

```
score >= 80: APPROVED â†’ update EXTERNAL_SKILL_SOURCES.yaml status: trusted
score 60-79: CONDITIONAL â†’ flag for manual review, status: conditional
score < 60:  BLOCK â†’ status: quarantined, write to corp/quarantine/
```

---

## Step 6: Batch Scan Report

After scanning all targets, generate summary report:

```markdown
# Strix Batch Scan Report â€” [DATE]
| Repo | Score | Decision |
|------|-------|----------|
| ... | ... | ... |
```

Write to: `telemetry/qa_receipts/gate_security/batch_report_[DATE].md`

---

## Step 7: Update SKILL_REGISTRY

```yaml
# After APPROVED decision, update entry:
- id: [repo-id]
  status: trusted
  strix_score: [score]
  strix_date: [date]
```

---

## Cycle 4 Batch Scan Targets

107 repos in corpus â€” priority order:
1. Any `status: pending` first
2. Repos without `scan_score` field
3. Oldest entries (ingested earliest)

**Estimated time:** ~2-3 min per repo with NemoClaw autorun = ~3-4 hours for full corpus

**Recommendation:** Run as background agent task during off-hours.

---

*Maintained by: Security GRC | Last updated: 2026-03-20 (Cycle 4)*

---

## Trivy Integration — Added 2026-03-23

Trivy is now the PRIMARY vulnerability scanner trong strix-scan pipeline.
Runs BEFORE NemoClaw to pre-filter repos.

### Trivy Pre-Scan (Step 0 — added before Step 1)
`ash
# Quick trivy pre-scan on repo URL
trivy repo  \
  --format json \
  --scanners vuln,secret,misconfig \
  --severity HIGH,CRITICAL \
  --output telemetry/qa_receipts/gate_security/trivy_prescan_.json \
  --quiet

# Exit code 1 = CRITICAL found ? auto BLOCK, skip NemoClaw
trivy repo  --exit-code 1 --severity CRITICAL --quiet
if (0 -eq 1) { Write-Host "BLOCK: Critical CVE found by Trivy"; exit 1 }
`

### Trivy Score Contribution to Strix Matrix
| Trivy Finding | Strix Deduction |
|--------------|----------------|
| CRITICAL CVE | -30 pts (likely BLOCK) |
| HIGH CVE | -15 pts |
| Secrets exposed | -40 pts (auto BLOCK) |
| Misconfigs | -10 pts |
| Clean | 0 pts |

Skill reference: skills/trivy/SKILL.md
Source: aquasecurity/trivy | Apache 2.0 | 521 contributors
