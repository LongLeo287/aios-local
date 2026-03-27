# [RULE-DYNAMIC-01] No Hardcoding Policy
# Issued by: CEO LongLeo | Date: 2026-03-22 | Status: MANDATORY
# Scope: All agents, all rule files, all boot files, all scripts

---

## CORE RULE

> **NEVER hardcode machine-specific values.**
> The AI OS runs on different machines, users, and environments.
> Hardcoded paths, usernames, counts, or ports = system breakage.

---

## 1. WHAT MUST NOT BE HARDCODED

| Category | Bad (hardcoded) | Good (dynamic) |
|----------|----------------|----------------|
| Workspace root | `D:\AI OS CORP\AI OS\` | "the directory containing GEMINI.md" |
| User home | `C:\Users\R9000P 2021.LONGLEO\` | `$env:USERPROFILE` (PowerShell) / `~` (bash) |
| AI tool system dirs | `C:\Users\VUA2HAND\.gemini\` | `$env:USERPROFILE\.gemini\` |
| Dept count | `"22 departments"` | `corp/org_chart.yaml` → `company.departments.count` |
| Corp state | snapshot in boot file | `brain/shared-context/blackboard.json` (live) |
| Service ports | `7474`, `3000`, etc. | `ops/scripts/config.json` |
| Agent version | `"Sonnet 4.6"` | LLM router config |

---

## 2. HOW TO DISCOVER PATHS DYNAMICALLY

### Workspace Root
```
Agent boot file (GEMINI.md / CLAUDE.md) is always at the workspace root.
Workspace root = directory containing the boot file.
All other paths are RELATIVE to workspace root.
```

### User Home (System Data)
```
PowerShell : $env:USERPROFILE
Python     : os.path.expanduser("~")
Node.js    : os.homedir()
Bash       : $HOME
```

### AI Tool System Directories
```
Antigravity data : $env:USERPROFILE\.gemini\
Claude Code data : $env:USERPROFILE\.claude\
Ollama models    : $env:USERPROFILE\.ollama\
```

### Dept Count
```
Source: corp/org_chart.yaml
Field : company.version (document version controls this)
Count : grep "^  [a-z]" corp/org_chart.yaml | wc -l  (count dept keys)
Rule  : Always read org_chart.yaml for the authoritative count.
```

### Service Ports & URLs
```
Source: ops/scripts/config.json
Rule  : All services read their ports from this file. Never hardcode 7474, 3000, etc.
```

---

## 3. RULE FILES & BOOT FILES — How to Write

### When writing a rule file:
- Use RELATIVE paths: `brain/shared-context/blackboard.json` ✅
- Avoid ABSOLUTE paths: `D:\AI OS CORP\AI OS\brain\...` ❌
- If must reference workspace root: write `<AI_OS_ROOT>` as placeholder

### When writing boot files (GEMINI.md / CLAUDE.md):
- Corp status → reference blackboard.json, do NOT snapshot inline
- Dept count → reference org_chart.yaml, do NOT hardcode number
- Storage path → reference RULE-STORAGE-01, do NOT duplicate content

### When writing scripts (.ps1, .py, .sh):
- Use `$PSScriptRoot` or `os.path.dirname(__file__)` to find script location
- Resolve workspace root from script's relative position
- Load config from `ops/scripts/config.json`, not hardcoded strings

---

## 4. PROCEDURE — When System Changes (New Machine / New Path)

When the AI OS moves to a new machine or the root path changes:

```
STEP 1: Update ops/scripts/config.json
        → Set "workspace_root" to new absolute path
        → Update any service URLs if ports changed

STEP 2: Update RULE-STORAGE-01
        → Change workspace root reference in Section 1
        → Change user home reference in Section 2

STEP 3: Run boot sequence verification
        → Check all relative paths still resolve correctly
        → Test: claude "verify all paths in CLAUDE.md boot sequence exist"

STEP 4: Update blackboard.json session info
        → New session ID, new timestamp

STEP 5: Commit to git (if available) with message:
        "system: migrate to new machine/path [date]"
```

---

## 5. EXCEPTIONS (When Hardcoding is Acceptable)

| Case | Why OK |
|------|--------|
| Example/documentation comments | Clearly labeled as example only |
| Git commit messages | One-time, not system-affecting |
| Telemetry receipts | Historical record, not used for routing |

---

*Issued: 2026-03-22 | Must be read BEFORE any agent modifies rule files or boot files.*
*"Flexible systems survive. Rigid systems break."*
