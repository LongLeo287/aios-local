# browser-use — Wired as Web-Crawler Backend
Date: 2026-03-25
Status: INSTALLED (pip install browser-use)
Route: CIV pipeline → web-crawler agent → browser-use

## Usage in CIV
When CIV classifies input as WEB type:
→ web-crawler agent calls browser_use.Agent
→ LLM: ChatGoogle (gemini-3-flash) or Groq
→ Output: extracted content → brain/knowledge/notes/KI-<name>.md

## Install note
- Installed: 2026-03-25
- Python: 3.14 (browser_use __version__ not exposed but functional)
- Config: add BROWSER_USE_API_KEY to .env for cloud, or use local Chromium
