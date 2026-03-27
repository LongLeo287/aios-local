---
name: public_api_search_skill
description: "Tra cứu danh bạ Public APIs cho AI OS"
version: 1.0.0
owner: Dept 03
---
# public_api_search_skill (Tìm kiếm API Công Cộng)

## Mô tả
Kỹ năng này tận dụng kho tri thức `public-apis` để tìm kiếm các endpoint phục vụ cho việc tích hợp tính năng mới vào hệ thống mà không phải xây dựng từ số 0.

## Context Isolation
- Output: Trả về danh sách URL, method và requirement của Free API.
- Không tự động gửi request, chỉ trả về metadata.

## Cách sử dụng
1. Tác vụ: Liệt kê các bộ API thuộc chủ đề Sếp yêu cầu.
2. Nguồn dữ liệu mồi: `ecosystem/plugins/public-apis/`
3. Gọi công cụ: `search_public_api(category="cryptocurrency")`

*Auto-Spawned by Antigravity on 2026-03-27*
