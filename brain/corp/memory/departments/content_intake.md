# Memory: content_intake department (CIV)
# Type: department | Dept Number: 20 | Retention: 30d | Updated: 2026-03-23

## Always-Load Context
- Dept: Content Intake & Vetting (Dept 20) | Reports to: COO
- **PRIMARY ROLE: GATE 1 — Repo Evaluation** (Owner of `ops/workflows/repo-evaluation.md`)
- SINGLE ENTRY GATE for ALL external content AND repos into AI OS (RULE CIV-01)
- QUARANTINE folder: `<AI_OS_ROOT>/QUARANTINE/`
- intake_log.md: all active tickets — check first on boot
- Co-authority with Security GRC (strix-agent) for all repo/plugin vetting
- Classify first, act second — never process before classification (CIV-02)
- Every input gets a CIV ticket (CIV-03)

## SOP — Repo Evaluation (GATE 1 — RULE-PROCESS-01 Extended)

### When This Gate Triggers
Any request to bring an external repo/tool/package into AI OS → CIV issues a ticket and runs evaluation.

### Evaluation Workflow
Follow `ops/workflows/repo-evaluation.md` exactly:
```
Step 1: Identity & Purpose Analysis   → 5 Questions (README only)
Step 2: Conflict & Redundancy Check   → plugin-catalog.md + SKILL_REGISTRY.json
Step 3: Tier Assignment Decision      → Tier 1 / Tier 2 / Tier 3
Step 4: Integration Cost Estimate     → dependencies, port, API key, adapter, time
Step 5: Verdict                       → APPROVE / DEFER / REJECT
```

### Verdict Actions
| Verdict | Action |
|---------|--------|
| `APPROVE` | Update catalog `⚡`. Hand off to Dept 4 (Registry). |
| `DEFER` | Update catalog `🔖`. Add note with defer reason + target phase. |
| `REJECT` | Update catalog `❌`. Add reason. Notify CEO if it was CEO-requested. |

### Key Rules
1. **"No clone by default"** — CIV does NOT clone repos. Only reads README + public info.
2. No repo bypasses this gate. Even CEO-suggested repos must receive a CIV ticket.
3. Tier 1 is FROZEN — CIV cannot APPROVE a repo as Tier 1 without explicit CEO approval.
4. If repo conflicts with existing Tier 1 tool → automatic REJECT.

### Ticket Format
`CIV-[YYYY-MM-DD]-[SEQ]`
Status flow: `RECEIVED → CLASSIFYING → EVALUATING → VERDICT`

### Cross-Dept Dependencies
- All depts: submit repo requests via blackboard.json
- Dept 10 (Security): co-vetting authority, runs Phase 1 security scan after APPROVE
- Dept 4 (Registry): receives APPROVE verdict, runs plugin-integration.md

## Rolling Memory (30-day):
→ [2026-03-23] CIV formally designated as GATE 1 owner for all repo intake.
→ [2026-03-23] repo-evaluation.md created and owned by CIV. 5-step process with APPROVE/DEFER/REJECT.
→ [2026-03-23] 3-Tier Architecture enforced — Tier 3 repos auto-REJECT.
