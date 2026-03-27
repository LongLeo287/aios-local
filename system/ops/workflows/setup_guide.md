# Department: operations
# AI OS CORP â€” Setup Guide
# Sau khi clone, chá»‰ cáº§n 2 bÆ°á»›c lÃ  cháº¡y Ä‘Æ°á»£c

## âš¡ Quick Start

```powershell
# 1. Clone repo
git clone <repo-url> "d:\AI OS CORP"

# 2. CÃ i Python dependencies (1 láº§n)
cd "<AI_OS_ROOT>"
pip install -r requirements.txt

# 3. Khá»Ÿi Ä‘á»™ng
"<AI_OS_ROOT>\launcher\AI OS CORP.cmd"
```

---

## System Requirements (cÃ i 1 láº§n náº¿u chÆ°a cÃ³)

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org/downloads) hoáº·c `winget install Python.Python.3.12` |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) hoáº·c `winget install OpenJS.NodeJS` |
| Git | any | `winget install Git.Git` |
| Docker | any | [docker.com](https://docker.com/products/docker-desktop) |
| Ollama | any | [ollama.ai](https://ollama.ai/download) |

> **Bun, uv** â€” optional, cáº§n khi dÃ¹ng claude-mem hoáº·c cognee

---

## Python Dependencies

Táº¥t cáº£ trong `requirements.txt` â€” cháº¡y 1 láº§n:

```powershell
pip install -r requirements.txt
```

| Package | DÃ¹ng cho |
|---------|---------|
| python-dotenv | ClawTask, AgAuto |
| pypdf | ClawTask (Ä‘á»c PDF) |
| fastapi + uvicorn | ACP, AgAuto API |
| supabase | ClawTask backend |
| requests + httpx | HTTP chung |
| mem0ai | Agent memory plugin |
| firecrawl-py | Web intelligence (Phase 2) |
| crewai | Multi-agent (Phase 4) |
| lightrag-hku | Knowledge graph (Phase 3) |

---

## Special Installs (cáº§n thÃªm bÆ°á»›c)

### MaxKB
```powershell
cd "<AI_OS_ROOT>\plugins\MaxKB"
docker compose up -d
# UI: http://localhost:8080/maxkb
```

### claude-mem (trong Claude Code)
```
/plugin install claude-mem
```

### nullclaw (binary Ä‘Ã£ cÃ³ sáºµn)
```
# KhÃ´ng cáº§n cÃ i thÃªm â€” binary cÃ³ táº¡i:
REMOTE\claws\nullclaw\zig-out\bin\nullclaw.exe
```

---

## External API Keys

ThÃªm vÃ o `ops/secrets/MASTER.env`:

```env
OPENROUTER_API_KEY=sk-or-...
FIRECRAWL_API_KEY=fc-...
```

---

*Dashboard: `launcher\AI OS CORP.cmd` â†’ [I] Install Manager Ä‘á»ƒ kiá»ƒm tra tráº¡ng thÃ¡i*

