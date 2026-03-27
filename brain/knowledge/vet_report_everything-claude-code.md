# Strix Vet Report: everything-claude-code
**Date:** 2026-03-14 10:49:53
**Status:** FAIL
**Critical Findings:** 2
**Warnings:** 41

## Verdict

FAIL - Critical issues found. DO NOT ingest into AI OS until resolved.

## Findings

| Level | Category | Detail | File |
|-------|----------|--------|------|
| PASS | GIT_HOOK | No active hooks found | `` |
| CRITICAL | NPM_SCRIPT | postinstall script makes network call: echo '\n  ecc-universal installed!\n  Run: npx ecc-install typescript\n  Docs: https://github.com/affaan-m/everything-claude-code\n' | `D:\APP\QUARANTINE\everything-claude-code\package.json` |
| WARN | NETWORK_CALL | curl to external URL | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\utils.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.cursor\hooks\adapter.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.cursor\hooks\before-read-file.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.cursor\hooks\before-shell-execution.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.cursor\hooks\before-tab-file-read.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\claw.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\setup-package-manager.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\cost-tracker.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\evaluate-session.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\insaits-security-wrapper.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\pre-bash-tmux-reminder.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\quality-gate.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\run-with-flags.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\session-end.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\suggest-compact.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\lib\hook-flags.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\lib\package-manager.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\scripts\lib\utils.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\hooks\evaluate-session.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\hooks\hooks.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\hooks\suggest-compact.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\integration\hooks.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\package-manager.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\session-aliases.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\session-manager.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\utils.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\tests\scripts\setup-package-manager.test.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.opencode\index.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.opencode\plugins\ecc-hooks.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\everything-claude-code\.opencode\tools\security-audit.ts` |
| WARN | SENSITIVE_ACCESS | User profile path access | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\scripts\instinct-cli.py` |
| WARN | SENSITIVE_ACCESS | User profile path access | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\scripts\test_parse_instinct.py` |
| WARN | SENSITIVE_ACCESS | User profile path access | `D:\APP\QUARANTINE\everything-claude-code\skills\videodb\scripts\ws_listener.py` |
| WARN | SENSITIVE_ACCESS | Environment variable access | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\agents\start-observer.sh` |
| WARN | SENSITIVE_ACCESS | User profile path access | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\hooks\observe.sh` |
| WARN | SENSITIVE_ACCESS | Environment variable access | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\scripts\detect-project.sh` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\everything-claude-code\scripts\claw.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\everything-claude-code\scripts\hooks\quality-gate.js` |
| WARN | OBFUSCATION | eval dynamic execution | `D:\APP\QUARANTINE\everything-claude-code\.opencode\tools\security-audit.ts` |
| WARN | OBFUSCATION | subprocess shell execution | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\scripts\instinct-cli.py` |
| WARN | OBFUSCATION | subprocess shell execution | `D:\APP\QUARANTINE\everything-claude-code\skills\continuous-learning-v2\scripts\test_parse_instinct.py` |
| CRITICAL | HARDCODED_SECRET | Hardcoded secret | `D:\APP\QUARANTINE\everything-claude-code\tests\lib\utils.test.js` |


## Next Step

STOP. Review CRITICAL items. Delete quarantine folder if unsolvable: Remove-Item -Recurse -Force 'D:\APP\QUARANTINE\everything-claude-code'
