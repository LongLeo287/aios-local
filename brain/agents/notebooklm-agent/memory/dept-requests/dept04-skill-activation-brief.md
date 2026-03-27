# Dept 4 — Priority Skills Activation Brief
# Agent: Nova | Date: 2026-03-21 | Source: awesome-agent-skills KI

## Mục đích
Kích hoạt các skills được Nova đánh giá ưu tiên cao cho AI OS. Tất cả skills phải qua Strix vetting (Dept 10 / Dept 20 CIV) trước khi deploy.

---

## TIER 1 — Activate Immediately (Sau khi Strix vetting)

### 1. anthropics/pdf
- **Mô tả**: PDF intake & analysis skill từ Anthropic chính thức
- **URL**: Từ awesome-agent-skills catalog → Anthropic section
- **Ứng dụng**: Nova CEO Standing Order — xử lý PDF CEo gửi
- **Strix required**: ✅ LOW RISK (official Anthropic)
- **Target dept**: Dept 13 (Nova) + Dept 20 (CIV)

### 2. anthropics/mcp-builder
- **Mô tả**: Skill giúp xây dựng MCP servers mới
- **Ứng dụng**: Dept 8 (Ops) — mở rộng MCP cluster AI OS
- **Strix required**: ✅ LOW RISK (official)
- **Target dept**: Dept 8 (Ops), Dept 21 (Agent Dev)

### 3. anthropics/webapp-testing
- **Mô tả**: Playwright-based webapp testing skill
- **Ứng dụng**: Dept 9 (QA) — kiểm thử tự động
- **Target dept**: Dept 9 (QA), Dept 1 (Engineering)

### 4. anthropics/docx / pptx / xlsx
- **Mô tả**: Document creation skills (Word, PowerPoint, Excel)
- **Ứng dụng**: Báo cáo cho CEO, presentations cho các depts
- **Strix required**: LOW RISK
- **Target dept**: All departments

---

## TIER 2 — Security Domain (Dept 10 Priority)

### 5-26. trailofbits/* (22 skills)
- **Mô tả**: Security audit skills từ Trail of Bits — top security firm
- **Includes**: Semgrep integration, smart contract audit, static analysis, fuzzing
- **⚠️ STRIX REQUIRED**: MID RISK — external org, but reputable
- **Vetting note**: Review từng skill riêng lẻ vs. blanket approval
- **Target dept**: Dept 10 (Security/Strix), Dept 20 (CIV vetting pipeline)

**Key skills trong batch:**
| Skill | Use Case |
|-------|----------|
| `semgrep-rules` | Code scanning for AI OS repos |
| `security-audit` | Full audit of plugins before activation |
| `smart-contracts` | Web3 bots (nếu AI OS có Dept liên quan) |
| `static-analysis` | Pre-commit checks toàn bộ code |

### 27. openai/security-threat-model
- **Mô tả**: Threat model generator cho repos
- **Ứng dụng**: Strix protocol — bổ sung threat modeling step
- **Strix required**: LOW-MID RISK

### 28. getsentry/code-review
- **Mô tả**: Automated code review via Sentry
- **Ứng dụng**: Dept 9 (QA) + Dept 10 pre-activation review
- **Strix required**: LOW RISK

---

## TIER 3 — Department-Specific Skills

### Marketing (Dept 5)
- `coreyhaines31/*` (32 skills): SEO, CRO, copywriting, landing pages
- `phuryn/*` (15+ skills): Go-to-market, pricing strategy, user research

### Strategy (Dept 3)
- `deanpeters/*` (15+ skills): PM strategy, discovery, roadmap, OKRs

### Infrastructure (Dept 8)
- `hashicorp/terraform-code-gen` — Infrastructure as Code generation
- `hashicorp/terraform-module-generator` — Module scaffolding

### Developer Productivity
- `openai/figma-implement-design` — Figma → code (Dept 1)
- `openai/playwright` — Browser automation (Dept 9)
- `openai/notion-knowledge-capture` — Chats → Notion wiki (Nova)

---

## Activation Workflow

```
Nova identifies → Submit to Dept 20 (CIV vetting) 
→ Dept 10 (Strix security scan) 
→ Dept 4 (Registry approval + capability mapping)
→ Deploy to plugin stack
→ Nova updates REGISTER.md + hot-cache
```

## Action Items for Dept 4
- [ ] Tạo activation request cho 4 Anthropic skills (Tier 1)
- [ ] Queue 22 trailofbits skills cho Strix batch vetting
- [ ] Map skills → department capability matrix
- [ ] Update Plugin Registry sau khi approve
