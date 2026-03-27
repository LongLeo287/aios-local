---
source: https://github.com/obra/superpowers
ingested_at: 2026-03-16T10:14:00+07:00
domain: AI|Development|AgentSkills|Methodology
trust_level: HIGH
vet_status: PASS
tags: [superpowers, claude-code, tdd, sub-agent, skills-framework, jesse-vincent, agentic-dev, anthropic-marketplace]
---

# Superpowers — Deep Analysis (obra/Jesse Vincent)

**Repo:** https://github.com/obra/superpowers  
**Lab (experimental):** https://github.com/obra/superpowers-lab  
**Author:** Jesse Vincent (obra) — creator of Bugzilla, K-9 Mail  
**Status:** Officially accepted into **Anthropic Claude plugin marketplace**  
**Stars:** Thousands+ (viral)

---

## Tổng quan Triết học

> "AI agents fail by skipping steps. Superpowers builds scaffolding that makes skipping impossible."

Superpowers không phải framework code — là **bộ quy trình kỷ luật** biến Claude Code từ "intelligent autocomplete" thành "senior AI developer".

**Core insight:** LLMs tự nhiên muốn ra code nhanh (instant gratification). Superpowers dùng **psychological framing + mandatory gates** để buộc agent đi đúng quy trình.

---

## Skills Directory Tree (Đầy đủ)

```
superpowers/
├── skills/
│   ├── subagent-driven-development/   ← Core: dispatch sub-agents cho tasks
│   │   └── SKILL.md
│   ├── using-git-worktrees/           ← Isolated workspaces
│   │   └── SKILL.md
│   ├── dispatching-parallel-agents/   ← Parallel task execution
│   │   └── SKILL.md
│   ├── requesting-code-review/        ← Request review
│   │   └── SKILL.md
│   ├── receiving-code-review/         ← Process review feedback
│   │   └── SKILL.md
│   ├── writing-skills/               ← Meta: write new skills
│   │   └── SKILL.md
│   └── [more skills...]
├── scripts/                           ← Utility scripts
└── README.md

superpowers-lab/                       ← Experimental
└── skills/
    ├── using-tmux-for-interactive-commands/
    │   └── SKILL.md
    └── [experimental skills...]
```

**Install locations:**
- `~/.claude/skills/` (personal)
- `~/.config/superpowers/skills/` (config)
- `.claude/skills/` (project-level)

---

## 5-Phase Workflow Chi Tiết

### Phase 1: Socratic Brainstorming (`/superpowers:brainstorm`)
```
User: "Tôi muốn thêm authentication"
Agent: "Bạn thực sự đang cố giải quyết vấn đề gì?"
→ Iterative refinement (hỏi từng phần nhỏ)
→ Spec được approve từng chunk
→ Design document hoàn chỉnh được tạo
```
**Tại sao Socratic?** Buộc user clarify trước khi AI commit. Tránh "build the wrong thing right".

### Phase 2: Structured Planning (`/superpowers:write-plan`)
Plan format bắt buộc:
```markdown
## Task N: [Tên ngắn gọn]
**Files:** `exact/path/to/file.ts`
**Code:** [Complete code, không phải snippets]
**Tests:** [Test cases cụ thể]
**Verification:** [Cách verify task done]
**Estimated time:** 2-5 minutes
```
> ⚠️ Tasks phải nhỏ (2-5 phút). Tasks lớn hơn → phải break down.

### Phase 3: Git Worktree Setup (`using-git-worktrees`)
```bash
# Sau khi design approved:
git worktree add ../project-task-1 feature/task-1
git worktree add ../project-task-2 feature/task-2
# Mỗi task có isolated branch + working directory
# Test baseline clean verified trước khi implement
```

### Phase 4: Sub-Agent Execution (`/superpowers:execute-plan`)

```
Main Agent (Orchestrator)
    │
    ├── Task 1 → spawn Sub-Agent A (fresh context)
    │               │
    │               ├── 🔴 RED: Write failing test
    │               ├── ✅ GREEN: Write minimal code
    │               ├── 🔵 REFACTOR: Clean up
    │               └── ✓ Return result
    │
    ├── [Code Review triggered between tasks]
    │
    ├── Task 2 → spawn Sub-Agent B
    │   ...
    └── Task N → spawn Sub-Agent N
```

**Sub-agent benefits:**
- Fresh context = không bị contaminate bởi previous tasks
- Parallel execution qua `dispatching-parallel-agents`
- Scope-limited = ít hallucination hơn

**Execution modes:**
```
Sequential:  Task 1 → review → Task 2 → review → Task 3
Batch:       [Task 1, 2, 3] → human checkpoint → [Task 4, 5, 6]
Parallel:    Task 1 ─┬─ Task 2
                     └─ Task 3 (via git worktrees)
```

### Phase 5: Automated Code Review (Between Every Task)
```
Review report format:
├── 🔴 CRITICAL: [Block — must fix before next task]
├── 🟡 MEDIUM:   [Should fix]
└── 🟢 LOW:      [Nice to have]

If CRITICAL found → Next task BLOCKED → Fix required
```
**Reviews check:**
1. Spec compliance (vs. original plan)
2. Code quality (patterns, naming, complexity)
3. Test coverage
4. Security issues

---

## Mandatory TDD Enforcement

### RED → GREEN → REFACTOR (Enforced, not suggested)

```python
# WRONG — Claude bị bắt phải xóa code này:
def authenticate(user, password):
    return True  # Code viết trước test

# CORRECT sequence:
# Step 1 (RED): 
def test_authenticate_valid_user():
    assert authenticate("alice", "correct") == True  # FAIL (function chưa có)

# Step 2 (GREEN):
def authenticate(user, password):
    # Minimum code to pass test
    return db.verify(user, password)

# Step 3 (REFACTOR):
def authenticate(user: str, password: str) -> bool:
    """Verify user credentials against database."""
    return db.verify_credentials(user, password)
```

**Enforcement mechanism:**
- Skill instructions explicitly state: "If you see code written before tests, delete it"
- Agent committed to TDD in brainstorm phase → Cialdini Commitment principle

---

## Psychological Principles (Unique Feature)

Superpowers design tích hợp **Cialdini's 6 Principles of Influence** để increase LLM compliance:

### 1. Commitment & Consistency
```
"In the brainstorm phase, you agreed to follow TDD.
You committed to writing tests first.
Be consistent with that commitment."
→ LLM không muốn contradictory với prior commitment
```

### 2. Authority
```
"Senior engineers always follow RED-GREEN-REFACTOR.
This is an academically verified best practice.
The best developers in the world use this approach."
→ LLM defers to authoritative framing
```

### 3. Social Proof
```
"All professional software teams use code review.
The best open-source projects require tests before merging.
This is standard practice among top engineers."
→ LLM follows perceived social norms
```

### 4. Scarcity (Used subtly)
```
"This task window is limited.
Write focused, minimal code that solves just this task."
→ Tránh scope creep
```

### 5. Liking (Rapport building)
```
Socratic approach tạo collaborative feeling
→ User feels heard → More likely to follow structured process
→ Agent "likes" the collaborative relationship
```

### 6. Reciprocity
```
"I've helped you clarify the design.
Now let's honor that work by following the plan carefully."
→ Commitment to not waste prior effort
```

---

## tmux Integration (superpowers-lab)

Skill `using-tmux-for-interactive-commands`:
```bash
# Dùng tmux để control interactive CLI tools
tmux new-session -d -s agent-task-1
tmux send-keys -t agent-task-1 "npm test --watch" Enter
# Agent có thể observe output + respond
# Cho phép long-running processes trong background
```
**Use cases:**
- Test runners với watch mode
- Database shells (psql, sqlite3)
- Dev servers
- Interactive REPLs

---

## Self-Improvement System

```
Claude có thể:
1. Đọc skill-writing/SKILL.md → học cách viết skills
2. Identify gap trong workflow
3. Write NEW SKILL để fill gap
4. Add to skills directory
5. Hệ thống mở rộng từ usage experience
```

**Meta-skill: `writing-skills/SKILL.md`**
Teaches Claude how to:
- Structure SKILL.md files đúng format
- Write effective descriptions (triggers)
- Include executable scripts
- Test skill effectiveness

---

## Plugin Marketplace

```bash
# Cài từ Anthropic Claude marketplace:
/plugin install superpowers@claude-plugins-official

# Hoặc add marketplace:
/marketplace add https://plugins.anthropic.com/marketplace
/plugin install superpowers
```

---

## Installation (DIY)

```bash
# Clone repo
git clone https://github.com/obra/superpowers

# Copy vào Claude skills directory
cp -r superpowers/skills/* ~/.claude/skills/

# Hoặc project-level:
cp -r superpowers/skills/* .claude/skills/

# Lab skills (experimental):
git clone https://github.com/obra/superpowers-lab
cp -r superpowers-lab/skills/* ~/.claude/skills/
```

---

## So sánh với AI OS (Deep)

| Feature | Superpowers | AI OS | Gap/Opportunity |
|---------|-------------|-------|-----------------|
| Skill format | SKILL.md | SKILL.md | ✅ Compatible |
| Workflow enforcement | Mandatory gates | Optional/suggested | ⚠️ AI OS có thể học |
| TDD enforcement | Hard (delete violations) | Không có | 🔴 Add TDD skill |
| Sub-agent dispatch | Built-in | Manual | 🔴 Add sub-agent |
| Code review | Automated between tasks | Manual | 🟡 Add review skill |
| Git worktrees | Built-in | Không có | 🟡 Add worktree skill |
| Psychological framing | Cialdini principles | Không explicit | 🟢 Apply to task.md |
| Self-improvement | Write new skills | skill_loader.ps1 | ✅ Đã có |
| tmux integration | Experimental | Không có | 🟢 Nice to have |
| Plugin marketplace | Anthropic marketplace | Không có | 🟢 Long-term |

---

## Actionable Adaptations cho AI OS

### 1. Adopt Mandatory Workflow Gates
```markdown
# Thêm vào skills/task_manager/SKILL.md:
## MANDATORY SEQUENCE
You MUST NOT write code until you have:
- [ ] Clarified requirements (brainstorm)
- [ ] Written implementation plan (user approved)
- [ ] Written failing tests (RED phase)
Only then proceed to GREEN phase.
```

### 2. Add TDD Skill
```
File: skills/tdd-enforcer/SKILL.md
Trigger: "khi viết code mới"
Content: RED-GREEN-REFACTOR cycle + enforcement rules
```

### 3. Psychological Framing trong task.md
```
Thêm commitment anchors:
"Bạn đã đồng ý với plan này. Hãy nhất quán với cam kết đó."
"Senior engineers trong AI OS team luôn test trước khi code."
```

### 4. Sub-Agent Pattern cho Complex Tasks
```
Complex task → spawn sub-agent với SPECIFIC scope
→ Review sub-agent output trước khi accept
→ Main agent tiếp tục với reviewed result
```

---

## References
- [GitHub](https://github.com/obra/superpowers)
- [superpowers-lab](https://github.com/obra/superpowers-lab)
- [Medium breakdown](https://medium.com)
- [Pasquale's analysis](https://pasqualepillitteri.it)
- [yuv.ai article](https://yuv.ai)
- [Cialdini's Influence](https://www.influenceatwork.com)
