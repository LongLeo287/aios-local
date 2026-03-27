# 🎬 Skill Tải Video cho Google Antigravity (Gemini CLI)

> Tải video từ **YouTube, Facebook, TikTok, Instagram, Twitter/X** và hàng nghìn trang web khác — chỉ cần dán link!

---

## 🚀 Cài đặt (1 lần duy nhất)

### Bước 1: Cài công cụ cần thiết

Mở **PowerShell** hoặc **Terminal**, chạy lần lượt:

```powershell
# Cài yt-dlp (công cụ tải video)
pip install yt-dlp

# Cài ffmpeg (xử lý video/audio)
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
```

### Bước 2: Copy skill vào Gemini

Copy thư mục `tai-video-skill` vào đường dẫn sau:

```
%USERPROFILE%\.gemini\antigravity\skills\tai-video\
```

> **Lưu ý:** Chỉ cần copy file `SKILL.md` vào trong thư mục `tai-video`. Tạo thư mục nếu chưa có.

Cấu trúc đúng:

```
%USERPROFILE%\.gemini\
  └── antigravity\
      └── skills\
          └── tai-video\
              └── SKILL.md     ← file này
```

---

## 💡 Cách sử dụng

Sau khi cài xong, mở Gemini CLI và **nói tự nhiên**:

| Bạn nói | Gemini sẽ làm |
|---------|---------------|
| `Tải video này: https://youtube.com/...` | Tải video chất lượng cao nhất |
| `Tải nhạc từ link này: https://...` | Trích xuất audio thành MP3 |
| `Download video Facebook: https://fb.watch/...` | Tải video Facebook |
| `Tải video TikTok: https://tiktok.com/...` | Tải video TikTok (không watermark) |

### Ví dụ thực tế

```
> Tải video này về Desktop: https://www.youtube.com/shorts/_SKLKEusM9w
```

Gemini sẽ tự động:
1. ✅ Nhận diện link → chọn công cụ phù hợp
2. ✅ Tải video chất lượng tốt nhất
3. ✅ Lưu file và báo kết quả (tên file, dung lượng, vị trí)

---

## 🌐 Hỗ trợ những trang nào?

YouTube, Facebook, TikTok, Instagram, Twitter/X, Vimeo, Dailymotion, Bilibili, và **hơn 1.800 trang web khác**.

Danh sách đầy đủ: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

---

## ❓ Gặp lỗi?

| Vấn đề | Cách xử lý |
|--------|------------|
| `pip` không nhận | Cài Python từ https://python.org (nhớ tick ✅ "Add to PATH") |
| Video cần đăng nhập | Nói thêm: "dùng cookies từ Chrome" |
| Không tải được | Chạy `pip install -U yt-dlp` để cập nhật phiên bản mới nhất |

---

**Tác giả:** Nguyễn Duy Tùng — Antigravity AI Workforce  
**Phiên bản:** 1.0 · Tháng 3/2026
