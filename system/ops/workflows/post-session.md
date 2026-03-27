# Department: operations
ï»¿# post-session.md â€” AI OS Session Close Hook
# Version: 1.0 | Updated: 2026-03-14
# Authority: Tier 2 (Operations)
# Executed by: Any agent at end of every session (before disconnect)

---

## AUTO-TRIGGER â€” Khi nÃ o cháº¡y?

Antigravity Tá»° Äá»˜NG cháº¡y post-session khi nháº­n Báº¤T Ká»² signal nÃ o:

| Signal | VÃ­ dá»¥ | Trigger |
|--------|-------|--------|
| CEO nÃ³i káº¿t thÃºc | "káº¿t thÃºc phiÃªn" / "end session" / "táº¡m biá»‡t" / "xong rá»“i" | âœ… Cháº¡y ngay |
| Task hoÃ n thÃ nh | CEO approve káº¿t quáº£ cuá»‘i, khÃ´ng há»i thÃªm | âœ… Cháº¡y ngay |
| PhiÃªn má»›i báº¯t Ä‘áº§u | "báº¯t Ä‘áº§u phiÃªn má»›i" / "khá»Ÿi Ä‘á»™ng láº¡i" | âœ… Handoff session cÅ© trÆ°á»›c |

**KHÃ”NG Ä‘á»£i CEO nÃ³i:** "handoff" / "cáº­p nháº­t blackboard" / "viáº¿t brief" / "update HUD"

---
## Purpose

Ensure continuity between sessions by saving context, archiving evidence,
and leaving clear handoff notes for the next session.

---

## Execution Steps (Run in Order)

### Step 0.5: LTM Auto-Save (Long-Term Memory â€” NEW)
```
Before closing session â€” save key context to vector memory:
  python system/ops/scripts/save_session_memory.py --from-blackboard
  OR
  python system/ops/scripts/save_session_memory.py "[tÃ³m táº¯t phiÃªn ngáº¯n gá»n]"

This ensures AI OS remembers what happened across sessions (vectorized, not just text).
Silent fail if LTM offline â€” never block session close.
```

### Step 1: Context Snapshot
```
Write to smart_memory:
  {
    "session_end": "[ISO 8601]",
    "last_task": "[task_id or description]",
    "status": "[COMPLETE | IN_PROGRESS | BLOCKED]",
    "key_decisions": ["...", "..."],
    "open_items": ["...", "..."]
  }
```

### Step 2: Blackboard Handoff Note
```
If status = IN_PROGRESS (task not fully done):
  Update blackboard.json context field:
  {
    "session_interrupted": true,
    "last_completed_step": "[step N]",
    "next_step": "[step N+1 description]",
    "notes": "[anything next session needs to know]"
  }

If status = IDLE (nothing in progress):
  Set blackboard.json: handoff_trigger = null, status = "IDLE"
```

### Step 3: Knowledge Update
```
If any new knowledge was generated this session:
  â†’ Update knowledge/knowledge_index.md with new entry
  â†’ Save relevant notes to knowledge/[topic].md

If cognitive_reflector ran this session:
  â†’ Ensure lessons are saved to cosmic_memory
```

### Step 3B: Autonomous Facility Sanitation (Dept 22)
```
Tá»° Äá»˜NG CHáº Y á»ž CUá»I PHIÃŠN LÃ€M VIá»†C.
Trigger: Gá»i ká»‹ch báº£n dá»n dáº¹p há»‡ luá»µ (aios_deep_cleaner) Ä‘á»ƒ quÃ©t toÃ n cá»¥c.

Script: python system/ops/scripts/aios_deep_cleaner.py --auto-delete --stale-days 14

Quy táº¯c dá»n dáº¹p (RULE-CLEANUP-01):
1. QuÃ©t root directory (<AI_OS_ROOT>) vÃ  Ä‘áº©y má»i file táº¡o nhÃ¡p láº¡c loÃ i (.md, .py, .txt, .log) khÃ´ng thuá»™c há»‡ thá»‘ng vÃ o `storage/vault/DATA/stray_files/` Ä‘á»ƒ khoanh vÃ¹ng rÃ¡c.
2. XÃ³a sáº¡ch cÃ¡c repo má»“ cÃ´i/rá»—ng trong `brain/knowledge/repos/*`.
3. Clear cÃ¡c report vÃ  log rÃ¡c cÅ© (>14 ngÃ y) khá»i `QUARANTINE/` vÃ  `storage/vault/DATA/`.

Silent fail náº¿u khÃ´ng cÃ³ gÃ¬ cáº§n dá»n â€” KHÃ”NG block session close.
```

### Step 4: Receipt Archive (if large)
```
Check: telemetry/receipts/ file count

If file count > 50:
  â†’ Move receipts older than 7 days to telemetry/receipts/archive/
  â†’ Log: "Archived [N] receipts"

Do NOT delete receipts â€” only archive.
```

### Step 5: Skill Registry Check
```
If any new SKILL.md was created or modified this session:
  â†’ Reminder: "Run skill_loader.ps1 to update registry"

If skills/experimental/ has files not yet reviewed:
  â†’ Reminder: "N skills in experimental/ awaiting review"
```

### Step 6: Session Close Announcement (Auto + Telegram notify)
```
Output (Vietnamese):

"ðŸ“‹ PhiÃªn lÃ m viá»‡c káº¿t thÃºc.
- ÄÃ£ lÆ°u: context + decisions vÃ o smart_memory
- Tráº¡ng thÃ¡i: [COMPLETE | IN_PROGRESS | BLOCKED]
- Ghi chÃº cho phiÃªn sau: [1-2 cÃ¢u]
- Nháº¯c nhá»Ÿ: [skill registry / experimental skills náº¿u cÃ³]"
```

```powershell
# BÃ¡o Star Office UI: phiÃªn Ä‘Ã£ Ä‘Ã³ng, chuyá»ƒn sang idle
python "d:\LongLeo\Project\AI OS\dashboard\set_state_aios.py" --state idle --detail "PhiÃªn lÃ m viá»‡c Ä‘Ã£ káº¿t thÃºc - Táº¡m biá»‡t!"
```

### Step 7: HUD Auto-Update (non-blocking)
```
Trigger: always run at session end â€” even if previous steps failed

powershell ops/scripts/update_hud.ps1 -Quiet
â†’ Port check (Ollama:11434, ClawTask:7474, LightRAG:9621)
â†’ Count open_items tá»« blackboard.json
â†’ Count pending proposals tá»« corp/proposals/
â†’ Update hud/STATUS.json (machine-readable)
â†’ Update hud/HUD.md services table (2-way write)
â†’ Create hud/snapshots/<date>_<time>.md (history)
â†’ Telegram: session summary (náº¿u cÃ³ token)

On failure: skip silently â€” log warning only, NEVER block session close
```

---


## On Failure

If any step fails:
- Log warning, continue to next step
- Critical: Step 1 (context snapshot) â€” retry once if fails
- If Step 1 still fails: write manually to blackboard.json context field

