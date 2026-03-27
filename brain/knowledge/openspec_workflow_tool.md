---
source: https://github.com/Fission-AI/OpenSpec (local clone: D:\Project\DATA\Archive\eco-ingest\OpenSpec)
ingested_at: 2026-03-16T10:34:00+07:00
domain: AI|Workflow|SpecFirst|Development
trust_level: HIGHEST
vet_status: PASS
tags: [openspec, spec-first, slash-commands, planning, claude-code, cursor, ai-workflow, fission-ai]
---

# OpenSpec — Spec-First AI Development Workflow

**Repo:** https://github.com/Fission-AI/OpenSpec  
**NPM:** `@fission-ai/openspec`  
**Support:** 20+ AI tools (Claude, Cursor, Copilot, etc.)  
**Philosophy:** Agree before you build

---

## Core Problem

> AI coding agents code before aligning on specs → vague prompts → unpredictable results.

OpenSpec adds **lightweight spec layer** giữa idea và code:
```
Idea → /opsx:propose → SPEC APPROVED → /opsx:apply → /opsx:archive
```

---

## Workflow Demo

```text
You: /opsx:propose add-dark-mode
AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md  — why we're doing this, what's changing
     ✓ specs/       — requirements and scenarios
     ✓ design.md    — technical approach
     ✓ tasks.md     — implementation checklist

You: /opsx:apply
AI:  ✓ 1.1 Add theme context provider
     ✓ 1.2 Create toggle component
     ✓ 2.1 Add CSS variables
     ✓ 2.2 Wire up localStorage
     All tasks complete!

You: /opsx:archive
AI:  Archived to openspec/changes/archive/2025-01-23-add-dark-mode/
```

---

## Slash Commands

### Core Workflow
| Command | Action |
|---------|--------|
| `/opsx:propose <idea>` | Generate spec artifacts (proposal, specs, design, tasks) |
| `/opsx:apply` | Implement tasks from spec |
| `/opsx:archive` | Archive completed change |

### Extended Workflow (select via `openspec config profile`)
| Command | Action |
|---------|--------|
| `/opsx:new` | Start new change |
| `/opsx:continue` | Resume in-progress change |
| `/opsx:ff` | Fast-forward — skip to next step |
| `/opsx:verify` | Verify implementation |
| `/opsx:sync` | Sync spec with codebase |
| `/opsx:bulk-archive` | Archive multiple changes |
| `/opsx:onboard` | Onboard team member |

---

## Spec Artifacts Structure

```
openspec/
└── changes/
    ├── add-dark-mode/          ← Active change
    │   ├── proposal.md         ← Why + what
    │   ├── specs/              ← Requirements + scenarios
    │   ├── design.md           ← Technical approach
    │   └── tasks.md            ← Implementation checklist
    └── archive/
        └── 2025-01-23-add-dark-mode/
            └── [completed specs]
```

---

## Setup

```bash
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init

# Update agent instructions
openspec update

# Configure profile  
openspec config profile  # Select workflow depth
```

---

## So sánh với Alternatives

| Tool | Pros | Cons |
|------|------|------|
| **OpenSpec** | Lightweight, fluid, 20+ tools | - |
| GitHub Spec Kit | Thorough | Heavyweight, Python setup required |
| AWS Kiro | Powerful | Locked to their IDE, Claude-only |
| Nothing | Quick | Vague prompts, unpredictable |

---

## Patterns Học Được cho AI OS

### Pattern 1: Proposal → Spec → Design → Tasks
```
Tương tự implementation_plan.md của AI OS, nhưng có thêm:
→ proposal.md: *why* trước khi *what*
→ specs/ folder riêng với scenarios
→ Archive completed changes (lịch sử quyết định)
```

### Pattern 2: Archived Changes = Decision History
```
Mỗi feature được archive kèm full spec → 
→ AI tương lai có thể trace *tại sao* code được viết vậy
→ AI OS: tạo archives/ trong .ai-memory/
```

### Pattern 3: `/opsx:verify` Command
```
Sau khi implement → riêng 1 command verify
→ AI OS: verify step sau mỗi major change
```

---

## Relevance cho AI OS

| Aspect | Assessment |
|--------|------------|
| Adopt as-is | Partial — install vào AI OS project |
| Key pattern | Proposal → Spec before Code |
| Workflow gate | Tương tự Superpowers mandatory gates |
| Archive pattern | Bổ sung cho implementation_plan.md |

---

## References
- [GitHub](https://github.com/Fission-AI/OpenSpec)
- [NPM](https://www.npmjs.com/package/@fission-ai/openspec)
- [Docs](https://openspec.dev)
