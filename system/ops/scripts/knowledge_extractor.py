#!/usr/bin/env python3
"""
knowledge_extractor.py — AI OS Knowledge Extraction Module
Nén một repository (RAW CLONE) thành 1 file Markdown duy nhất để tối ưu:
- RAG / LLM context loading
- Ổ cứng (bỏ qua .git, ảnh, node_modules)
- Lỗi MAX_PATH trên Windows

Sử dụng:
python system/ops/scripts/knowledge_extractor.py --dir QUARANTINE/incoming/repos/my_repo [--cleanup]
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Prevent UnicodeEncodeError when piping stdout on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# ================= Configuration =================
MAX_FILE_SIZE_MB = 10
MAX_DEPTH = 10
_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])

PROCESSED_DIR = Path(_AOS_ROOT) / "brain" / "knowledge" / "processed_repos"

IGNORE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "vendor", "venv", ".venv",
    "env", ".env", "__pycache__", "dist", "build", "out", "target",
    "bin", "obj", ".idea", ".vscode", "coverage", ".next", ".nuxt"
}

IGNORE_EXTS = {
    # Images/Media
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".mp4", ".webm", ".mov", ".mp3", ".wav",
    # Binaries/Compiled
    ".exe", ".dll", ".so", ".dylib", ".class", ".jar", ".pyc", ".pyo", ".pyd", ".whl",
    # Documents/Other
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".tar", ".gz", ".rar", ".7z",
    # Lock files
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock", "Cargo.lock"
}
# Also ignore strictly named lock files
IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock", "Cargo.lock"
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def is_text_file(filepath: Path) -> bool:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False

def get_language(ext: str) -> str:
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "tsx", ".jsx": "jsx",
        ".html": "html", ".css": "css", ".scss": "scss", ".json": "json", ".md": "markdown",
        ".yml": "yaml", ".yaml": "yaml", ".sh": "bash", ".bash": "bash", ".ps1": "powershell",
        ".go": "go", ".rs": "rust", ".java": "java", ".c": "c", ".cpp": "cpp", ".h": "c",
        ".cs": "csharp", ".php": "php", ".rb": "ruby", ".sql": "sql", ".xml": "xml"
    }
    return ext_map.get(ext.lower(), "")

def extract_knowledge(repo_path: Path, cleanup: bool = False) -> bool:
    if not repo_path.exists() or not repo_path.is_dir():
        log(f"[ERROR] Thư mục không tồn tại: {repo_path}")
        return False

    repo_name = repo_path.name
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROCESSED_DIR / f"{repo_name}_knowledge.md"

    log(f"[EXTRACTING] {repo_name} -> {out_file.name}")

    total_files = 0
    total_lines = 0

    with open(out_file, "w", encoding="utf-8") as out:
        out.write(f"# KNOWLEDGE EXTRACT: {repo_name}\n")
        out.write(f"> **Extracted on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"> **Source:** {repo_path.name}\n\n")
        out.write("---\n\n")

        for root_dir, dirs, files in os.walk(repo_path):
            current_depth = len(Path(root_dir).relative_to(repo_path).parts)
            if current_depth > MAX_DEPTH:
                dirs.clear() # Anti-Symlink/Deep Loop: Prune search tree here
                continue

            # Filter directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]

            for file in files:
                if file in IGNORE_FILES: continue

                fpath = Path(root_dir) / file
                if fpath.is_symlink(): continue # Prevent symlink bypass
                if fpath.suffix.lower() in IGNORE_EXTS: continue

                # File size limits (Anti-Zip Bomb)
                try:
                    if fpath.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                        log(f"  [SKIP] {file} vượt giới hạn {MAX_FILE_SIZE_MB}MB")
                        continue
                except Exception:
                    continue

                # Double check to prevent binary read
                if not is_text_file(fpath): continue

                rel_path = fpath.relative_to(repo_path)
                lang = get_language(fpath.suffix)

                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    lines_count = len(content.splitlines())

                    if lines_count == 0: continue # Skip empty files

                    out.write(f"## File: `{rel_path.as_posix()}`\n")
                    out.write(f"```{lang}\n")
                    out.write(content)
                    if not content.endswith('\n'):
                        out.write("\n")
                    out.write("```\n\n")

                    total_files += 1
                    total_lines += lines_count
                except Exception as e:
                    log(f"  [WARN] Không thể đọc {rel_path}: {e}")

    log(f"[DONE] Đã nén {total_files} files ({total_lines} dòng) vào {out_file.name}")

    if cleanup:
        log(f"[CLEANUP] Đang xóa thư mục thô: {repo_path}")
        try:
            shutil.rmtree(repo_path, ignore_errors=True)
            log(f"[CLEANUP] Đã xóa {repo_name}")
        except Exception as e:
            log(f"[ERROR] Không thể xóa {repo_path}: {e}")

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knowledge Extractor for AI OS")
    parser.add_argument("--dir", required=True, help="Đường dẫn đến thư mục repo clone thô")
    parser.add_argument("--cleanup", action="store_true", help="Xóa thư mục thô sau khi nén thành công")
    args = parser.parse_args()

    extract_knowledge(Path(args.dir), args.cleanup)
