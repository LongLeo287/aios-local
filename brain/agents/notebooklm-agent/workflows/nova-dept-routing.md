---
description: Nova — Dept Routing Workflow. Sau khi hoàn thành intake, route kết quả đến đúng phòng ban dựa trên insights trong synthesis.
dept: All Depts (22)
agent: Nova (notebooklm-agent)
version: "1.0"
updated: "2026-03-21"
---

# Nova — Dept Routing Workflow

## Routing Decision Matrix

Sau khi intake xong, đọc synthesis → xác định dept nào cần nhận:

| Nếu synthesis chứa... | Route đến | Action |
|-----------------------|-----------|--------|
| Code architecture, language, framework | Dept 1 (Eng) | Gửi tech brief |
| Testing, QA patterns | Dept 2 (QA) | Gửi test strategy |
| Security vulnerabilities, CVE | Dept 10 (Security) ⚠️ | LOCAL mode — gửi threat brief |
| Marketing hooks, copywriting | Dept 5 (Marketing) | Gửi content brief |
| Claims cần fact-check | Dept 7 (Content Review) | Gửi claim list |
| New plugin/skill/tool | Dept 4 (Registry) | Gửi eval request |
| Repo/plugin cần vetting | Dept 20 (CIV) | Gửi verdict request |
| Training pattern, learning | Dept 16 (OD&L) | Gửi learning guide |
| Agent capability gap | Dept 21 (Agent Dev) | Gửi gap report |
| Kiến thức mới cho AI OS | Dept 22 (Data Upgrade) | Gửi KI artifact |
| KPI, metrics, performance | Dept 18 (Monitoring) | Gửi metrics brief |
| Budget / cost implications | Dept 12 (Finance) LOCAL | Gửi cost analysis |
| Legal / IP / license | Dept 14 (Legal) LOCAL | Gửi legal brief |

## Cách gửi request đến dept

```
File: memory/dept-requests/dept[NN]-[name].md

Thêm dòng vào bảng Pending Requests:
| [YYYY-MM-DD] | [request description] | [HIGH/MED/LOW] | ⏳ Pending |
```

## Priority Rules

1. **CEO input** → luôn HIGH
2. **Security (Dept 10)** → luôn HIGH, LOCAL ONLY
3. **Legal (Dept 14)** → luôn HIGH, LOCAL ONLY
4. **1 input → nhiều dept** → gửi đến TẤT CẢ dept liên quan
5. **Không biết route nào** → Dept 22 (Data Upgrade) nhận mặc định

---

*Nova Dept Routing Workflow v1.0 | 2026-03-21*
