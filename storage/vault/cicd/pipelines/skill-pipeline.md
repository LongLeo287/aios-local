# CI/CD Pipeline: Skill Validation
# Trigger: New skill added to skills/ | Owner: registry_capability
# Purpose: Validate SKILL.md before activating in SKILL_REGISTRY

## Steps

- [ ] Step 1: Check SKILL.md exists
      Path: skills/<name>/SKILL.md (REQUIRED)
- [ ] Step 2: Validate SKILL.md structure
      Must have: Purpose, When to use, How to use sections
- [ ] Step 3: Check for conflicts
      Query: kho/plugins/registry.json (no duplicate purpose in Tier 1)
- [ ] Step 4: Security review (if code skill)
      Agent: strix-agent scan if skill has .py or .ps1 files
- [ ] Step 5: Register in SKILL_REGISTRY.json
      Add: { name, path, tags, tier, version, status: "pending_ceo" }
- [ ] Step 6: CEO notification
      Channel: notification-bridge (SKILL_CREATED)
      Message: "[NEW SKILL] <name> — awaiting CEO approval"
- [ ] Step 7: On CEO approve
      Update: SKILL_REGISTRY.json status = "active"
      Update: FAST_INDEX.json
      Update: hud/STATUS.json skills count

## On Failure
- Do NOT add to SKILL_REGISTRY
- Log: corp/memory/global/decisions_log.md (SKILL_REJECTED)
