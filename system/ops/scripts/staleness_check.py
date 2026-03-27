#!/usr/bin/env python3
"""
staleness_check.py — Hệ thống theo dõi độ tươi dữ liệu dựa trên Hash/ETag
Trả về UNCHANGED nếu dữ liệu chưa có update mới, trả về CHANGED nếu đã update hoặc chưa từng nạp.
"""
import os
import sys
import json
import argparse
import requests
import hashlib
from pathlib import Path

_AOS_ROOT = os.getenv("AOS_ROOT") or str(Path(__file__).resolve().parents[3])
REGISTRY_FILE = Path(_AOS_ROOT) / "brain" / "knowledge" / "hash_registry.json"

def load_registry():
    if REGISTRY_FILE.exists():
        try: return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except: return {}
    return {}

def save_registry(data):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def check_url_staleness(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        etag = response.headers.get("ETag")
        last_mod = response.headers.get("Last-Modified")

        current_hash = None
        if etag: current_hash = etag
        elif last_mod: current_hash = last_mod
        else:
            if int(response.headers.get("Content-Length", 1000000)) < 5000000:
                resp_get = requests.get(url, timeout=10)
                current_hash = hashlib.md5(resp_get.content).hexdigest()
            else:
                return "CHANGED"

        registry = load_registry()
        if url in registry and registry[url] == current_hash:
            return "UNCHANGED"

        registry[url] = current_hash
        save_registry(registry)
        return "CHANGED"
    except Exception as e:
        return "CHANGED"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Staleness Checker")
    parser.add_argument("url", help="URL cần kiểm tra độ tươi")
    args = parser.parse_args()

    status = check_url_staleness(args.url)
    print(status)
    if status == "UNCHANGED":
        sys.exit(0)
    else:
        sys.exit(1)
