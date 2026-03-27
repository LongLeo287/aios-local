# Department: operations
---
description: Supabase connection debug â€” ClawTask API backend khÃ´ng switch sang supabase
---

# Supabase Debug Workflow

## Khi nÃ o dÃ¹ng workflow nÃ y?

ClawTask API tráº£ vá» `"backend": "json"` thay vÃ¬ `"backend": "supabase"`.

---

## Step 1: Verify .env tá»“n táº¡i vÃ  cÃ³ Ä‘Ãºng giÃ¡ trá»‹

```powershell
# Check .env trong thÆ° má»¥c clawtask
cat "<AI_OS_ROOT>\tools\clawtask\.env"
```

Pháº£i tháº¥y:
```
SUPABASE_URL=https://xxxx.supabase.co   â† khÃ´ng Ä‘Æ°á»£c rá»—ng
SUPABASE_KEY=eyJhbGci...                â† anon key tá»« Supabase dashboard
```

**Fix náº¿u trá»‘ng:** Cháº¡y lá»‡nh sau (thay YOUR_PROJECT_REF vÃ  YOUR_ANON_KEY):
```powershell
@"
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY
DATA_DIR=/app/data
TZ=Asia/Ho_Chi_Minh
"@ | Set-Content "<AI_OS_ROOT>\tools\clawtask\.env"
```

---

## Step 2: Restart Docker container Ä‘á»ƒ load .env má»›i

```powershell
# Tá»« thÆ° má»¥c clawtask
cd "<AI_OS_ROOT>\tools\clawtask"

# Docker Compose V1 (náº¿u cÃ i standalone)
docker-compose down && docker-compose up -d

# Docker Compose V2 (náº¿u cÃ i qua Docker Desktop)
docker compose down && docker compose up -d

# Hoáº·c dÃ¹ng batch file cÃ³ sáºµn
.\docker-manage.bat
```

---

## Step 3: Verify container Ä‘Ã£ load .env

```powershell
# Check env vars inside container
docker exec clawtask_api printenv | findstr SUPABASE

# Expected output:
# SUPABASE_URL=https://xxxx.supabase.co
# SUPABASE_KEY=eyJhbGci...
```

---

## Step 4: Check /api/status

```powershell
(Invoke-WebRequest -Uri "http://localhost:7474/api/status" -UseBasicParsing).Content
```

**Expected response (Supabase OK):**
```json
{
  "backend": "supabase",
  "supabase": true,
  "port": 7474
}
```

**Still showing `"backend": "json"`?** â†’ Go to Step 5.

---

## Step 5: Check Supabase project is active (not paused)

1. Má»Ÿ: https://supabase.com/dashboard/project/YOUR_PROJECT_REF
2. Check project status â€” náº¿u PAUSED, click "Resume"
3. Sau khi resume, Docker restart láº¡i (Step 2)

---

## Step 6: Verify tasks table schema

Cháº¡y trong Supabase SQL Editor:
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'tasks' AND table_schema = 'public'
ORDER BY ordinal_position;
```

Pháº£i tháº¥y: `id`, `title`, `agent_id`, `status`, `priority`, `created_at`, `blockers`, `notes`

**Thiáº¿u `agent_id`?** Cháº¡y:
```sql
ALTER TABLE public.tasks ADD COLUMN IF NOT EXISTS agent_id text;
```

---

## Step 7: Test task insertion

```powershell
$headers = @{"Content-Type"="application/json"}
$body = '{"title":"Debug test","agent_id":"antigravity","priority":"low"}'
(Invoke-WebRequest -Uri http://localhost:7474/api/tasks/add -Method POST -Body $body -Headers $headers -UseBasicParsing).Content
```

**Response náº¿u thÃ nh cÃ´ng:**
```json
{"ok": true, "task": {"id": "T...", "title": "Debug test", "agent_id": "antigravity"}}
```

---

## Known Issues Log

| Date | Issue | Fix Applied |
|------|-------|------------|
| 2026-03-20 | .env SUPABASE_URL trá»‘ng trong root .env | Táº¡o .env riÃªng trong tools/clawtask/ |
| 2026-03-20 | docker exec khÃ´ng available in PS context | Sá»­ dá»¥ng docker compose hoáº·c docker-manage.bat |

---

*Maintained by: Engineering Dept | Last updated: 2026-03-20*

