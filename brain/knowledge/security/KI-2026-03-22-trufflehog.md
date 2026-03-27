---
id: KI-2026-03-22-trufflehog
source: https://github.com/trufflesecurity/trufflehog
type: TOOL
domain: ['security', 'devsecops', 'ci-cd']
dept: security_grc
agents: ['security_shield', 'fbi-watchdog']
created: 2026-03-22T22:37:16.443912
---

# TruffleHog Secret Scanner

> 700+ detectors for secrets/credentials in Git/GitHub/AWS/GCP/files. 16k★. Go binary — use via Docker or binary download. CI/CD integration.

**Source:** [https://github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)  
**Type:** TOOL | **Dept:** security_grc  
**Relevant Agents:** security_shield, fbi-watchdog

## AI OS Notes
Run before any plugin is added to AI OS. Add to CI/CD: `trufflehog git plugins/<plugin>`. Best practice: scan on every new repo ingest.

## Install / Use
```
docker run trufflesecurity/trufflehog git <repo-url>
```

## Key Concepts
_See source URL_

## Cross-links
- SKILL.md: `plugins/22-trufflehog/SKILL.md`
- FAST_INDEX: keyword `trufflehog_secret_sc`
