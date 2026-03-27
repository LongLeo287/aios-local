---
id: security_scanning_reference
name: Security Scanning Reference
version: 1.0.0
tier: 3
domain: security
cost_tier: standard
status: active
author: AI OS (synthesized from TruffleHog, Katana, PentestOPS, hintshell)
updated: 2026-03-14
sources:
  - https://github.com/trufflesecurity/trufflehog  (25K stars, AGPL-3.0)
  - https://github.com/projectdiscovery/katana     (15.9K stars, MIT)
  - https://github.com/0xBugatti/PentestOPS        (303 stars, MIT)
  - https://github.com/philau2512/hintshell         (Rust CLI, NOASSERTION)
tags: [security, scanning, pentest, secret-detection, web-crawling, devtools]
accessible_by:
  - Antigravity
  - Claude Code
  - Developer
load_on_boot: false
---

# Security Scanning Reference — AI OS Skill

> Synthesized from 4 security repos. Used for: code review, secret detection, pentest planning, web recon.

---

## 1. Secret & Credential Detection (TruffleHog patterns)

> Source: trufflesecurity/trufflehog — 25K stars, Go, AGPL-3.0

### Credential Patterns to Detect

```regex
# OpenAI
sk-[a-zA-Z0-9]{32,}
sk-proj-[a-zA-Z0-9_-]{100,}

# Anthropic
sk-ant-[a-zA-Z0-9_-]{95,}

# GitHub
ghp_[a-zA-Z0-9]{36}          # Personal Access Token
gho_[a-zA-Z0-9]{36}          # OAuth Token
ghs_[a-zA-Z0-9]{36}          # App Token
github_pat_[a-zA-Z0-9_]{82}  # Fine-grained PAT

# AWS
AKIA[A-Z0-9]{16}              # Access Key ID
[a-zA-Z0-9+/]{40}            # Secret Access Key (context-dependent)

# Google
AIza[0-9A-Za-z_-]{35}        # Google API Key
[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com  # OAuth Client ID

# Generic high-entropy (> 3.5 bits/char Shannon entropy)
# Strings 20+ chars in key=value or Bearer context

# Database connection strings
(postgres|mysql|mongodb)://[^:]+:[^@]+@
```

### TruffleHog Scan Approach

```bash
# Docker (no install needed)
docker run --rm -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest \
  filesystem --directory /pwd --only-verified

# GitHub org scan
trufflehog github --org=your-org --only-verified

# Git history scan
trufflehog git file:///path/to/repo --since-commit HEAD~100

# Single file
trufflehog filesystem --directory ./src
```

### Key Principles (TruffleHog)
- **Verify secrets**: Don't just detect — verify they're active (reduces false positives 95%)
- **Scan git history**: Deleting from current code does NOT remove from git history
- **CI Integration**: Run on every PR, block merge if verified secrets found
- **Entropy threshold**: Use Shannon entropy > 3.5 bits/char for generic detection

---

## 2. Web Crawling & Recon (Katana patterns)

> Source: projectdiscovery/katana — 15.9K stars, Go, MIT

### Katana Scan Commands

```bash
# Basic crawl
katana -u https://target.com

# Deep crawl with JavaScript rendering
katana -u https://target.com -js-crawl -d 5

# Headless (Playwright)
katana -u https://target.com -headless

# API endpoint discovery
katana -u https://target.com -ef css,png,jpg,svg \
  -o endpoints.txt

# Crawl + filter interesting endpoints
katana -u https://target.com -js-crawl \
  -mr "api|admin|dashboard|config|secret|token|auth"

# Scope-limited crawl
katana -u https://target.com \
  -cs target.com \     # scope include
  -fs custom -fr "logout|signout"  # filter out
```

### Katana for AI OS Usage
- **Endpoint discovery**: Map all API routes before security testing
- **JavaScript crawl**: Find client-side routes in SPAs (React, Vue, Next.js)
- **Asset enumeration**: List all JS bundles for source map analysis
- **Form discovery**: Find input vectors for injection testing

---

## 3. Penetration Testing Operations (PentestOPS patterns)

> Source: 0xBugatti/PentestOPS — 303 stars, TypeScript, MIT, 2025

### Pentest Project Lifecycle

```
Phase 1: Reconnaissance
  - Passive: OSINT, Shodan, LinkedIn, GitHub dorking
  - Active: Port scan (nmap), service detection, subdomain enum

Phase 2: Enumeration
  - Web: Directory bruteforce (gobuster/feroxbuster)
  - API: Endpoint discovery (katana), param fuzzing
  - Service: Banner grabbing, version detection

Phase 3: Vulnerability Assessment
  - CVE lookup for detected versions
  - Configuration review (SSRF, IDOR, auth bypass)
  - Injection testing (SQLi, XSS, SSTI, CSRF)

Phase 4: Exploitation
  - PoC development
  - Privilege escalation
  - Lateral movement

Phase 5: Reporting
  - Finding severity: Critical/High/Medium/Low/Info
  - CVSS scoring
  - Remediation recommendations
  - Executive summary
```

### Common Findings Template

```markdown
## Finding: [Title]

**Severity:** Critical | High | Medium | Low | Informational
**CVSS:** [score]
**CWE:** [CWE-XXX]

### Description
Brief description of the vulnerability.

### Evidence
- URL: https://target.com/vulnerable/endpoint
- Request: [HTTP request]
- Response: [HTTP response showing the issue]

### Impact
What an attacker can do with this.

### Remediation
Specific fix recommendations with code examples.

### References
- https://owasp.org/...
```

---

## 4. Shell Command Intelligence (hintshell approach)

> Source: philau2512/hintshell — Rust + TypeScript, AI-powered CLI

### hintshell Concepts for AI OS

hintshell is a real-time CLI suggestion tool that:
- Learns from command history (fuzzy-match, frequency analysis)
- AI-powered completion (via LLM provider)
- Cross-shell: Bash, Zsh, PowerShell

### Shell Safety Patterns (Integration with pre-ingest-check.ps1)

```
DANGEROUS patterns to detect in scripts:
  eval(...)           → Code injection risk
  exec(...)           → Process execution risk
  os.system(...)      → Shell injection
  shell=True          → Python subprocess injection
  $(command)          → Shell command substitution
  `command`           → Backtick command substitution
  base64 -d | bash    → Encoded payload execution
  curl URL | bash     → Remote code execution
  wget URL | sh       → Remote code execution
  pickle.loads()      → Python deserialization attack
  __import__()        → Dynamic import (obfuscation)

SAFE alternatives:
  subprocess.run([], shell=False)    → Use list args
  shlex.split(command)               → Safe string parse
  pathlib.Path                       → Path traversal safe
```

---

## 5. Quick Security Checklist for AI OS Ingest

Before ingesting ANY external repo (from pre-ingest-check.ps1):

```
[ ] Stars >= 50 (credibility signal)
[ ] Age >= 3 months (established)
[ ] Not a suspicious fork
[ ] Author in trusted list OR manually verified
[ ] No .exe/.dll/.bat/.msi files
[ ] No .env/.key/id_rsa files in repo
[ ] No hardcoded credentials (TruffleHog patterns above)
[ ] No shell injection patterns (eval, exec, shell=True)
[ ] Permissive license (MIT/Apache-2.0/BSD)
[ ] README explains what the code does
[ ] No unusual network requests in scripts
```

---

## Resources

- **TruffleHog**: https://github.com/trufflesecurity/trufflehog | https://trufflesecurity.com
- **Katana**: https://github.com/projectdiscovery/katana | https://projectdiscovery.io
- **PentestOPS**: https://github.com/0xBugatti/PentestOPS
- **hintshell**: https://github.com/philau2512/hintshell
- **OWASP Top 10**: https://owasp.org/www-project-top-ten
- **CVE Database**: https://nvd.nist.gov
