# registry_ingest.md — Ingest Queue: CIV → Registry & Capability
# Owner: registry-manager-agent (Registry & Capability, Dept 14)
# Written by: ingest-router-agent (CIV, Dept 20)
# Read by: registry-manager-agent at boot + after each CIV delivery
# Ref: content-intake-flow.md STEP 5 → knowledge-distribution-flow.md STEP D1

---

<!-- QUEUE FORMAT — ingest-router writes new entries at BOTTOM -->
<!-- registry-manager reads from TOP, marks processed entries as [DONE] -->

<!-- EXAMPLE ENTRY:
## INGEST — CIV-2026-03-22-000 — [EXAMPLE]
Status: EXAMPLE
civ_ticket: CIV-2026-03-22-000
content_type: REPO
destination_path: <AOS_ROOT>/plugins/example-plugin/
quality_score: 9
source_url: https://github.com/example/repo
tags: [plugin, tools]
civ_analysis: <AOS_ROOT>/security/QUARANTINE/vetted/repos/example-plugin/_CIV_ANALYSIS.md
delivered_at: 2026-03-22T00:00:00+07:00
[DONE — processed by registry-manager-agent]
-->

<!-- New entries appended below this line -->
