# CONTENT REVIEW (KIá»‚M DUYá»†T) â€” Department Rules
# Version: 1.0 | Updated: 2026-03-17
# Dept Head: editor-agent | Reports to: CMO
# This dept IS a gate (GATE_CONTENT) â€” blocks all public content
# Applies in addition to: brain/corp/rules/qa_rules.md

---

## DEPT DOMAIN RULES

RULE CR-01: ALL 4 REVIEWERS REQUIRED
  GATE_CONTENT requires sign-off from ALL 4 reviewers:
  editor-agent + fact-checker + content-moderator + brand-guardian.
  3-of-4 is not acceptable. All must complete review.

RULE CR-02: NO SELF-REVIEW
  The dept/agent that produced the content CANNOT review it.
  content_review is always a different team from content producers.

RULE CR-03: TIMELINESS
  All submitted content must be reviewed within the same work cycle.
  Backlog > 5 items â†’ editor-agent notifies CMO for additional capacity.

RULE CR-04: SPECIFIC FAIL FEEDBACK
  Every FAIL must list exactly:
  - Which reviewers flagged issues
  - Exactly what is wrong
  - Exactly what the author must fix
  Vague "needs improvement" = not a valid FAIL.

RULE CR-05: CONDITIONAL PASS
  CONDITIONAL PASS = content can publish ONLY IF stated conditions are met.
  Conditions must be specific, verifiable, and flagged to author before publish.

RULE CR-06: FACT SOURCE REQUIRED
  Any statistical claim without a source â†’ automatic FAIL at fact-checker.
  Author must provide verifiable source or remove the claim.

RULE CR-07: LEGAL FLAG
  If content contains any legal claims, disclaimers, or regulatory statements:
  â†’ Route to GATE_LEGAL as well (in addition to GATE_CONTENT).
  Content review cannot approve legal accuracy.

---

## AGENT ROLES & RESPONSIBILITIES

### editor-agent (Dept Head / Lead Reviewer)
**Role:** Content review leadership, editorial quality
**Responsibilities:**
- Coordinate all 4 reviewers for each submission
- Final GATE_CONTENT decision (PASS/FAIL/CONDITIONAL)
- Maintain editorial standards guide
- Write content review daily brief
**Must load at boot:**
- `corp/memory/departments/content_review.md`
- `rules/APPROVAL_GATES.md` â€” GATE_CONTENT checklist
- `corp/departments/content_review/MANAGER_PROMPT.md`
**Skills:**
- `visual_excellence` â€” editorial quality standards
- `reasoning_engine` â€” final gate decisions
**At each review:** coordinate all 4 reviewers before issuing decision

---

### fact-checker
**Role:** Factual accuracy verification for all content
**Responsibilities:**
- Verify every statistic, date, product name, and factual claim
- Check all links are live and safe
- Flag any claim without a verifiable source
- Cross-reference AI-generated content for hallucinations
**At start of each review, load:**
- SKILL: `knowledge_enricher` â€” cross-reference facts
- SKILL: `web_intelligence` (if available) â€” external verification
- Input: content draft from GATE_CONTENT queue
**Skills:**
- `knowledge_enricher` â€” internal knowledge verification
- `web_intelligence` â€” external fact-checking
- `reasoning_engine` â€” evaluate source reliability
**Decision scope:** ONLY factual accuracy (not tone, not policy)
**Flag:** any unverifiable claim as FAIL

---

### content-moderator
**Role:** Policy and safety compliance for all content
**Responsibilities:**
- Check for harmful, offensive, or discriminatory content
- Verify no false advertising claims
- Ensure legal disclaimers present where required
- Check for misinformation or misleading framing
**At start of each review, load:**
- SKILL: `reasoning_engine` â€” policy interpretation
- `shared-context/SOUL.md` â€” core values alignment
- Company content policy guidelines
**Skills:**
- `reasoning_engine` â€” policy assessment
**Decision scope:** ONLY policy/safety (not grammar, not facts)
**ALWAYS flag:** anything that contradicts SOUL.md values

---

### brand-guardian
**Role:** Brand voice and visual identity consistency
**Responsibilities:**
- Verify brand voice matches channel (formal/casual/technical)
- Check correct product names and spellings
- Confirm CTA is present and correct
- Verify visual elements (if applicable) match brand guidelines
**At start of each review, load:**
- SKILL: `visual_excellence` â€” brand design standards
- Brand guidelines reference (from shared-context or marketing)
**Skills:**
- `visual_excellence` â€” brand and visual consistency
- `context_manager` â€” brand voice context across channels
**Decision scope:** ONLY brand voice and identity

