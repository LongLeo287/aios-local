import os

ROOT = os.environ.get("AOS_ROOT", ".")
TARGETS = ["system", "tools", "brain", "ecosystem", "launcher", "storage"]

def clean(fp):
    try:
        with open(fp, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return

    changed = False
    new_lines = []

    for line in lines:
            changed = True
        else:
            new_lines.append(line)

    if changed:
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("Cleaned:", fp)
        except Exception as e:
            print("Failed to save:", fp, e)

for d in TARGETS:
    walk = os.path.join(ROOT, d)
    if not os.path.exists(walk): continue
    for r, d_names, f_names in os.walk(walk):
        if any(skip in r for skip in ["QUARANTINE", ".git", "node_modules", ".venv", "site-packages", "__pycache__", os.path.join("knowledge", "repos")]):
            continue
        for f in f_names:
            if f.endswith(".py"):
                clean(os.path.join(r, f))

