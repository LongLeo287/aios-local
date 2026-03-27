# CLIENT INTAKE GATEWAY â€” SOP v1.0
# AI OS Corp | Tier 1 â€” Operations
# Effective: 2026-03-18

> **Model:** BÃªn ngoÃ i káº¿t ná»‘i vÃ o AI OS Corp Ä‘á»ƒ sá»­ dá»¥ng AI agents nhÆ° dá»‹ch vá»¥.
> Client â†’ Channel â†’ Intake Agent â†’ Proposal â†’ Delivery Pipeline

---

## 1. Cá»•ng Tiáº¿p Nháº­n

AI OS Corp tiáº¿p nháº­n yÃªu cáº§u qua **4 kÃªnh**:

| KÃªnh | Platform | Agent xá»­ lÃ½ | Status |
|------|----------|-------------|--------|
| Telegram | Bot @AICorpBot | nullclaw `client-intake` agent | ðŸŸ¡ Cáº§n config |
| Discord | #project-intake channel | tinyclaw `intake-agent` | ðŸŸ¡ Cáº§n config |
| Web Form | `intake.aios-corp.local` | project-intake-agent SKILL | ðŸŸ¡ Cáº§n build |
| WhatsApp | Business API | nullclaw `whatsapp` channel | ðŸ”´ Phase 2 |

---

## 2. Intake Flow

```
[CLIENT gá»­i brief qua Channel]
         â”‚
         â–¼
[NULLCLAW / TINYCLAW â€” Channel Gateway]
  - nháº­n message
  - sanitize & validate input
  - route Ä‘áº¿n project-intake-agent
         â”‚
         â–¼
[PROJECT-INTAKE-AGENT â€” thu tháº­p thÃ´ng tin]
  Thu tháº­p 5 fields báº¯t buá»™c:
  1. project_type    â€” Web / Mobile / AI / Data / Automation / Other
  2. description     â€” MÃ´ táº£ ngáº¯n (max 500 words)
  3. timeline        â€” Deadline mong muá»‘n
  4. budget_range    â€” Bracket: <$500 | $500-2k | $2k-10k | $10k+
  5. contact_info    â€” Telegram/Email/Discord handle
         â”‚
         â–¼
[VALIDATE & SCORE]
  - Completeness check (táº¥t cáº£ 5 fields?)
  - Feasibility score (1-10) dá»±a trÃªn skill registry
  - Priority: URGENT / NORMAL / LOW
         â”‚
         â–¼
[ROUTE TO PROPOSAL ENGINE]
  â†’ Ghi vÃ o: shared-context/client_intake/YYYY-MM-DD_HHMMSS_<slug>.json
  â†’ Notify: operations dept + CEO (náº¿u budget > $2k)
  â†’ Tá»± Ä‘á»™ng trigger Proposal Engine
```

---

## 3. Brief Template (Client-Facing)

Khi client nháº¯n tin láº§n Ä‘áº§u, bot tá»± Ä‘á»™ng gá»­i form sau:

```
ðŸ‘‹ ChÃ o má»«ng Ä‘áº¿n AI OS Corp!

Äá»ƒ báº¯t Ä‘áº§u, vui lÃ²ng tráº£ lá»i 5 cÃ¢u há»i:

1ï¸âƒ£ Loáº¡i project: Web / Mobile / AI Chatbot / Data / Automation / KhÃ¡c
2ï¸âƒ£ MÃ´ táº£ ngáº¯n: [Max 500 chá»¯]
3ï¸âƒ£ Deadline mong muá»‘n: [DD/MM/YYYY]
4ï¸âƒ£ Budget: DÆ°á»›i $500 / $500-2k / $2k-10k / $10k+
5ï¸âƒ£ CÃ¡ch liÃªn láº¡c: [Telegram/Email]

Sau khi Ä‘iá»n xong, team sáº½ pháº£n há»“i trong 2 giá» lÃ m viá»‡c. âœ…
```

---

## 4. Intake Record Schema

```json
{
  "intake_id": "INTAKE-20260318-001",
  "received_at": "2026-03-18T09:55:00+07:00",
  "channel": "telegram",
  "client": {
    "handle": "@client_username",
    "contact": "email@example.com"
  },
  "brief": {
    "project_type": "web",
    "description": "...",
    "timeline": "2026-04-30",
    "budget_range": "$2k-10k"
  },
  "scoring": {
    "feasibility": 8,
    "priority": "NORMAL",
    "matched_skills": ["ui-ux", "shell_assistant", "visual_excellence"]
  },
  "status": "PENDING_PROPOSAL",
  "assigned_dept": null,
  "proposal_id": null
}
```

---

## 5. Routing Rules

| Budget | Feasibility | Action |
|--------|-------------|--------|
| $10k+ | Any | Notify CEO immediate + auto-propose |
| $2k-10k | â‰¥7 | Auto-propose â†’ operations approval |
| $500-2k | â‰¥5 | Auto-propose â†’ ops handles |
| <$500 | Any | Standard SOP â€” ops team |
| Any | <4 | Flag: "Skill gap" â†’ R&D dept evaluate |

---

## 6. Files & Paths

| File | Má»¥c Ä‘Ã­ch |
|------|---------|
| `shared-context/client_intake/` | ThÆ° má»¥c lÆ°u táº¥t cáº£ intake records |
| `shared-context/client_intake/_index.json` | Index táº¥t cáº£ intakes |
| `shared-context/brain/corp/proposals/` | Proposals auto-generated |
| `shared-context/brain/corp/escalations.md` | CEO escalations |

---

*Channel configs: xem `REMOTE/claws/nullclaw/configs/client_gateway.json`*
*Sau khi intake: trigger `PROPOSAL_ENGINE_SOP.md`*

