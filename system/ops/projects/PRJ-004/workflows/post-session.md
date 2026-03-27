---
description: POS project session close â€” run before closing/switching workspace
---

# post-session.md â€” Tiem Nuoc Nho v5
# Managed by: <AI_OS_ROOT>\projects\PRJ-004\workflows\

## Steps

### 1. TypeScript Final Check
```powershell
cd D:\Tiem_Nuoc_Nho_v5
npx tsc --noEmit --skipLibCheck
```
Fix any errors before closing. Do NOT leave TS errors overnight.

### 2. Update Blackboard
```json
{
  "_updated": "<ISO timestamp>",
  "_active_workspace": {
    "project_id": "PRJ-004",
    "session_closed_at": "<ISO timestamp>",
    "session_summary": "<1-sentence summary>"
  }
}
```

### 3. Soul Backup (if significant work done)
```powershell
powershell -ExecutionPolicy Bypass -File "<AI_OS_ROOT>\scripts\memory\backup_soul.ps1"
Copy-Item "<AI_OS_ROOT>\scripts\memory\soul_backup.zip" `
          -Destination "D:\Tiem_Nuoc_Nho_v5\.docs\soul_backup.zip" -Force
```

### 4. Announce (Vietnamese)
```
"âœ… PhiÃªn lÃ m viá»‡c Ä‘Ã£ Ä‘Ã³ng.
- ÄÃ£ lÃ m: [list]
- CÃ²n láº¡i: [list]
- Backup: done"
```

