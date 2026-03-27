# Nova Hot Cache | Updated: 2026-03-21 | v4.1
# CEO Standing Order: ACTIVE â€” All inputs must be analyzed & archived

---

## ðŸ”´ PINNED RULES (KhÃ´ng bao giá» override)

### [RULE-STORAGE-01] Storage Location *(CEO 2026-03-21 â€” Tuyá»‡t Ä‘á»‘i)*
| | Path | Action |
|---|---|---|
| âœ… **Project files** | `D:\Project\AI OS\` | Táº¡o/lÆ°u Táº¤T Cáº¢ project files táº¡i Ä‘Ã¢y |
| ðŸ”’ **System data** | `C:\...\'.gemini`, `.claude`, `.codex`, `.nullclaw`, `.ollama` | KHÃ”NG xÃ³a / KHÃ”NG di chuyá»ƒn |
| âŒ **Banned** | `C:\Desktop`, `C:\Documents`, `C:\Temp`, báº¥t ká»³ C:\ khÃ¡c | KHÃ”NG táº¡o files |
| âš ï¸ **Exception** | `C:\...\antigravity\skills\` | ÄÆ°á»£c mirror tá»« D: (source of truth = D:) |

**Full rule:** `D:\Project\AI OS\brain\knowledge\notes\RULE-STORAGE-01-storage-location.md`

---

## ðŸ“š Active Notebooks (0/30)

| ID | Name | Plugin | Privacy | Last Used | Dept | KI Path |
|----|------|--------|---------|-----------|------|---------|
| â€” | (chá» CEO input Ä‘áº§u tiÃªn) | â€” | â€” | â€” | â€” | â€” |

---

## ðŸ”‘ Domain Terms (8/30)

| Term | Äá»‹nh nghÄ©a ngáº¯n | Source |
|------|-----------------|--------|
| SKILL.md | File Ä‘á»‹nh nghÄ©a skill: name, description, trigger, commands | AI OS Corp Standard |
| open-notebook | Self-hosted NLM alternative, 16+ AI providers, Ollama support | ecosystem/plugins/open-notebook |
| notebooklm-skill | Plugin browser automation â†’ query Google NotebookLM | ecosystem/plugins/notebooklm-skill |
| gitingest | Convert repo â†’ clean text digest cho NLM input | ecosystem/plugins/gitingest |
| grounding | CÃ¢u tráº£ lá»i dá»±a trÃªn source, cÃ³ citation â€” KHÃ”NG hallucinate | NLM Core Rule |
| synthesis | Tá»•ng há»£p nhiá»u nguá»“n â†’ 1 output cÃ³ cáº¥u trÃºc + citation | Nova Core Task |
| intake | Quy trÃ¬nh tiáº¿p nháº­n vÃ  phÃ¢n loáº¡i input tá»« CEO/Depts | Nova v4.0 |
| KI | Knowledge Item â€” artifact lÆ°u trá»¯ kiáº¿n thá»©c vÃ o brain/knowledge/ | AI OS Corp |

---

## ðŸ“¥ CEO Input Queue (Standing Order)

| # | Input | Type | Status | Priority |
|---|-------|------|--------|----------|
| â€” | Chá» CEO cung cáº¥p | â€” | â³ Ready | â€” |

---

## ðŸ“‹ Dept Pending Requests (tá»« v3.0 sessions)

| Dept | Request | Priority | Status |
|------|---------|----------|--------|
| Dept 4 (Registry) | Review táº¥t cáº£ SKILL.md descriptions < 1024 chars | HIGH | â³ Pending |
| Dept 5 (Marketing) | ÄÃ¡nh giÃ¡ prompts.chat cho content calendar | MED | â³ Pending |
| Dept 8 (Ops) | Import 69 Antigravity workflows vÃ o ClawTask | MED | â³ Pending |
| Dept 16 (OD&L) | Táº¡o GEMINI.md hot cache pattern cho agents | LOW | â³ Pending |

---

## âš¡ Tool Status (checked: 2026-03-21)

| Plugin | Status | Port | Notes |
|--------|--------|------|-------|
| open-notebook | âœ… Running | 5055 (API) / 8502 (UI) | Docker Up 2h+ |
| SurrealDB | âœ… Running | 8000 | open-notebook backend |
| gitingest | âœ… Available | â€” | Plugin installed |
| notebooklm-skill | âš ï¸ Auth needed | â€” | Cáº§n Google login 1 láº§n |
| firecrawl | â“ Check key | â€” | FIRECRAWL_API_KEY required |
| open-notebooklm | â“ Not checked | â€” | Fireworks API key required |
| notebooklm-mcp-cli | â“ Not tested | â€” | Python env required |

---

## ðŸ”— Quick Commands

```bash
# Check open-notebook health
curl http://localhost:5055/health

# open-notebook UI
# â†’ http://localhost:8502

# gitingest a repo
python ecosystem/plugins/gitingest/src/gitingest/main.py --url "GITHUB_URL" --output /tmp/digest.txt

# notebooklm-skill (tá»« ecosystem/plugins/notebooklm-skill)
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..." --notebook-url "..."
```

---

*Nova | Hot Cache v4.0 | 2026-03-21 | CEO Standing Order: ACTIVE*

