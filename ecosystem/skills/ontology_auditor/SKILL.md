---
name: ontology_auditor
description: Siêu kỹ năng quét rác vũ trụ, đóng gói vũ khí mồ côi và render lại Org Graph.
version: 1.0.0
author: Antigravity
owner_dept: monitoring_inspection
---
# ONTOLOGY AUDITOR (MA TRẬN TIẾN HÓA)

**Kích hoạt:** Khi Sếp hoặc hệ thống yêu cầu "Dọn dẹp", "Quét rác", "Render Org Graph".
**Hành động:** Chạy kịch bản `python system/ops/scripts/ontology_auditor.py`.
**Kết quả:** Dọn sạch các Agent, Workflow, Skill, Plugin mồ côi và ép chúng vào đúng vị trí trên Đồ thị nhận thức.

## Cách dùng (Cho SRE-Agent)
Mở terminal và gõ:
```bash
python "d:\AI OS CORP\AI OS\system\ops\scripts\ontology_auditor.py"
```
