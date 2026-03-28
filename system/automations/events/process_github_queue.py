#!/usr/bin/env python3
"""
process_github_queue.py — AI OS Batch GitHub Intake Tool (Cập nhật RULE-CIV-02)
Đọc URL từ storage/vault/DATA/Github.txt và ĐƯA VÀO PENDING_REPOS.md.
Nghiêm cấm clone trực tiếp ở bước này để tuân thủ PENDING GATE.
Sau khi đẩy vào PENDING thành công, xóa URL khỏi Github.txt.
"""

import os
import sys
import datetime
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VAULT_FILE = os.path.join(ROOT, "storage", "vault", "DATA", "Github.txt")
PENDING_FILE = os.path.join(ROOT, "storage", "vault", "DATA", "PENDING_REPOS.md")

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def process_queue():
    if not os.path.exists(VAULT_FILE):
        print(f"File không tồn tại: {VAULT_FILE}")
        return

    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    if not urls:
        print("Không có URL nào trong Github.txt để xử lý.")
        return

    print(f"=> Tìm thấy {len(urls)} URLs cần xử lý trong Github.txt.")

    # Đọc PENDING hiện tại để tránh trùng
    existing_pending = set()
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            existing_pending = set(re.findall(r'https://github\.com/[\w\-\.]+/[\w\-\.]+', f.read()))

    added_count = 0
    with open(PENDING_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n## Batch từ Github.txt — {now()}\n\n")
        f.write("| STT | Repo | Ghi chú | Ngày thêm |\n")
        f.write("|-----|------|---------|-----------|\n")

        for i, url in enumerate(urls, 1):
            url_clean = url.rstrip('/')
            if url_clean in existing_pending:
                print(f"  [!] {url_clean} đã có trong PENDING_REPOS.md. Bỏ qua.")
                continue

            repo_name = url_clean.split("/")[-1]
            owner_repo = "/".join(url_clean.split("/")[-2:])

            f.write(f"| {i} | [{owner_repo}]({url_clean}) | Auto-queued từ Github.txt | {now()[:10]} |\n")
            print(f"  [+] Đã thêm vào PENDING: {owner_repo}")
            added_count += 1

    # Xóa trắng file Github.txt sau khi xử lý xong (nếu có URL đã đọc)
    if urls:
        with open(VAULT_FILE, 'w', encoding='utf-8') as _f:
            pass
        print(f"\n=> [RULE-CIV-02 OK] Đã chuyển {added_count} URLs mới vào PENDING_REPOS.md.")
        print("=> Github.txt đã được dọn sạch.")
    else:
        print(f"\n=> [RULE-CIV-02 OK] Không có URL mới nào được thêm.")

    print("=> Bước tiếp: Chạy system/ops/scripts/civ_classifier.py để duyệt.")

if __name__ == "__main__":
    process_queue()
