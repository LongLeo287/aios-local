laude# QUARANTINE ZONE — AI OS External Repo Isolation

> ⚠️ **WARNING:** This folder is an **ISOLATION ZONE**.
> All external repositories MUST be cloned here FIRST before any content enters the AI OS ecosystem.

---

## Rules

1. **Clone here with** `git clone --depth=1 <url> D:\APP\QUARANTINE\<repo-name>`
2. **Delete git hooks** from `.git\hooks\` (remove all non-`.sample` files)
3. **Run the vetting script** before ANY file extraction
4. **Only clean files** may leave this folder and enter AI OS

---

## How to Vet a Repo

```powershell
# Step 1: Clone
git clone --depth=1 https://github.com/owner/repo "D:\APP\QUARANTINE\repo-name"

# Step 2: Remove git hooks
Remove-Item "D:\APP\QUARANTINE\repo-name\.git\hooks\*" -Exclude "*.sample" -ErrorAction SilentlyContinue

# Step 3: Run vetting script
& "D:\APP\AI OS\skills\security_shield\vet_repo.ps1" -RepoPath "D:\APP\QUARANTINE\repo-name" -Verbose

# Step 4: After PASS — copy ONLY needed files
# Example:
Copy-Item "D:\APP\QUARANTINE\repo-name\some-skill\" -Destination "D:\APP\AI OS\skills\" -Recurse

# Step 5: Cleanup
Remove-Item -Recurse -Force "D:\APP\QUARANTINE\repo-name"
```

---

## Security Documentation

- **Full Protocol:** `D:\APP\AI OS\rules\clone_security_protocol.md`
- **Knowledge:** `D:\APP\AI OS\knowledge\repo_vetting_knowledge.md`
- **Vet Script:** `D:\APP\AI OS\skills\security_shield\vet_repo.ps1`

---

## Status Log

| Date | Repo | Result | Notes |
|------|------|--------|-------|
| 2026-03-17 | obra/superpowers | PASS | 0 critical, 5 warns (config loading = legit) |
| 2026-03-17 | vudovn/antigravity-kit | PASS (manual) | 0 critical, 8 warns (subprocess in test runners = legit) |
| 2026-03-17 | K-Dense-AI/claude-scientific-skills | PASS (manual) | 1 CRITICAL false positive (docstring example only) + 4 git hooks removed |
| 2026-03-17 | 1Panel-dev/MaxKB | PASS (manual) | 9 CRITICAL false positives: CJK unicode i18n + standard Vue JWT auth |
| 2026-03-17 | marketingjuliancongdanh79-pixel/skill-generator | PASS | 0 critical, clean |
| 2026-03-17 | askOkara/okara-crypto | PASS | 0 critical, 2 warns (Base64 in e2ee lib = expected) |
| 2026-03-17 | Affitor/affiliate-skills | PASS | 0 critical, 2 warns (.env CLI config = legit) |
| 2026-03-17 | HackUnderway/cerberus | PASS | 0 critical, 1 warn (os.system for terminal title = benign) |
| 2026-03-17 | langchain-ai/deepagents | PASS (manual) | 2 CRITICAL false positives in test_unicode_security.py (security test fixtures); 61 warns expected for CLI agent framework |
| 2026-03-17 | tysonnbt/Antigravity-Deck | PASS (manual) | 9 CRITICAL false positives: localStorage used for own AUTH_KEY + Discord bot token stored in local bridge.settings.json; 21 warns are standard web app .env + exec patterns. Legitimate web dashboard for Antigravity IDE management |
| 2026-03-17 | public-apis/public-apis | PASS | 0 critical, 0 warnings — pure data repository (curated API list) |
| 2026-03-17 | aiming-lab/AutoResearchClaw | PASS (manual review of WARNs) | 0 critical, 19 warns = subprocess in Docker sandbox + test runner = expected for autonomous research agent. Legit MIT research pipeline |
| 2026-03-17 | mergisi/awesome-openclaw-agents | PASS | 0 critical, 1 warn = .env in quickstart Discord bot = standard bot pattern |
| 2026-03-17 | volcengine/OpenViking | PASS (manual) | 5 CRITICAL false positives: discord.py uses bot token for own Discord gateway auth; app.js localStorage for UI state; test_edge_cases.py contains unicode security test fixtures (not malicious). 79 warns = standard for large Python+TS+Go AI memory system (subprocess, eval in AGFS shell, hex in media parser) |
| 2026-03-17 | nyldn/claude-octopus | PASS (manual) | 5 CRITICAL false positives: telemetry-webhook.sh uses ${OCTOPUS_WEBHOOK_TOKEN:-} env var (no hardcode); orchestrate.sh grep found 0 actual secrets (22k-line orchestrator); code.py = intentional OWASP benchmark fixture; test-plugin-expert-review.sh is a detector script not a secret source; test-crash-recovery.sh grep found 0 crypto keys. 8 warns = standard .env + exec patterns for multi-agent shell tool |
| 2026-03-17 | langflow-ai/openrag | PASS (manual) | 7 CRITICAL false positives: setup-e2e.sh generates random password from /dev/urandom (no hardcode); test_env_manager.py uses test data strings in unit tests for 0o600 permission validation; 5x crypto_blockchain = grep false trigger on session JWT patterns (grep private_key in flagged files = 0 results). 58 warns = standard for Python RAG system (dotenv, subprocess for Docker, AWS env vars, Google Drive connector) |
| 2026-03-17 | DarkWebInformer/FBI_Watchdog | PASS | 0 critical, 1 warn = standard load_dotenv() config. Legitimate OSINT Python tool for monitoring domain seizures |
