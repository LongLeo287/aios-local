---
id: CAPABILITY-MAP-001
type: REFERENCE
domain: [system, skills, plugins, discovery]
dept: all
created: 2026-03-22
version: 1.0
authority: registry_capability
---

# AI OS Corp — Capability Map
## Skill / Plugin Discovery Index (Human + Agent readable)

> **Mục đích:** `knowledge_navigator` đọc file này ở Phase 3 để tìm đúng skill/plugin  
> cho mỗi domain tag thay vì keyword guessing.  
> Accuracy cải thiện từ ~65% → ~90% khi dùng CAPABILITY_MAP + LightRAG.

---

## Upgrade Path

```
NOW (Phase 1):   knowledge_navigator reads CAPABILITY_MAP.md → 90% accuracy
NEXT (Phase 2):  LightRAG graph indexes all SKILL.md + manifest.json → 95%+ accuracy
                 Run: python ops/scripts/index_skills_lightrag.py
FUTURE (Phase 3): GitNexus impact analysis → exact blast radius when modifying plugins
                  Run: npx gitnexus analyze (in AI OS root)
```

---

## Domain → Skill/Plugin Map

### ai_ml (AI/ML, LLMs, RAG, Embeddings)
| Need | Use | Type | Path |
|------|-----|------|------|
| Knowledge search / RAG | `knowledge_enricher` | skill | brain/skills/knowledge_enricher/ |
| Graph-based RAG | `LightRAG` | plugin | plugins/LightRAG/ |
| Document ingestion | `open-notebook` | plugin | plugins/open-notebook/ |
| Research synthesis | `notebooklm-skill` | plugin | plugins/notebooklm-skill/ |
| Multi-source aggregation | `multi-source-aggregation` | skill | brain/skills/multi-source-aggregation/ |
| Reasoning + decision | `reasoning_engine` | skill | brain/skills/reasoning_engine/ |
| Cognitive patterns | `cognitive_reflector` | skill | brain/skills/cognitive_reflector/ |
| LLM routing | `llm_router` | skill | brain/skills/llm_router/ |
| NLP + data extract | `langextract` | plugin | plugins/langextract/ |

### backend (Python, API, FastAPI, Node.js)
| Need | Use | Type | Path |
|------|-----|------|------|
| Shell + scripts | `shell_assistant` | skill | brain/skills/shell_assistant/ |
| Production QA | `production_qa` | skill | brain/skills/production_qa/ |
| Architecture linting | `fsd_architectural_linter` | skill | brain/skills/domains/frontend/ |
| Resilience + retry | `resilience_engine` | skill | brain/skills/resilience_engine/ |
| Performance profiling | `performance_profiler` | skill | brain/skills/performance_profiler/ |
| Diagnostics | `diagnostics_engine` | skill | brain/skills/diagnostics_engine/ |

### web_frontend (React, Vue, HTML, CSS, UI)
| Need | Use | Type | Path |
|------|-----|------|------|
| UI/UX generation | `visual_excellence` | skill | brain/skills/visual_excellence/ |
| UI PRO generation | `ui-ux-pro-max` | plugin | plugins/ui-ux-pro-max/ |
| Accessibility | `accessibility_grounding` | skill | brain/skills/accessibility_grounding/ |
| SEO/AEO | `seo-aeo-optimization` | skill | brain/skills/seo-aeo-optimization/ |

### devops (Docker, CI/CD, k8s, infra)
| Need | Use | Type | Path |
|------|-----|------|------|
| Shell + deployment | `shell_assistant` | skill | brain/skills/shell_assistant/ |
| Resilience | `resilience_engine` | skill | brain/skills/resilience_engine/ |
| Diagnostics | `diagnostics_engine` | skill | brain/skills/diagnostics_engine/ |
| Cloudflare deploy | `cloudflare-skills` | plugin | plugins/cloudflare-skills/ |
| Vercel deploy | `vercel-agent-skills` | plugin | plugins/vercel-agent-skills/ |

### cybersecurity (CVE, pentest, OWASP, secrets)
| Need | Use | Type | Path |
|------|-----|------|------|
| GATE_SECURITY scan | `security_shield` | skill | brain/skills/security_shield/ |
| Repo vetting | `skill_sentry` | skill | brain/skills/skill_sentry/ |
| Leak detection | `zeroleaks` | plugin | plugins/zeroleaks/ |
| CVE tracking | `cybersecurity` | skill | brain/skills/cybersecurity/ |
| Cert scanning | `cerberus-cve-tool` | plugin | plugins/cerberus-cve-tool/ (check) |

### marketing (SEO, content, social, campaigns)
| Need | Use | Type | Path |
|------|-----|------|------|
| Web intelligence | `web_intelligence` | skill | brain/skills/web_intelligence/ |
| SEO/AEO | `seo-aeo-optimization` | skill | brain/skills/seo-aeo-optimization/ |
| Channel management | `channel_manager` | skill | brain/skills/channel_manager/ |
| Notification | `notification_bridge` | skill | brain/skills/notification_bridge/ |

### legal (GDPR, contracts, IP, compliance)
| Need | Use | Type | Path |
|------|-----|------|------|
| Legal reasoning | `reasoning_engine` | skill | brain/skills/reasoning_engine/ |
| Knowledge enrichment | `knowledge_enricher` | skill | brain/skills/knowledge_enricher/ |
| Web research | `web_intelligence` | skill | brain/skills/web_intelligence/ |

### finance (budget, cost, invoice, API cost)
| Need | Use | Type | Path |
|------|-----|------|------|
| Cost tracking | `cost_manager_skill` | skill | brain/skills/domains/finance/ |
| Performance metrics | `performance_profiler` | skill | brain/skills/performance_profiler/ |
| Data analysis | `insight_engine` | skill | brain/skills/insight_engine/ |

### knowledge_mgmt (KI, memory, index, graph)
| Need | Use | Type | Path |
|------|-----|------|------|
| Knowledge navigation | `knowledge_navigator` | skill | brain/skills/knowledge_navigator/ |
| Knowledge enrichment | `knowledge_enricher` | skill | brain/skills/knowledge_enricher/ |
| Memory (session) | `cosmic_memory` | skill | brain/skills/cosmic_memory/ |
| Memory (long-term) | `smart_memory` | skill | brain/skills/smart_memory/ |
| Memory (neural) | `neural_memory` | skill | brain/skills/neural_memory/ |
| Archiving | `archivist` | skill | brain/skills/archivist/ |
| Graph RAG | `LightRAG` | plugin | plugins/LightRAG/ |
| Context management | `context_manager` | skill | brain/skills/context_manager/ |

### registry (skill, plugin, agent lifecycle)
| Need | Use | Type | Path |
|------|-----|------|------|
| Skill generation | `skill_generator` | skill | brain/skills/skill_generator/ |
| Skill sentry | `skill_sentry` | skill | brain/skills/skill_sentry/ |
| Agent creation | `orchestrator_pro` | skill | brain/skills/orchestrator_pro/ |
| Proposal engine | `proposal_engine` | skill | brain/skills/proposal_engine/ |

### codebase_navigation (code understanding, refactoring, debugging)
| Need | Use | Type | Path |
|------|-----|------|------|
| Code exploration | `gitnexus-exploring` | skill | tools/gitnexus-web/gitnexus/skills/ |
| Blast radius analysis | `gitnexus-impact-analysis` | skill | tools/gitnexus-web/gitnexus/skills/ |
| Bug tracing | `gitnexus-debugging` | skill | tools/gitnexus-web/gitnexus/skills/ |
| Refactoring | `gitnexus-refactoring` | skill | tools/gitnexus-web/gitnexus/skills/ |
| PR review | `gitnexus-pr-review` | skill | tools/gitnexus-web/gitnexus/skills/ |
| Cypher graph query | `gitnexus-cli` | skill | tools/gitnexus-web/gitnexus/skills/ |

### google_workspace (GAS, Sheets, Docs, Drive)
| Need | Use | Type | Path |
|------|-----|------|------|
| Google Apps Script | `gas_skill` | skill | brain/skills/domains/google-workspace/ |
| Sheets performance | `sheets_performance_optimization` | skill | brain/skills/domains/google-workspace/ |

### databases (Supabase, PostgreSQL, SQL)
| Need | Use | Type | Path |
|------|-----|------|------|
| Supabase patterns | `supabase_postgres_best_practices` | skill | brain/skills/domains/databases/ |

### mobile (React Native, Android, APK)
| Need | Use | Type | Path |
|------|-----|------|------|
| APK modification | `Android_APK_Modification` | skill | brain/skills/ |

---

## Quick Lookup: By Capability

| Capability | Best Tool | Accuracy |
|-----------|-----------|---------|
| Semantic search over documents | `LightRAG` (mix mode) | 95%+ |
| Code relationship graph | `GitNexus` (cypher) | 95%+ |
| Plugin impact analysis | `GitNexus` (impact tool) | 90%+ |
| Memory across sessions | `cosmic_memory` / `smart_memory` | 85%+ |
| Web scraping | `web_intelligence` / `langextract` | 85%+ |
| Security scan (repo) | `security_shield` / `zeroleaks` | 95%+ |
| UI generation | `visual_excellence` / `ui-ux-pro-max` | 90%+ |
| Knowledge ingestion | `knowledge_enricher` + `open-notebook` | 90%+ |
| Agent orchestration | `orchestrator_pro` / `corp_orchestrator` | 90%+ |
| Notification to CEO | `notification_bridge` | 99%+ |

---

## Finding Tools — Decision Tree

```
NEED A TOOL FOR: <task>
    │
    ├─ Is it about AI/RAG/Memory?      → LightRAG, knowledge_enricher, open-notebook
    ├─ Is it about code/repos?         → GitNexus (explore/impact/debug/refactor)
    ├─ Is it about security?           → security_shield, zeroleaks, skill_sentry
    ├─ Is it about UI?                 → visual_excellence, ui-ux-pro-max
    ├─ Is it about deployment?         → shell_assistant, cloudflare-skills, vercel-agent-skills
    ├─ Is it about data extraction?    → langextract, web_intelligence, knowledge_enricher
    ├─ Is it about memory?             → cosmic_memory → smart_memory → LightRAG
    └─ Unsure?                         → query LightRAG: aquery("<task>", mode="mix")
                                         OR check knowledge_index.md
```

---

## LightRAG Query Interface (when service running at localhost:5055)

```python
# knowledge_navigator Phase 3 upgrade
import httpx
result = await httpx.post(
    "http://localhost:5055/api/rag/query",
    json={"query": domain_tag, "mode": "mix"}
)
# Returns: entities, relationships, relevant chunks → identify skill/plugin
```

---

## GitNexus Query Interface (when MCP active)

```
# Impact analysis — what breaks if I remove plugin X?
gitnexus://repo/ai-os/impact?symbol=<plugin_id>&depth=3

# Explore skill dependencies
gitnexus://repo/ai-os/context?symbol=<skill_id>

# Raw graph query
cypher: MATCH (s:Skill)-[:CALLS]->(p:Plugin) WHERE s.id = '<id>' RETURN p
```

---

*Capability Map v1.0 | 2026-03-22 | Updated by: registry-manager-agent*  
*Cross-check with: SKILL_REGISTRY.json, plugins/registry.json, knowledge_index.md*
