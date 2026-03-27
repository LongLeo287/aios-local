---
id: KI-2026-03-22-staging-foundation
type: REFERENCE
domain: staging
dept: all
created: 2026-03-22
foundation: true
tags: ['staging', 'deployment', 'docker', 'production', 'devops']
---

# AI OS Corp — Staging & Deployment

## Staging Environment

### Current State: Local-Only
AI OS Corp currently runs entirely on local machine:
- No cloud deployment
- All services bind to 127.0.0.1
- Docker-based services (open-notebook, lobe-chat, prometheus) run locally

### Services That Can Be Staged (Docker-ready)
| Service | Docker Image | Notes |
|---------|--------|-------|
| open-notebook | `docker compose up -d` | `plugins/open-notebook/` |
| lobe-chat | `lobehub/lobe-chat:latest` | Single container |
| prometheus+grafana | `docker compose up -d` | `plugins/prometheus-grafana-alerts/` |
| vieneu-tts | `docker compose up -d` | `plugins/vieneu-tts/` |

### Deployment Checklist
Before deploying any service:
1. `security/QUARANTINE/vet_repo.ps1` — scan for security issues
2. Set environment variables via `ops/secrets/`
3. Update `ops/runtime/` with service config
4. Add health check to `services_control.py`
5. Test via ClawTask Services panel

### Monitoring
- Prometheus (:9090) + Grafana (:4000) — currently local
- Alert channel: Telegram via nullclaw bot
- See: `plugins/prometheus-grafana-alerts/`

---
*Foundation KI — created 2026-03-22*
