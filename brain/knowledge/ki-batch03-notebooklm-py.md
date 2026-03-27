# KI: notebooklm-py — Unofficial Python API cho Google NotebookLM

## Metadata
- **Source:** https://github.com/teng-lin/notebooklm-py
- **Category:** Tools / AI Integration
- **Priority:** 🟡 HIGH — NotebookLM Agent skill
- **Ingested:** 2026-03-21
- **Batch:** 03

## Tóm Tắt
Unofficial Python API + agentic skill cho Google NotebookLM. Cho phép programmatic access đến NotebookLM's features — **kể cả capabilities mà web UI không expose**. Via Python, CLI, và AI agents.

## Tính Năng
### Content Generation (All NotebookLM Studio Types)
- Audio overview generation
- Briefing docs
- Study guides
- FAQ và timelines
- All studio content types

### Beyond Web UI
- Programmatic batch processing
- Agent-driven notebook management
- CLI access
- Automation workflows

### Agent Setup
- Compatible với Claude Code, Codex, OpenClaw

## Installation
```bash
pip install notebooklm-py

# Development
git clone https://github.com/teng-lin/notebooklm-py
pip install -e ".[dev]"
```

## What You Can Build
- Automated research pipelines
- Batch notebook processing
- AI agent that manages NotebookLM
- Content generation automation

## Liên Quan AI OS
- **CRITICAL CONNECTION**: Nova Agent là NotebookLM specialist trong AI OS
- Cho phép Nova access NotebookLM programmatically (không chỉ qua web)
- Tích hợp vào `brain/agents/notebooklm-agent/`
- Bổ sung cho `nova-intake-report` workflow

## AI OS Action
```
STATUS: 🔴 CRITICAL for Nova — Install cho NotebookLM agent
COMMAND: pip install notebooklm-py
INTEGRATION: brain/agents/notebooklm-agent/ 
NEXT: Tạo nova skill sử dụng notebooklm-py API
```
