# ops/tools/vscode-extensions.md
# AI OS Corp — VS Code Extensions Registry
# Version: 1.0 | 2026-03-25
# Auto-install via: ops/scripts/install_vscode_extensions.ps1

---

## Required Extensions (Auto-installed at boot)

| Extension ID | Name | Purpose | Tier |
|---|---|---|---|
| `zixfel.ag-auto-click-scroll` | AG Auto Click Scroll | Tự động click/scroll Antigravity response | tier1 |
| `ms-python.python` | Python | Chạy Python scripts (aos.py, fix_skill_tiers.py) | tier1 |
| `ms-vscode.powershell` | PowerShell | Chạy .ps1 scripts (update_hud.ps1, setup.ps1) | tier1 |
| `yzhang.markdown-all-in-one` | Markdown All in One | Edit .md files (AGENT prompts, workflows) | tier1 |
| `redhat.vscode-yaml` | YAML | Edit org_chart.yaml, SKILL_REGISTRY configs | tier2 |
| `GitHub.copilot` | GitHub Copilot | AI coding assist | tier2 |

## Optional Extensions (install on demand)

| Extension ID | Name | Purpose |
|---|---|---|
| `ms-vscode-remote.remote-ssh` | Remote SSH | Connect to remote VPS/server |
| `ms-azuretools.vscode-docker` | Docker | Manage containers |
| `eamodio.gitlens` | GitLens | Git history + blame |

---

## Auto-Install Process

Xem: `ops/scripts/install_vscode_extensions.ps1`

Script tự động:
1. Kiểm tra VS Code (`code --version`) — nếu không có thì skip với warning
2. Loop qua Required extensions → `code --install-extension <id>`
3. Log kết quả vào `telemetry/receipts/vscode_extensions_<date>.log`
4. Update blackboard.json `vscode_extensions_installed: true`

Trigger: `pre-session.md` Step 0 (boot check) — nếu `vscode_extensions_installed != true`

---

## ag-auto-click-scroll Integration

Extension ID: `zixfel.ag-auto-click-scroll`
Source: https://open-vsx.org/extension/zixfel/ag-auto-click-scroll

**Integration với AI OS:**
- Khi Antigravity render response → extension tự scroll + click "Accept"
- Giảm thao tác thủ công khi AI OS đang chạy automated cycle
- Không cần cài tay — `install_vscode_extensions.ps1` handle

---

*Registry v1.0 | Managed by ops/scripts/install_vscode_extensions.ps1*
