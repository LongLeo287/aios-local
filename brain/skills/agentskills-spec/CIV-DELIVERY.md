# DELIVERY RECEIPT — CIV-2026-03-17-001
# From: ingest-router-agent (CIV Dept 20)
# Delivered: 2026-03-17T16:20:00+07:00
# VALUE_TYPE: SKILL (primary), KNOWLEDGE, WORKFLOW

## Source
URL: https://github.com/agentskills/agentskills
Org: Anthropic (official agentskills.io specification)
License: Apache-2.0

## What This Is
The official specification repository for Agent Skills format.
This is the CANONICAL REFERENCE for the skill format AI OS uses.

Key contents:
- SKILL.md specification (front matter + instruction format)
- Reference SDK for skill discovery and loading
- Example skills collection
- Specification for write-once, use-everywhere skill portability

## STATUS FOR skill-creator-agent
ACTION REQUIRED:
1. Clone repo: git clone https://github.com/agentskills/agentskills skills/agentskills-spec/
2. Catalog as TYPE: SPEC_REFERENCE (not a regular skill — it IS the spec)
3. Extract any example SKILL.md templates into skills/templates/
4. Update SKILL_REGISTRY.json with spec_version from this repo
5. Confirm to knowledge-curator-agent that spec is loaded

## STATUS FOR knowledge-curator-agent
ACTION REQUIRED:
1. Index README.md content into knowledge/agent_architecture/skill_spec.md
2. Add to knowledge_index.md under domain: AI_ARCHITECTURE

## STATUS FOR archivist-agent (Operations)
ACTION REQUIRED:
1. Extract skill lifecycle workflow to workflows/agent-skill-discovery.md
2. Reference source: agentskills.io + this repo

## Relevance Score: 10/10
## Priority: CRITICAL — foundational spec
