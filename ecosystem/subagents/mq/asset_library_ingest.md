# asset_library_ingest.md — Ingest Queue: CIV → Asset Library
# Owner: knowledge-curator-agent (Asset Library, Dept 15)
# Written by: ingest-router-agent (CIV, Dept 20)
# Read by: knowledge-curator-agent at boot + after each CIV delivery
# Ref: content-intake-flow.md STEP 5 → knowledge-distribution-flow.md STEP D1

---

<!-- QUEUE FORMAT — ingest-router writes new entries at BOTTOM -->
<!-- knowledge-curator reads from TOP, marks processed entries as [DONE] -->

<!-- EXAMPLE ENTRY (delete when first real entry arrives):
## INGEST — CIV-2026-03-22-000 — [EXAMPLE]
Status: EXAMPLE
civ_ticket: CIV-2026-03-22-000
content_type: DOCUMENT
destination_path: <AOS_ROOT>/brain/knowledge/documents/example.md
quality_score: 8
source_url: https://example.com
tags: [ai, reference]
delivered_at: 2026-03-22T00:00:00+07:00
[DONE — processed by knowledge-curator-agent]
-->

<!-- New entries appended below this line -->
