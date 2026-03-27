# Clone Security Protocol (CSP)
**Version:** 1.0  
**Enforcement Level:** MANDATORY — No exceptions.

---

## DIRECTIVE
Before cloning ANY external repository into `D:\APP\AI OS`, `D:\APP\Workspaces`, or `D:\APP\DATA`:
1. ALL repos MUST be cloned into `D:\APP\QUARANTINE\<repo-name>` FIRST.
2. Run `vet_repo.ps1` against the quarantine directory.
3. Only after a PASS result may the content be moved/copied into the AI OS ecosystem.

---

## Step-by-Step Pre-Clone Vetting

### STAGE 1: GitHub Profile Analysis (Manual — before any git clone)

Before touching Git, inspect the repo visually on GitHub:

| Check | Pass Condition | Red Flag |
|-------|---------------|----------|
| Stars | > 50 preferred | < 10 stars + no known author = suspicious |
| Last Commit | Active (< 1 year) | Abandoned repo with sudden new commit |
| Contributors | Multiple OR single known author | Single anon author, no history |
| Issues/PRs | Healthy discussion | Zero issues + zero PRs = ghost repo |
| License | Open source (MIT, Apache2, BSD) | No license |
| README quality | Clear, professional | Vague descriptions hiding purpose |
| Sudden star spike | Normal growth | 0 stars → 5000 overnight = astroturfing |

### STAGE 2: Quarantine Clone

```powershell
# ALWAYS use this pattern. NEVER clone directly into D:\APP\AI OS
$REPO_URL = "https://github.com/owner/repo-name"
$REPO_NAME = "repo-name"
git clone --depth=1 $REPO_URL "D:\APP\QUARANTINE\$REPO_NAME"
```

**WHY `--depth=1`:** Shallow clone only gets current commit. Reduces attack surface from malicious commit history.

### STAGE 3: Automated Scan

```powershell
# Run the vetting script
D:\APP\AI OS\skills\security_shield\vet_repo.ps1 -RepoPath "D:\APP\QUARANTINE\repo-name"
```

### STAGE 4: Review Scan Report

Open the generated report at `D:\APP\QUARANTINE\repo-name\_VET_REPORT.md`.

- If `STATUS: PASS` → Proceed to Stage 5.
- If `STATUS: WARN` → Manual review required, user decides.
- If `STATUS: FAIL` → DELETE the quarantine folder. Do NOT ingest.

### STAGE 5: Content-Only Extraction (NOT full clone copy)

**DO NOT** `xcopy` or `robocopy` the entire repo blindly.  
**DO** extract only the specific files needed:

```powershell
# Example: Extract only .md documentation files from a repo
Copy-Item "D:\APP\QUARANTINE\repo-name\*.md" -Destination "D:\APP\AI OS\knowledge\" -Recurse
# Or: Copy specific skill folder
Copy-Item "D:\APP\QUARANTINE\repo-name\skills\ui-ux-pro-max\" -Destination "D:\APP\AI OS\skills\" -Recurse
```

### STAGE 6: Post-Move Security Sweep

After copying into AI OS:
```powershell
# Run security_shield scan on newly added files
# (Invoke security_shield skill: /scan on the destination folder)
```

---

## ABSOLUTE RULES

1. **NEVER run `npm install`, `pip install`, or any package manager** inside a quarantine repo without first reading every line of `package.json` / `requirements.txt`.
2. **NEVER execute any script** (`.ps1`, `.sh`, `.bat`, `.py`) found in a cloned repo without reading it fully.
3. **NEVER open** a cloned repo in VS Code or any editor that runs extension scripts automatically.
4. **ALWAYS use `--depth=1`** for git clone.
5. **ALWAYS delete** the quarantine folder after extraction is complete.
6. **GIT HOOKS RULE:** After clone, ALWAYS check `D:\APP\QUARANTINE\repo\.git\hooks\` — delete ALL hook files before doing any git operations.

---

## Data Leak Prevention

### What information could leak?
- API keys / tokens in environment variables
- File contents if malicious code reads and POSTs them
- System information (hostname, username, paths)
- `.gemini/` folder contents (AI context)

### Mitigation
- Do NOT run any scripts from cloned repos while connected to internet, unless you have read 100% of the script.
- If a repo requires `npm install`: Read ALL `package.json` scripts first (`preinstall`, `postinstall`, `prepare`).
- Set Windows Firewall rule to block outbound from PowerShell during test runs if needed.

---

## Trusted Repo Categories (Lower Risk — still MUST go through QUARANTINE)

| Trust Level | Criteria |
|-------------|---------|
| HIGH | Official org repo (anthropics/, microsoft/, google/) |
| MEDIUM | 1000+ stars, active for 2+ years, known author |
| LOW | New repo, small stars, anonymous author |
| REJECT | No README, `.git/hooks` with executables, postinstall scripts to unknown URLs |

Even HIGH trust repos go through Quarantine — just with faster review.

---

## Emergency: If You Suspect Compromise

1. **Immediately** disconnect from internet (disable Wi-Fi)
2. Audit recently accessed files: `Get-ChildItem D:\APP -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 50`
3. Check running processes: `Get-Process | Where-Object { $_.CPU -gt 10 }`
4. Check network connections: `netstat -ano | findstr ESTABLISHED`
5. Delete the quarantine folder: `Remove-Item -Recurse -Force "D:\APP\QUARANTINE\suspect-repo"`
