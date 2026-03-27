# Strix Vet Report: agent-skills-standard
**Date:** 2026-03-14 10:50:00
**Status:** WARN
**Critical Findings:** 0
**Warnings:** 20

## Verdict

WARN - Warnings found. Manual review required before ingestion. See findings below.

## Findings

| Level | Category | Detail | File |
|-------|----------|--------|------|
| PASS | GIT_HOOK | No active hooks found | `` |
| WARN | NPM_SCRIPT | prepare script exists (review manually): husky | `D:\APP\QUARANTINE\agent-skills-standard\package.json` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\vite.config.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\index.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\commands\upgrade.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\DetectionService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\FeedbackService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\GitService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\RegistryService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\SkillDiscoveryService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\SyncService.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\DetectionService.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\FeedbackService.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\GitService.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\RegistryService.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\SkillValidator.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\__tests__\SyncService.spec.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\scripts\test-e2e.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\server\src\main.ts` |
| WARN | SENSITIVE_ACCESS | .env file access | `D:\APP\QUARANTINE\agent-skills-standard\server\src\core\core.module.ts` |
| WARN | OBFUSCATION | exec dynamic execution | `D:\APP\QUARANTINE\agent-skills-standard\cli\src\services\DetectionService.ts` |


## Next Step

Review each WARN item manually. If comfortable, proceed with caution. Document your review decision.
