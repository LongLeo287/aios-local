---
name: Cybersecurity Skills
description: AI OS cybersecurity skill bundle. Web app security testing (SQLi, XSS, API security), penetration testing workflows, and security assessment capabilities. Delivered from CIV ingest pipeline.
department: security_grc
tier: 2
category: security
status: active
tags: [security, pentest, sqli, xss, api-security, web-security, assessment]
---

# Cybersecurity Skills

**Repo:** `brain/skills/cybersecurity`
**Type:** Skill bundle / reference
**Source:** CIV delivery pipeline
**Department:** Security / GRC
**Tier:** 2 — ready to use

## What it is

A curated set of cybersecurity skills delivered into AI OS brain. Covers offensive security (assessment tools) and defensive (policy/compliance) workflows.

## Skills Covered

### Web Application Security
- **SQL Injection:** Detection, exploitation patterns, parameterized query remediation
- **XSS (Cross-Site Scripting):** DOM-based, reflected, stored XSS detection
- **API Security:** Auth testing, rate limit assessment, OWASP API Top 10

### Tools Integration
Maps to Security Console tools in ClawTask:
| Tool | Location | Skill |
|------|----------|-------|
| GitHacker | `plugins/GitHacker/` | .git exposure scan |
| identYwaf | `plugins/identYwaf/` | WAF fingerprinting |
| zeroleaks | `plugins/zeroleaks/` | Secret detection |
| claude-bug-bounty | `plugins/claude-bug-bounty/` | AI-assisted bug finding |

## Usage by Agents

```bash
# Security agent workflow
1. Define target → ClawTask Security Console
2. Select tool + scope
3. Run via /api/tool-run → results in secLog
4. Generate report → telemetry/receipts/
```

## AI OS Integration
- **Owner dept:** `security_grc` → `corp/departments/security_grc/`
- **ClawTask panel:** Security Console (view `security`)
- **Pairs with:** `security/rules/`, `security/secrets/`
- **Feeds:** Telemetry receipts + Blackboard security advisories
