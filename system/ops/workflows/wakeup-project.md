# Department: operations
---
description: Láº¥y brain data tá»« .ai-memory/ trong project ra restore vÃ o session má»›i
---

# Wakeup dá»± Ã¡n

Khi user cÃ³ lá»‡nh rÃµ rÃ ng: "Wakeup dá»± Ã¡n [tÃªn dá»± Ã¡n]" (lá»‡nh gá»i Ä‘á»™c láº­p chá»‰ dÃ nh cho dá»± Ã¡n, lÆ°u Ã½ ráº±ng pháº§n lá»›n thá»i gian há»‡ thá»‘ng sáº½ tá»± Wakeup khi khá»Ÿi Ä‘á»™ng báº±ng `pre-session`):

1. XÃ¡c nháº­n: "TÃ´i sáº½ restore brain data tá»« .ai-memory\ trong project. XÃ¡c nháº­n chÆ°a?"

1. XÃ¡c nháº­n: "TÃ´i sáº½ restore brain data tá»« .ai-memory\ trong project [TÃªn]. XÃ¡c nháº­n chÆ°a?"

2. Náº¿u user khÃ´ng cung cáº¥p Ä‘Æ°á»ng dáº«n dá»± Ã¡n cá»¥ thá»ƒ, hÃ£y TÃŒM Láº I tÃªn dá»± Ã¡n trong CÃ‚U Lá»†NH CHAT cá»§a user (vÃ­ dá»¥ "Wakeup dá»± Ã¡n Tiem_Nuoc_Nho_v5") Ä‘á»ƒ tá»± suy luáº­n vÃ  ná»‘i vÃ o `$ProjectsRoot`.

// turbo
3. Cháº¡y script:
```powershell
& "<AI_OS_ROOT>\scripts\wakeup.ps1" -ProjectPath "ÄÆ¯á»œNG_DáºªN_Tá»šI_TÃŠN_Dá»°_ÃN_TRONG_CÃ‚U_CHAT"
```

Script sáº½:
- Äá»c `.ai-memory\` tá»« bÃªn trong project
- Restore brain sessions vá» `~\.gemini\antigravity\brain\`
- Restore knowledge items
- Auto-seed session hiá»‡n táº¡i vá»›i key artifacts (task.md, walkthrough...)
- Há»i user náº¿u khÃ´ng tá»± detect Ä‘Æ°á»£c session ID

4. ThÃ´ng bÃ¡o: "âœ… ÄÃ£ restore xong â€” tiáº¿p tá»¥c lÃ m viá»‡c bÃ¬nh thÆ°á»ng!"

