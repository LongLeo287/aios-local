# client_reception â€” Department Memory
# Owner: project-intake-agent | Retention: 30-day rolling | Layer: Department
# Updated: 2026-03-19 | Format: see brain/corp/memory/MEMORY_SPEC.md

## Always-Load Context
Dept: client_reception
Status: DORMANT (activate only when CEO offline)
Escalation path: project-intake-agent â†’ COO â†’ CEO (Telegram for urgent)
Managed plugins: nullclaw (client-facing), tinyclaw (internal ops)
Auto-approve threshold: < $2,000 USD
Intake protocol: brain/corp/sops/CLIENT_INTAKE_GATEWAY.md

---

## Sprint 1 â€” 2026-03-19 (Initial Setup)

### Architecture Decisions
- Dept created as part of AI OS Corp v2.4 (21st department)
- DORMANT mode by default â€” designed for CEO-offline scenarios
- Phase 1 channels: Telegram + Discord via nullclaw bot
- Phase 2 channels (planned): WhatsApp, Web form portal

### Lessons Learned
- (populate after first active client intake)

### Known Patterns
- (populate after first active sprint)

### Active Client Queue
- (populate when dept activates)

### Revenue Tracking
- Total revenue all-time: $0 (not yet activated)

### Cross-Dept Dependencies
- COO: activation authorization, escalation target
- Operations: receives kickoff brief after client ACCEPT
- Finance: tracks invoices and payment
- Security GRC: reviews any client with security-related requirements

---
*Append new sprints below. Archivist rotates entries older than 30 days.*

