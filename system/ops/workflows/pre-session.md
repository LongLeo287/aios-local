# Department: operations
﻿# pre-session.md — AI OS Session Freshness Checklist
# Version: 4.0 | Updated: 2026-03-22
# Authority: Tier 2 (Operations)
# When to read: ON-DEMAND — after boot sequence, or at start of long session
# NOT required every boot — reference only

---

## Purpose

Supplement to boot sequence. Helps agent verify system freshness and announce status.
Read this when: CEO explicitly asks for system check, or session is resuming after a long gap.

---

## Checklist (Run in Order)

### Step 1: SKILL_REGISTRY Freshness Check

```
Read: brain/shared-context/SKILL_REGISTRY.json → check metadata.last_built

If last_built > 7 days ago:
  → Warning: "Registry có thể cũ. Xem xét chạy skill_loader.ps1?"

If SKILL_REGISTRY.json missing or empty:
  → CRITICAL: Cannot proceed until registry is rebuilt. Notify CEO.
```

---

### Step 2: Knowledge Base Status

```
Check and report:
  - plugins/       → số lượng plugins installed
  - brain/knowledge/ → categories present (repos, web, docs, notes)
  - channels/      → bridge running? (check port 5001)
  - SKILL_REGISTRY → số entries active

Output format (Vietnamese):
"🧠 Trạng thái Knowledge Base:
  - Plugins: [N] installed
  - Knowledge categories: [list]
  - Remote bridge: [running/offline]
  - Registry: [N] skill entries"
```

---

### Step 3: Session Announcement (Vietnamese)

```
Output to CEO:

"✅ AI OS đã khởi động đầy đủ.
- Identity: SOUL.md ✅
- Rules: GOVERNANCE.md ✅
- Roster: AGENTS.md ✅ ([N] agents)
- Strategy: THESIS.md ✅ (40 pillars)
- Output formats: report_formats.md ✅
- Blackboard: [N] active tasks
- Skills: [N] registry entries
- Status: Sẵn sàng nhận lệnh từ CEO"
```

---

### Step 4: Security Awareness

```
SkillSentry 9-layer scanner: ACTIVE (passive monitoring)
- Scans any new plugin/skill before activation
- Monitors channel messages for prompt injection
- Rules: brain/knowledge/notes/RULE-DYNAMIC-01-no-hardcode.md
- Blocks operations violating governance rules
```

---

## On Failure

If any step fails:
- Log warning, continue — do NOT abort session
- Report failure to CEO (Vietnamese)

---

## On-Demand References (NOT in boot sequence)

```
Corp daily cycle:    ops/workflows/corp-daily-cycle.md    ← Trigger: "aos corp start"
Storage rule:        brain/knowledge/notes/RULE-STORAGE-01-storage-location.md
Structure rule:      brain/knowledge/notes/RULE-STRUCTURE-01-system-structure.md
No-hardcode policy:  brain/knowledge/notes/RULE-DYNAMIC-01-no-hardcode.md
```
