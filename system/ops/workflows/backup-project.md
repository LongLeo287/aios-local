# Department: operations
---
description: LÆ°u chat history vÃ  brain data VÃ€O trong folder dá»± Ã¡n Ä‘á»ƒ chuyá»ƒn mÃ¡y
---

# Backup dá»± Ã¡n nÃ y

Khi user cÃ³ lá»‡nh rÃµ rÃ ng: "Backup dá»± Ã¡n [tÃªn dá»± Ã¡n]" (chá»‰ dÃ¹ng riÃªng cho dá»± Ã¡n, khÃ´ng dÃ¹ng cho há»‡ thá»‘ng AI OS):

1. XÃ¡c Ä‘á»‹nh project path: 
   - Æ¯u tiÃªn 1 Láº¤Y TÃŠN Dá»° ÃN Tá»ª CÃ‚U Lá»†NH CHAT cá»§a user (Vd: "Backup dá»± Ã¡n Tiem_Nuoc_Nho_v5") vÃ  ná»‘i vÃ o `$ProjectsRoot`.
   - Æ¯u tiÃªn 2: XÃ¡c Ä‘á»‹nh tá»« workspace Ä‘ang má»Ÿ.

// turbo
2. Cháº¡y script:
```powershell
& "<AI_OS_ROOT>\scripts\backup.ps1" -ProjectPath "ÄÆ¯á»œNG_DáºªN_Tá»šI_TÃŠN_Dá»°_ÃN_TRONG_CÃ‚U_CHAT"
```

Script sáº½ táº¡o folder `.ai-memory\` bÃªn trong project, chá»©a:
- `brain\` â€” toÃ n bá»™ chat session artifacts (task.md, walkthrough, plans...)
- `knowledge\` â€” knowledge items
- `memory_config.json` â€” metadata

3. ThÃ´ng bÃ¡o: "ÄÃ£ lÆ°u brain data vÃ o [project]\.ai-memory\"

**Äá»ƒ chuyá»ƒn mÃ¡y:** chá»‰ cáº§n copy toÃ n bá»™ project folder sang lÃ  xong â€” khÃ´ng cáº§n lÃ m gÃ¬ thÃªm.

