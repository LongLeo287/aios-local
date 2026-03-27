# open-notebook Startup Note
# Port: 5055 | Role: content-analyst-agent (CIV STEP 3.5)

## Start open-notebook

If installed via plugins/openrag or similar:
`ash
cd plugins/openrag  # or wherever open-notebook is installed
python -m open_notebook.server --port 5055
`

## Verify running:
`ash
curl http://localhost:5055/health
`

## Alternative (khi open-notebook DOWN):
Claude Code CLI có thể thay thế bằng cách:
1. gitingest <repo_path> → tạo DIGEST.md
2. Dùng DEVELOPER role + 6 CIV questions
3. Output: _CIV_ANALYSIS.md (cùng format)

Ref: ops/workflows/claude-code-handoff.md → CIV Integration section
