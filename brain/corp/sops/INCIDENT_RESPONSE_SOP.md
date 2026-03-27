# INCIDENT_RESPONSE_SOP.md â€” Security Incident Response Playbook
# Version: 1.0 | Updated: 2026-03-17
# Authority: Tier 1 (Security & GRC) / BLOCKING
# Lead: strix-agent / security_grc dept

---

## Overview

This SOP defines the AI OS Corp response to security incidents.
All incidents are managed by security_grc dept.
CRITICAL incidents override all other work priorities.

```
DETECT (strix-agent / continuous)
    â”‚
    v
CLASSIFY severity (CRITICAL / HIGH / MEDIUM / LOW)
    â”‚
    â”œâ”€â”€ CRITICAL â†’ Pause affected systems â†’ Direct L3 to CEO
    â”œâ”€â”€ HIGH     â†’ L2 to COO â†’ response within session
    â”œâ”€â”€ MEDIUM   â†’ L1 within security_grc dept
    â””â”€â”€ LOW      â†’ Log, monitor, no escalation
    â”‚
    v
CONTAIN â†’ INVESTIGATE â†’ REMEDIATE â†’ VERIFY â†’ CLOSE
```

---

## Severity Classification

| Level | Examples | SLA | Who Notified |
|-------|---------|-----|-------------|
| CRITICAL | Prompt injection in production, data exfiltration, admin credential exposure | IMMEDIATE | CEO directly |
| HIGH | New plugin with score 40-59, unauthorized workspace access, suspicious API calls | Same session | COO + strix-agent |
| MEDIUM | License violation found, policy non-compliance | 1-2 cycles | security_grc internally |
| LOW | Minor access pattern anomaly, outdated dependency | Next cycle | Log only |

---

## Phase 1: DETECT

strix-agent monitors continuously:
- All new files appearing in plugins/ or ingestion/
- All outbound API calls
- Agent memory access patterns (cross-dept boundary violations)
- gatekeeper.ps1 logs for unauthorized attempts
- SkillSentry scans on all new repos/plugins

incident-agent monitors:
- API rate limit violations (may indicate exfiltration)
- Repeated authentication failures
- Unusual cross-dept data access

---

## Phase 2: CLASSIFY + INITIAL RESPONSE

On incident detection, write to `shared-context/brain/corp/escalations.md`:
```markdown
## SECURITY INCIDENT â€” [INC-ID] â€” [DATETIME]
Severity: CRITICAL | HIGH | MEDIUM | LOW
Detected by: <agent>
Type: <prompt-injection | unauthorized-access | data-exfiltration | license-violation | other>

Description: <what was detected>
Affected systems: <list of files, agents, or depts affected>
Evidence: <receipt path or scan results>

Initial containment taken:
  - <immediate action, e.g., "blocked execution of plugin X">

Awaiting: CEO response (if CRITICAL) | COO response (if HIGH)
```

**CRITICAL immediate actions (before waiting for CEO):**
- Halt execution of the flagged tool/plugin/agent
- Remove from SKILL_REGISTRY if newly ingested
- Quarantine to `ingestion/quarantine/`
- Revoke workspace access if applicable

---

## Phase 3: CONTAIN

```
LOW/MEDIUM: security_grc handles containment internally
  - Remove or quarantine flagged item
  - Restrict access for flagged agent

HIGH: COO coordinates containment
  - Brief affected dept heads
  - Pause affected pipelines

CRITICAL: CEO commands containment
  - May pause ALL external-facing operations
  - May require full system checkpoint
```

---

## Phase 4: INVESTIGATE

incident-agent investigates:
1. **Root cause:** How did this happen?
2. **Blast radius:** What has been affected?
3. **Timeline:** When did it start?
4. **Vector:** How did it enter?

Write investigation report:
```markdown
## INVESTIGATION REPORT â€” [INC-ID]

Timeline:
  [DATETIME]: First indicator
  [DATETIME]: Detection
  [DATETIME]: Containment

Root cause: [technical explanation]
Blast radius: [what was potentially affected]
Attack vector: [how it entered]
Evidence:
  - [file paths, logs, scan results]

Recommendations:
  1. [immediate fix]
  2. [systemic prevention]
```

---

## Phase 5: REMEDIATE

Based on investigation:
```
LOW: patch the specific item
HIGH: patch + policy update + security brief
CRITICAL: full remediation plan â†’ CEO approved â†’ deployed â†’ verified
```

Remediation tracked in `corp/memory/departments/security_grc.md`

---

## Phase 6: VERIFY + CLOSE

```
1. security-scanner re-scans remediated item
2. compliance-agent confirms policy updated
3. access-control-agent verifies no residual access
4. strix-agent runs full workspace health check

On clean verification:
  - Close incident in escalations.md
  - Write post-mortem to proposals/ for CEO
  - Update security rules if needed
  - Update SKILL_REGISTRY blacklist if applicable

INC-ID status: CLOSED
```

---

## Post-Incident Mandatory Review

For every HIGH or CRITICAL incident, strategy dept writes post-mortem:
```markdown
# Post-Mortem: [INC-ID]

What happened: [summary]
Why it happened: [root cause]
How we caught it: [detection method]
Impact: [what was affected]
What we fixed: [remediation]
Prevention going forward: [new rules or checks added]
CEO action required: YES | NO
```

---

*"The question is not if there will be incidents. The question is how fast and clean the response is."*

