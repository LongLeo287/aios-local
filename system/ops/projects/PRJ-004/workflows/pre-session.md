---
description: POS project session initialization â€” run at start of every work session
---

# pre-session.md â€” Tiem Nuoc Nho v5
# Managed by: <AI_OS_ROOT>\projects\PRJ-004\workflows\

## Steps

### 1. Boot & Validate
```
1. Read <AI_OS_ROOT>\projects\PRJ-004\CLAUDE.md
2. Read <AI_OS_ROOT>\CLAUDE.md
3. Run: powershell -File "<AI_OS_ROOT>\gatekeeper.ps1" -CheckID PRJ-004
```

### 2. Dev Server Check
```powershell
$conn = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue
if ($conn.TcpTestSucceeded) { "âœ… Dev server: http://localhost:3000" }
else { "âš ï¸ Start with: cd D:\Tiem_Nuoc_Nho_v5 && npm run dev" }
```

### 3. TypeScript Health Check
```powershell
cd D:\Tiem_Nuoc_Nho_v5
npx tsc --noEmit --skipLibCheck
# Expected: no output (zero errors)
```

### 4. Blackboard Check
```
Read: <AI_OS_ROOT>\shared-context\blackboard.json
- COMPLETE â†’ review Claude Code results
- BLOCKED  â†’ investigate, report to user
- IDLE     â†’ fresh session, ready
```

### 5. Announce (Vietnamese)
```
"âœ… Dá»± Ã¡n Tiem Nuoc Nho v5 sáºµn sÃ ng.
- Dev: http://localhost:3000
- TypeScript: [0 lá»—i]
- Tráº¡ng thÃ¡i: IDLE"
```

