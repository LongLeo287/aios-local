# 🧠 Intelligence Upgrade Analysis: Claude Patterns Integration

Based on research into `Piebald-AI/claude-code-system-prompts` and the `Claude Agent SDK`, we are upgrading the AI OS with senior-level orchestration patterns.

## 🚀 Key Insights & System Mappings

### 1. Dynamic Prompt Assembly (Mode-Based)
*   **Insight:** Claude Code uses different "fragment stacks" for Planning, Exploration, and Delegation.
*   **Upgrade:** We will modify `ORCHESTRATION_SOP.md` to require Agents to switch "Mental Context" (Prompts) when moving between `PLANNING` and `EXECUTION` modes.

### 2. Guardrails with XML Tagging
*   **Insight:** Extensive use of `<task>`, `<rules>`, `<guidelines>`, and `<examples>` to keep the model grounded.
*   **Upgrade:** All AI OS rules (e.g., `agent_behavior.md`) will be restructured to use strict XML-bounded sections for better instruction adherence.

### 3. Human-in-the-Loop (HITL) SDK Patterns
*   **Insight:** Use of `canUseTool` callbacks to intercept sensitive actions.
*   **Upgrade:** We will formalize the "Safety Shield" protocol in `AGENTS.md` to mirror the `canUseTool` logic for any destructive file system operations.

### 4. System Reminders & Reflection
*   **Insight:** Periodic "reminders" injected into the context window to prevent drift.
*   **Upgrade:** Implementing a "Context Refresh" ritual where the Orchestrator forces a re-read of the `blackboard.json` and `THESIS.md` every 5-10 tool calls.

---

## 🛠️ Action Plan: Intelligence Injection

### [ ] Phase A: Rule Restructuring
Update `agent_behavior.md` and `AGENTS.md` with XML-schema grounding.

### [ ] Phase B: Orchestration SOP Update
Integrate the "Mode-Switch" protocol into `ORCHESTRATION_SOP.md`.

### [ ] Phase C: Extension Core Upgrade (Phase 10)
Use these patterns to build the `AIEngine.js` - specifically how it prompts Gemini Nano using the "Prefilled Response Skeleton" technique found in the research.

---

**Bạn có đồng ý với bản phân tích và kế hoạch nâng cấp này không?** Sau khi bạn chốt, tôi sẽ tiến hành cập nhật kho lưu trữ quy tắc của hệ thống.
