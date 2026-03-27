<#
.SYNOPSIS
    AI OS -- Migrate YAML frontmatter into existing SKILL.md files.
    Prepends the frontmatter block to each file WITHOUT modifying existing body content.

.USAGE
    & "<AI_OS_ROOT>\scripts\migrate_skill_frontmatter.ps1"
    & "<AI_OS_ROOT>\scripts\migrate_skill_frontmatter.ps1" -DryRun

.NOTES
    Updated: 2026-03-14
    Source metadata: shared-context/SKILL_REGISTRY.json
#>

param([switch]$DryRun)

$AiOsRoot = $env:AOS_ROOT

# ---- Frontmatter definitions for each skill ----
# Source: SKILL_REGISTRY.json v2 (manually curated dependency graph)
$SkillMeta = @{

"accessibility_grounding" = @{
path       = "$AiOsRoot\skills\accessibility_grounding\SKILL.md"
frontmatter = @"
---
id: accessibility_grounding
name: Accessibility Grounding
version: 1.1.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: WCAG compliance and Accessibility Tree parsing for efficient web control.

accessible_by:
  - QA
  - UX

dependencies:
  - visual_excellence

exposed_functions:
  - name: wcag_check
  - name: screen_reader_simulation
  - name: parse_accessibility_tree

consumed_by: []
emits_events: []
listens_to: []
---

"@
}

"archivist" = @{
path       = "$AiOsRoot\agents\archivist\SKILL.md"
frontmatter = @"
---
id: archivist
name: Archivist
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: File organization, log rotation, and knowledge indexing across workspaces.

accessible_by:
  - Orchestrator

dependencies:
  - smart_memory
  - knowledge_enricher

exposed_functions:
  - name: index_workspace
  - name: rotate_logs
  - name: aggregate_docs
  - name: purify_workspace

consumed_by: []
emits_events:
  - workspace_indexed
  - logs_rotated
listens_to:
  - session_end
---

"@
}

"cognitive_evolver" = @{
path       = "$AiOsRoot\skills\cognitive_evolver\SKILL.md"
frontmatter = @"
---
id: cognitive_evolver
name: Cognitive Evolver
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Self-modifying strategy and paradigm evolution based on accumulated insights.

accessible_by:
  - Architect

dependencies:
  - insight_engine
  - cosmic_memory

exposed_functions:
  - name: paradigm_shift
  - name: self_improvement
  - name: update_strategy

consumed_by: []
emits_events:
  - strategy_updated
listens_to:
  - reflection_complete
---

"@
}

"cognitive_reflector" = @{
path       = "$AiOsRoot\agents\cognitive_reflector\SKILL.md"
frontmatter = @"
---
id: cognitive_reflector
name: Cognitive Reflector
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Post-task reflection engine -- outcome vs plan comparison, lesson extraction.

accessible_by:
  - All agents

dependencies:
  - cosmic_memory
  - insight_engine

exposed_functions:
  - name: reflect_on_task
  - name: extract_lessons
  - name: update_knowledge

consumed_by: []
emits_events:
  - reflection_complete
  - lessons_extracted
listens_to:
  - task_complete
  - task_failed
---

"@
}

"cosmic_memory" = @{
path       = "$AiOsRoot\skills\cosmic_memory\SKILL.md"
frontmatter = @"
---
id: cosmic_memory
name: Cosmic Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Observation-based long-term memory for cross-session recall (Smallville style).

accessible_by:
  - Architect
  - Orchestrator

dependencies:
  - smart_memory

exposed_functions:
  - name: extract_observation
  - name: cross_session_recall
  - name: generate_reflection

consumed_by:
  - cognitive_evolver
emits_events:
  - observation_stored
listens_to:
  - reflection_complete
---

"@
}

"diagnostics_engine" = @{
path       = "$AiOsRoot\skills\diagnostics_engine\SKILL.md"
frontmatter = @"
---
id: diagnostics_engine
name: Diagnostics Engine
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Full system health audit and project quality scoring (React Doctor style).

accessible_by:
  - Architect
  - Chief of Staff

dependencies:
  - performance_profiler

exposed_functions:
  - name: health_audit
  - name: project_scoring
  - name: generate_diagnostic_report

consumed_by: []
emits_events:
  - health_report_ready
listens_to: []
---

"@
}

"insight_engine" = @{
path       = "$AiOsRoot\skills\insight_engine\SKILL.md"
frontmatter = @"
---
id: insight_engine
name: Insight Engine
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Cross-domain pattern discovery and trend analysis.

accessible_by:
  - Researcher
  - Analyst

dependencies:
  - reasoning_engine
  - neural_memory

exposed_functions:
  - name: pattern_recognition
  - name: trend_analysis
  - name: cross_domain_synthesis

consumed_by:
  - cognitive_evolver
emits_events:
  - insight_discovered
listens_to: []
---

"@
}

"knowledge_enricher" = @{
path       = "$AiOsRoot\skills\knowledge_enricher\SKILL.md"
frontmatter = @"
---
id: knowledge_enricher
name: Knowledge Enricher
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Metadata enrichment and contextual cross-linking of knowledge entries.

accessible_by:
  - Researcher

dependencies:
  - web_intelligence
  - neural_memory

exposed_functions:
  - name: metadata_enrichment
  - name: contextual_linking
  - name: backfill_knowledge

consumed_by:
  - archivist
emits_events:
  - knowledge_enriched
listens_to: []
---

"@
}

"neural_memory" = @{
path       = "$AiOsRoot\skills\neural_memory\SKILL.md"
frontmatter = @"
---
id: neural_memory
name: Neural Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Associative neural-network style recall and knowledge graph synthesis.

accessible_by:
  - Researcher
  - Developer

dependencies:
  - context_manager

exposed_functions:
  - name: associative_recall
  - name: graph_synthesis
  - name: semantic_link

consumed_by:
  - insight_engine
  - knowledge_enricher
emits_events:
  - graph_updated
listens_to: []
---

"@
}

"notification_bridge" = @{
path       = "$AiOsRoot\skills\notification_bridge\SKILL.md"
frontmatter = @"
---
id: notification_bridge
name: Notification Bridge
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Push notifications and multi-channel alerting (ccpoke Protocol).

accessible_by:
  - Orchestrator
  - User Experience

dependencies: []

exposed_functions:
  - name: send_alert
  - name: manage_subscriptions
  - name: push_to_channel

consumed_by:
  - orchestrator_pro
emits_events:
  - alert_sent
listens_to:
  - task_complete
  - task_failed
  - health_report_ready
---

"@
}

"orchestrator_pro" = @{
path       = "$AiOsRoot\agents\orchestrator_pro\SKILL.md"
frontmatter = @"
---
id: orchestrator_pro
name: Orchestrator Pro
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Full multi-agent orchestration -- decompose, delegate, monitor, synthesize.

accessible_by:
  - Antigravity

dependencies:
  - reasoning_engine
  - smart_memory
  - notification_bridge
  - shell_assistant

exposed_functions:
  - name: decompose_task
  - name: delegate_to_agent
  - name: monitor_progress
  - name: synthesize_report

consumed_by: []
emits_events:
  - task_delegated
  - phase_complete
listens_to:
  - task_complete
  - task_failed
---

"@
}

"performance_profiler" = @{
path       = "$AiOsRoot\skills\performance_profiler\SKILL.md"
frontmatter = @"
---
id: performance_profiler
name: Performance Profiler
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Latency auditing, resource tracking and performance bottleneck detection.

accessible_by:
  - Dev
  - QA

dependencies: []

exposed_functions:
  - name: audit_latency
  - name: track_resources
  - name: generate_profile_report

consumed_by:
  - diagnostics_engine
emits_events:
  - profile_ready
listens_to: []
---

"@
}

"production_qa" = @{
path       = "$AiOsRoot\skills\production_qa\SKILL.md"
frontmatter = @"
---
id: production_qa
name: Production QA
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Adversarial QA reviews and cryptographically-auditable task receipts.

accessible_by:
  - QA
  - Architect

dependencies:
  - reasoning_engine

exposed_functions:
  - name: adversarial_review
  - name: generate_receipt
  - name: edge_case_hunt
  - name: regression_check

consumed_by:
  - orchestrator_pro
emits_events:
  - receipt_generated
  - qa_failed
listens_to:
  - task_complete
---

"@
}

"reasoning_engine" = @{
path       = "$AiOsRoot\skills\reasoning_engine\SKILL.md"
frontmatter = @"
---
id: reasoning_engine
name: Reasoning Engine
version: 1.0.0
tier: 1
status: active
author: AI OS Core Team
updated: 2026-03-14
description: First-principles problem decomposition and technical logic chains.

accessible_by:
  - Orchestrator
  - Claude Code
  - Antigravity

dependencies:
  - context_manager

exposed_functions:
  - name: decompose_problem
  - name: evaluate_tradeoffs
  - name: chain_of_thought

consumed_by:
  - orchestrator_pro
  - insight_engine
  - production_qa
  - security_shield
emits_events: []
listens_to: []
---

"@
}

"resilience_engine" = @{
path       = "$AiOsRoot\skills\resilience_engine\SKILL.md"
frontmatter = @"
---
id: resilience_engine
name: Resilience Engine
version: 1.0.0
tier: 1
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Circuit breakers, retry logic, and self-healing protocols.

accessible_by:
  - All agents

dependencies: []

exposed_functions:
  - name: circuit_breaker
  - name: retry_with_backoff
  - name: error_recovery
  - name: fallback_plan

consumed_by:
  - shell_assistant
  - web_intelligence
emits_events:
  - circuit_opened
  - recovery_triggered
listens_to:
  - tool_failed
---

"@
}

"security_shield" = @{
path       = "$AiOsRoot\skills\security_shield\SKILL.md"
frontmatter = @"
---
id: security_shield
name: Security Shield
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Defensive security auditing, vulnerability scanning and auto-remediation.

accessible_by:
  - QA
  - DevOps

dependencies:
  - reasoning_engine

exposed_functions:
  - name: vulnerability_scan
  - name: auto_remediate
  - name: compliance_check
  - name: threat_model

consumed_by: []
emits_events:
  - vulnerability_found
  - compliance_passed
listens_to: []
---

"@
}

"shell_assistant" = @{
path       = "$AiOsRoot\skills\shell_assistant\SKILL.md"
frontmatter = @"
---
id: shell_assistant
name: Shell Assistant
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Shell mastery and automated script execution with safety guards.

accessible_by:
  - DevOps
  - Developer
  - Claude Code

dependencies:
  - resilience_engine

exposed_functions:
  - name: execute_command
  - name: generate_script
  - name: parse_output
  - name: safe_run

consumed_by:
  - orchestrator_pro
emits_events:
  - command_executed
  - command_failed
listens_to: []
---

"@
}

"smart_memory" = @{
path       = "$AiOsRoot\skills\smart_memory\SKILL.md"
frontmatter = @"
---
id: smart_memory
name: Smart Memory
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: ASM-style fact extraction and selective recall across sessions.

accessible_by:
  - Orchestrator
  - Claude Code

dependencies:
  - context_manager

exposed_functions:
  - name: extract_facts
  - name: recall_selective
  - name: consolidate_memory

consumed_by:
  - orchestrator_pro
  - archivist
  - cosmic_memory
emits_events:
  - facts_extracted
listens_to:
  - task_complete
---

"@
}

"visual_excellence" = @{
path       = "$AiOsRoot\skills\visual_excellence\SKILL.md"
frontmatter = @"
---
id: visual_excellence
name: Visual Excellence
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Cinematic UI generation and Apple-style premium visual storytelling.

accessible_by:
  - Designer
  - UX

dependencies: []

exposed_functions:
  - name: ui_audit
  - name: style_guide_enforcement
  - name: cinematic_layout
  - name: generate_palette

consumed_by:
  - accessibility_grounding
emits_events: []
listens_to: []
---

"@
}

"web_intelligence" = @{
path       = "$AiOsRoot\skills\web_intelligence\SKILL.md"
frontmatter = @"
---
id: web_intelligence
name: Web Intelligence
version: 1.0.0
tier: 2
status: active
author: AI OS Core Team
updated: 2026-03-14
description: Katana-style web crawling, scraping and structured data extraction.

accessible_by:
  - Researcher
  - Orchestrator

dependencies:
  - resilience_engine

exposed_functions:
  - name: smart_scrape
  - name: site_mapping
  - name: deep_crawl
  - name: extract_structured

consumed_by:
  - knowledge_enricher
emits_events:
  - crawl_complete
listens_to: []
---

"@
}

}

# ---- PROCESS EACH SKILL ----
$success = 0
$skipped = 0
$failed  = 0

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  AI OS -- Skill Frontmatter Migration          " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($skillId in $SkillMeta.Keys | Sort-Object) {
    $meta = $SkillMeta[$skillId]
    $filePath = $meta.path

    if (-not (Test-Path $filePath)) {
        Write-Host "  [SKIP] $skillId -- file not found: $filePath" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    $existing = Get-Content $filePath -Raw

    # Skip if already has frontmatter
    if ($existing -match "^---") {
        Write-Host "  [SKIP] $skillId -- already has frontmatter" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    $newContent = $meta.frontmatter + $existing

    if ($DryRun) {
        Write-Host "  [DRY] $skillId -- would prepend frontmatter ($($newContent.Length) bytes)" -ForegroundColor Yellow
    } else {
        try {
            Set-Content -Path $filePath -Value $newContent -Encoding UTF8 -NoNewline:$false
            Write-Host "  [OK]  $skillId -- frontmatter added" -ForegroundColor Green
            $success++
        } catch {
            Write-Host "  [ERR] $skillId -- $($_.Exception.Message)" -ForegroundColor Red
            $failed++
        }
    }
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  MIGRATION REPORT                             " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Nothing written." -ForegroundColor Magenta
} else {
    Write-Host "  Updated : $success skills" -ForegroundColor Green
    Write-Host "  Skipped : $skipped (already done or not found)" -ForegroundColor Gray
    Write-Host "  Failed  : $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
}
Write-Host ""
Write-Host "Next: run skill_loader.ps1 to verify all skills are discovered." -ForegroundColor Cyan
Write-Host ""

