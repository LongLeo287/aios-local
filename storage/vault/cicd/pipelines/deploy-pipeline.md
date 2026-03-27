# CI/CD Pipeline: Deploy
# Trigger: CEO approves system update | Owner: engineering
# Purpose: Safe deployment of AI OS changes

## Steps (DEVELOPER role in Claude Code)

- [ ] Step 0: Git snapshot
      Command: git add . && git commit -m "snapshot: pre-deploy-<id>"

- [ ] Step 1: Backup config
      Copy: .env -> .env.bak.<timestamp>
      Copy: brain/shared-context/blackboard.json -> .bak

- [ ] Step 2: Apply changes
      Type: FILE update | SCRIPT run | CONFIG change
      Check: no Tier 0 files modified without CEO approval

- [ ] Step 3: QA gate
      qa-gate.md: verify outputs match acceptance criteria
      FAIL twice: rollback to snapshot

- [ ] Step 4: Update version
      File: version.json (increment patch version)
      File: blackboard.json last_actions_this_cycle[]

- [ ] Step 5: Notify
      notification-bridge (SYSTEM_UPDATE)
      Message: "[DEPLOY] v<version> — <summary>"

## Rollback
  git reset --hard HEAD~1
  Restore: .env.bak -> .env
