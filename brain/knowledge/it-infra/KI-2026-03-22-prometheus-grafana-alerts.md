---
id: KI-2026-03-22-prometheus-grafana-alerts
source: https://github.com/fdhhhdjd/class-prometheus-grafana-telegram-alerts
type: TOOL
domain: it-infra
dept: it_infra, engineering
compatible_ai_os: true
propose_clone: true
status: CLONED -> plugins/prometheus-grafana-alerts/
created: 2026-03-22T23:23:54.299876
---

# Prometheus + Grafana + Telegram Alerts Stack

> Complete monitoring stack. Docker Compose: Prometheus + Grafana + cAdvisor + Telegram alerts.

**CLONED to:** `plugins/prometheus-grafana-alerts/`  
**Deploy:** `docker compose up -d`

## Architecture
- Node.js :8081 → prom-client → /metrics endpoint  
- Prometheus :9090 → scrapes metrics + cAdvisor :8082  
- Grafana :4000 → dashboards + alert rules → Telegram bot

## AI OS Integration Plan
Modify prometheus.yml to scrape AI OS services:
```yaml
scrape_configs:
  - job_name: clawtask
    static_configs:
      - targets: ['host.docker.internal:7474']
  - job_name: ollama  
    static_configs:
      - targets: ['host.docker.internal:11434']
```
