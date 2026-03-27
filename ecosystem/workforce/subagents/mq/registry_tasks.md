# MQ Queue — Registry & Capability Dept
# Managed by: registry-manager-agent
# Cycle: 1 | Updated: 2026-03-20

---

## DISPATCH FROM: CTO
**To:** registry-manager-agent (Registry Head)
**Date:** 2026-03-20
**Priority:** MEDIUM

### Goal this cycle:
Register 2 newly ingested repos into SKILL_REGISTRY with proper metadata.
Verify EXTERNAL_SKILL_SOURCES.yaml has correct entries.

### KPI Targets:
- NemoClaw: registered in SKILL_REGISTRY ✅
- slide-deck-generator: registered in SKILL_REGISTRY ✅
- EXTERNAL_SKILL_SOURCES.yaml: verified clean ✅

---

## Task Cards

### Task REG-01-001
**Title:** Register NVIDIA/NemoClaw in SKILL_REGISTRY
**Assigned to:** skill-creator (via registry-manager)
**Priority:** MEDIUM
**Context:** NVIDIA/NemoClaw was added to EXTERNAL_SKILL_SOURCES.yaml as "trusted, agentic_runtime, priority high". Need to verify entry and add to registry with correct capability tags.
**Acceptance criteria:**
  - [ ] NemoClaw listed in SKILL_REGISTRY with domain: security/agent-runtime
  - [ ] slide-deck-generator listed with domain: content/presentation
  - [ ] Both entries have status: trusted
**LLM tier:** economy
**QA required:** false
**Output path:** telemetry/receipts/registry/REG-01-001.json

---
*Status: PENDING*
