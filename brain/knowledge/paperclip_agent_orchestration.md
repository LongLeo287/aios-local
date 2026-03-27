---
source: https://github.com/paperclipai/paperclip
ingested_at: 2026-03-16T10:07:00+07:00
domain: AI|Architecture|AgentOrchestration
trust_level: HIGH
vet_status: PASS
tags: [agent-orchestration, multi-agent, ai-company, open-source, self-hosted, node-js]
---

# Paperclip AI — Multi-Agent Orchestration Platform

**Repo:** https://github.com/paperclipai/paperclip  
**Concept:** "Zero-human companies" — điều hành công ty hoàn toàn bằng AI agents  
**Name origin:** Inspired by "Paperclip Maximizer" thought experiment (misaligned AI)  
**License:** Open-source, self-hosted

---

## Tổng quan

Paperclip là **control plane** để quản lý đội ngũ AI agents như một công ty thực sự.  
Không phải chatbot framework — là **quản lý tổ chức AI**.

> "Hire virtual employees, assign roles, delegate goals, control budgets."

---

## Core Architecture

```
┌─────────────────────────────────────────┐
│  PAPERCLIP PLATFORM                     │
│                                         │
│  ┌──────────┐    ┌──────────────────┐   │
│  │ React UI │    │  Node.js Server  │   │
│  │ Dashboard│    │  (Orchestrator)  │   │
│  └──────────┘    └────────┬─────────┘   │
│                           │             │
│         ┌─────────────────┼──────────┐  │
│         ▼                 ▼          ▼  │
│    ┌─────────┐      ┌─────────┐  ┌────┐ │
│    │ AI CEO  │      │ AI CTO  │  │...│  │
│    │ Agent   │      │ Agent   │  │   │  │
│    └────┬────┘      └────┬────┘  └────┘ │
│         │ delegates      │              │
│    ┌────▼────┐      ┌────▼────┐         │
│    │Engineer │      │Engineer │         │
│    │ Agent   │      │ Agent   │         │
│    └─────────┘      └─────────┘         │
└─────────────────────────────────────────┘
```

**Tech Stack:** Node.js (≥v20) + React  
**Model:** Org-chart-as-orchestration — hierarchy như công ty thực

---

## 5 Key Features

### 1. Agent Orchestration (Org Chart)
- Tạo AI organizational chart với roles: CEO, CTO, Engineers, etc.
- AI CEO delegate tasks xuống CTO → Engineers
- Mỗi goal traceable về company mission
- Hỗ trợ: Claude Code, OpenClaw, Codex, Cursor + custom adapters

### 2. Ticket System (Communication)
- Toàn bộ giao tiếp qua ticket-based system
- **Immutable audit log** — mọi quyết định, conversation đều được ghi
- Full observability + accountability
- Tickets = persistent tasks, không mất khi restart

### 3. Heartbeat System
- Agents được schedule "wake up" theo interval
- Tự kiểm tra work queue, thực hiện tasks autonomously
- **Bring-Your-Own-Agent** — bất kỳ agent nào nhận được heartbeat signal đều tích hợp được
- Không cần human trigger

### 4. Cost Control
- Per-agent **monthly budget** caps
- Hard spending limits — agent tự pause khi hit limit
- Tracking chi phí API calls real-time
- Ngăn unexpected expenses khi agents chạy autonomous

### 5. Observability Dashboard
- React UI quản lý toàn bộ AI workforce
- Monitoring dashboards
- Audit trails cho compliance
- Clipmart (planned): marketplace cho pre-built company templates

---

## So sánh với AI OS

| Feature | AI OS | Paperclip |
|---------|-------|-----------|
| Agent roles | Skills/Plugins | Org chart (CEO/CTO/Engineers) |
| Communication | Blackboard/Channels | Ticket system |
| Scheduling | Manual trigger | Heartbeat (auto) |
| Cost control | Không có | Per-agent budget |
| Audit | Conversation logs | Immutable audit log |
| Scope | Single machine | Multi-agent company |

---

## Patterns học được từ Paperclip

### Pattern 1: Heartbeat cho AI OS
```
Thay vì user nói "Wakeup" → AI OS tự wake up theo schedule
→ Check ticket queue → thực hiện pending tasks
```

### Pattern 2: Ticket-based Task Delegation
```
User → tạo "ticket" (task description)
→ Agent nhận ticket → thực hiện → update status
→ Immutable log của mọi action
```

### Pattern 3: Budget per Skill
```
Mỗi skill trong AI OS có API budget cap
→ Tránh skill "runaway" tốn token không kiểm soát
```

### Pattern 4: Goal Traceability
```
Mọi task phải traceable về project goal
→ Agent từ chối task không liên quan đến goal
```

---

## Setup (Self-hosted)

```bash
# Requirements: Node.js >= 20
git clone https://github.com/paperclipai/paperclip
cd paperclip
npm install
npm run dev
# UI tại http://localhost:3000
```

---

## Đánh giá cho AI OS

| Aspect | Assessment |
|--------|------------|
| **Relevance** | HIGH — cùng domain multi-agent orchestration |
| **Inspiration** | Heartbeat, ticket system, cost control |
| **Adopt** | Concepts, không phải full adoption |
| **Maturity** | Early-stage, Clipmart chưa có |
| **Self-hostable** | ✅ Phù hợp với philosophy AI OS |

---

## References
- [GitHub](https://github.com/paperclipai/paperclip)
- [eWeek Review](https://www.eweek.com)
- [Reddit Discussion](https://www.reddit.com/r/LocalLLaMA)
