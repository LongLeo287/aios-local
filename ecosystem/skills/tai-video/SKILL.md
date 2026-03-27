---
name: tai-video
description: Tải video từ Facebook, YouTube, TikTok và hàng nghìn trang web khác bằng yt-dlp. Kích hoạt khi user yêu cầu tải video, download video, lưu video từ bất kỳ URL nào.
---

// turbo-all

# Tải Video bằng yt-dlp

**Luôn sử dụng `yt-dlp`** cho MỌI thao tác tải video. Hỗ trợ Facebook, YouTube, TikTok, Instagram, Twitter/X, và [hàng nghìn trang khác](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Khi nào kích hoạt skill này

- User yêu cầu **tải video**, **download video**, **lưu video** từ URL
- User gửi link video và muốn tải về
- User yêu cầu tải nhạc/audio từ video

## Dependencies

| Tool | Kiểm tra | Cài đặt |
|------|----------|---------|
| `yt-dlp` | `yt-dlp --version` | `pip install yt-dlp` |
| `ffmpeg` | `ffmpeg -version` | `winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements` |

> [!IMPORTANT]
> Sau khi cài ffmpeg bằng winget, cần refresh PATH:
> ```powershell
> $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
> ```

## Tải video (mặc định — chất lượng tốt nhất)

```powershell
yt-dlp -o "<output_dir>\%(title).100B s.%(ext)s" "<URL>"
```

### Giải thích tham số output

| Phần | Ý nghĩa |
|------|---------|
| `%(title).100Bs` | Tên video, cắt tối đa 100 byte (tránh tên file quá dài) |
| `%(ext)s` | Extension tự động (mp4, webm...) |

## Tải audio (chỉ khi user yêu cầu)

```powershell
yt-dlp -x --audio-format mp3 -o "<output_dir>\%(title).100Bs.%(ext)s" "<URL>"
```

## Tải video chọn chất lượng

### Liệt kê các định dạng có sẵn

```powershell
yt-dlp -F "<URL>"
```

### Tải định dạng cụ thể

```powershell
yt-dlp -f <format_id> -o "<output_dir>\%(title).100Bs.%(ext)s" "<URL>"
```

## Tải playlist / nhiều video

```powershell
yt-dlp -o "<output_dir>\%(playlist_title)s\%(title).100Bs.%(ext)s" "<PLAYLIST_URL>"
```

## Xử lý lỗi thường gặp

| Lỗi | Giải pháp |
|-----|-----------|
| Video cần đăng nhập | Dùng `--cookies-from-browser chrome` để lấy cookies từ trình duyệt |
| Tên file bị lỗi encoding | Thêm `--encoding utf-8` hoặc dùng `%(id)s` thay `%(title)s` |
| Bị chặn tải | Thử `--user-agent "Mozilla/5.0"` hoặc dùng cookies |
| FFmpeg not found | Cài ffmpeg theo bảng Dependencies ở trên |

## Quy tắc quan trọng

1. **Mặc định lưu vào thư mục hiện tại** của user, trừ khi user chỉ định nơi khác
2. **Luôn dùng đường dẫn tuyệt đối** cho output directory
3. **Luôn set `SafeToAutoRun: true`** vì skill này có annotation `// turbo-all`
4. **Sau khi tải xong**, thông báo: tên file, kích thước, vị trí lưu
5. **Nếu tên file bị lỗi encoding** (ký tự đặc biệt), rename lại cho gọn
