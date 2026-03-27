# CI/CD Pipeline: Daily Health Check
# Trigger: Phase 0 of corp-daily-cycle.md | Owner: system_health
# Purpose: Verify AI OS services + data integrity each cycle

## Steps

- [ ] Step 1: Port checks
      Ollama:11434, ClawTask:7474, LightRAG:9621
      FAIL: log to blackboard.json open_items[] + notify CEO

- [ ] Step 2: SKILL_REGISTRY consistency check
      For each entry: verify skills/<name>/SKILL.md exists
      MISS: flag for skill-discovery-auto.md

- [ ] Step 3: QUARANTINE folder integrity
      Verify: incoming/ vetted/ rejected/ all exist
      Check: no stuck pending tickets (>7 days old)

- [ ] Step 4: Memory freshness
      Check: blackboard.json last_phase7 < 48h ago?
      STALE: suggest corp cycle to CEO

- [ ] Step 5: Git status
      Run: git status (should be clean or 1 unpushed commit)
      WARN: flag if >10 untracked files

- [ ] Step 6: Update STATUS.json
      Write: hud/STATUS.json with current service states

- [ ] Step 7: Report to CEO (if issues found)
      Channel: notification-bridge (SYSTEM_ERROR)
