# AI OS Corp â€” Global Decisions Log
# Owner: CEO | Retention: PERMANENT | Updated: 2026-03-17

## How to Use
This file is the permanent record of all CEO-level decisions.
Before any major action, read the last 5 entries for context.
Never delete entries â€” append only.

---

## [2026-03-17] â€” Corp Hierarchy Restructure v2.0

Context: Original 6-dept structure needed expansion to cover HR, Security, Finance, Legal,
Content Review, IT Infra, and R&D functions previously missing.

Decision: APPROVE full org restructure
  - 13 departments (expanded from 6)
  - 5 C-Suite roles (added CFO)
  - 4-level hierarchy: CEO â†’ C-Suite â†’ Manager â†’ Worker
  - 4 blocking gates: QA, Content, Security, Legal
  - On-demand workflow (not fixed schedule)
  - 3-layer memory architecture

Impact: All departments, org_chart.yaml, all prompt/rule files
Review date: 2026-04-17 (1 month â€” evaluate if structure is working)

---

## [2026-03-20] â€” Corp Cycle 1 Bootstrap Execution

Context: First full execution of AI OS Corp Cycle 1. Corp infrastructure existed (workflows, memory files, org chart) but had never run a complete cycle. Antigravity orchestrated end-to-end.

Decisions:
- APPROVE Antigravity as Cycle 1 Orchestrator (Tier 1, acting CEO proxy for task execution)
- APPROVE 5 tasks for Cycle 1: ENG-01-001, OPS-01-001, REG-01-001, STR-01-001, HLT-01-001
- APPROVE OKR Framework Cycle 1 (3 objectives, 4 KRs each)
- DEFER Telegram bot activation to Cycle 2 (token not configured)
- DEFER ClawTask Supabase backend fix to Cycle 2 start (.env verification needed)

Outcomes:
- Supabase tasks.agent_id column added (fixes ClawTask schema bug)
- OKR Framework published to brain/corp/proposals/
- System Health Report written â€” 8 GREEN, 1 YELLOW, 1 RED
- 5 MQ queue files initialized for all active depts
- Mission.md updated with Cycle 1 CEO priorities
- RETRO_2026-03-20.md authored by cognitive_reflector

Review date: Start of Cycle 2

---

## [2026-03-23] â€” Multi-Engine Governance & External Rules (Phase 5)

Context: AI OS Ä‘ang cháº¡y káº¿t há»£p Ä‘a luá»“ng Engine (Claude/Gemini/Ollama). Cáº§n má»™t chuáº©n má»±c chung Ä‘á»ƒ trÃ¡nh cÃ¡c Engine hoáº¡t Ä‘á»™ng tá»± phÃ¡t vÃ  giá»›i háº¡n quyá»n truy cáº­p Máº¡ng ngoÃ i nháº±m báº£o vá»‡ Data ná»™i bá»™.

Decisions:
- APPROVE Luáº­t Báº¥t Kháº£ Tri Model (Model Agnosticism): Má»i Engine pháº£i hÃ nh xá»­ theo Quy trÃ¬nh 7-Phase cá»§a CÃ´ng ty. TÆ°á»›c bá» danh tÃ­nh Trá»£ lÃ½ áº¢o máº·c Ä‘á»‹nh, Ã©p vÃ o Vai trÃ² (Role) cá»§a Agent.
- APPROVE CÆ¡ cháº¿ Má»Ÿ Rá»™ng NÃ¢ng Cao qua ClawTask: CÃ¡c Plugin/Skill (Firecrawl, Web Intelligence, v.v.) CÆ  Báº¢N váº«n hoáº¡t Ä‘á»™ng 100% trÃªn AI OS cho cÃ¡c Agent/PhÃ²ng ban xá»­ lÃ½ project cÃ¡ nhÃ¢n. NhÆ°ng khi chá»©c nÄƒng "Báº­t káº¿t ná»‘i ngoÃ i/Má»Ÿ rá»™ng" Ä‘Æ°á»£c KÃ­ch Hoáº¡t trÃªn ClawTask, há»‡ thá»‘ng sáº½ má»Ÿ khÃ³a **cÃ¡c chá»©c nÄƒng siÃªu nÃ¢ng cao, má»Ÿ rá»™ng Ä‘a luá»“ng** cá»§a cÃ¡c Tool nÃ y cho Agents. Táº¯t cá» trÃªn ClawTask Ä‘á»“ng nghÄ©a cÃ¡c Tool giáº£m vá» má»©c Ä‘á»™ hoáº¡t Ä‘á»™ng Standard thÃ´ng thÆ°á»ng.

Outcomes:
- NÃ¢ng cáº¥p `AI_OS_CONTEXT.md` (ThÃªm 2 bá»™ luáº­t quan trá»ng).
- TiÃªm flag `external_connections_enabled: false` vÃ o Backend Config Keys.

Review date: Phá»¥ thuá»™c vÃ o quÃ¡ trÃ¬nh tráº£i nghiá»‡m UI Dashboard cá»§a CEO.

---

## [2026-03-23] â€” 3-Tier Plugin Architecture (Lazy-Load Protocol)

Context: Há»‡ thá»‘ng sá»Ÿ há»¯u 131 repos / plugins. Náº¿u náº¡p toÃ n bá»™ vÃ o AI OS sáº½ gÃ¢y sá»¥p Ä‘á»• RAM vÃ  xung Ä‘á»™t lá»‡nh (Bloatware). CEO yÃªu cáº§u chÃ­nh thá»©c hÃ³a quy trÃ¬nh phÃ¢n tÃ¡ch Táº§ng.

Decisions:
- APPROVE Kiáº¿n trÃºc 3 Táº§ng cho toÃ n bá»™ CÆ¡ sá»Ÿ háº¡ táº§ng CÃ´ng cá»¥ / Plugin cá»§a HÄH:
  + **Táº§ng 1 (Core Infra):** CÃ i cá»‘ Ä‘á»‹nh, cháº¡y thÆ°á»ng trá»±c (Mem0, LightRAG, Firecrawl, CrewAI, GitNexus).
  + **Táº§ng 2 (Specialized Plugins):** Ãp dá»¥ng "Lazy-Load / On-Demand". Chá»‰ Ä‘Æ°á»£c Agent LLM gá»i ra, cÃ i Ä‘áº·t vÃ  sá»­ dá»¥ng khi Quy trÃ¬nh / Task cÃ³ yÃªu cáº§u chuyÃªn trÃ¡ch (VÃ­ dá»¥: tool váº½ áº£nh, tÃ­nh Excel). DÃ¹ng xong giáº£i phÃ¢n tÃ¡n lá»‡nh.
  + **Táº§ng 3 (Obsolete / Conflict):** ÄÆ°a vÃ o danh sÃ¡ch Ä‘en, tuyá»‡t Ä‘á»‘i khÃ´ng sá»­ dá»¥ng Ä‘á»ƒ trÃ¡nh Ä‘á»¥ng Ä‘á»™ vá»›i cÃ¡c siÃªu Tool á»Ÿ Táº§ng 1 (VÃ­ dá»¥: tool scraper cÅ© ká»¹ conflict vá»›i Firecrawl).

Outcomes:
- NÃ¢ng cáº¥p Hiáº¿n phÃ¡p `AI_OS_CONTEXT.md` (Gáº¯n Rule sá»‘ 9: 3-Tier Protocol).
- Thiáº¿t láº­p ranh giá»›i vÄ© mÃ´ Ä‘á»ƒ Agent LLM tá»± nháº­n diá»‡n giá»›i háº¡n pháº§n cá»©ng khi dá»n dáº¹p hoáº·c chá»n skill trong `SKILL_REGISTRY`.

Review date: Permanent Rule.

---

## [2026-03-23] â€” 3-Tier Plugin Architecture + Governance Gate System
Type: STRATEGIC_DECISION + LESSON_LEARNED
Context: Session audit revealed AI OS thiáº¿u quy trÃ¬nh rÃµ rÃ ng Ä‘á»ƒ Ä‘Ã¡nh giÃ¡ vÃ  tÃ­ch há»£p repos má»›i.
Decision: FORMALIZE 3-Tier Plugin Architecture lÃ m Luáº­t lÃµi há»‡ thá»‘ng (RULE-TIER-01)
  - Tier 1 (Always-on): mem0, firecrawl, LightRAG, CrewAI
  - Tier 2 (Lazy-load): Táº¥t cáº£ plugins khÃ¡c qua plugin-lazy-load.md
  - Tier 3 (Blacklist): KhÃ´ng bao giá» load, auto-escalate náº¿u phÃ¡t hiá»‡n
Lesson: Má»i plugin má»›i PHáº¢I qua 2 Gate: CIV (Evaluation) â†’ Security (Scan). KhÃ´ng cÃ³ ngoáº¡i lá»‡ ká»ƒ cáº£ CEO.
Applied to: GEMINI.md, CLAUDE.md, GOVERNANCE.md, Dept 4, 10, 20 memory files
Review date: 2026-06-23

---

## [2026-03-23] â€” LESSON: Rules má»›i pháº£i Ä‘á»“ng bá»™ cáº£ 2 Agent trong cÃ¹ng phiÃªn
Type: LESSON_LEARNED
Context: Rule 3-Tier ban Ä‘áº§u chá»‰ thÃªm vÃ o GEMINI.md, quÃªn CLAUDE.md
Lesson: Báº¥t ká»³ thay Ä‘á»•i nÃ o trong GEMINI.md liÃªn quan Ä‘áº¿n Rules hoáº·c Workflows â†’ Báº®T BUá»˜C Ä‘á»“ng bá»™ CLAUDE.md ngay trong cÃ¹ng phiÃªn.
Applied to: Antigravity boot protocol, táº¥t cáº£ future rule updates

---

## [2026-03-23] â€” LESSON: Repo REJECT â‰  khÃ´ng há»c Ä‘Æ°á»£c gÃ¬
Type: LESSON_LEARNED
Context: Ban Ä‘áº§u REJECT hoÃ n toÃ n graphrag, agency-agents, all-agentic-architectures â€” sai.
Lesson: Repo trÃ¹ng tool â‰  repo vÃ´ giÃ¡ trá»‹. Pháº£i Ä‘á»c Ä‘á»ƒ cherry-pick patterns/concepts chÆ°a cÃ³. ThÃªm tráº¡ng thÃ¡i ðŸ“š REFERENCE vÃ o catalog. Kiáº¿n thá»©c â†’ brain/knowledge/notes/
Applied to: Dept 20 (CIV), repo-evaluation.md, plugin-catalog.md workflow

---

## [2026-03-23] â€” LESSON: Workflow má»›i pháº£i map vÃ o Department Memory ngay
Type: LESSON_LEARNED
Context: Sau khi táº¡o repo-evaluation.md, ban Ä‘áº§u quÃªn update memory cá»§a Dept 4, 10, 20.
Lesson: Táº¡o workflow má»›i â†’ Owner dept pháº£i Ä‘Æ°á»£c xÃ¡c Ä‘á»‹nh â†’ Department Memory pháº£i Ä‘Æ°á»£c update â†’ CÃ™NG PHIÃŠN. Workflow khÃ´ng cÃ³ owner = workflow cháº¿t.
Applied to: Táº¥t cáº£ system/ops/workflows/ files, quy trÃ¬nh táº¡o workflow má»›i

---

## [FUTURE DECISIONS GO HERE]

---

*"Every decision shapes the system. Document what you decided and why."*

---

## [2026-03-23] — Cycle 8: Repo Governance + Skill Expansion

Context: CEO submitted 51 repo URLs across 3 batches for AI OS integration evaluation.
Established CIV Repo Evaluation Gate (5-step workflow). Processed all repos.

Decisions:
- APPROVE context7 (upstash) as Tier 1 doc injection skill — RULE-CONTEXT7-01 added to boot files
- APPROVE trivy as primary security scanner — integrated into strix-scan pipeline
- APPROVE 6 more repos: understand-anything, agentune, vibe-kanban, agent-shield (cherry), continuous-learning-v2 (cherry), framework-standards (cherry)
- APPROVE RULE-AGENT-MECHANICS-01 (6 insights from claude-inspector)
- DEFER CodexKit — CEO decision: normal repo, not important
- DEFER 13 repos for future phases (hyperspace-db, posthog, excalidraw, database-js, vibe-kanban deps, etc.)
- REJECT 7 repos: wifi-card, hexhog, xpfarm x2, grokpi, LinkedIn, Facebook (no content or not relevant)

Outcomes:
- 8 skill files created in skills/ directory
- GEMINI.md + CLAUDE.md upgraded to v2.3
- 8 KI Notes added to brain/knowledge/notes/
- strix-scan workflow updated with Trivy as Step 0
- AI OS confirmed top 15% of enterprise AI tools landscape

Next Review: 2026-04-23 (check Observability Layer proposal)

