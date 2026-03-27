# Department: operations
---
description: Plugin Integration Process â€” AI OS Corp (Quy trÃ¬nh tÃ­ch há»£p Plugin)
---

# Plugin Integration Workflow
# Version: 1.0 | 2026-03-23 | Owner: Antigravity (Dept 4 â€” Registry)

Quy trÃ¬nh báº¯t buá»™c khi tÃ­ch há»£p báº¥t ká»³ repo/plugin/tool má»›i vÃ o AI OS Corp.
Trigger: `aos integrate <plugin_id>` hoáº·c khi CEO request.

> âš ï¸ **PRE-GATE:** Workflow nÃ y chá»‰ cháº¡y SAU KHI `ops/workflows/repo-evaluation.md` cho phÃ¡n quyáº¿t **APPROVE**.
> Náº¿u chÆ°a cháº¡y repo-evaluation â†’ STOP, quay láº¡i bÆ°á»›c Ä‘Ã¡nh giÃ¡ trÆ°á»›c.


---

## PHASE 0 â€” Catalog & Conflict Check

### 0.1 â€” ÄÃ¡nh dáº¥u repo trong plugin-catalog.md

Má»Ÿ `plugins/plugin-catalog.md` vÃ  cáº­p nháº­t tráº¡ng thÃ¡i:

| KÃ½ hiá»‡u | Ã nghÄ©a |
|---------|---------|
| `ðŸ‘ï¸` | ÄÃ£ Ä‘á»c/kháº£o sÃ¡t README |
| `ðŸ”–` | Giá»¯ láº¡i, cÃ³ thá»ƒ dÃ¹ng sau |
| `âœ…` | Äang sá»­ dá»¥ng (theo dÃµi version) |
| `âš¡` | Äang trong quÃ¡ trÃ¬nh tÃ­ch há»£p |
| `âŒ` | Loáº¡i bá» (trÃ¹ng chá»©c nÄƒng / khÃ´ng phÃ¹ há»£p) |

**Rule:** Má»i repo trong `plugins/` pháº£i cÃ³ tráº¡ng thÃ¡i trong catalog trÆ°á»›c khi Ä‘á»c code.

### 0.2 â€” Conflict check

Kiá»ƒm tra chá»©c nÄƒng má»›i cÃ³ trÃ¹ng vá»›i plugin hiá»‡n cÃ³ khÃ´ng:

```
1. Liá»‡t kÃª chá»©c nÄƒng chÃ­nh cá»§a plugin má»›i
2. So sÃ¡nh vá»›i plugins/registry.json (status: active)
3. So sÃ¡nh vá»›i blackboard.json infrastructure section
4. Náº¿u trÃ¹ng: Ä‘Ã¡nh giÃ¡ "bá»• sung" hay "thay tháº¿"
   - Bá»• sung â†’ OK, ghi rÃµ use case phÃ¢n biá»‡t
   - Thay tháº¿ â†’ pháº£i deprecate plugin cÅ© trÆ°á»›c
```

### 0.3 â€” Update catalog: âš¡ (in progress)

---

## PHASE 1 â€” Security Scan (RULE-PROCESS-01 Báº¯t buá»™c)

**Owner: Dept 10 â€” Security/GRC (Strix)**

```bash
# Cháº¡y nemoclaw-strix-scan trÃªn repo
# See: ops/workflows/nemoclaw-strix-scan.md
```

Minimum check:
- [ ] License compatible (MIT/Apache/BSD preferred; AGPL flag for CEO review)
- [ ] No hardcoded credentials, API keys
- [ ] No cryptominer, obfuscated code
- [ ] Source repo is public/verified
- [ ] `pip show <package>` hoáº·c `npm info <package>` â€” verify publisher

Káº¿t quáº£: **CLEAR** hoáº·c **FLAG** (CEO quyáº¿t Ä‘á»‹nh náº¿u FLAG)

---

## PHASE 2 â€” Táº¡o Plugin Structure (PLUGIN_SPEC.md)

```
plugins/<plugin_id>/
â”œâ”€â”€ manifest.json     [REQUIRED]
â”œâ”€â”€ PLUGIN.md         [REQUIRED] â€” hÆ°á»›ng dáº«n cho agents
â”œâ”€â”€ README.md         [REQUIRED] â€” tá»•ng quan
â”œâ”€â”€ <adapter>.py      [náº¿u cáº§n wrapper]
â””â”€â”€ tests/            [REQUIRED]
    â””â”€â”€ test_<id>.py  â€” smoke tests
```

### manifest.json checklist
- [ ] `id`, `name`, `version`, `type`, `status` Ä‘iá»n Ä‘áº§y Ä‘á»§
- [ ] `agent_hooks` khai bÃ¡o Ä‘Ãºng hooks dÃ¹ng
- [ ] `auto_load: false` (máº·c Ä‘á»‹nh â€” khÃ´ng tá»± load khi boot)
- [ ] `can_crash_os: false` â€” báº¯t buá»™c
- [ ] `conflict_check` section: ghi káº¿t quáº£ phase 0
- [ ] `upstream_check`: táº§n suáº¥t check version má»›i

---

## PHASE 3 â€” Version Tracking Setup

ThÃªm vÃ o **Version Tracking table** trong `plugin-catalog.md`:

```markdown
| <plugin_id> | <current_version> | <frequency> | <update_command> |
```

**Táº§n suáº¥t theo má»©c Ä‘á»™ quan trá»ng:**
- Core agent tools â†’ Weekly
- Data/bridge tools â†’ Monthly
- Security tools â†’ Weekly
- Reference/UI â†’ Quarterly

---

## PHASE 4 â€” ÄÄƒng kÃ½ Registry

Cáº­p nháº­t `plugins/registry.json`:

```json
{
  "id": "<plugin_id>",
  "type": "<cognitive|data|bridge|ui>",
  "status": "active",
  "auto_load": false,
  "path": "plugins/<plugin_id>/",
  "manifest": "plugins/<plugin_id>/manifest.json",
  "notes": "<mÃ´ táº£ ngáº¯n, ngÃ y tÃ­ch há»£p>",
  "registered_at": "YYYY-MM-DD",
  "upstream_check": "<frequency> â€” <command>"
}
```

Cáº­p nháº­t `total_registered` vÃ  `active_count`.

---

## PHASE 5 â€” Activation Commands (RULE-ACTIVATION-01)

**Náº¿u plugin cáº§n cmd/powershell Ä‘á»ƒ kÃ­ch hoáº¡t:**

### 5a â€” ThÃªm vÃ o Dashboard (dashboard.ps1)

Má»Ÿ `<AI_OS_ROOT>\launcher\dashboard.ps1` vÃ  thÃªm vÃ o section **PLUGIN MANAGER**:

```powershell
# Trong menu [P] Plugin Manager â†’ sub-menu
"<plugin_id>" = @{
    Name = "<Display Name>"
    Check = { <check if installed/running> }
    Install = "<install command>"
    Start = "<start command, náº¿u cÃ³>"
    Port = <port náº¿u cÃ³ service, $null náº¿u khÃ´ng>
}
```

### 5b â€” ThÃªm vÃ o ClawTask (Port 7474)

Náº¿u plugin lÃ  má»™t **service cÃ³ port** â†’ thÃªm vÃ o `$SERVICES` trong `dashboard.ps1`.

Náº¿u plugin lÃ  **library/tool** (khÃ´ng cÃ³ port) â†’ chá»‰ thÃªm vÃ o Plugin Manager section.

### 5c â€” Update MASTER.env (náº¿u cáº§n API key)

```
<AI_OS_ROOT>\ops\secrets\MASTER.env
```

---

## PHASE 6 â€” Test & Verify

```bash
# 1. Cháº¡y smoke tests
python plugins/<plugin_id>/tests/test_<id>.py

# 2. Verify registry
python -c "import json; r=json.load(open('plugins/registry.json')); print([p for p in r['plugins'] if p['id']=='<id>'])"

# 3. Test activation tá»« dashboard (náº¿u cÃ³)
# Má»Ÿ AI OS CORP.cmd â†’ [P] Plugin Manager â†’ chá»n plugin
```

---

## PHASE 7 â€” Update Blackboard & Catalog

```
1. blackboard.json: cáº­p nháº­t open_items náº¿u Ä‘Ã¢y lÃ  OPEN task
2. plugin-catalog.md: status âš¡ â†’ âœ…, thÃªm version tracking
3. telemetry/receipts/<plugin_id>/: log activation Ä‘áº§u tiÃªn
```

---

## PHASE 7b â€” Register Rules, Skills & Workflow Hooks (Báº®T BUá»˜C)

> ÄÃ¢y lÃ  bÆ°á»›c thÆ°á»ng bá»‹ bá» qua. Pháº£i lÃ m NGAY SAU Phase 7.

### 7b.1 â€” ThÃªm RULE vÃ o GEMINI.md

Náº¿u plugin thay Ä‘á»•i cÃ¡ch agent lÃ m viá»‡c, PHáº¢I thÃªm rule rÃµ rÃ ng:

```
Má»Ÿ: <AI_OS_ROOT>\GEMINI.md
ThÃªm vÃ o SECTION 3 â€” ANTIGRAVITY SPECIFIC RULES:

**[RULE-<XYZ>-01]** <TÃªn rule>:
  1. Khi nÃ o dÃ¹ng plugin nÃ y
  2. CÃ¡ch gá»i (import, function)
  3. Scope: phÃ²ng ban nÃ o / agent nÃ o
  
Full docs: plugins/<plugin_id>/PLUGIN.md
```

### 7b.2 â€” ÄÄƒng kÃ½ SKILL_REGISTRY.json

```
Má»Ÿ: brain/shared-context/SKILL_REGISTRY.json
ThÃªm entry vÃ o "entries" array:
{
  "id": "<plugin_id>",
  "name": "<Display Name>",
  "tier": 2,
  "status": "active",
  "source": "plugin",
  "path": "plugins/<plugin_id>/SKILL.md",
  "adapter": "plugins/<plugin_id>/<adapter>.py",
  "description": "<MÃ´ táº£ ngáº¯n khi nÃ o dÃ¹ng>",
  "domain": "<data|core|bridge|ui>",
  "accessible_by": ["<agent_ids>"],
  "exposed_functions": ["<function_names>"],
  "listens_to": { "<hook>": "<function_call>" },
  "rule": "<RULE-ID>",
  "noop_safe": true
}
TÄƒng "count" lÃªn.
Validate: python -c "import json; json.load(open('brain/shared-context/SKILL_REGISTRY.json'))"
```

### 7b.3 â€” Hook vÃ o Workflows liÃªn quan

Kiá»ƒm tra vÃ  cáº­p nháº­t cÃ¡c workflow sá»­ dá»¥ng plugin nÃ y:

```
- ops/workflows/knowledge-ingest.md  â†’ step "fetch URL/search"
- ops/workflows/corp-daily-cycle.md  â†’ náº¿u plugin cháº¡y daily
- ops/workflows/agent-workflow.md    â†’ náº¿u agent cáº§n dÃ¹ng plugin
```

Cá»¥ thá»ƒ: tÃ¬m cÃ¡c bÆ°á»›c hiá»‡n dÃ¹ng fallback thá»§ cÃ´ng â†’ thay báº±ng adapter call.

---

## VERSION TRACKING â€” Weekly/Monthly Checks

```powershell
# Cháº¡y tá»« dashboard: [V] Version Check (má»›i thÃªm)
# Hoáº·c cháº¡y thá»§ cÃ´ng:
pip show mem0ai
pip show firecrawl-py
pip show crewai
# â†’ So sÃ¡nh vá»›i version trong plugin-catalog.md
# â†’ Náº¿u cÃ³ version má»›i: pip install --upgrade <package>
```

---

*Workflow Owner: Antigravity | Dept 4 Registry | Last updated: 2026-03-23*
*"Catalog first. Security second. Register third. Never skip."*

