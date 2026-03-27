# Claude Code Ecosystem Knowledge
**Sources:**  
- `affaan-m/everything-claude-code` — Battle-tested configuration suite  
- `thedotmack/claude-mem` — Persistent memory plugin  
- `shanraisshan/claude-code-best-practice` — Best practices  
**Extracted:** 2026-03-14

---

## everything-claude-code: The Configuration Suite

### Components (adopt in AI OS)
| Component | Description | AI OS Mapping |
|-----------|-------------|---------------|
| **Agents** | Specialized agents for dev lifecycle stages | `skills/` folder agents |
| **Skills** | Reusable workflow definitions (e.g., TDD) | `skills/` folder |
| **Commands** | Slash commands for triggering actions | `workflows/` folder |
| **Rules** | Guidelines Claude Code always follows | `rules/` folder |
| **Hooks** | Auto-run scripts on specific events | **NEW — implement this** |

### 🔥 Hooks System (High Priority)
Hooks run automatically when Claude Code does something:
```
HOOK EXAMPLES:
- After file write → auto-lint + type-check
- Before commit → run tests
- After task complete → update task.md
```
**AI OS Action:** Create `hooks/` folder with PowerShell hook scripts.

### Key Innovations
1. **Continuous learning** — Claude remembers what works
2. **Memory optimization** — Compress context regularly
3. **Security scanning** — Auto-scan for vulnerabilities after code changes
4. **Production-ready** — Designed to build full products, not toys

---

## claude-mem: Persistent Memory Plugin

### Architecture
```
Claude Code action (file read/write/search)
    ↓
Hook captures tool usage observation
    ↓  
AI compresses → semantic summary
    ↓
Store locally (SQLite or PostgreSQL + pgvector)
    ↓
Progressive disclosure:
  - Future sessions: show index only
  - On request: fetch full memory
```

### Key Features
- **100% local/private** — No external APIs needed
- **Semantic search** — Search by meaning, not just keyword
- **Progressive disclosure** — Index first, details on-demand (saves tokens)
- **Project namespaces** — Separate memory per project
- **Install as plugin** — `claude mcp install claude-mem`

### How to Install
```bash
# Install as Claude Code plugin
claude mcp install claude-mem

# Or manual install
git clone https://github.com/thedotmack/claude-mem
```

**AI OS Relevance:** This directly upgrades our `smart_memory` + `cosmic_memory` skills. Install immediately.

---

## Best Practices for Claude Code (AI OS Operations)

### Context Management
1. Start fresh conversations for each new topic (use `/clear`)
2. Use `/compact` to compress history mid-session
3. Identify and ONLY include necessary files in context
4. Clean workspace — exclude irrelevant dirs in `.gitignore`

### Prompt Engineering
1. Use "think hard" or "ultrathink" for complex reasoning
2. Ask for architectural explanation BEFORE code generation
3. Treat prompts as templates — version and reuse them
4. Use Shift+Tab→Tab to enter Plan Mode before risky operations

### CLAUDE.md / AGENTS.md Best Practices
- Update with architectural decisions after each major change
- Store preferences and conventions → Claude "remembers" them
- Include anti-patterns to avoid (negative examples)

### Git/GitHub Integration
- Claude Code can generate commit messages, handle branching
- Can open PRs automatically via GitHub Actions
- Never force push; use `--force-with-lease`

### Treating Claude as a Teammate
- Give it context like you would a senior engineer
- Use it for first-draft functions, then iterate
- Let it design prompt pipelines
- Grant "auto execute" only for READ-ONLY commands
