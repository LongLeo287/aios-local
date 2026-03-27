---
name: agentshield
description: Security auditor for AI agent code. Scans agent prompts, skills, and code for security vulnerabilities, prompt injection risks, and unsafe patterns before deployment.
---

# AgentShield — AI Agent Security Auditor

## What it Does
Cherry-picked from `everything-claude-code` (affaan-m/everything-claude-code v1.9.0)
Security-first auditing for AI agent code, skills, and prompts.

## When to Use
- Before deploying a new agent or skill to AI OS Corp
- When reviewing third-party skill code
- As part of GATE_SECURITY in plugin-integration workflow
- Regular audits of existing agent prompts

## Audit Checklist

### Prompt Security
```
□ No prompt injection vulnerabilities (user input directly in system prompt)
□ No role-confusion patterns ("ignore previous instructions")  
□ No data exfiltration paths (agent sending data to external URLs without auth)
□ No hardcoded credentials or API keys in prompts
□ Scope is clearly bounded (agent can't exceed its defined role)
```

### Code Security
```
□ No exec() or eval() on user input
□ No subprocess with shell=True on untrusted input
□ File access scoped to AI OS root only
□ No unrestricted network calls
□ Dependencies locked (pinned versions)
```

### Data Handling
```
□ No PII logging
□ No sensitive data in plain-text files
□ Memory (Mem0) stores only non-sensitive summaries
□ Outputs sanitized before display
```

## Quick Audit Command
```bash
# Run AgentShield on a skill or agent file
agentshield audit ./skills/my-skill/SKILL.md
agentshield audit ./corp/agents/my-agent.md
agentshield scan-dir ./skills/  # Scan all skills
```

## Security Score Output
```
AgentShield Score: 87/100
✅ No prompt injection patterns
✅ No hardcoded secrets  
⚠️  WARN: Subprocess call without validation (line 42)
✅ Data handling: SAFE
Decision: CONDITIONAL — fix warning before deploy
```

## Notes
- Source: github.com/affaan-m/everything-claude-code (cherry-pick)
- 113 contributors | v1.9.0 (Mar 2026)
- Owner: Dept 10 (Security GRC) — run before every new skill
- Works alongside: trivy (infrastructure), strix-scan (full pipeline)
- Full documentation available in `security-guide.md` within this folder.
