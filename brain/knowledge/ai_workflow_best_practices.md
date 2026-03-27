# AI Workflow Best Practices — Knowledge Base
# Source: D:\LongLeo\Project\DATA\POST.txt (Ingested 2026-03-15)
# Category: Tier 4 — Knowledge Library
# 469 lines, 90KB of community-curated AI development knowledge

---

## 1. REACT ENTERPRISE BOILERPLATE — Pro Folder Structure

**Repo:** `github.com/fdhhhdjd/react-enterprise-boilerplate`

### Folder Structure
```
src/
├── assets/         # Images, fonts, icons, global styles
├── components/     # Shared UI (Button, Modal...)
├── constant/       # Constants, enums
├── features/       # Business logic — organized by feature
├── hooks/          # Custom React hooks
├── layouts/        # Layout components (MainLayout, AuthLayout)
├── pages/          # Page components (route-mapped)
├── routes/         # Routing config
└── store/          # Global state (Redux/Zustand)
```

### 4 Core Architecture Principles
1. **Separation of Concerns** — Each folder has one role
2. **Feature-Based Structure** — `features/auth/` = components + services + hooks + slice + types
3. **Reusability** — `components/` for shared UI, `hooks/` for shared logic
4. **Scalable State** — Centralized `store/`, easy to debug and extend

---

## 2. SKILL CREATOR — Meta-Skill for Building AI Skills

### What is a Skill?
- An AI Skill = a **folder** containing: `SKILL.md` + resources/ + examples/ + scripts/ + workflows/
- NOT a one-file prompt — always a full package
- Benefits: Git-manageable, shareable, context-efficient (loaded on demand only)

### 5-Phase Skill Creation Pipeline
1. **Ideation & Draft** — Outline what the Skill should do
2. **Test & Evaluate** — Compare Skill vs no-Skill with real prompts (A/B test)
3. **Analyze & Demo** — Side-by-side output comparison, quantitative metrics
4. **Refine & Iterate** — Improve based on feedback, repeat
5. **Optimize Activation** — Fine-tune `description` field so AI triggers the Skill at right moment

### Skill Generator v4.0 — 5-Phase Pipeline
- **Phase 1 Deep Interview** — 5-10 questions using 5 techniques
- **Phase 2 Knowledge Extraction** — Goal, Instructions, Examples, Constraints
- **Phase 3 Pattern Detection** — 6 skill architectures (Script, Multi-Resource, Context-Aware, Safety-First, Pipeline, Composable)
- **Phase 4 Scaffold & Generate** — 10+ files per skill package
- **Phase 5 Live Test & Refine** — Dry run, auto-optimize, A/B testing, version tracking

### 7 Principles of a Perfect Skill
1. **Atomic Logic** — 1 skill = 1 job
2. **Semantic Trigger** — Description has enough keywords for auto-activation
3. **4 Core Sections** — Goal + Instructions + Examples + Constraints
4. **Show Don't Tell** — Full examples with Input/Output
5. **Semantic Precision** — Correct verbs (Extract, Identify, Generate...)
6. **Error Recovery** — Handle vague or erroneous user input
7. **Black Box Scripts** — Scripts have `--help` and `--dry-run`

### 8-Platform Compatibility
| Platform | Format | Install Path |
|----------|--------|-------------|
| Antigravity | Multi-file | `~/.gemini/antigravity/skills/` |
| Claude Code | Multi-file | `.claude/skills/` |
| Cursor | Multi-file | `.cursor/skills/` |
| OpenClaw/Cline/Aider | Single SKILL_FULL.md | — |

---

## 3. MULTI-AGENT SYSTEMS — Architecture Patterns

### Evolution: Chatbot → Agent → Multi-Agent → Autonomous Workflow

#### Claude Code (Auto-Spawning)
- Terminal-only, spawns up to 10 subagents automatically
- Best for: large codebase analysis, bug hunting in parallel
- Cost: Pro $20/mo, Max $100-200/mo + API token billing
- Weakness: most expensive, 100% terminal (non-tech hostile), parallel writes risk conflict

#### Cursor (Git Worktree Isolation)
- IDE-native, up to 8 agents on 8 independent branches
- Best for: new features, multi-file editing, shipping PRs fast
- Cost: Pro $20/mo (~225 Claude req), Ultra $200/mo
- Weakness: agents isolated (no shared context), no UI testing, credit burns fast

#### Antigravity (Mission Control)
- All-model access (Gemini Pro/Flash + Claude Sonnet/Opus + GPT) — currently FREE
- Best for: UI verification (browser automation, screenshot, video), verify-heavy tasks
- Cost: FREE (Public Preview), Google AI Pro $20/mo
- Weakness: must manually setup agents (no auto-spawn), ecosystem still maturing

### Cost Optimization Tips for OpenClaw
1. **Single Agent + Skills** — Instead of multi-agent, one agent + skills. Reduced cost from $300+/week to $90/month
2. **Smart Routing** — Simple tasks (heartbeat, lookup) → cheap model. Complex tasks → powerful model. Up to 70% cost reduction
3. **Prompt Caching** — Fix system instructions at top of prompt for provider caching. Saved from $720 to $72/month
4. **Context Management** — Create new conversations regularly, clean up SOUL.md, move specialized content to skills
5. **Local Models** — Light tasks via local model → zero API cost
6. **Daily Cost Monitoring** — Detect anomalies early before "wake up to a huge bill"

---

## 4. PROFESSIONAL AI PROMPTING — 8-Layer Stack

1. **Task** — "I want [ACTION] to achieve [SPECIFIC SUCCESS CRITERIA]"
   - No role-play. No pretending. Be direct.
2. **Context Files** — Upload expertise, rules, work style in separate files BEFORE starting
   - "Before answering, read all these files: [file.md] — [what file contains]"
3. **Reference** — Show examples, don't describe them. Give AI concrete output to match
4. **Brief** — Answer 3 questions: What type of output + length? What output must NOT sound like? What does success look like?
5. **Rules** — Personal rules file: standards, aesthetics, audience, prohibitions
   - Add: "If you're about to violate any of my rules, stop and notify me"
6. **Conversation** — "DO NOT execute anything yet. Ask me clarifying questions one at a time"
7. **Plan** — "Before writing, list 3 most important rules from my context file. Then outline your execution plan"
8. **Alignment** — "Only begin work when we have fully aligned"

---

## 5. CLAUDE CODE BEST PRACTICES

### Core Concepts
- **Commands** (`.claude/commands/`) — Workflow entry-points, call with `/command-name`
- **Sub-Agents** (`.claude/agents/`) — Specialized agents with name, color, tools, permissions
- **Skills** (`.claude/skills/`) — Reusable knowledge/workflows
- **Hooks** (`.claude/hooks/`) — Auto-run scripts on specific events outside agent loop
- **MCP Servers** — Connect Claude to external tools, databases, APIs
- **Memory** — CLAUDE.md for long-term project context

### Key Workflows
- **RPI Loop** — Research → Plan → Implement (NEVER jump straight to coding)
- **Plan Mode** — Always start with `/plan` to align direction first
- **Ralph Wiggum Loop** — For long autonomous runs

### Tips
- CLAUDE.md: max 150 lines to avoid context noise
- Use `/compact` when session > 50% context (reduces cost, increases accuracy)
- Create Sub-agents per feature (backend-agent, ui-agent) not one generic agent
- Commit after every small task
- Voice prompting with Wispr Flow for speed
- Wildcard permissions like `Bash(npm run *)` reduce confirmation dialogs
- `/doctor` to diagnose system errors
- Run terminal in background so Claude monitors logs while fixing code

---

## 6. AI-FIRST DESIGN WORKFLOW

1. **Clarify with AI first** (ChatGPT/Claude/Gemini) — User flow, IA, wireframe text, edge cases
2. **UI Generation** (Figma Make/Relume/Uizard) — 5-10 variations in seconds
3. **Refine Structure** — Rebuild with proper Auto Layout, fix hierarchy, standardize spacing
4. **Build Component System** — Convert AI output into Button/Form/Card/Header components
5. **Apply Visual Design** — Typography system, spacing logic, color hierarchy, accessibility
6. **Prototype & Audit** — Use AI to audit: "List 10 usability issues in this flow"

---

## 7. SECURITY BEST PRACTICES

### API Key Security
- NEVER store keys in `.txt`, `.docx`, or plain text files
- Always use `.env` files + add to `.gitignore`
- Tell AI explicitly: "Never write API keys to `.txt` or `.docx`"
- Set repo to private before any push

### Code Architecture Security
- **View** (Frontend) — What users see
- **Controller** (Backend) — Request processing
- **Model** (Backend) — Data storage
- Max 200-300 lines per file. 1 file = 1 responsibility

### Database Security (Supabase RLS)
- RLS = Row Level Security — Each row has its own guard
- Protection goes to individual data row, not just the table level

---

## 8. GENERATIVE AI PROJECT STRUCTURE

```
generative_ai_project/
├── config/           # model_config.yaml, logging_config.yaml
├── data/             # cache/, embeddings/, vectordb/
├── src/
│   ├── core/         # base_llm.py, gpt_client.py, model_factory.py
│   ├── prompts/      # templates.py, chain.py (multi-step)
│   ├── rag/          # embedder.py, retriever.py, vector_store.py, indexer.py
│   ├── processing/   # chunking.py, tokenizer.py, preprocessor.py
│   └── inference/    # inference_engine.py, response_parser.py
├── docs/             # README.md, SETUP.md
├── scripts/          # setup_env.sh, run_tests.sh, build_embeddings.py
└── Root/             # requirements.txt, Dockerfile, .gitignore
```

---

## 9. ANTIGRAVITY ALLOW LIST — Safe Commands to Add

### Docker & Server Monitoring
```bash
docker ps              # View running containers
docker logs            # Read logs (AI self-debug)
docker-compose ps      # Service status
pm2 status             # Node.js/Python background apps
pm2 logs               # PM2 logs
```

### Network & API Testing
```bash
curl    # Test API connections / HTTP webhooks
ping    # Basic network connectivity
```

### Git (Read-Only)
```bash
git status    # Track file changes
git diff      # Code diff
git log       # Commit history
git branch    # Branch list
```

### Node.js
```bash
npm install / npm ci / npm list
npm run dev / build / lint / format / test
```

### Python
```bash
pip install / pip list / python --version
pytest / python -m venv
```

### ⚠️ NEVER add to Allow List
- `prisma db push`, `npx drizzle-kit push` — Can silently mutate production DB
- `migrate` commands without user confirmation

---

## 10. AGENT SKILLS vs TOOLS vs MCP

| Level | Technology | What it does |
|-------|-----------|-------------|
| Hands | Tools/Function Calling | Execute a single command |
| Nervous System | MCP | Connect AI to external data sources |
| Handbook | **Agent Skills** | Strategy + knowledge + workflow + examples |

**Skills = on-demand context loading**: Agent keeps a short index of available skills. Only loads full SKILL.md when task requires it → saves context window, increases accuracy.

**The future**: A "skill marketplace" where developers share specialized skills (accounting, legal, data engineering) that any agent can install.

---

*Ingested from: D:\LongLeo\Project\DATA\POST.txt*
*Date: 2026-03-15 | Added to: knowledge/*
