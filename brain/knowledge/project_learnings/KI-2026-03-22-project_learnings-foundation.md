---
id: KI-2026-03-22-project-learnings-foundation
type: REFERENCE
domain: project_learnings
dept: all
created: 2026-03-22
foundation: true
tags: ['learnings', 'post-mortem', 'lessons', 'patterns', 'mistakes']
---

# AI OS Corp — Project Learnings & Post-Mortems

## AI OS Project Learnings

### 2026-03-22 Session Learnings

#### Port Confusion: 4747 vs 7474
- **Problem:** ClawTask (:7474) and GitNexus (:4747) port numbers are reversed — easy to confuse
- **Learning:** Always prefix port references with service name. Add visual labels in dashboard.
- **Fix:** Both services now clearly labeled in startup.ps1 output

#### Module Pattern (ClawTask)
- **Discovery:** ClawTask uses `_MODULES` list in clawtask_api.py
- **Pattern:** Each module: `handle_get(handler, path)`, `handle_post(handler, path)`, `MODULE_INFO`
- **New modules added:** module_gitnexus, module_ag_auto

#### Auto-Accept Agent Design
- **Problem:** VS Code extension approach too tightly coupled to VS Code
- **Solution:** Built ag_auto_accept.py as subprocess wrapper + HTTP API
- **Learning:** AI OS tools should be standalone HTTP services, not editor plugins

#### Knowledge Base Quality
- **Issue:** 525 KI entries but heavy in bmad_repo (199) and skills_standard_repo (167) — repo dumps
- **Learning:** KI entries should be curated insights, not raw file lists
- **Action:** Focus future KI on "Key Concepts" and "AI OS Integration" sections

### Recurring Issues
1. `Stop-Process python` kills ALL Python services (ClawTask + side services)
2. `startup.ps1` needs `-NoLocal` flag to skip GitNexus/DeepAgents when only ClawTask needed

---
*Foundation KI — created 2026-03-22*
