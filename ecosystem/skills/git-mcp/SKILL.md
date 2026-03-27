---
name: git-mcp
description: Read, search, and manipulate Git repositories directly through MCP. Use for code history analysis, commit inspection, diff viewing, branch management, and repository exploration within AI OS Corp.
---

# Git MCP — Repository Intelligence

## What it Does
Direct Git operations through MCP without shell commands:
- Read file contents at any commit
- Search across commit history
- Get diffs between commits/branches
- List branches, tags, remotes
- View blame information

**Source:** Anthropic official MCP | `mcp-server-git` (uvx)

## When to Use
- Analyzing code history before making changes
- Finding when/who introduced a bug (git blame)
- Comparing versions across commits
- Repository exploration without switching context
- Automated code review support

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `git_log` | View commit history with filters |
| `git_diff` | Show diff between commits/branches |
| `git_show` | Show content of any commit |
| `git_blame` | Line-by-line attribution |
| `git_status` | Current working tree status |
| `git_branch` | List/create/delete branches |
| `git_search_commits` | Search commit messages |
| `git_read_file` | Read file at specific commit |

## Usage Examples

```python
# Find when a bug was introduced
git_log(path="plugins/firecrawl/firecrawl_adapter.py", max_count=20)

# See what changed in last commit
git_diff(target="HEAD~1")

# Search commits mentioning "mem0"
git_search_commits(query="mem0", max_results=10)

# Read a file at a specific commit
git_read_file(repo_path="d:\\AI OS CORP\\AI OS", file_path="skills/context7/SKILL.md", ref="HEAD")
```

## Setup
```json
// Already in claude_desktop_config.json:
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "d:\\AI OS CORP\\AI OS"]
    }
  }
}
```

## Requirements
- `uv` installed (`winget install astral-sh.uv`)
- Repository path must be accessible

## Notes
- Works on Windows path with escaped backslashes
- Default repo: `d:\AI OS CORP\AI OS`
- Add multiple repos by running multiple server instances
- Owner: Dept 1 (Engineering) — use for code archaeology
