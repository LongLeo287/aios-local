---
id: agentic_architectures_reference
name: Agentic Architectures Reference
version: 1.0.0
tier: 2
domain: ai-integration
cost_tier: standard
status: active
source: https://github.com/FareedKhan-dev/all-agentic-architectures
stars: 2901
license: MIT
updated: 2026-03-14
tech_stack: [Python, Pydantic, LiteLLM, OpenAI API]
tags: [agentic, architecture, patterns, multi-agent, planning, reasoning, LLM]
accessible_by: [Antigravity, Claude Code, Developer]
load_on_boot: false
---

# Agentic Architectures Reference

> 17 practical agentic design patterns for building LLM-powered AI systems.
> Source: FareedKhan-dev/all-agentic-architectures (2901 stars, MIT)

---

## Architecture Index

| # | Pattern | Core Idea | When to Use |
|---|---------|-----------|-------------|
| 01 | **Reflection** | Agent reviews & critiques its own output | Improve quality of generated code/text |
| 02 | **Tool Use** | Agent calls external tools/APIs | Fetch data, run code, interact with world |
| 03 | **ReAct** | Reason → Act → Observe loop | Step-by-step problem solving |
| 04 | **Planning** | Decompose goals into sub-tasks | Complex multi-step objectives |
| 05 | **Multi-Agent** | Multiple specialized agents collaborate | Parallel tasks, diverse expertise |
| 06 | **PEV** | Plan → Execute → Verify cycle | High-stakes tasks needing validation |
| 07 | **Blackboard** | Shared memory agents read/write to | Loosely coupled collaborative systems |
| 08 | **Episodic + Semantic** | Memory with episode recall + concept store | Personalized, context-aware assistants |
| 09 | **Tree of Thoughts** | Branch multiple reasoning paths | Exploration of solution space |
| 10 | **Mental Loop** | Continuous self-monitoring internal state | Long-running autonomous agents |
| 11 | **Meta-Controller** | Agent that manages other agents | Orchestration, routing, load balancing |
| 12 | **Graph** | Agents as nodes in a directed graph | Complex dependency workflows |
| 13 | **Ensemble** | Multiple agents vote on best answer | Reliability, reduce hallucination |
| 14 | **Dry Run** | Simulate execution before committing | Safe code execution, risk reduction |
| 15 | **RLHF** | Human feedback shapes agent behavior | Alignment, continuous improvement |
| 16 | **Cellular Automata** | Agents follow local rules, emergent behavior | Simulation, swarm intelligence |
| 17 | **Reflexive Metacognitive** | Agent monitors its own cognitive process | Self-improving, adaptive reasoning |

---

## Pattern Deep Dives

### 01 — Reflection
```
Agent output → Critic evaluates → Revised output
```
- Agent produces initial answer
- Internal or external critic identifies flaws
- Agent revises based on critique
- Repeat until quality threshold met

**Python pattern:**
```python
def reflection_loop(agent, critic, task, max_rounds=3):
    response = agent.generate(task)
    for _ in range(max_rounds):
        critique = critic.evaluate(response)
        if critique.score >= threshold:
            break
        response = agent.revise(response, critique)
    return response
```

---

### 02 — Tool Use
```
Task → LLM decides tool → Tool executes → Result → LLM continues
```
- LLM chooses from registered tools based on task
- Tool is executed with structured args (Pydantic model)
- Result returned to LLM context
- LLM continues reasoning with result

**Tool registration pattern:**
```python
from pydantic import BaseModel

class SearchArgs(BaseModel):
    query: str
    max_results: int = 5

tools = {
    "web_search": (search_fn, SearchArgs),
    "run_code": (code_runner, CodeArgs),
    "read_file": (file_reader, FileArgs),
}
```

---

### 03 — ReAct (Reasoning + Acting)
```
Thought → Action → Observation → Thought → ...
```
- Interleaves reasoning traces with tool calls
- Each step: Think (why) → Act (do) → Observe (result)
- Grounded — actions verify reasoning
- Best for: debugging, research, sequential workflows

**ReAct loop:**
```python
while not done:
    thought = llm.think(context)
    action = llm.choose_action(thought, tools)
    observation = tools[action.name](**action.args)
    context.add(thought, action, observation)
    done = llm.is_done(context)
```

---

### 04 — Planning
```
Goal → Decompose → Sub-tasks → Execute each → Aggregate
```
- Hierarchical task decomposition (HTD)
- Plan is generated upfront, then executed step-by-step
- Can be linear or DAG (parallel branches)
- Re-planning if execution fails

**Plan schema (Pydantic):**
```python
class Task(BaseModel):
    id: str
    description: str
    dependencies: list[str] = []
    status: Literal["pending", "running", "done", "failed"]

class Plan(BaseModel):
    goal: str
    tasks: list[Task]
    
    def get_ready_tasks(self):
        return [t for t in self.tasks 
                if t.status == "pending" 
                and all(dep.status == "done" for dep in t.dependencies)]
```

---

### 05 — Multi-Agent
```
Orchestrator → Routes task → Specialist Agents → Aggregate results
```
- Each agent has specialized role and context
- Orchestrator manages routing and aggregation
- Agents communicate via message passing or shared state
- Can run in parallel (async) or sequential

**Agent types pattern:**
```python
agents = {
    "researcher": ResearchAgent(model="gpt-4o"),
    "coder": CodeAgent(model="claude-3-5-sonnet"),
    "reviewer": ReviewAgent(model="gpt-4o-mini"),
    "orchestrator": OrchestratorAgent(agents=agents),
}
```

---

### 06 — PEV (Plan → Execute → Verify)
```
Plan → Execute → Verify → Accept or Re-plan
```
- Adds explicit verification step
- Verifier can be: LLM, test suite, human-in-loop
- Re-plan if verification fails
- Good for: code generation, data pipelines

---

### 07 — Blackboard
```
Agents ←→ Shared Blackboard (read/write) ←→ Agents
```
- Central knowledge store all agents can read/write
- No direct agent-to-agent communication
- Loosely coupled — agents are independent
- State machine drives which agent acts next

**Blackboard schema:**
```python
class Blackboard(BaseModel):
    problem: str
    partial_solutions: list[dict] = []
    hypotheses: list[dict] = []
    final_answer: str | None = None
    metadata: dict = {}
```

---

### 08 — Episodic + Semantic Memory
```
Experience → Episode Store   → Recall similar episodes
Context   → Semantic Store  → Retrieve relevant concepts
```
- **Episodic**: specific past interactions (vector DB)
- **Semantic**: general knowledge, concepts (knowledge graph)
- Combined: personalized agent that learns from history

---

### 09 — Tree of Thoughts (ToT)
```
Root thought → Branch N paths → Evaluate each → Prune → Best path
```
- BFS or DFS through thought space
- Each node = partial solution
- Evaluator scores each node
- Backtrack if path is dead end
- Best for: math, puzzles, creative writing

---

### 10 — Mental Loop
```
Perception → Internal State → Decision → Action → Perception...
```
- Agent maintains persistent internal state
- Continuous loop (not request-response)
- State machine: idle → perceiving → planning → acting → reflecting
- Best for: long-running autonomous agents

---

### 11 — Meta-Controller
```
Task → Meta-Controller → [Agent A, Agent B, Agent C] → Best result
```
- Orchestrator that routes based on task type
- Monitors agent performance, switches if needed
- Manages: timeouts, retries, load balancing
- Can spawn/terminate sub-agents dynamically

---

### 12 — Graph Architecture
```
Nodes (Agents) + Edges (Dependencies) → DAG execution
```
- Represent workflow as directed acyclic graph
- Parallel execution of independent nodes
- Natural for: ETL pipelines, CI/CD, data processing
- Use networkx or LangGraph for implementation

---

### 13 — Ensemble
```
Task → N independent agents → Vote/aggregate → Final answer
```
- Same task sent to multiple agents (or models)
- Aggregation strategies: majority vote, weighted average, best-of-N
- Reduces hallucination, increases reliability
- Cost: N × single agent cost

---

### 14 — Dry Run
```
Agent generates plan → Simulate in sandbox → Check for errors → Commit or abort
```
- Agent plans actions without executing them
- Simulator predicts outcomes
- Human or automated review
- Commit only if safe
- Best for: code deployment, financial transactions

---

### 15 — RLHF (Reinforcement Learning from Human Feedback)
```
Agent output → Human rates → Reward model → Policy update → Better output
```
- Collect agent outputs
- Humans rank outputs (preference pairs)
- Train reward model on preferences
- Fine-tune base model with PPO
- Continuous improvement loop

---

### 16 — Cellular Automata
```
Grid of agents → Each follows local rules → Emergent global behavior
```
- Each agent only knows its neighbors
- Simple local rules → complex global patterns
- Best for: simulation, swarm robotics, distributed systems
- Conway's Game of Life is classic example

---

### 17 — Reflexive Metacognitive
```
Agent acts → Metacognitive layer monitors → Detects anomalies → Adjusts strategy
```
- Two-level system: object-level reasoning + meta-level monitoring
- Meta-level asks: "Is my reasoning sound? Am I stuck in a loop?"
- Can modify its own prompts, memory, tool selection
- Most sophisticated — self-improving agents

---

## Technology Stack (from repo)

```
LiteLLM      → Unified LLM API (OpenAI, Anthropic, Gemini...)
Pydantic     → Structured data modeling for tool args and agent state
LangChain    → Optional — chain composition helpers
networkx     → Graph-based architectures
OpenAI API   → Primary LLM provider in examples
```

## Selection Guide

```
Simple Q&A               → Tool Use (02)
Sequential reasoning     → ReAct (03)
Complex goal             → Planning (04) or PEV (06)
Parallel tasks           → Multi-Agent (05) or Graph (12)
Unreliable output        → Ensemble (13) or Reflection (01)
Long-running agent       → Mental Loop (10)
Shared context           → Blackboard (07)
Personalization          → Episodic + Semantic (08)
Creative exploration     → Tree of Thoughts (09)
High-risk actions        → Dry Run (14)
Self-improvement         → RLHF (15) or Reflexive Metacognitive (17)
Distributed simulation   → Cellular Automata (16)
Route to specialists     → Meta-Controller (11)
```
