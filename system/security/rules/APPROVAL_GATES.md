# APPROVAL_GATES.md — AI OS Universal Approval Gates
# Version: 2.0 | Updated: 2026-03-17
# Authority: Tier 2 (Operations) + Tier 2 Gate
# Replaces: v1.0 (3 gates, no corp mode)

---

## Overview

All AI OS outputs pass through approval gates before being delivered or published.
Gates are **BLOCKING** — nothing passes without explicit PASS.

Two gate systems operate simultaneously:
- **System Gates** (Personal AI OS) — protect technical quality
- **Corp Gates** (Corp Mode) — protect organizational quality

---

## SYSTEM GATES (Personal AI OS)

### GATE_HITL — Human-in-the-Loop
**Stage:** Phase 3 (PLAN), after brainstorm, before delegate
**Operator:** USER (You)
**Rule:** Antigravity CANNOT proceed to Phase 4 without your explicit approval
**Bypass:** None. This gate is sovereign.

```
Approve  → write blackboard.json READY → auto-delegate
Edit     → Antigravity revises → re-present → user re-reviews
Reject   → task cancelled or completely re-planned
```

### GATE_GATEKEEPER — Workspace Access
**Stage:** Phase 4 (DELEGATE), before Claude Code launch
**Operator:** scripts/gatekeeper.ps1 (automated)
**Rule:** Claude Code only gets access to explicitly registered workspaces

```
GRANT    → Claude Code launches
DENY     → Stop. Log. Report to user. Do NOT proceed.
Bypass:  None. CEO override requires updating registry.json.
```

### GATE_SKILL_ENTRY — New Skill Registration
**Stage:** When any new skill added to registry
**Operator:** strix-agent (GATE_SECURITY)
**Rule:** No skill enters production without passing 9-layer SkillSentry scan

```
Score >= 60  → PASS → move to skills/domains/ or skills/core/
Score 40-59  → CONDITIONAL → quarantine watch period
Score < 40   → BLOCK → never enters production
CEO override required to accept score < 40
```

---

## CORP GATES (Corp Mode — All Blocking)

### GATE_QA — Code & System Quality
**Operated by:** qa_testing dept (security-engineer-agent / superpowers-agent)
**Blocks:** Engineering outputs before deploy

**Full checklist (all items required):**
```
CODE QUALITY:
  [ ] Tests written and passing (unit + integration)
  [ ] Test coverage delta positive or maintained
  [ ] No linting errors or critical warnings

SECURITY:
  [ ] No hardcoded secrets or credentials
  [ ] Input validation present
  [ ] No SQL injection vectors
  [ ] No unsafe eval/exec patterns

ARCHITECTURE:
  [ ] Follows established architecture patterns
  [ ] All dependencies approved + whitelisted
  [ ] Error handling covers failure paths

OPERATIONS:
  [ ] Logging appropriate (not too verbose, not silent)
  [ ] Config environment-aware (not hardcoded)
  [ ] Rollback path exists if deploy fails
```

**Decision:**
- PASS → engineering output approved for deploy
- FAIL → specific items failing + fixes required → return to worker
- CONDITIONAL → can proceed IF stated conditions met before production

---

### GATE_CONTENT — Public Content Quality
**Operated by:** content_review dept (editor-agent / fact-checker / content-moderator)
**Blocks:** All public-facing content (marketing, support, social) before publish

**Full checklist:**
```
EDITORIAL:
  [ ] Grammar and spelling correct
  [ ] Tone matches channel (formal/casual/brand)
  [ ] Format follows channel guidelines

FACTUAL:
  [ ] All stats verifiable (sourced)
  [ ] No hallucinated claims
  [ ] Links work + are safe
  [ ] Dates and product names accurate

POLICY:
  [ ] No harmful/discriminatory content
  [ ] No false advertising claims
  [ ] Legal disclaimers present if needed

BRAND:
  [ ] Brand voice consistent
  [ ] Correct product spelling/naming
  [ ] CTA present and accurate
```

---

### GATE_SECURITY — New Plugin/Skill/Repo
**Operated by:** security_grc dept (strix-agent / security-scanner)
**Blocks:** Any external tool, plugin, repo before registration/use
**Mode:** Autonomous — security_grc can initiate this without manager request

**Full checklist (SkillSentry 9-layer + extras):**
```
STATIC ANALYSIS:
  [ ] No known malware signatures
  [ ] No homoglyphs or zero-width characters in code
  [ ] No encoded or obfuscated payloads
  [ ] No prompt injection patterns

PERMISSION SCAN:
  [ ] READ_SENSITIVE + NETWORK_SEND combination: BLOCK
  [ ] Outbound domains: all whitelisted
  [ ] No new outbound domains without CEO approval

LICENSE CHECK:
  [ ] MIT / Apache 2.0 / BSD: PASS
  [ ] GPL: CONDITIONAL (requires disclosure plan)
  [ ] Proprietary/BUSL: BLOCK unless CEO approves

REPUTATION:
  [ ] Source from EXTERNAL_SKILL_SOURCES.yaml whitelist
  [ ] GitHub: min 50 stars OR known organization
  [ ] Last commit < 24 months ago

SCORE THRESHOLD:
  Score >= 60  → PASS
  Score 40-59  → CONDITIONAL (quarantine monitoring)
  Score < 40   → BLOCK (CEO override with documented reason required)
```

---

### GATE_LEGAL — Agreements & External Commitments
**Operated by:** legal dept (legal-agent / contract-agent)
**Blocks:** Any external agreement, contract, or vendor commitment before signing
**CEO sign-off required on ALL PASS decisions (legal cannot self-approve signing)**

**Full checklist:**
```
CONTRACT STRUCTURE:
  [ ] Parties correctly identified
  [ ] Jurisdiction and governing law specified
  [ ] Effective date and term defined

IP & DATA:
  [ ] IP ownership clause clear
  [ ] Data processing clauses present (if personal data)
  [ ] GDPR/privacy compliance confirmed

RISK:
  [ ] Indemnification reviewed
  [ ] Limitation of liability present
  [ ] Termination conditions defined

FINAL:
  [ ] CEO approval obtained before signing
  [ ] Copy stored in legal/contracts/
```

---

## Gate Decision Reference

| Gate | Operated By | Blocks | CEO Override? |
|------|------------|--------|--------------|
| GATE_HITL | USER | Plan → Delegate | N/A (user IS the CEO) |
| GATE_GATEKEEPER | gatekeeper.ps1 | Workspace access | Update registry.json |
| GATE_SKILL_ENTRY | strix-agent | Skill registration | Written + documented |
| GATE_QA | qa_testing | Code deploy | Documented exception |
| GATE_CONTENT | content_review | Content publish | CMO + CEO written ok |
| GATE_SECURITY | security_grc | External tools | CEO written + documented |
| GATE_LEGAL | legal | External agreements | CEO must always approve |

---

## Gate Bypass Policy

Bypassing a gate is **always** an exception, never a default.
Any bypass must be:
1. Documented in corp/memory/global/decisions_log.md
2. Signed by CEO or designated C-Suite authority
3. Time-bounded (bypass is for this specific item, not permanent)
4. Post-event reviewed at next retro

*"Gates are not obstacles. They are the organization's immune system."*
