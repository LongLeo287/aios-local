# APPROVAL_GATES.md â€” Gate Checklists for All 4 Corp Gates
# Version: 1.0 | Created: 2026-03-22
# Referenced by: corp-gate-flow.md, corp-daily-cycle.md (Phase 5)
# Authority: Tier 2 (Operations) â€” overridden only by Tier 0-1

---

## GATE_QA â€” Engineering Output Checklist

**Operated by:** qa_testing dept (test-manager-agent)
**Blocks:** All code/system changes before deployment

### Checklist (ALL must pass for PASS verdict):

```
[ ] Q1  â€” All automated tests pass (unit + integration)
[ ] Q2  â€” Test coverage â‰¥ 70% for new code
[ ] Q3  â€” No hardcoded secrets, credentials, or API keys
[ ] Q4  â€” No obvious linting/type errors
[ ] Q5  â€” RULE-DYNAMIC-01 satisfied (no absolute paths in code)
[ ] Q6  â€” Error handling present for external calls
[ ] Q7  â€” No breaking changes to existing API contracts (or documented)
[ ] Q8  â€” Receipt written to telemetry/receipts/<dept>/<T-ID>.json
```

**Scoring:**
- All 8 PASS â†’ **GATE_QA: PASS**
- Q1â€“Q4 fail â†’ **GATE_QA: FAIL** (blocking â€” must fix before re-submit)
- Q5â€“Q8 fail â†’ **GATE_QA: CONDITIONAL** (must fix within 1 cycle)

**Receipts:** `telemetry/qa_receipts/gate_qa/<T-ID>.json`

---

## GATE_CONTENT â€” Content Output Checklist

**Operated by:** content_review dept (editor-agent)
**Blocks:** All public-facing content before publish

### Checklist (ALL must pass for PASS verdict):

```
[ ] C1  â€” No spelling/grammar errors (editor-agent review)
[ ] C2  â€” Factual claims verified (fact-checker review)
[ ] C3  â€” Brand voice consistent with SOUL.md tone
[ ] C4  â€” No trademark/IP violations (brand-guardian review)
[ ] C5  â€” CTA present and correct (where applicable)
[ ] C6  â€” Content policy compliant â€” no harmful/misleading content
[ ] C7  â€” Target channel format correct (tweet â‰  blog â‰  email)
[ ] C8  â€” CEO-sensitive topics flagged for CEO review (optional publish)
```

**Team:** editor-agent (C1,C7) | fact-checker (C2) | content-moderator (C6) | brand-guardian (C3,C4,C8)
All 4 must sign off before final PASS.

**Receipts:** `telemetry/qa_receipts/gate_content/<T-ID>.json`

---

## GATE_SECURITY â€” Security Scan Checklist

**Operated by:** security_grc dept (strix-agent â€” autonomous)
**Blocks:** New plugins, skills, external repos, data egress

### SkillSentry 9-Layer Scan (automated):

```
[ ] S1  â€” License check: OSI-approved or compatible license
[ ] S2  â€” Dependency audit: no known CVEs in direct deps
[ ] S3  â€” No hardcoded credentials or secrets in code
[ ] S4  â€” No suspicious outbound network calls
[ ] S5  â€” No eval/exec with untrusted input (code injection vectors)
[ ] S6  â€” File access limited to declared scope (no unauthorized paths)
[ ] S7  â€” No data exfiltration patterns (unusual data sends)
[ ] S8  â€” Supply chain: author/repo reputation check
[ ] S9  â€” SOUL.md alignment: no contradictions to core values
```

**Score:** Each layer = 0 (FAIL) or 1 (PASS). Total = 0â€“9.

**Verdict:**
- Score 8â€“9 â†’ **PASS** (â‰¥ 60% threshold met)
- Score 5â€“7 â†’ **CONDITIONAL** â€” quarantine watch 7 days, monitoring enabled
- Score < 5 â†’ **BLOCK** â€” CEO override required to unblock
- Any S4/S7 FAIL with confirmed threat â†’ **CRITICAL L3 escalation regardless of total score**

**Receipts:** `telemetry/qa_receipts/gate_security/<item-id>.json`

**Critical path:** strix-agent â†’ DIRECT L3 to `shared-context/brain/corp/escalations.md` (skip L1/L2)

---

## GATE_LEGAL â€” Legal Review Checklist

**Operated by:** legal dept (legal-agent)
**Blocks:** Contracts, partnerships, data sharing agreements

### Checklist:

```
[ ] L1  â€” Contract structure complete (parties, scope, term, termination)
[ ] L2  â€” No clauses that override CEO authority or agent governance rules
[ ] L3  â€” IP ownership clauses: all AI OS output remains AI OS Corp property
[ ] L4  â€” Data privacy: GDPR/local law compliant (gdpr-agent review)
[ ] L5  â€” No unlimited liability clauses
[ ] L6  â€” Dispute resolution jurisdiction acceptable
[ ] L7  â€” License grants are limited, revocable, non-exclusive (where applicable)
[ ] L8  â€” Financial terms match CFO-approved budget
```

**Team:** contract-agent (L1,L2,L5,L6) | ip-agent (L3,L7) | gdpr-agent (L4) | legal-agent (L8)

**Verdict:**
- All pass â†’ **CLEAR TO SIGN** â€” STILL requires CEO final approval before signing
- Any fail â†’ **REVISIONS NEEDED** â€” specific clauses flagged
- L2 or L5 fail â†’ **DO NOT SIGN** â€” L3 escalation with full analysis

**Receipts:** `telemetry/qa_receipts/gate_legal/<T-ID>.json`

---

## Gate Escalation Matrix

| Gate | 1st FAIL | 2nd FAIL | 3rd FAIL | CRITICAL |
|------|----------|----------|----------|---------|
| GATE_QA | Worker fixes, re-submit | Worker + Manager review | L2 to CTO | n/a |
| GATE_CONTENT | Author revises | Author + CMO review | L2 to CMO | n/a |
| GATE_SECURITY | CONDITIONAL watch | BLOCK + L2 to CTO/COO | CEO override required | Direct L3 â€” work pauses |
| GATE_LEGAL | Revisions needed | Legal chief review | DO NOT SIGN + L3 | Direct L3 â€” CEO required |

---

*"A gate is not an obstacle. It is proof that quality was checked."*

