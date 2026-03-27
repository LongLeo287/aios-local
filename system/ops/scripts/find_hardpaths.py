import os

def scan_files():
    root_dir = os.environ.get("AOS_ROOT", ".")
    ignore_dirs = {"node_modules", ".git", ".venv", "storage", "brain", "QUARANTINE", "__pycache__"}
    extensions = {".py", ".ps1", ".cmd", ".bat", ".yaml", ".json"}

    found = []

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            if "d:\\AI OS CORP" in line or "d:/AI OS CORP" in line or "D:\\AI OS CORP" in line:
                                found.append(f"{path}:{i} -> {line.strip()[:100]}")
                except Exception:
                    pass

    for f in found:
        print(f)

if __name__ == "__main__":
    scan_files()

