#!/usr/bin/env python3
"""
aios_code_polisher.py â€” Global Codebase Sanitizer & Formatter
Purpose: Scans the entire AI OS directory to fix corrupted encodings,
inject missing English docstrings, standardize whitespace, and catch syntax bugs.
"""

import os
import sys
import ast

ROOT_DIR = os.environ.get("AOS_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
TARGET_DIRS = ["system", "tools", "brain", "ecosystem", "launcher", "storage"]

def fix_encoding(filepath):
    """Detect non-UTF8 and convert to UTF8 to fix corrupted characters."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
            return 0  # already good
    except UnicodeDecodeError:
        pass

    # Try reading as CP1252 (common cause of Windows Vietnamese mojibake)
    try:
        with open(filepath, 'r', encoding='cp1252') as f:
            content = f.read()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    except Exception as e:
        print(f"  [!] Failed to fix encoding for {filepath}: {e}")
        return 0

def format_clean_code(content):
    """Basic cleanliness: strip trailing whitespace, normalize line endings."""
    lines = content.splitlines()
    cleaned = [line.rstrip() for line in lines]
    return '\n'.join(cleaned) + '\n'

def inject_english_docstrings(filepath):
    """Parse AST to find missing docstrings and inject default English ones."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip():
        return 0

    try:
        tree = ast.parse(content)
    except Exception as e:
        print(f"  [!] Syntax/Logic Error in {filepath}: {e}")
        return -1

    lines = content.splitlines()
    injected = 0
    modifications = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                # Node lacks docstring
                if not node.body: continue
                # Skip single-line functions to prevent unexpected indents above the signature
                if node.body[0].lineno == node.lineno:
                    continue
                insert_line = node.body[0].lineno - 1
                indent = " " * node.body[0].col_offset
                doc_str = f'{indent}"""TODO: Add description for {node.name}"""\n'
                modifications.append((insert_line, doc_str))
                injected += 1

    if modifications:
        # Sort reverse to insert from bottom up without messing up line numbers
        modifications.sort(key=lambda x: x[0], reverse=True)
        for lineno, doc in modifications:
            lines.insert(lineno, doc)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')

    return injected

def run_polisher():
    print(f"Starting Global Codebase Polish for {ROOT_DIR}...")
    encodings_fixed = 0
    docstrings_added = 0
    syntax_errors = 0
    files_cleaned = 0

    for d in TARGET_DIRS:
        walk_dir = os.path.join(ROOT_DIR, d)
        if not os.path.exists(walk_dir): continue

        for root, dirs, files in os.walk(walk_dir):
            norm_root = root.replace('\\', '/')
            if any(skip in norm_root for skip in ["QUARANTINE", ".git", "node_modules", ".venv", "site-packages", "__pycache__", "knowledge/repos"]):
                continue

            for file in files:
                filepath = os.path.join(root, file)

                # 1. Encoding check (All text-like files)
                if file.endswith(('.py', '.md', '.ps1', '.json', '.yaml', '.txt')):
                    if fix_encoding(filepath):
                        encodings_fixed += 1
                        print(f"  [+] Fixed encoding: {filepath}")

                # 2. Python specific logic
                if file.endswith('.py'):
                    # Clean trailing whitespace
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        cleaned = format_clean_code(content)
                        if cleaned != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(cleaned)
                            files_cleaned += 1

                        # Inject docstrings
                        added = inject_english_docstrings(filepath)
                        if added > 0:
                            docstrings_added += added
                            print(f"  [+] Added {added} docstrings to {filepath}")
                        elif added < 0:
                            syntax_errors += 1
                    except Exception as e:
                        pass # Ignore unresolved binary/read issues

    print("\n--- Polish Summary ---")
    print(f"Encodings Repaired: {encodings_fixed}")
    print(f"Missing English Docstrings Injected: {docstrings_added}")
    print(f"Files Whitespace Cleaned: {files_cleaned}")
    print(f"Syntax/Logic Blockers Found: {syntax_errors}")

if __name__ == "__main__":
    run_polisher()

