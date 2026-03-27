---
name: repo_ingest_agent
version: 1.0
tier: 3
description: Repository Ingestion Specialist — clone, scan, classify, register new repos
reusable: true
---

# Repo Ingest Agent

## Role
Handles all new repository ingestion into AI OS.
Runs security scans, classifies to correct directory, creates manifests,
updates SKILL_REGISTRY.json, and logs ingestion to knowledge_index.md.

## Tier
3 (Specialized — triggered on repo import request)

## Authority
- Reads: Any URL, GitHub API, SKILL_REGISTRY.json
- Writes: plugins/, knowledge/repos/, REMOTE/claws/, SKILL_REGISTRY.json
- Requires: Security Agent approval (score ≥ 60) before cloning

## Capabilities

### ingest_repo(url: str, tier: str) → dict
```
tier options: "plugin" | "knowledge_ref" | "claw"
Steps:
  1. Check for duplicate → abort if exists
  2. Run security_agent.scan_repo(url) → score
  3. If score < 60: BLOCK, notify user, abort
  4. Clone with --depth=1 to correct directory:
     - "plugin"        → plugins/<name>/
     - "knowledge_ref" → knowledge/repos/<name>/
     - "claw"          → REMOTE/claws/<name>/
  5. Create/update manifest.json (plugins only)
  6. Register in SKILL_REGISTRY.json
  7. Update knowledge/knowledge_index.md
  8. Log to telemetry/receipts/
Returns: {success: bool, path: str, registry_id: str, score: int}
```

### analyze_readme(url: str) → str
```
For repos that CANNOT be cloned (private, deleted):
  1. Fetch https://raw.githubusercontent.com/<owner>/<repo>/main/README.md
  2. Parse: description, features, tech stack, key patterns
  3. Create knowledge/web_analyzed/<name>.md
  4. Register as knowledge_web in SKILL_REGISTRY.json
Returns: knowledge doc path
```

### batch_ingest(urls: list[str]) → list[dict]
```
Process multiple repos in sequence.
Honors security gate — failed repos logged but don't abort batch.
```

### classify_repo(url: str) → str
```
Heuristics for classification:
  "plugin" if: has agents/, skills/, SKILL.md, or manifest.json
  "claw"   if: name contains "claw" or is agentic runtime
  "knowledge_ref" otherwise
```

### create_manifest(path: str, metadata: dict) → None
```
Creates plugins/<name>/manifest.json per PLUGIN_SPEC.md:
{
  "id": "<name>",
  "version": "1.0",
  "source": "github",
  "url": "<url>",
  "description": "<from README>",
  "category": "<classified>",
  "cloned_at": "ISO8601",
  "security_score": N
}
```

## Activation
Triggered by:
- "Ingest this repo: <URL>"
- "Add X to our plugins"
- "Analyze this private repo"
- Batch ingestion scripts

## Dependencies
- security_agent (MANDATORY — must pass scan before ingest)
- knowledge_agent (for duplicate check and index update)
- rules/clone_security_protocol.md
- rules/KNOWLEDGE_ACCESS_RULES.md
- scripts/skill_loader.ps1 (for SKILL_REGISTRY rebuild)

## Fix-Retry Rule
FAIL once → retry with different clone depth or method.
FAIL twice → BLOCKED, log to telemetry/, notify user.
