# Nova System Register v1.0
# Agent: Nova | Date: 2026-03-21 | AI OS Corp

## 📋 Identity
- **Full name:** Nova — Research Intelligence Specialist
- **Agent type:** Specialist Agent (Tier 3)
- **Primary dept:** Dept 13 (R&D) + cross-dept 1–22
- **Status:** ACTIVE | CEO Standing Order: ACTIVE

---

## 📁 File Structure

```
brain/agents/notebooklm-agent/
├── AGENT.md                         ← Identity, rules, SOP, dept map (v4.1)
├── REGISTER.md                      ← This file — system index
├── memory/
│   ├── hot-cache.md                  ← Active context (CEO queue, tool status)
│   ├── synthesis-log.md              ← Session history log
│   ├── notebooks.json                ← Cloud NLM notebook registry
│   └── dept-requests/               ← Per-dept request queues
│       ├── dept04-registry.md
│       ├── dept05-marketing.md
│       ├── dept07-content-review.md
│       ├── dept08-ops.md
│       ├── dept10-security-strix.md
│       ├── dept16-odl.md
│       ├── dept18-monitoring.md
│       ├── dept20-civ.md
│       ├── dept21-agent-development.md
│       └── dept22-data-upgrade.md
└── workflows/
    ├── nova-intake.md               ← CEO Standing Order intake (7-step SOP)
    └── nova-dept-routing.md         ← Route synthesis ke depts
```

---

## 🔌 Plugin Stack

| Plugin | Type | Endpoint | Use Case |
|--------|------|----------|----------|
| **open-notebook** (Docker) | LOCAL | :5055 (API) / :8502 (UI) | PRIMARY — all private/sensitive inputs |
| **notebooklm-skill** (Antigravity) | CLOUD | browser automation | Google NLM queries |
| **notebooklm-skill** (direct plugin) | CLOUD | same as above | Mirror of antigravity version |
| **gitingest** | LOCAL tool | CLI | Digest repos before analysis |
| **firecrawl** | API | configured via env | Web crawl |
| **open-notebooklm** | LOCAL | — | Audio podcast synthesis |

---

## 📏 Operating Rules (12 rules)

| Code | Rule | Priority |
|------|------|----------|
| NLM-01 | LOCAL FIRST | HIGH |
| NLM-02 | NO HALLUCINATE | HIGH |
| NLM-03 | ALWAYS ARCHIVE | HIGH |
| NLM-04 | CITE SOURCE | MED |
| NLM-05 | DEP ROUTING | MED |
| NLM-06 | NEVER ADD WITHOUT METADATA | HIGH |
| NLM-07 | SMART ADD | MED |
| NLM-08 | TOOL SELECTION MATRIX | HIGH |
| NLM-09 | 2-FAILURE ESCALATION | HIGH |
| NLM-10 | run.py WRAPPER | HIGH |
| NLM-11 | CEO PRIORITY | CRITICAL |
| NLM-12 | KNOWLEDGE STORE PROTOCOL | HIGH |

---

## 🔗 Connections

```
open-notebook API       : http://localhost:5055
open-notebook UI        : http://localhost:8502
SurrealDB               : localhost:8000
ClawTask Dashboard      : http://localhost:7474 (Nova panel)
API Bridge              : http://localhost:7000
```

---

## 🗺️ Dept Coverage

22 phòng ban / Nova routing đầy đủ:
- Depts 1–22, với đặc biệt:
  - Dept 10, 12, 14 → **LOCAL ONLY** (open-notebook)
  - Dept 22 → **Primary partner** (CEO Standing Order)
  - Dept 21 → **Agent development** (NEW)

---

## 🔄 Workflows

| Workflow | File | Trigger |
|----------|------|---------|
| CEO Standing Order Intake | workflows/nova-intake.md | Bất kỳ input nào từ CEO |
| Dept Routing | workflows/nova-dept-routing.md | Sau khi intake xong |

---

*Nova System Register v1.0 | 2026-03-21*
