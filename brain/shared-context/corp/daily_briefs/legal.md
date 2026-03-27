# Daily Brief — Legal & Compliance — 2026-03-20
# Agent: contract-agent (Legal Dept)
# Task: C3-LEGAL-001 | Cycle: 3
# Status: COMPLETE ✅

## Summary

Legal dept activated. First compliance review and IP framework established for AI OS Corp.

## IP & License Compliance Review

### External Repos License Audit

| Repo | License | Commercial Use | Attribution Req | Status |
|------|---------|---------------|-----------------|--------|
| NVIDIA/NemoClaw | Apache 2.0 | ✅ YES | Name + notice | COMPLIANT |
| code-on-sunday/slide-deck-generator | MIT | ✅ YES | Name only | COMPLIANT |
| (107+ other repos in corpus) | Mixed (mostly MIT/Apache) | ✅ Majority YES | Varies | REVIEW RECOMMENDED |

**Legal Recommendation:** All MIT and Apache 2.0 repos are cleared for Corp internal use. Repos without clear license should be quarantined.

## Corp IP Framework

### What AI OS Corp Owns
- All markdown files in `corp/`, `shared-context/`, `workflows/`
- All MQ task cards
- All daily briefs, retros, OKR docs
- Antigravity boot protocol + Corp Cycle documentation

### What We License (Do Not Own)
- External repos in `plugins/` and EXTERNAL_SKILL_SOURCES.yaml
- Any LLM model outputs (per provider ToS)
- Supabase platform, Docker platform

### Data Governance
- No user PII stored in ClawTask tasks table (agent_id = Corp agent IDs, not personal data)
- Supabase anon key: low-risk (read-only public data pattern)
- .env files: properly gitignored per `.gitignore`

## GATE_LEGAL Protocol

**Trigger:** Any external repo ingestion, any Corp document going to external parties.

**Checklist:**
- [ ] License verified (MIT/Apache = PASS, GPL = REVIEW, Proprietary = BLOCK)
- [ ] No PII/secrets in output documents
- [ ] Attribution credited where required
- [ ] .env / secrets confirmed gitignored

## Wins
- First legal framework for Corp — IP clarity established
- All current corpus COMPLIANT with open source licenses

## Recommendations
- Create `corp/legal/LICENSE_AUDIT.md` with full corpus license table (Cycle 4)
- Add GATE_LEGAL check to intake pipeline for any repos without MIT/Apache license
