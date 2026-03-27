---
source: https://github.com/khanhbkqt/spawn-agent
ingested_at: 2026-03-16T10:22:00+07:00
domain: AI|Architecture|AgentSkills|SubAgent
trust_level: HIGH
vet_status: PASS
tags: [spawn-agent, antigravity, sub-agent, gemini-cli, codex-cli, context-isolation, orchestration]
---

# spawn-agent — Sub-Agent Delegation Skill for Antigravity

**Repo:** https://github.com/khanhbkqt/spawn-agent  
**Author:** khanhbkqt (Vietnamese developer)  
**Target:** Antigravity (thiếu native sub-agent support)  
**Worker agents:** Gemini CLI, Codex CLI

> ⚡ **Trực tiếp liên quan đến AI OS** — đây là skill giải quyết limitation của Antigravity environment hiện tại.

---

## Vấn đề Giải Quyết

**Antigravity không có native sub-agent delegation.**

Khi main agent làm tất cả trong 1 session:
- File reads → tốn context
- Build outputs → tốn context  
- Error traces → tốn context
- → **Context window overflow** → agent mất định hướng

**Giải pháp:** Main agent = Orchestrator, delegate implementation xuống Worker agents.

---

## Architecture

```
┌─────────────────────────────────────────┐
│  MAIN AGENT (Antigravity)               │
│  Role: ORCHESTRATOR                     │
│  - Planning                             │
│  - Task delegation                      │
│  - Review outcomes                      │
│  - Context: CLEAN (chỉ goals + results) │
└──────────────┬──────────────────────────┘
               │ delegate
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ WORKER A     │ │ WORKER B     │
│ Gemini CLI   │ │ Codex CLI    │
│              │ │              │
│ - Implement  │ │ - Research   │
│ - Fix bugs   │ │ - Query code │
│ - Refactor   │ │ - Analysis   │
│ Context: OK  │ │ Context: OK  │
│ (isolated)   │ │ (isolated)   │
└──────────────┘ └──────────────┘
```

---

## Core Features

### 1. Scoped Task Delegation
Delegate các loại tasks:
- 🐛 Fix a specific bug
- ➕ Add a function/feature
- 🔄 Refactor specific files
- 🔍 Research without polluting main context
- 📊 Query codebase for information

### 2. Context Isolation
```
Main Agent Session:
├── Goals (persistent)
├── Plan (persistent)
├── Delegated task descriptions
└── Worker results (compact summaries)
    ← Không có raw build logs, stack traces, etc.

Worker Agent Session (ephemeral):
├── Task description (từ main agent)
├── Relevant files
├── Build outputs
├── Stack traces
└── Implementation details
    → Kết thúc khi task done → discard context
```

### 3. Delegation Templates

Template chuẩn để main agent viết task cho worker:

```markdown
## DELEGATION TASK

**Goal:** [Mô tả rõ ràng 1-2 câu về kết quả mong muốn]

**Scope:**
- Files được phép modify: [list files]
- Files KHÔNG được touch: [list files]
- Chỉ làm: [specific actions]

**Constraints:**
- Không thay đổi public API
- Không thêm dependencies mới
- Test phải pass sau khi xong

**Context cần biết:**
[Minimal context — chỉ những gì worker cần]

**Expected Output:**
- [ ] Files modified: [list]
- [ ] Tests passing: [specific test names]
- [ ] Summary of changes (3-5 bullets)
```

### 4. Worker Agents

**Gemini CLI:**
```bash
gemini -p "$(cat delegation-task.md)" --context $(ls relevant-files)
```

**Codex CLI:**
```bash
codex "$(cat delegation-task.md)"
```

---

## Khi Nào Dùng spawn-agent

✅ **Nên dùng khi:**
- Task có scope rõ ràng (fix bug X trong file Y)
- Cần research codebase mà không muốn pollute main context
- Tasks independent (không cần main agent intervention)
- Implementation phức tạp với nhiều file reads

❌ **Không nên dùng khi:**
- Task cần real-time back-and-forth với user
- Task phụ thuộc vào output của task trước (chưa done)
- Task cần main agent's full context để quyết định

---

## Integration với AI OS

### Vào skill loader
```
Đặt spawn-agent skill tại:
d:\Project\AI OS\skills\spawn-agent\SKILL.md
```

### Workflow khi có large task
```
User: "Refactor toàn bộ scripts/memory/"
Main Agent:
  1. Phân tích → break thành 3 subtasks
  2. spawn worker A: "Refactor backup_soul.ps1"
  3. spawn worker B: "Refactor wake_up.ps1"  
  4. spawn worker C: "Update integration tests"
  5. Review outputs từ A, B, C
  6. Merge/validate results
  7. Report to user
```

### Context Window Management
```
Trước spawn-agent:
Main context = goals + all file contents + build logs + errors
→ Overflow sau vài tasks phức tạp

Sau spawn-agent:
Main context = goals + delegation summaries + final results
→ Sạch, scalable hơn nhiều
```

---

## So sánh với Superpowers Sub-Agent

| Feature | Superpowers | spawn-agent |
|---------|-------------|-------------|
| Platform | Claude Code | Antigravity |
| Workers | Claude sub-agents | Gemini CLI, Codex CLI |
| Context isolation | ✅ Fresh sub-agent | ✅ Isolated CLI session |
| Parallel | ✅ via git worktrees | ✅ Parallel CLI calls |
| Template | Implicit in skill | ✅ Explicit delegation template |
| Review step | ✅ Automated | Manual (main agent reviews) |

---

## Liên quan đến AI OS Skill System

Skill này complement tốt với:
- `superpowers_agentic_framework.md` → cùng concept sub-agent
- `mcp_protocol_spec.md` → MCP sampling primitive (server-initiated sub-agent)
- `paperclip_agent_orchestration.md` → orchestrator pattern

**Next step cho AI OS:**
Clone skill này vào `skills/spawn-agent/` và adapt delegation templates cho AI OS context.

---

## References
- [GitHub](https://github.com/khanhbkqt/spawn-agent)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [OpenAI Codex CLI](https://github.com/openai/codex)
