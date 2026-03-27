# KI-MULTI-AGENT-PATTERNS-01 — Multi-Agent Patterns từ AgentScope & AgentTrafficControl
**Nguồn:** agentscope-ai/agentscope (Alibaba) + gkamradt/agenttrafficcontrol
**Ngày:** 2026-03-23 | **Verdict:** REFERENCE — học patterns, không integrate

---

## 1. AgentScope — Alibaba Multi-Agent Framework

### Agentic Reinforcement Learning (RL)
AgentScope triển khai Agentic RL — agents tự học từ feedback loops:
```
Agent acts → Environment responds → Reward signal → Policy update → Agent improves
```
**AI OS ứng dụng:** Corp Learning Loop đã có cơ chế tương tự. Mở rộng:
- Reward = CEO approval / task success
- Penalty = escalation / task failure
- Store outcomes in `decisions_log.md` → feed back into future prompts

### Distributed Agent Execution
```python
# AgentScope pattern: agents trên nhiều nodes
AgentScope.init(
    model_configs=[...],
    host="localhost",
    port=12345,
    use_monitor=True           # Built-in monitoring
)

# Launch distributed agent
agent = AgentScope.create_agent("worker", distributed=True)
```
**AI OS ứng dụng:** CrewAI đã cover phần này. AgentScope dùng nếu cần scale ngang.

### Real-time Voice Agent Pattern
```python
# Pattern: Voice input → LLM process → Voice output
voice_agent = VoiceAgent(
    model="whisper-large",
    tts="edge-tts",
    interrupt_enabled=True     # User có thể ngắt agent đang nói
)
```
**AI OS ứng dụng:** DEFER — cần khi build voice interface (Phase 8+)

### Human-in-the-Loop với MCP
```python
# Agents pause và đợi human input trước khi action quan trọng
@htil_checkpoint
def deploy_to_production(code):
    # Agent dừng ở đây, gửi request review tới CEO
    human_approval = await request_approval(code, reviewer="CEO")
    if human_approval:
        execute_deploy(code)
```
**AI OS ứng dụng:** Pattern này NÊN áp dụng cho mọi action có side-effects trong AI OS Corp.

---

## 2. AgentTrafficControl — Agent Load Balancing

### Core Problem
Khi nhiều agents cùng gọi LLM:
- Rate limit bị hit → requests fail
- Cost spike do duplicate calls
- No retry logic → silent failures

### Pattern: LLM Router
```python
class LLMRouter:
    def __init__(self):
        self.queues = {
            "primary": AsyncQueue(maxsize=10),    # GPT-4/Claude primary
            "fallback": AsyncQueue(maxsize=50),   # GPT-3.5/Haiku fallback  
            "batch": AsyncQueue(maxsize=200),     # Batch processing
        }
    
    def route(self, request):
        if request.priority == "high":
            return self.queues["primary"]
        elif request.tokens > 4096:
            return self.queues["batch"]
        else:
            return self.queues["fallback"]
```
**AI OS ứng dụng:** Dept 1 (Engineering) — implement khi AI OS có >5 concurrent agents.

### Pattern: Circuit Breaker
```python
class CircuitBreaker:
    """Stop calling a failing service after N failures"""
    def __init__(self, failure_threshold=5, recovery_time=60):
        self.failures = 0
        self.state = "CLOSED"   # CLOSED=normal, OPEN=blocking, HALF_OPEN=testing
    
    async def call(self, func):
        if self.state == "OPEN":
            raise CircuitOpenError("Service temporarily unavailable")
        try:
            result = await func()
            self.reset()
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"     # Stop calling
            raise
```
**AI OS ứng dụng:** Wrap Firecrawl, LightRAG, Mem0 calls với circuit breaker.

### Traffic Shaping: Token Budget
```python
# Limit agent spending per session
class TokenBudget:
    def __init__(self, max_tokens_per_session=100_000):
        self.budget = max_tokens_per_session
    
    def check(self, estimated_tokens):
        if self.budget - estimated_tokens < 0:
            raise BudgetExceededError("Session token limit reached")
        self.budget -= estimated_tokens
```
**AI OS ứng dụng:** Đã có `budget.json` trong ClawTask — extend này.

---

## Action Items cho AI OS

| Pattern | Priority | Owner | When |
|---------|----------|-------|------|
| HTIL checkpoints cho critical actions | P2 | Dept 10 | Phase 6 |
| Circuit breaker for Tier 1 services | P2 | Dept 1 | Phase 7 |
| Token budget enforcement | P3 | Dept 15 | Phase 8 |
| LLM Router (multi-agent scale) | P3 | Dept 1 | Phase 8+ |

*KI Note v1.0 | 2026-03-23 | Source: agentscope-ai/agentscope + gkamradt/agenttrafficcontrol*
