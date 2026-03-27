# Agentic AI Patterns — AI OS Knowledge Library
# Extracted from: agency-agents, deepagents, bmad_repo, cognee
# Updated: 2026-03-17

---

## Pattern 1: Role-First Multi-Agent System (agency-agents)

All 120+ agency agent personalities follow the Role-First pattern:
each agent has a **single, focused identity** (one role, one domain)
with specific success metrics, memory behavior, and communication style.

```
Agent = Role Definition + Memory Strategy + Success Metrics + Communication Style
     ↓
Clear identity → consistent, predictable outputs
No identity → hallucinated, inconsistent behavior
```

**Key insight:** Give every agent a *vibe* line: one sentence that captures personality.
Example: `"Finds the growth channel nobody's exploited yet — then scales it."`

---

## Pattern 2: BMAD Agile Agent Team (bmad_repo)

The BMAD Method defines a complete agile product team as agents:
```
Analyst → Product Manager → Architect → Scrum Master → Developer → QA → UX → Writer
```

Each agent has:
- **Menu triggers** (short codes: `CP`, `SP`, `QA`)
- **Primary workflow** (one sentence what it does)
- **Handoff protocol** (what it passes to the next agent)

This enables a complete software product lifecycle run entirely by agents.

---

## Pattern 3: DeepAgents Harness (deepagents/LangGraph)

DeepAgents implements the **Supervisor + Subagent** agentic pattern using LangGraph:

```python
# Core structure:
supervisor = create_supervisor(
    agents=[researcher, coder, analyst],
    model=llm,
    prompt="Route task to best subagent"
)
# State flows through a graph:
# START → Supervisor → [specialized agent] → Supervisor → END
```

**AI OS translation:**
- `orchestrator_pro` = Supervisor
- Specialist agents = subagents
- `shared-context/blackboard.json` = LangGraph state

**Key insight:** Supervisors should have routing logic, not domain expertise.
Domain experts are the subagents.

---

## Pattern 4: Cognee Knowledge Graph Memory (cognee)

Cognee makes agent memory queryable via knowledge graphs:

```python
import cognee
cognee.add(text)          # Add to memory
cognee.cognify()          # Process into KG
results = cognee.search(  # Query semantic memory
    "What did we decide about the API?",
    SearchType.INSIGHTS
)
```

**AI OS translation:**
- Store agent outputs → `cognee.add()`
- After each session → `cognee.cognify()` to build KG
- Before each task → `cognee.search()` to retrieve context
- This gives agents **persistent, queryable long-term memory**

---

## Pattern 5: From Personality to Agent (extraction protocol)

When ingesting agency-agents personalities into AI OS:

```
1. Read personality file (agency-agents/<domain>/<name>.md)
2. Extract:
   - Role definition → SKILL.md description
   - Core capabilities → exposed_functions
   - Success metrics → keep as-is
   - Communication style → behavior notes
3. Add AI OS-specific fields:
   - tier (Tier 2 = subagent, Tier 3 = agent)
   - accessible_by
   - source (original file path)
4. Write SKILL.md to agents/ or subagents/
```

---

## Pattern 6: Agentic Workflow Templates (agency-agents/examples)

The agency-agents repo includes workflow composition examples:
- `workflow-startup-mvp.md` — full MVP from idea to launch
- `workflow-book-chapter.md` — multi-agent content creation
- `workflow-landing-page.md` — Design + Copy + Analytics team
- `workflow-with-memory.md` — persistent agent memory via Nexus

**AI OS translation:** These map to Cowork Session Templates in `cowork/COWORK_PROTOCOL.md`

---

## Pattern 7: OpenClaw-RL Self-Improvement (openclaw-rl)

OpenClaw implements async reinforcement learning for agent improvement:

```
Agent executes task → Evaluator scores output → RL updates agent policy
```

**AI OS translation:**
- After each major task: cognitive_reflector scores output quality
- Low scores → feed to cognitive_evolver for capability update
- Track: success rate, latency, user satisfaction per agent
- Monthly: prune underperforming agents, promote successful ones

---

## Pattern 8: PageIndex Vectorless RAG (pageindex)

PageIndex uses structural parsing (headings, sections) instead of vectors:

```
Document → Parse structure → RAPTOR tree → Query by section path
```

**AI OS translation:**
- Use PageIndex for structured docs: RFCs, PRDs, manuals
- Use NexusRAG for unstructured corpus
- Use Cognee for dynamic, session-based memory
- Layer these: PageIndex (structure) + NexusRAG (semantic) + Cognee (episodic)
