---
id: KI-2026-03-22-cybersecurity-foundation
type: REFERENCE
domain: cybersecurity
dept: all
created: 2026-03-22
foundation: true
tags: ['security', 'cybersecurity', 'threats', 'quarantine', 'gatekeeper']
---

# AI OS Corp — Cybersecurity Framework

## AI OS Cybersecurity Posture

### Threat Model
- **Attack surface:** Local services on 127.0.0.1 (closed to internet by default)
- **Key risk:** Agentic code execution (ClawWork, E2B sandbox exposure)
- **Mitigation:** NemoClaw-inspired 4-layer sandbox (see REFERENCE KI)

### Defense Layers (NemoClaw-inspired)
1. **Network:** Services bind to 127.0.0.1 only (not 0.0.0.0)
2. **Filesystem:** Agents work in designated paths (plugins/, workspace/)
3. **Process:** ag-auto-accept controlled via API, not raw stdin injection
4. **Inference:** 9router validates model outputs before tool execution

### Tools
- `security/QUARANTINE/vet_repo.ps1` — vets repos before cloning
- `security/gatekeeper.ps1` — blocks dangerous tool use patterns
- strix security-agent — automated code scanning agent

### Workflows
- `nemoclaw-strix-scan.md` — security scan workflow
- `secrets-management.md` — env vars and DPAPI encryption

---
*Foundation KI — created 2026-03-22*
