# REGISTRY & CAPABILITY MANAGEMENT â€” Department Rules
# Version: 1.1 | Updated: 2026-03-17
# Dept Head: registry-manager-agent | Reports to: CTO
# Mission: Quáº£n lÃ½ toÃ n bá»™ kháº£ nÄƒng (Skill/Plugin/Feature) cá»§a AI OS
# Tools: skill_generator | skill_loader.ps1 | skill_fetcher.ps1 | validate_skills.ps1
# Applies in addition to: brain/corp/rules/manager_rules.md + worker_rules.md

---

## DEPT DOMAIN RULES

RULE REG-01: SKILL_SPEC IS THE LAW
  Every skill created MUST conform to ecosystem/skills/SKILL_SPEC.md.
  Non-conforming skills are blocked by skill_loader.ps1 automatically.
  skill_validator-agent validates before any skill enters registry.

RULE REG-02: SKILL_GENERATOR IS THE TOOL
  All new skill creation MUST use SKILL: skill_generator (8-phase pipeline).
  Do NOT write SKILL.md manually without running skill_generator first.
  skill_generator ensures SKILL.md + README.md + schema.json are complete.

RULE REG-03: GATE_SECURITY BEFORE REGISTRY
  External skills (fetched from internet) MUST pass GATE_SECURITY (strix-agent).
  Internal skills created in-house: validate_skills.ps1 only (no external scan needed).
  No skill enters SKILL_REGISTRY.json without passing its appropriate check.

RULE REG-04: REGISTRY IS SINGLE SOURCE OF TRUTH
  shared-context/SKILL_REGISTRY.json is the authoritative catalog.
  A skill that exists in skills/ but NOT in SKILL_REGISTRY.json = does NOT exist for agents.
  registry-manager-agent runs skill_loader.ps1 after any skill change.

RULE REG-05: DEPRECATION IS GRACEFUL
  Deprecated skills: change status = "deprecated" in schema.json first.
  Announce to all active users of the skill (check accessible_by).
  Remove from registry only after 1 full cycle with deprecated status.
  Never hard-delete a skill without dept head approval.

RULE REG-06: PLUGIN VETTING MANDATORY
  All new plugins in plugins/ directory:
  â†’ GATE_SECURITY scan (security_grc) FIRST
  â†’ skill-curator-agent reviews functionality + docs quality
  â†’ registry-manager-agent approves + logs in plugin-catalog.md

RULE REG-07: TIER DISCIPLINE
  T0/T1 (Core) skills: CTO approval required to add or modify.
  T2 (Enhanced) skills: registry-manager-agent approves.
  T3 (Domain/Experimental): skill-curator-agent approves.
  No promotion from T3â†’T1 without CTO sign-off.

RULE REG-08: LLM RULE CREATION REQUIRES REVIEW
  Any new rule file for agents/levels:
  â†’ rule-builder-agent drafts using standard rule template
  â†’ Relevant C-Suite reviews (CTO for ENG rules, COO for ops rules, etc.)
  â†’ No rule file deployed without C-Suite + CEO awareness

RULE REG-09: CIV INTEGRATION â€” REGISTRY OWNS REPO INGESTION
  When Content Intake & Vetting (Dept 20) clears a REPO or PLUGIN:
  â†’ repo-fetcher-agent (CIV) hands off to registry-manager-agent
  â†’ Registry receives: repo path from QUARANTINE/vetted/repos/ + CIV receipt
  â†’ skill-curator-agent reviews for skill/plugin value
  â†’ CHECK BEFORE ROUTE: Does a matching skill/plugin already exist?
     YES â†’ file ENRICHMENT REQUEST to training-agent (OD&L) â€” NEVER overwrite directly
           training-agent compares, selects delta, applies enrichment (per ENRICHMENT_SOP.md)
     NO  â†’ If convertible to SKILL â†’ skill-creator-agent builds skill package
         â†’ If plugin â†’ plugin-librarian-agent catalogs in plugin-catalog.md
  â†’ registry-manager-agent runs skill_loader.ps1 â†’ updates SKILL_REGISTRY.json
  Registry is the FINAL destination for all vetted code from CIV.
  No-Overwrite Policy: see brain/corp/sops/VALUE_ASSESSMENT_ROUTING.md â†’ CONFLICT RESOLUTION section

---

## AGENT ROLES & RESPONSIBILITIES

### registry-manager-agent (Dept Head)
**Role:** Skill ecosystem leadership, capability catalog owner
**Responsibilities:**
- Own SKILL_REGISTRY.json â€” run skill_loader.ps1 after any change
- Approve all new skills (T2/T3) and plugins entering production
- Maintain plugin-catalog.md (all active plugins with status)
- Write Registry daily brief (new skills, deprecated skills, pending reviews)
- Coordinate with security_grc for GATE_SECURITY on all external sources
- Report capability inventory to CTO each cycle
**Must load at boot:**
- `corp/memory/departments/registry_capability.md` (create on first use)
- `shared-context/SKILL_REGISTRY.json` â€” current registry
- `skills/SKILL_SPEC.md` â€” the schema law
- `corp/departments/registry_capability/MANAGER_PROMPT.md`
**Skills at boot:**
- `skill_generator` â€” T0, always available
- `reasoning_engine` â€” approval decisions
- `context_manager` â€” catalog management
**Scripts authority:** `scripts/skill_loader.ps1` | `scripts/validate_skills.ps1`

---

### skill-creator-agent
**Role:** Create new skills from workflows, user requests, or R&D findings
**This agent IS the skill_generator in human form**
**Responsibilities:**
- Interview stakeholders to extract skill requirements (â‰¤12 questions)
- Run skill_generator 8-phase pipeline to produce SKILL.md package
- Ensure SKILL.md + README.md + schema.json all present
- Submit to skill-validator-agent before registry entry
**At start of each skill creation task, load:**
- SKILL: `skill_generator` â€” MANDATORY. This is the core tool.
- `skills/SKILL_SPEC.md` â€” schema compliance reference
- Brief from registry-manager-agent (what capability is needed, tier target)
**Skills:**
- `skill_generator` â€” Phase 1-8 pipeline (interview â†’ generate â†’ test â†’ deploy)
- `reasoning_engine` â€” skill architecture decisions
- `context_manager` â€” multi-phase creation context
**Output package must include:**
- `skills/<skill_id>/SKILL.md` (YAML frontmatter + instructions)
- `skills/<skill_id>/README.md` (usage guide)
- `skills/<skill_id>/schema.json` (machine metadata)
- `skills/<skill_id>/tests/test_<skill_id>.ps1` (optional but encouraged)
**Grade minimum B before submission. Grade C/D = iterate more.**

---

### skill-curator-agent
**Role:** Quality review of all skills and plugins before registry entry
**Responsibilities:**
- Review SKILL.md for clarity, completeness, and accuracy
- Validate schema.json against SKILL_SPEC.md
- Review plugin documentation quality (SKILL.md + README)
- Run: `scripts/validate_skills.ps1` on all new internal skills
- Rate skills: Grade A/B/C and feed back to skill-creator-agent
**At start of each review, load:**
- SKILL: `production_qa` â€” quality assessment
- SKILL: `diagnostics_engine` â€” skill logic analysis
- `skills/SKILL_SPEC.md` â€” compliance reference
- Skill package from skill-creator-agent
**Skills:**
- `production_qa` â€” quality gate for skill docs
- `diagnostics_engine` â€” detect logic gaps, missing edge cases
- `reasoning_engine` â€” evaluate skill design quality
**Review checklist:**
  - [ ] YAML frontmatter complete and valid
  - [ ] All required files present (SKILL.md + README + schema.json)
  - [ ] Skill id matches directory name
  - [ ] No hardcoded secrets or keys
  - [ ] Dependencies resolve to existing skills
  - [ ] accessible_by lists valid agent roles
  - [ ] Exposed functions documented clearly
**Output:** Grade (A/B/C) + specific feedback â†’ skill-creator-agent

---

### plugin-librarian-agent
**Role:** Plugin catalog management and lifecycle tracking
**Responsibilities:**
- Maintain `shared-context/plugin-catalog.md` (all plugins with: status/version/owner/last-scan)
- Track plugin health: active / deprecated / awaiting-scan
- Coordinate with security_grc for GATE_SECURITY scan on each plugin
- Deactivate plugins that fail GATE_SECURITY or have no maintainer
- Report plugin inventory to registry-manager-agent
**At start of each catalog task, load:**
- SKILL: `knowledge_enricher` â€” catalog search and aggregation
- SKILL: `context_manager` â€” catalog maintenance
- `shared-context/plugin-catalog.md`
- `plugins/` directory listing
**Skills:**
- `knowledge_enricher` â€” plugin research, catalog query
- `context_manager` â€” multi-plugin context
**Plugin catalog entry format:**
```
| Plugin | Version | Status | Owner | Last Security Scan | Score |
```

---

### rule-builder-agent
**Role:** Create and maintain rules for agents, departments, and operational levels
**Responsibilities:**
- Draft new rule files when departments need them (using template from brain/corp/rules/)
- Update existing rules when policies change (C-Suite instruction)
- Ensure rules don't conflict with each other (check ceo_rules â†’ worker_rules chain)
- Maintain rules index: RULES_INDEX.md (what rule files exist and where)
**At start of each rule building task, load:**
- SKILL: `reasoning_engine` â€” rule logic design
- `corp/rules/ceo_rules.md` â€” top-level constraints (nothing lower can contradict)
- `corp/rules/worker_rules.md` â€” baseline worker constraints
- Brief from requesting dept or C-Suite (what behavior to encode)
**Skills:**
- `reasoning_engine` â€” rule logic, conflict detection
- `context_manager` â€” multi-rule consistency checking
**Rule template (every new rule file follows this):**
```markdown
# <DEPT/LEVEL> â€” Rules
# Version: 1.0 | Updated: <date>
# Authority: <who owns this rule set>
# Applies in addition to: <parent rules>

## RULES
RULE <PREFIX>-NN: <TITLE IN CAPS>
  <description. specific, testable, non-negotiable>
  Violation: <consequence>
```
**Never create rules that contradict ceo_rules.md**

