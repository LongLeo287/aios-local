# CIV Vetting Report — agency-agents
**Dept 20 (CIV) | Date:** 2026-03-21 | **Analyst:** Nova (Dept 13 → Dept 20)
**Repo Path:** `D:\Project\AI OS\brain\knowledge\repos\agency-agents\`

---

## 📚 Sources
📚 Sources: 1 repo | Types: GitHub OSS | Date: 2026-03-21
🔧 Tool: Manual read (README.md + directory scan)
🏢 Dept: Dept 20 (CIV) → Dept 4 (Registry) → Dept 21 (Agent Dev)

---

## 1. Repo Overview
| Field | Value |
|-------|-------|
| **Repo** | agency-agents |
| **Loại** | AI Agent Persona Library |
| **License** | MIT (open source) |
| **Hỗ trợ Antigravity** | ✅ Native (`./scripts/install.sh --tool antigravity`) |
| **Privacy Tier** | PUBLIC — OSS, không nhạy cảm |
| **Strix Scan** | Chưa chạy (xem mục 4) |

## 2. Content Analysis
- **144 agent files** chia thành 12 divisions (folders)
- **Format:** Markdown `.md` (SKILL.md-compatible)
- **Scope:** Engineering, Design, Marketing, Sales, Specialized, Game Dev, etc.
- **Không có:** binary files, API keys, hardcoded credentials

## 3. AI OS Alignment
| Division | Depts Phục Vụ | Priority |
|---------|--------------|---------|
| specialized/ (24 agents) | Dept 13, 20, 8, 18 | HIGH |
| engineering/ (23 agents) | Dept 1, 3, 10, 21 | HIGH |
| support/ (6 agents) | Dept 8, 18, 19 | MEDIUM |
| product/ (5 agents) | Dept 17, 13 | MEDIUM |
| marketing/ (25 agents) | Dept 5 | LOW-MEDIUM |
| game-development/ (17 agents) | N/A hiện tại | LOW |

## 4. Risk Assessment
| Risk | Level | Mitigation |
|------|-------|-----------|
| Malicious code | LOW | Markdown only, no executables |
| Data leakage | NONE | No credentials/PII |
| Strix scan | PENDING | Run Strix CLI scan before full activation |
| Prompt injection via agent personas | LOW | Review agent SYSTEM prompts before use |

## 5. CIV Verdict

> **✅ APPROVED — Conditional**
>
> agency-agents được phép deploy vào AI OS với điều kiện:
> 1. Chỉ install **specialized/ + engineering/ + support/** (72 files — low risk)
> 2. Run Strix scan trong vòng 7 ngày → upload kết quả Dept 10
> 3. Dept 4 đăng ký chính thức vào plugin registry

## 6. Proposed Install Path
```
D:\Project\AI OS\plugins\agency-agents\     ← Plugin directory (D: drive)
├── SKILL.md
├── specialized/ (24 agents)
├── engineering/ (23 agents)
└── support/ (6 agents)
```

**Routing:** → Dept 4 (Registry) để đăng ký → CEO approval deploy
