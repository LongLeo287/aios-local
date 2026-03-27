# DELIVERY RECEIPT — CIV-2026-03-17-002
# From: ingest-router-agent (CIV Dept 20)
# Delivered: 2026-03-17T16:20:00+07:00
# VALUE_TYPE: SKILL (primary), KNOWLEDGE

## Source
URL: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
License: Apache-2.0
Author: Community (NOT official Anthropic — "Anthropic" = agentskills.io compatibility)

## What This Is
734 structured cybersecurity skills in agentskills.io format.
MITRE ATT&CK mapped. Compatible with Claude Code, Copilot, Cursor, Gemini CLI.

Skill categories:
- Cloud Security: AWS S3 Bucket Audit, Azure AD Config, GCP Security Assessment
- Threat Intelligence: APT Group Analysis, MITRE Navigator integration
- Web App Security: SQLi, XSS, API security testing
- Malware Analysis: static + dynamic analysis workflows
- DFIR: Digital Forensics + Incident Response
- SOC Operations: alert triage, threat hunting
- Container Security: Docker/K8s scanning

## DEPLOYMENT STATUS: RESTRICTED
Security flag: Contains offensive cybersecurity techniques.
MUST NOT be deployed to agents without Security GRC approval.
Tag: [RESTRICTED_DEPLOY] — strix-agent approval required per agent.

## STATUS FOR skill-creator-agent
ACTION REQUIRED:
1. Clone repo: git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills skills/cybersecurity/
2. Catalog all 734 skills with tag [RESTRICTED_DEPLOY]
3. Create subfolder index: skills/cybersecurity/INDEX.md (list all 734 by category)
4. Add to SKILL_REGISTRY.json with status=RESTRICTED_DEPLOY
5. Alert strix-agent (Security GRC) for deployment review

## STATUS FOR knowledge-curator-agent
ACTION REQUIRED:
1. Extract MITRE ATT&CK mapping → knowledge/cybersecurity/mitre_attck/mapping.md
2. Index categories → knowledge/cybersecurity/skill_catalog.md

## ENRICHMENT ALERT FOR strix-agent (Security GRC Dept 10)
HIGH PRIORITY: 734 cybersec skills available in skills/cybersecurity/
Review categories for deployment clearance.
After approval: update each skill tag from [RESTRICTED_DEPLOY] to [APPROVED]
Training-agent will load cleared skills into strix-agent's skill set.

## Relevance Score: 9/10
## Priority: HIGH — high-value skill library for Security GRC
