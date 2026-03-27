# neural-link-sync.md â€” Knowledge Graph & Registry Synchronization
# Version: 1.1 | Updated: 2026-03-26
# Department: [DEPT-07] KNOWLEDGE & REGISTRY CAPABILITY (Archivist Agent)
# Mode: EVENT-DRIVEN (Chá»‰ quÃ©t khi cÃ³ dá»¯ liá»‡u má»›i, tá»‘i Æ°u Quota/Context)
# Trigger: Cuá»‘i STEP 5 cá»§a `content-intake-flow.md` hoáº·c lá»‡nh thá»§ cÃ´ng `aos neural sync`

---

## 1. Má»¥c ÄÃ­ch (Purpose)
Báº£n Ä‘á»“ Kiáº¿n trÃºc ToÃ n cáº§u cá»§a AI OS (Neural Link) khÃ´ng thá»ƒ lÃ  má»™t tá»‡p cháº¿t. Báº¥t cá»© khi nÃ o cÃ³ Repo má»›i Ä‘Æ°á»£c náº¡p vÃ o qua quÃ¡ trÃ¬nh Intake, hoáº·c bá»‹ xÃ³a Ä‘i, há»‡ thá»‘ng pháº£i cáº­p nháº­t sÆ¡ Ä‘á»“ ngay láº­p tá»©c Ä‘á»ƒ cÃ¡c Trá»£ lÃ½ AI (Antigravity, Claude Code) khÃ´ng bá»‹ máº¥t phÆ°Æ¡ng hÆ°á»›ng.

Quy trÃ¬nh nÃ y hÆ°á»›ng dáº«n `Archivist Agent` cáº­p nháº­t Máº¡ng LÆ°á»›i Nháº­n Thá»©c 3D thÃ´ng qua Sá»• ÄÄƒng KÃ½ Tá»•ng (Master Registry) vÃ  NÃ£o bá»™ Cá»‘t lÃµi (LightRAG).

## 2. Quy TrÃ¬nh Cáº­p Nháº­t (Sync Routine)

**BÆ¯á»šC 1: XÃ¢y Dá»±ng Sá»• ÄÄƒng KÃ½ (Index Build)**
- Lá»‡nh thá»±c thi: `python "<AI_OS_ROOT>\system\ops\scripts\registry_indexer.py"`
- HÃ nh Ä‘á»™ng: QuÃ©t toÃ n cá»¥c táº¥t cáº£ Repo, Plugin, Tool á»Ÿ cáº£ 2 BÃ¡n Cáº§u (Local Core & Remote Ecosystem). Cáº­p nháº­t danh sÃ¡ch 300+ Entities vÃ o `<AI_OS_ROOT>\system\registry\SYSTEM_INDEX.yaml`.

**BÆ¯á»šC 2: Cáº¥p Dá»¯ Liá»‡u Ngá»¯ NghÄ©a (Narrative Feed)**
- Lá»‡nh thá»±c thi: `python "<AI_OS_ROOT>\system\ops\scripts\graph_feeder.py"`
- HÃ nh Ä‘á»™ng: Dá»‹ch tá»‡p cáº¥u hÃ¬nh tÄ©nh (YAML) thÃ nh vÄƒn báº£n ngá»¯ nghÄ©a há»c (Narrative Text) Ä‘á»ƒ mÃ¡y há»c RAG cÃ³ thá»ƒ láº­p báº£n Ä‘á»“. Xuáº¥t ra tá»‡p `SYSTEM_INDEX_NARRATIVE.txt`.

**BÆ¯á»šC 3: Dá»‡t Máº¡ng LÆ°á»›i (Graph Injection)**
- Lá»‡nh thá»±c thi: KÃ­ch hoáº¡t `LightRAG.insert` thÃ´ng qua Script hoáº·c Adapter vá»›i Ä‘áº§u vÃ o lÃ  tá»‡p Narrative vá»«a sinh ra.
- Káº¿t quáº£: KhÃ´ng gian 3D cá»§a há»‡ thá»‘ng Ä‘Æ°á»£c dá»‡t láº¡i thÃ nh cÃ´ng. AI cÃ³ thá»ƒ truy váº¥n `Ai thuá»™c nhÃ¡nh nÃ o, Ai káº¿t ná»‘i vá»›i Repo nÃ o`.

## 3. Quy Táº¯c Truy Xuáº¥t Cá»§a Agent (Retrieval Rules)
Táº¥t cáº£ cÃ¡c Agent khi nháº­n Task tá»« CEO (VÃ­ dá»¥: "HÃ£y má»Ÿ tool X", "Kiá»ƒm tra repo Y"):
1. Äá»ŒC `SYSTEM_INDEX.yaml`: Äá»ƒ láº¥y tá»a Ä‘á»™ tuyá»‡t Ä‘á»‘i mÃ  khÃ´ng cáº§n scan Ä‘Ä©a.
2. DÃ™NG `GitNexus MCP`: Náº¿u cáº§n Ä‘Ã o sÃ¢u xuá»‘ng cÃ¢y cáº¥u trÃºc AST cá»§a repo Ä‘Ã³.
3. Cáº¤M: Lá»‡nh `find` hoáº·c `ls -R` mÃ¹ má» gÃ¢y rÃ¡c bá»™ nhá»›.

---
> "Biáº¿t mÃ¬nh biáº¿t ta, trÄƒm tráº­n trÄƒm tháº¯ng. AI khÃ´ng biáº¿t mÃ¬nh Ä‘ang á»Ÿ Ä‘Ã¢u trong há»‡ thá»‘ng thÃ¬ chá»‰ lÃ  cá»— mÃ¡y vÃ´ dá»¥ng." - Kiáº¿n trÃºc sÆ° AI OS.

