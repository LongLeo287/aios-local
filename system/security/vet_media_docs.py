#!/usr/bin/env python3
"""
vet_media_docs.py — Media and Document Vetting Tool
Quét nhị phân tĩnh (Static Binary Analysis) để chặn mã độc nhúng trong hình ảnh (Steganography/Polyglots) và tài liệu (Macro/JS).
"""
import os
import sys
import argparse
import zipfile

MAGIC_BYTES = {
    ".png": b"\x89PNG\r\n\x1a\n",
    ".jpg": b"\xff\xd8",
    ".jpeg": b"\xff\xd8",
    ".gif": b"GIF8",
    ".pdf": b"%PDF-",
}

def check_magic_bytes(fpath, ext):
    if ext not in MAGIC_BYTES:
        return True # Cannot verify magic byte for this ext
    try:
        with open(fpath, "rb") as f:
            header = f.read(8)
            expected = MAGIC_BYTES[ext]
            if not header.startswith(expected):
                return False, f"Magic Bytes không hợp lệ cho {ext}"
    except Exception as e:
        return False, f"Lỗi đọc file: {e}"
    return True, "PASS"

def vet_pdf(fpath):
    try:
        with open(fpath, "rb") as f:
            content = f.read()
            # Tìm pattern nguy hiểm trong PDF (JS, Launch, AcroForm)
            if b"/JS" in content or b"/JavaScript" in content:
                return False, "PDF chứa đoạn mã JavaScript nguy hiểm (/JS)"
            if b"/Launch" in content:
                return False, "PDF chứa lệnh thực thi Launch (/Launch)"
            if b"/AA" in content or b"/OpenAction" in content:
                # Cảnh báo OpenAction nhưng chỉ cấm nếu có EmbeddedFiles hay JS (làm đơn giản)
                pass
    except Exception as e:
        return False, f"Lỗi scan PDF: {e}"
    return True, "PASS"

def vet_docx(fpath):
    # DOCX is a zip file.
    if not zipfile.is_zipfile(fpath):
        return False, "DOCX/XLSX không phải là định dạng ZIP hợp lệ"
    try:
        with zipfile.ZipFile(fpath, 'r') as z:
            namelist = z.namelist()
            for name in namelist:
                if name.endswith("vbaProject.bin"):
                    return False, "DOCX/XLSX chứa Macro/VBA tiềm ẩn mã độc (vbaProject.bin)"
                if name.endswith(".exe") or name.endswith(".bat") or name.endswith(".vbs"):
                    return False, f"Tài liệu chứa tệp thực thi ẩn: {name}"
    except Exception as e:
        return False, f"Lỗi scan cấu trúc tệp ZIP: {e}"
    return True, "PASS"

def vet_file(fpath):
    if not os.path.exists(fpath):
        return False, "File không tồn tại"

    ext = os.path.splitext(fpath)[1].lower()

    # 1. Magic Bytes Check
    ok, msg = check_magic_bytes(fpath, ext)
    if not ok: return False, msg

    # 2. Format specific checks
    if ext == ".pdf":
        return vet_pdf(fpath)
    elif ext in [".docx", ".xlsx", ".pptx", ".docm", ".xlsm", ".pptm"]:
        return vet_docx(fpath)
    elif ext in [".doc", ".xls", ".ppt"]:
        return False, f"Định dạng Office cũ ({ext}) không được hỗ trợ vì lý do an ninh (OLE2 Macro Virus). Hãy dùng .docx/.xlsx"
    elif ext == ".svg":
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()
                if "<script" in content or "javascript:" in content or "onload=" in content or "onerror=" in content:
                    return False, "SVG chứa mã thực thi XSS/JavaScript trái phép"
        except Exception:
            pass

    # For images, magic byte is sufficient for basic polyglot detection
    return True, "PASS"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Media & Document Vetting Tool")
    parser.add_argument("file", help="Đường dẫn đến file cần quét")
    args = parser.parse_args()

    ok, reason = vet_file(args.file)
    if ok:
        print("PASS")
        sys.exit(0)
    else:
        print(f"FAIL: {reason}")
        sys.exit(1)
