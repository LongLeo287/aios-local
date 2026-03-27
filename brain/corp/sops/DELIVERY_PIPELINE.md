# DELIVERY PIPELINE â€” SOP v1.0
# AI OS Corp | Tier 1 â€” Operations
# Effective: 2026-03-18

> **Má»¥c Ä‘Ã­ch:** Quy trÃ¬nh hoÃ n chá»‰nh tá»« khi client ACCEPT proposal â†’ Deliver â†’ Invoice.
> Tiáº¿p ná»‘i tá»« `CLIENT_INTAKE_GATEWAY.md` vÃ  `Proposal Engine`.

---

## Tá»•ng Quan Pipeline

```
PROPOSAL ACCEPTED
      â”‚
      â–¼
[Phase 1: KICKOFF]        â”€ 1 ngÃ y
  - XÃ¡c nháº­n scope
  - Assign team
  - Setup workspace
      â”‚
      â–¼
[Phase 2: EXECUTION]      â”€ Theo timeline Ä‘Ã£ commit
  - Dept leads nháº­n brief
  - Agents thá»±c thi
  - Progress tracking
      â”‚
      â–¼
[Phase 3: QA & REVIEW]    â”€ 1-3 ngÃ y
  - QA dept kiá»ƒm tra
  - Client review round 1
  - Revisions (2 rounds max)
      â”‚
      â–¼
[Phase 4: DELIVERY]       â”€ 1 ngÃ y
  - Package deliverables
  - Handoff to client
  - Collect feedback
      â”‚
      â–¼
[Phase 5: INVOICE & CLOSE]â”€ 1 ngÃ y
  - Generate invoice
  - Payment tracking
  - Archive project
      â”‚
      â–¼
[Phase 6: LEARNING LOOP]  â”€ Auto
  - corp_learning_loop retro
  - Update KPI scoreboard
  - Knowledge extraction
```

---

## Phase 1: KICKOFF

**Trigger:** Client reply "ACCEPT" | "Äá»“ng Ã½" | "Proceed" vÃ o proposal

**Actions:**
1. `project_intake_agent` â†’ update status: `ACCEPTED`
2. Táº¡o **Project Workspace**:
   ```
   shared-context/projects/<PROJECT-ID>/
   â”œâ”€â”€ brief.json          â† copy intake record
   â”œâ”€â”€ proposal.md         â† accepted proposal
   â”œâ”€â”€ workspace/          â† working files
   â”œâ”€â”€ deliverables/       â† final output
   â””â”€â”€ comms_log.md        â† all client communications
   ```
3. Assign **Project Lead** tá»« operations
4. Create department briefs â†’ gá»­i vÃ o `subagents/mq/<dept>_brief.md`
5. Notify client: "âœ… Project [ID] Ä‘Ã£ Ä‘Æ°á»£c khá»Ÿi Ä‘á»™ng! Lead: [tÃªn agent]"

---

## Phase 2: EXECUTION

**Responsibility:** Dept leads + assigned agents

**Progress Tracking:**
- Má»—i agent update `shared-context/projects/<ID>/progress.json` sau má»—i task
- Format:
  ```json
  {
    "task": "Build login page",
    "agent": "frontend-agent",
    "status": "DONE",
    "output": "workspace/login.html",
    "timestamp": "..."
  }
  ```
- `ops-router` (tinyclaw) check progress má»—i 4h â†’ report cho ops

**Communication Rules:**
- Client update: má»—i 24-48h (tÃ¹y timeline)  
- All comms log vÃ o `comms_log.md`
- Blocker phÃ¡t sinh â†’ immediate ops notify

---

## Phase 3: QA & REVIEW

**QA Checklist** (qa-agent thá»±c hiá»‡n):
- [ ] Deliverables Ä‘Ãºng scope trong proposal
- [ ] KhÃ´ng cÃ³ bug/error rÃµ rÃ ng
- [ ] File format Ä‘Ãºng yÃªu cáº§u
- [ ] Docs Ä‘áº§y Ä‘á»§

**Client Review:**
- Gá»­i deliverables preview qua channel gá»‘c
- Wait 48h cho feedback
- Round 1 revision náº¿u cáº§n
- Round 2 revision (cuá»‘i) náº¿u cáº§n
- > 2 rounds â†’ OOscope, charge thÃªm â†’ CEO approval

---

## Phase 4: DELIVERY

**Delivery Package:**
```
deliverables/
â”œâ”€â”€ [project-files...]
â”œâ”€â”€ README.md           â† hÆ°á»›ng dáº«n sá»­ dá»¥ng
â”œâ”€â”€ DELIVERY_RECEIPT.md â† confirm handoff
â””â”€â”€ support_contact.md  â† liÃªn há»‡ há»— trá»£ sau delivery
```

**Handoff:**
1. Zip vÃ  share qua channel (hoáº·c link Google Drive/cloud)
2. Client kÃ½ nháº­n `DELIVERY_RECEIPT.md` (reply "RECEIVED" hoáº·c "âœ…")
3. Update status: `DELIVERED`

---

## Phase 5: INVOICE & CLOSE

**Invoice Generation:**
```
shared-context/brain/corp/invoices/INVOICE-<YYYYMMDD>-<PROJECT-ID>.md

Content:
  - Project summary
  - Deliverables listed
  - Hours spent (náº¿u T&M)
  - Amount due
  - Payment methods: [bank transfer / crypto / PayPal]
  - Due: 7 ngÃ y
```

**Payment Status Tracking:**
- `shared-context/brain/corp/invoices/_payment_tracker.json`
- Reminder: +7 ngÃ y chÆ°a thanh toÃ¡n â†’ follow up
- Reminder: +14 ngÃ y â†’ escalate

**Project Close:**
- Archive to: `shared-context/projects/archive/<PROJECT-ID>/`
- Rating: thu tháº­p feedback 1-5 sao tá»« client
- Update `corp/kpi_scoreboard.json`: projects_delivered + 1

---

## Phase 6: LEARNING LOOP

**Auto-trigger** sau khi invoice PAID:

1. **corp_learning_loop** run retro cho project:
   - GÃ¬ Ä‘Ã£ tá»‘t? â†’ document trong `knowledge/project_learnings/`
   - GÃ¬ cáº§n cáº£i thiá»‡n?
   - Skill gap phÃ¡t hiá»‡n? â†’ Ä‘á» xuáº¥t training
   
2. **KPI Update:**
   - Revenue realized
   - Client satisfaction score
   - Delivery time vs estimate

3. **Knowledge Extraction:**
   - Náº¿u project táº¡o ra reusable code/skill â†’ Ä‘á» xuáº¥t thÃªm vÃ o SKILL_REGISTRY

---

## Project Status States

```
INTAKE_RECEIVED
    â†“
PROPOSAL_SENT
    â†“
PROPOSAL_ACCEPTED  â†  PROPOSAL_REJECTED (archive)
    â†“
KICKOFF
    â†“
IN_EXECUTION
    â†“
IN_QA_REVIEW
    â†“
CLIENT_REVIEW
    â†“
DELIVERED
    â†“
INVOICE_SENT
    â†“
PAID â†’ CLOSED
```

---

## SLA Targets

| Phase | Target Duration |
|-------|----------------|
| Intake â†’ Proposal | â‰¤ 2 giá» lÃ m viá»‡c |
| Proposal â†’ Kickoff | â‰¤ 1 ngÃ y sau ACCEPT |
| Execution | Per proposal timeline |
| QA | â‰¤ 20% total timeline |
| Delivery | â‰¤ 1 ngÃ y sau QA pass |
| Invoice | Ngay khi DELIVERED |
| Payment | Client: 7 ngÃ y |

---

*ThÆ° má»¥c projects: `shared-context/projects/`*
*Invoice: `shared-context/brain/corp/invoices/`*
*Knowledge: `knowledge/project_learnings/`*

