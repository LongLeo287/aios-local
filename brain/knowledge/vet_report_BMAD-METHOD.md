# Strix Vet Report: BMAD-METHOD
**Date:** 2026-03-14 10:49:48
**Status:** WARN
**Critical Findings:** 0
**Warnings:** 14

## Verdict

WARN - Warnings found. Manual review required before ingestion. See findings below.

## Findings

| Level | Category | Detail | File |
|-------|----------|--------|------|
| PASS | GIT_HOOK | No active hooks found | `` |
| WARN | NPM_SCRIPT | prepare script exists (review manually): command -v husky >/dev/null 2>&1 && husky || exit 0 | `D:\APP\QUARANTINE\BMAD-METHOD\package.json` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\validate-file-refs.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\commands\install.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\commands\status.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\installers\lib\core\installer.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\installers\lib\core\manifest-generator.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\installers\lib\custom\handler.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\installers\lib\modules\manager.js` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\lib\ui.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\BMAD-METHOD\tools\validate-doc-links.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\BMAD-METHOD\tools\validate-file-refs.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\installers\lib\core\dependency-resolver.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\BMAD-METHOD\tools\cli\lib\yaml-format.js` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\BMAD-METHOD\tools\schema\agent.js` |


## Next Step

Review each WARN item manually. If comfortable, proceed with caution. Document your review decision.
