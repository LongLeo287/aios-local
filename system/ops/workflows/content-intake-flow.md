# Department: content_intake
# Content Intake & Vetting — Intake Flow
# Version: 1.4 | Updated: 2026-03-27
# Owner: content_intake dept (intake-chief-agent)
# Change v1.4: +PENDING_REPOS.md role clarification | +RULE-CIV-02 PENDING gate | +STEP 6 CLEANUP
# Change v1.2: +Phase 0 Local-First Check | +Step 3.5 Gap Detection | +Step 3.6 GAP PROPOSAL ENGINE
# Coordinate: security_grc (repo vetting) | asset_library (knowledge) | registry (code)

---

## FULL PIPELINE MAP

```
╔══════════════════════════════════════════════════════════════╗
║              CONTENT INTAKE & VETTING PIPELINE  v1.3         ║
╚══════════════════════════════════════════════════════════════╝

USER / AGENT PROVIDES INPUT
(Thả tay bất cứ định dạng nào: Link Repo, URL, Document, PDF, Post, Hình ảnh)
            OR
BATCH INPUT FROM VAULT:
  storage/vault/DATA/PENDING_REPOS.md  ← Hàng đợi chờ CIV review (CHƯA được phép clone!)
  storage/vault/DATA/ACTIVE_REPOS.md   ← Đã qua CIV + CEO approve → được phép clone & ingest
  storage/vault/DATA/Github.txt        ← Raw links chưa phân loại

⚠️ RULE-CIV-02 — PENDING GATE:
  PENDING_REPOS.md = WAITING ROOM. Repo ở đây CHƯA được phân tích.
  NGHIÊM CẤM clone repo từ PENDING thẳng vào brain/QUARANTINE mà không qua CIV Review.
  Luồng bắt buộc: PENDING → CIV Analysis → CEO/intake-chief APPROVE → ACTIVE_REPOS.md → clone & ingest.

🚨 RULE TỐI THƯỢNG: Ngay khi nhận được mọi thể loại Input, hệ thống phải TỰ ĐỘNG CHẠY, TỰ ĐỘNG NHẬN, TỰ ĐỘNG PHÂN TÍCH và Cuối Cùng TỰ ĐỘNG NHẢ BÁO CÁO chuẩn "FORMAT 6 — Dashboard Analytics Report" (Xem presentation-protocol.md).
            │
            ▼
┌─────────────────────┐
│   PHASE 0 LOCAL     │  ← LightRAG query + INDEX.md check (NEW v1.2)
│   CHECK (ANTIGRAV)  │  ← FOUND? Return KI. NOT FOUND → continue
└─────────────────────┘
            │ NOT FOUND
            ▼
┌─────────────────────┐
│    intake-agent     │  ← Creates CIV ticket, stages to /incoming/
│  [GATE: TICKET]     │
└─────────────────────┘
            │
            ▼
┌─────────────────────┐
│  classifier-agent   │  ← Tags type: REPO/WEB/DOC/IMAGE/TEXT/PLUGIN
│  [GATE: CLASSIFY]   │
└─────────────────────┘
            │
    ┌───────┴──────────────────────────────┐
    │                                      │
    ▼                                      ▼
REPO / PLUGIN                     OTHER CONTENT
(SEC path)                        (CONTENT path)
    │                                      │
    ▼                                      │
┌──────────────────┐              ┌────────┴────────┐
│ repo-fetcher     │              │WEB_CONTENT       │
│ clone to         │              │ → web-crawler    │
│ /incoming/repos/ │              │                  │
└──────────────────┘              │DOCUMENT (PDF/Doc)│
    │                             │ → doc-parser     │
    ▼                             │                  │
┌──────────────────────────────┐  │IMAGE             │
│ SECURITY GRC (strix-agent)   │  │ → staging to     │
│ runs vet_repo.ps1            │  │   /incoming/imgs/│
│ 12-stage Strix scan          │  │                  │
│                              │  │TEXT/CONFIG       │
│ FAIL → REJECTED + BLACKLIST  │  │ → staging to     │
│ WARN → intake-chief REVIEW   │  │   /incoming/text/│
│ PASS → /vetted/repos/        │  └────────┬────────┘
└──────────────────────────────┘           │
    │ PASS                                  ▼
    │                             ┌──────────────────────┐
    ▼                             │ content-validator    │
┌──────────────────────────────┐  │ Score 1-10           │
│ ★ STEP 3.5 — NotebookLLM    │  │ Score 1-10           │
│   Content Analysis (v1.2)    │  │ < 4 → REJECTED       │
│                              │  │ ≥ 4 → /vetted/       │
│ Tool: open-notebook          │  └──────────┬───────────┘
│ Input: gitingest digest      │             │
│                              │             │
│ Questions (6 total v1.2):    │             │
│ • "Repo này làm gì?"         │             │
│ • "Conflict với hệ thống?"   │             │
│ • "Route về phòng nào?"      │             │
│ • "Chất lượng / rủi ro?"     │             │
│ • "Domain này AI OS đã có    │             │
│    agent/dept nào không?"    │             │
│ • "Đề xuất agent/dept mới    │             │
│    nếu chưa có?"             │             │
│                              │             │
│ Output: CIV Analysis Report  │             │
│   APPROVED  → /vetted/       │             │
│   REVIEW    → intake-chief   │             │
│   REJECTED  → /rejected/     │             │
│   GAP FOUND → Step 3.6 ★    │             │
└──────────────────────────────┘             │
            │ GAP FOUND
            ▼
┌──────────────────────────────┐
│ ★ STEP 3.6 — GAP PROPOSAL   │
│   ENGINE (ANTIGRAVITY)       │
│ Domain mới, chưa có agent?   │
│ → CEO Proposal [A/B/C/D]     │
│ A: Tạo agent-auto-create.md  │
│ B: Mở rộng dept hiện có      │
│ C: Tạo dept/group mới        │
│ D: Archive global            │
└──────────────────────────────┘
    │ APPROVED                               │
    └──────────────┬─────────────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  ingest-router      │
        │  [GATE: ROUTE]      │
        └─────────────────────┘
                   │
    ┌──────────────┼──────────────────────┐
    │              │                      │
    ▼              ▼                      ▼
Registry &    Asset & Knowledge        assets/
Capability    Library                  (images)
(code/plugins) (knowledge/docs/web)   → asset-tracker

                   │
                   ▼
           TICKET → INGESTED ✓
           Receipt written to destination agent
```

---

## INTAKE TICKET LIFECYCLE

```
LOCAL_HIT (return existing KI, no ticket needed)
     OR
RECEIVED → CLASSIFYING → VETTING → VALIDATING → ROUTING → INGESTED → CLEANED
                                              ↘
                                           REJECTED (any stage) → CLEANED_REJECTED
                         ↘
                      GAP_PROPOSED (parallel, non-blocking)
```

---

## WORKFLOW STEPS

### STEP 0 — Local-First Check ★ NEW v1.2
Trigger: Bất kỳ input nào — TRƯỚC KHI tạo CIV ticket
Agent: `ANTIGRAVITY` (Tier 1)
Skill: `smart_memory`, `LightRAG` (localhost:9621)
Actions:
- Query LightRAG: `rag.hybrid_query("<source URL or topic>", mode="mix")`
- Kiểm tra `brain/knowledge/INDEX.md` có source URL / domain không
- Chạy `system/ops/scripts/staleness_check.py <URL>` để tự động quyết định lấy dữ liệu:

Kết quả:
  UNCHANGED (No update / Known URL):
    → Trả về KI đã có cho user/agent
    → STOP (không tạo ticket, tiết kiệm băng thông)
  CHANGED (New or updated content):
    → Tiếp tục STEP 1 (tạo CIV ticket bình thường)

SLA: < 30 giây (local query)

---

### STEP 1 — Receive Input
Trigger: User/agent provides URL, file path, or content body
Agent: `intake-agent`
Actions:
- Create CIV-[DATE]-[SEQ] ticket in QUARANTINE/logs/intake_log.md
- Stage to QUARANTINE/incoming/ (temp folder by type)
- Set ticket status: RECEIVED
- Call classifier-agent

SLA: Immediate (synchronous)

---

### STEP 2 — Classify
Trigger: intake-agent hands off ticket
Agent: `classifier-agent`
Actions:
- Inspect content type (URL pattern, file extension, content body)
- Assign tag: REPO | WEB_CONTENT | DOCUMENT | IMAGE | TEXT | CONFIG | PLUGIN
- Update ticket with classification
- Route to correct pipeline branch
- Unknown → /incoming/unclassified/ + alert intake-chief-agent

SLA: < 5 minutes

---

### STEP 3A — Repo/Plugin Path
Trigger: classifier tag = REPO or PLUGIN
Agent: `repo-fetcher-agent` then `security-scanner` (Security GRC)
Actions:
- repo-fetcher: git clone (depth=1) into QUARANTINE/incoming/repos/<name>/
  - ⚠️ TIMEOUT RULE (v1.3): Giới hạn clone tối đa 120s. Nếu vượt quá, tự động SKIP repo, ghi log vào `skipped` list, và XÓA (rmtree) thư mục clone dở dang để chống bloat rác ổ cứng.
- Hand off to security-scanner: run vet_repo.ps1 (12-stage scan)
- strix-agent review _VET_REPORT.md
- PASS → move to QUARANTINE/vetted/repos/ → STEP 3.5
- WARN → hold, notify intake-chief-agent for manual review
- FAIL → move to QUARANTINE/rejected/ + log to rejected_log.md → CLOSED

SLA: < 1 corp cycle

---

### STEP 3.5 — NotebookLLM Content Analysis ★ UPGRADED v1.2
Trigger: Security scan PASS (REPO/PLUGIN path)
Agent: `content-analyst-agent` using `open-notebook` (port 5055, local)
Actions:
- Run gitingest on repo → convert to text digest
- Load digest into open-notebook
- Query **6 standard CIV questions** (v1.2 — thêm 2 câu gap detection):
  1. "Repo/plugin này làm gì? Mô tả chính xác purpose."
  2. "Có conflict hoặc overlap với tools đã có trong AI OS không?"
  3. "Phòng ban nào nên sử dụng repo này?"
  4. "Rủi ro nội dung: có sensitive data, suspicious logic, hoặc quality issues nào không?"
  5. ★ NEW: "Domain này (kỹ năng/lĩnh vực) AI OS đã có agent hoặc dept phụ trách chưa?" ← gap detection
  6. ★ NEW: "Nếu chưa có, đề xuất tên agent hoặc dept mới phù hợp nhất?"
- Generate CIV Analysis Report → save to QUARANTINE/vetted/repos/<name>/_CIV_ANALYSIS.md
  - **MANDATORY FORMAT:** Report phải xuất theo định dạng C-Suite (NO MARKDOWN HEADINGS, Dùng In hoa + Emoji, thuần ASCII) đúng chuẩn `presentation-protocol.md`.
- Decision:
  - APPROVED + no gap (score ≥ 7/10) → STEP 5
  - APPROVED + gap found (score ≥ 7/10) → STEP 3.6 (GAP PROPOSAL) → STEP 5
  - REVIEW (score 4-6) → intake-chief-agent manual review
  - REJECTED (score < 4) → move to /rejected/ → CLOSED

Output fields:
  purpose, conflicts[], recommended_dept, quality_score, risk_notes, verdict,
  gap_detected (bool), gap_domain, proposed_agent, proposed_dept

SLA: < 15 minutes per repo

---

### STEP 3.6 — GAP PROPOSAL ENGINE ★ NEW v1.2
Trigger: Step 3.5 output có `gap_detected = true`
Agent: `ANTIGRAVITY` (Tier 1 — escalate CEO decision)
Skill: `proposal_engine` + `reasoning_engine`

Actions:
1. Đọc `gap_domain` và `proposed_agent` từ _CIV_ANALYSIS.md
2. Cross-check với `corp/org_chart.yaml` + `brain/knowledge/CAPABILITY_MAP.md`
3. Xác nhận gap thực sự chưa có agent/dept cover
4. Tạo GAP PROPOSAL gửi CEO qua `notification_bridge` (Telegram):

```markdown
## 🔭 GAP DETECTED — CIV-<id> — <date>

**Source:** <repo_url>
**Gap domain:** <domain>
**Lý do:** Không có agent/dept nào cover domain "<domain>" này

**AI OS hiện có gần nhất:**
- Dept X (match ~60%) — scope: <mô tả>

**Đề xuất:**
[A] Tạo agent: `<domain>-agent` → ops/workflows/agent-auto-create.md
[B] Mở rộng Dept X thêm sub-domain "<domain>"
[C] Tạo Dept/Group mới (nếu domain đủ lớn ≥ 3 KI)
[D] Archive global — không assign dept cụ thể

**CEO chọn A/B/C/D → tiếp tục intake:**
```

5. Sau khi CEO chọn:
   - A → khởi động `agent-auto-create.md` (async — không block intake)
   - B/C → update `corp/org_chart.yaml` + `AGENTS.md` (async)
   - D → ghi vào `brain/knowledge/global/`
   - Mọi option → tiếp tục STEP 5 (intake không bị block)

Output: GAP_REPORT ghi vào `corp/gaps/GAP-<date>-<domain>.md`
SLA: Proposal gửi CEO < 5 phút | CEO response không bắt buộc để tiếp tục intake

---

### STEP 3B — Web Content Path
Trigger: classifier tag = WEB_CONTENT
Agent: `web-crawler-agent`
Actions:
- Fetch URL content (text + metadata)
- Check: no malicious redirects, no injected scripts
- Convert to markdown: QUARANTINE/incoming/web/<slug>.md
- Pass to content-validator-agent → STEP 4

SLA: < 10 minutes per URL

---

### STEP 3C — Document Path
Trigger: classifier tag = DOCUMENT (PDF, DOCX, MD)
Agent: Security GRC (strix-agent) + `doc-parser-agent`
Actions:
- strix-agent runs `system/security/vet_media_docs.py` (MANDATORY)
- FAIL → move to QUARANTINE/rejected/ + BLACKLIST
- PASS → doc-parser-agent extract: title, date, author, full text
- Structure as markdown: QUARANTINE/incoming/documents/<name>.md
- Pass to content-validator-agent → STEP 4

SLA: < 15 minutes per document

---

### STEP 3D — Image Path
Trigger: classifier tag = IMAGE
Agent: Security GRC (strix-agent) + `content-validator-agent`
Actions:
- strix-agent runs `system/security/vet_media_docs.py` (Check Magic Bytes for Steganography/Polyglots)
- FAIL → move to QUARANTINE/rejected/ + BLACKLIST
- PASS → Stage to QUARANTINE/incoming/images/<name>
- content-validator checks: verify safe imagery
- PASS → QUARANTINE/vetted/assets/ → STEP 5

SLA: < 5 minutes

---

### STEP 4 — Content Validation (non-repo)
Trigger: web-crawler, doc-parser, or direct text staging completes
Agent: `content-validator-agent`
Actions:
- Score content quality (1-10): relevance, accuracy, safety, SOUL.md alignment
- Score < 4 → REJECTED + log reason
- Score ≥ 4 → PASS → move to QUARANTINE/vetted/ → STEP 5
- Score ≥ 8 → flag for cosmic_memory (permanent retention candidate)

SLA: < 10 minutes

---

### STEP 5 — Route to Destination
Trigger: Content in /vetted/ with PASS status
Agent: `ingest-router-agent`
Actions:
- Match classification tag to destination (see Classification Table in rules.md)
- Move file from vetted/ to destination
- Write receipt to destination agent
- Update CIV ticket to INGESTED
- Confirm file exists at destination (verify)

Destinations (paths relative to <AOS_ROOT>):
  REPO/PLUGIN        → plugins/  OR  brain/skills/
  WEB_CONTENT        → brain/knowledge/web/
  DOCUMENT           → brain/knowledge/documents/
  IMAGE              → assets/images/
  TEXT               → brain/knowledge/text/
  CONFIG/RULES DOC   → corp/departments/<dept>/ or corp/rules/

Post-routing handoff:
  → After file lands at destination, ingest-router MUST trigger
    knowledge-distribution-flow.md STEP D1 by writing a receipt to:
    subagents/mq/asset_library_ingest.md (for WEB/DOCUMENT/TEXT)
    subagents/mq/registry_ingest.md     (for REPO/PLUGIN)
  → This receipt contains: { civ_ticket, content_type, destination_path, quality_score }

★ NEW v1.2 — Post-Route: skill-discovery-auto trigger
  IF content_type = REPO or PLUGIN:
    → registry-manager-agent runs skill-discovery-auto.md:
       Kiểm tra destination folder có SKILL.md chưa
       → Nếu không: auto-create SKILL.md (Skill Creator Ultra)
       → Rebuild FAST_INDEX.json
    Ref: ops/workflows/skill-discovery-auto.md

★ NEW v1.3 — Post-Route: Neural Link Graph Sync trigger
  TẤT CẢ Content nạp vào thành công (REPO, PLUGIN, DOCUMENT):
    → Archivist Agent chạy `neural-link-sync.md`.
    → Update `SYSTEM_INDEX.yaml` + `SYSTEM_INDEX_NARRATIVE.txt`.
    → Đảm bảo AI OS luôn biết vị trí của File/Repo mới.

SLA: < 5 minutes after content reaches /vetted/

---

### STEP 6 — QUARANTINE CLEANUP ⚡ (MANDATORY — RULE-QUARANTINE-01)
Trigger: STEP 5 hoàn tất (ticket status = INGESTED) HOẶC ticket status = REJECTED
Agent: `ingest-router-agent` (ngay sau khi ghi receipt xong)
Actions:
- **INGESTED path:**
  - Xóa toàn bộ: `QUARANTINE/incoming/<type>/<civ_ticket>/`
  - Xóa toàn bộ: `QUARANTINE/vetted/<type>/<civ_ticket>/`
  - ⚠️ GIỮ LẠI: `QUARANTINE/logs/intake_log.md` (chỉ log text, không phải repo)
  - ⚠️ GIỮ LẠI: `QUARANTINE/vetted/<name>/_CIV_ANALYSIS.md` (report nhỏ, không cần xóa)
- **REJECTED path:**
  - Xóa toàn bộ: `QUARANTINE/incoming/<type>/<civ_ticket>/`
  - Chuyển `QUARANTINE/vetted/<civ_ticket>/` → `QUARANTINE/rejected/` (log nhỏ)
- **Stale files (quá 7 ngày, không có ticket active):**
  - Xóa toàn bộ file/folder trong `QUARANTINE/incoming/` và `QUARANTINE/vetted/`
- Update ticket status: INGESTED → CLEANED | REJECTED → CLEANED_REJECTED

> ⚡ **RULE-QUARANTINE-01:** KHÔNG ĐƯỢC để repo nguyên trong QUARANTINE sau khi đã INGESTED.
> QUARANTINE chỉ là phòng tạm (staging area), KHÔNG phải nơi lưu trữ lâu dài.
> Vi phạm gây tích lũy hàng GB rác mỗi tuần, ảnh hưởng hiệu suất hệ thống.

SLA: Xóa ngay sau khi STEP 5 xác nhận file tồn tại tại destination

| Dept | Coordination |
|------|-------------|
| Security GRC | Co-authority on all REPO/PLUGIN vetting (vet_repo.ps1) |
| Registry & Capability | Destination for all REPO/PLUGIN after PASS |
| Asset & Knowledge Library | Destination for WEB/DOCUMENT/TEXT |
| Operations | Escalate CIV backlog issues to scrum-master |
| Monitoring & Inspection | Monitor CIV ticket queue for SLA breaches |

---

## ESCALATION PATH

| Issue | Escalation |
|-------|-----------|
| Unknown content type | intake-chief-agent manual review |
| WARN repo (borderline) | intake-chief → strix-agent joint review |
| FAIL repo (critical threat) | strix-agent → L3 (CEO) if sophisticated attack |
| CIV backlog > 5 tickets | intake-chief → COO |
| Destination agent not acknowledging | ingest-router → Monitoring dept |

---

### 🛡️ RULE-CIV-02: PENDING GATE STRICT ENFORCEMENT
Trạng thái `PENDING` trong `PENDING_REPOS.md` là trạng thái chờ. 
**NGHIÊM CẤM:**
1. Clone thẳng repo đang ở trạng thái `PENDING` vào bất kỳ thư mục nào trên đĩa cứng (kể cả `QUARANTINE`).
2. Tự động chuyển trạng thái từ `PENDING` sang `ACTIVE` mà không qua CIV Review.
3. Ghi dữ liệu/metadata (như nội dung README) của repo `PENDING` thẳng vào thư mục `brain/knowledge/repos` (Hành vi này Bypass hoàn toàn quá trình Intaking).

**Quy trình chuẩn cho RULE-CIV-02**:
1. AI/Agent dùng `system/ops/scripts/pending_civ_classifier.py` để phân tích tĩnh (URL, description) các repo `PENDING`. Script tạo report `CIV_PENDING_REPORT_*.md` với 3 danh sách: APPROVE, REVIEW, REJECT.
2. Sếp (CEO / Dept 20 Intake Chief) đọc report và quyết định.
3. Nếu đồng ý với list APPROVE, duyệt bằng script: `python system/ops/scripts/pending_civ_approve.py --auto-approve`. Lệnh này chuyển repo từ `PENDING` sang `ACTIVE`.
4. Chỉ khi repo nằm trong `ACTIVE_REPOS.md`, mới được phép kích hoạt `active_repos_pipeline.py` để thực hiện clone thật sự qua quy trình: `Github → QUARANTINE/incoming/repos → Strix Scan → brain/knowledge`.

> **Lưu ý ENFORCEMENT (2026-03-27)**: `batch_repo_intake.py` mode `pending` và `all` đã bị BLOCK TRÊN CODE (Sẽ báo lỗi và sys.exit(1)). Các chức năng tự động lấy nội dung từ Github bắt buộc chỉ được dùng trên repo đã APPROVED hoặc ACTIVE. Mọi script cũ bypass pipeline phải bị dừng chạy.

*(Phiên bản tài liệu 1.5 - Cập nhật ngày 2026-03-27)*
