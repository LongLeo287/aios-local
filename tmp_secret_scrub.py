import os, re

EXTS = (".py", ".ps1", ".md", ".json", ".yaml", ".txt", ".csv", ".bat", ".env.example", ".env.master.example")

patterns = {
    r"(?i)d:(/|\\\\|\\)project(/|\\\\|\\)ai os": "<AI_OS_ROOT>",
    r"(?i)d:(/|\\\\|\\)ai os corp(/|\\\\|\\)ai os remote": "<AI_OS_REMOTE_ROOT>",
    r"(?i)d:(/|\\\\|\\)ai os corp(/|\\\\|\\)ai os": "<AI_OS_ROOT>",
    r"(?i)c:(/|\\\\|\\)users(/|\\\\|\\)vua2hand": "<USER_PROFILE>",
    r"sk-[a-zA-Z0-9_-]{20,40}": "[REDACTED_API_KEY]",
    r"(?i)password\s*[:=]\s*['\"][^'\"]+['\"]": "PASSWORD='[REDACTED_PASSWORD]'",
    r"(?i)api[-_]?key\s*[:=]\s*['\"][^'\"]+['\"]": "API_KEY='[REDACTED_API_KEY]'",
    r"(?i)secret[-_]?key\s*[:=]\s*['\"][^'\"]+['\"]": "SECRET_KEY='[REDACTED_SECRET]'",
    r"[0-9]{8,11}:[a-zA-Z0-9_-]{35,}": "[REDACTED_TELEGRAM_TOKEN]",
    r"AIzaSy[0-9A-Za-z\-_]{33}": "[REDACTED_GEMINI_KEY]"
}

def scrub_dir(d):
    for root, dirs, files in os.walk(d):
        if ".git" in root or "node_modules" in root: continue
        for f in files:
            if not any(f.endswith(e) for e in EXTS): continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception:
                continue
                
            orig = content
            for p, rep in patterns.items():
                content = re.sub(p, rep, content)
            
            if content != orig:
                try:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"Sanitized: {path}")
                except Exception:
                    pass

for d in ["system", "brain", "ecosystem", "storage", "launcher", "scripts", "."]:
    if os.path.exists(d) and os.path.isdir(d):
        scrub_dir(d)
        
print("Universal Deep Scrub Complete.")
