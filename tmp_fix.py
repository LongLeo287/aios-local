import os, re

TARGET_DIRS = ["system", "brain", "ecosystem", "storage", "launcher", "scripts"]
EXTS = (".py", ".ps1", ".md", ".json", ".yaml", ".txt", ".csv", ".bat")

patterns = {
    r"(?i)d:(/|\\\\|\\)project(/|\\\\|\\)ai os": "<AI_OS_ROOT>",
    r"(?i)d:(/|\\\\|\\)ai os corp(/|\\\\|\\)ai os remote": "<AI_OS_REMOTE_ROOT>",
    r"(?i)d:(/|\\\\|\\)ai os corp(/|\\\\|\\)ai os": "<AI_OS_ROOT>",
    r"(?i)c:(/|\\\\|\\)users(/|\\\\|\\)vua2hand": "<USER_PROFILE>"
}

code_patterns_py = {
    r'(?i)r?["\']D:(/|\\\\|\\)Project(/|\\\\|\\)AI OS[/\\]?["\']': 'os.environ.get("AOS_ROOT", ".")',
    r'(?i)r?["\']D:(/|\\\\|\\)AI OS CORP(/|\\\\|\\)AI OS REMOTE[/\\]?["\']': 'os.environ.get("AOS_REMOTE_ROOT", "..")',
    r'(?i)r?["\']D:(/|\\\\|\\)AI OS CORP(/|\\\\|\\)AI OS[/\\]?["\']': 'os.environ.get("AOS_ROOT", ".")',
}

code_patterns_ps1 = {
    r'(?i)["\']D:(/|\\\\|\\)Project(/|\\\\|\\)AI OS[/\\]?["\']': '$env:AOS_ROOT',
    r'(?i)["\']D:(/|\\\\|\\)AI OS CORP(/|\\\\|\\)AI OS REMOTE[/\\]?["\']': '$env:AOS_REMOTE_ROOT',
    r'(?i)["\']D:(/|\\\\|\\)AI OS CORP(/|\\\\|\\)AI OS[/\\]?["\']': '$env:AOS_ROOT',
}

for d in TARGET_DIRS:
    if not os.path.exists(d): continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if not f.endswith(EXTS): continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception:
                continue
                
            orig = content
            
            if f.endswith((".md", ".json", ".yaml", ".txt", ".csv")):
                for p, rep in patterns.items():
                    content = re.sub(p, rep, content)
            
            elif f.endswith(".py"):
                for p, rep in code_patterns_py.items():
                    content = re.sub(p, rep, content)
                for p, rep in patterns.items():
                    content = re.sub(p, rep, content)

            elif f.endswith((".ps1", ".bat")):
                for p, rep in code_patterns_ps1.items():
                    content = re.sub(p, rep, content)
                for p, rep in patterns.items():
                    content = re.sub(p, rep, content)

            if content != orig:
                if f.endswith(".py") and "os.environ" in content and "import os" not in content:
                    content = "import os\n" + content
                try:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                except Exception:
                    pass

# Also do a blanket check on root directory files
for f in os.listdir("."):
    if os.path.isfile(f) and f.endswith(EXTS):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            orig = content
            for p, rep in patterns.items():
                content = re.sub(p, rep, content)
            if content != orig:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(content)
        except:
            pass

print("Sanitization completed via Python.")
