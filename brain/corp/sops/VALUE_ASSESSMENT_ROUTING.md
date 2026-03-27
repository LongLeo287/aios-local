# VALUE ASSESSMENT & ROUTING MATRIX
# Version: 1.1 | Updated: 2026-03-17
# Owner: classifier-agent + ingest-router-agent (CIV Dept 20)
# Purpose: Determine WHAT content can BECOME, not just what it IS
#
# This is the intelligence layer between CIV classification and routing.
# Every piece of cleared content must be assessed for VALUE_TYPE before routing.

---

## WHY VALUE ASSESSMENT EXISTS

A PDF about LangGraph agents can become KNOWLEDGE.
A PDF with a step-by-step workflow spec can become a WORKFLOW file.
A GitHub repo can become a SKILL, PLUGIN, MCP_SERVER, or TOOL_SCRIPT.
A governance document can become a RULE.
A prompt template can become an AGENT_DEFINITION.

**classifier-agent assigns INPUT TYPE (what it IS)**
**content-validator-agent assigns VALUE_TYPE (what it CAN BECOME)**

These are different questions. Both must be answered before routing.

---

## VALUE_TYPE TAXONOMY â€” Full 9 Categories

| VALUE_TYPE | Definition | Signals | Owner Dept |
|------------|-----------|---------|------------|
| `KNOWLEDGE` | Reference information, research, articles, summaries | No actionable structure; informational | Asset & Knowledge Library |
| `SKILL` | Reusable LLM capability packaged per SKILL_SPEC | SKILL.md present, or clear skill pattern in repo | Registry & Capability |
| `PLUGIN` | External code/tool that integrates with AI OS | Has integration interface, CLI, or MCP protocol | Registry & Capability |
| `WORKFLOW` | Step-by-step process or SOP for agents or humans | Sequential steps, flowchart, protocol doc | Operations dept |
| `MCP_SERVER` | Model Context Protocol server implementation | Has MCP protocol, tool definitions, server.py/ts | IT Infra + Engineering |
| `TOOL_SCRIPT` | Runnable script automating a task (PS1, Python, Bash) | Executable script file, no LLM needed to run | IT Infra / Operations |
| `RULE_POLICY` | Governance rule, SOP, policy, or constraint definition | Defines MUST/SHOULD/NEVER behavior for agents | rule-builder-agent â†’ relevant dept |
| `AGENT_DEFINITION` | New agent spec or prompt template | Defines agent role, responsibilities, skills | OD&L â†’ dept-builder-agent |
| `DATA_ASSET` | Structured data, dataset, config file, template | JSON/CSV/YAML/XLSX â€” not code, not knowledge | Asset Library â†’ asset-tracker |

---

## VALUE_TYPE SIGNALS â€” HOW TO DETECT

### SKILL signals:
- README mentions "prompt engineering", "LLM workflow", "agent capability"
- Has structured tool functions with docstrings
- Contains instruction patterns reusable across contexts
- File structure: SKILL.md / schema.json / instructions

### PLUGIN signals:
- Has command-line interface or API endpoint
- Integrates with another system (VS Code extension, browser extension, etc.)
- Has `package.json`, `pyproject.toml`, or similar build artifact
- In existing plugins/ directory patterns

### WORKFLOW signals:
- Contains numbered steps, sequential process
- Has mermaid/ASCII flow diagram
- Uses terms: "steps", "stages", "process", "SOP", "procedure"
- Has trigger condition + action + outcome structure

### MCP_SERVER signals:
- References Model Context Protocol
- Has `server.py`, `index.ts`, or `mcp.json`  
- Defines `tools:` or `resources:` blocks per MCP spec
- Repository name contains: mcp, server, bridge, protocol

### TOOL_SCRIPT signals:
- `.ps1`, `.py`, `.sh`, `.bat` file as primary asset
- No LLM instructions, just automation code
- Solves a specific operational task (backup, scan, clean, monitor)

### RULE_POLICY signals:
- Uses MUST/SHOULD/NEVER/PROHIBITED/REQUIRED language  
- Defines constraints on agent behavior
- Has "Rule", "Policy", "Governance", "SOP" in title
- Authored by an authority figure (compliance, legal, CEO)

### AGENT_DEFINITION signals:
- Contains agent role, responsibilities, skills list
- Follows "You are..." prompt pattern
- Has "must load at boot" or "responsibilities" section
- Defines a new worker or manager role

### DATA_ASSET signals:
- Pure data payload (JSON, CSV, YAML, XLSX, SQLite)
- Config file for existing system
- Template (blank form, JSON schema, spreadsheet template)

---

## ROUTING MATRIX â€” WHERE EACH VALUE_TYPE GOES

| VALUE_TYPE | Primary Destination | Action Required | Agent Responsible |
|-----------|-------------------|-----------------|------------------|
| `KNOWLEDGE` | `knowledge/<domain>/` | Index in knowledge_index.md | knowledge-curator-agent (Asset Library) |
| `SKILL` | `skills/<skill_id>/` | Run skill_generator or wrap existing | skill-creator-agent (Registry) |
| `PLUGIN` | `plugins/<plugin_id>/` | Catalog, security scan | plugin-librarian-agent (Registry) |
| `WORKFLOW` | `workflows/<name>.md` | Format to workflow standard | archivist-agent (Operations) |
| `MCP_SERVER` | `mcp_servers/<name>/` | Integration test + catalog | sysadmin-agent (IT Infra) + Engineering |
| `TOOL_SCRIPT` | `scripts/<name>.ps1` | Validate, register in scripts catalog | sysadmin-agent (IT Infra) |
| `RULE_POLICY` | `corp/rules/` or `corp/departments/<dept>/rules.md` | rule-builder-agent drafts routing | rule-builder-agent (Registry) â†’ COO |
| `AGENT_DEFINITION` | `corp/departments/<dept>/rules.md` (new agent spec) | dept-builder-agent builds full package | OD&L â†’ dept-builder-agent |
| `DATA_ASSET` | `assets/data/<name>` | Catalog + metadata | asset-tracker-agent (Asset Library) |

---

## CONFLICT RESOLUTION â€” TRAIN, DON'T OVERWRITE

> CORE PRINCIPLE: If a resource already exists at the destination, NEVER overwrite it.
> SELECT what is new/better. UPGRADE via training-agent. Preserve what works.

### Rule: CHECK BEFORE ROUTE

ingest-router-agent MUST check if destination already has a resource before routing.

Decision tree:
```
Does destination already have this resource?
    NO  â†’ CREATE NEW (normal routing)
    YES â†’ CONFLICT RESOLUTION FLOW:
              1. COMPARE versions (new vs existing)
              2. ASSESS delta: what is genuinely new/better?
              3. If new has improvements â†’ UPGRADE (TYPE 2 Enrichment via training-agent)
              4. If existing is already better â†’ DISCARD new, log reason
              5. If both have unique value â†’ MERGE selectively
              NEVER replace the full file without explicit CEO/COO approval
```

### CONFLICT RESOLUTION BY VALUE_TYPE

| VALUE_TYPE | Existing resource | Resolution |
|-----------|-----------------|------------|
| `SKILL` | Skill already in SKILL_REGISTRY | Compare capability scope â†’ upgrade if new skill covers more cases or adds new tools â†’ training-agent patches agent rules.md, does NOT replace SKILL.md |
| `KNOWLEDGE` | knowledge/ file already exists | Append new sections or update stale facts â†’ knowledge-curator merges delta, marks source |
| `WORKFLOW` | workflow file already exists | Compare steps â€” if new has clearer steps or new edge cases â†’ archivist-agent appends as revision note or replaces specific section, not entire file |
| `PLUGIN` | plugin already cataloged | Check version number â€” upgrade only if new version > existing and changelog confirms improvement |
| `MCP_SERVER` | MCP server already running | Do NOT replace â€” alert sysadmin for review. New version = staging test first, then swap |
| `TOOL_SCRIPT` | script already in scripts/ | Compare logic â€” if genuinely better: rename old as `<name>.v1.bak`, deploy new |
| `RULE_POLICY` | rule already exists in brain/corp/rules/ | NEVER auto-overwrite. rule-builder-agent flags conflict â†’ COO decision only |
| `AGENT_DEFINITION` | agent already exists in dept rules.md | Training, not replacement. Add new skill/capability to existing agent. Rewrite ONLY if role fundamentally changed + C-Suite approved |
| `DATA_ASSET` | dataset already in assets/ | Version new file as `<name>_v2.json`. Never delete old until confirmed superseded |

### What ingest-router-agent MUST output when conflict detected:
```
CONFLICT DETECTED â€” CIV-[ID]
New content: [name]
Existing at: [path]
Delta assessment: [what is new / what is same]
Recommended action: UPGRADE / DISCARD / MERGE
Routed to: training-agent (OD&L) for enrichment execution
Auto-overwrite: BLOCKED
```

### What training-agent does with a conflict:
1. Read existing resource
2. Read new content from CIV
3. DIFF: identify what new content adds that existing lacks
4. SELECT only the genuinely new/better parts
5. Apply enrichment per ENRICHMENT_SOP.md (TYPE 1/2/3/4 as appropriate)
6. Write ENRICHMENT RECEIPT documenting what changed and why
7. Archive new content in QUARANTINE/vetted/ as reference (do not route to destination)

---

## MULTI-VALUE CONTENT

Content can have MULTIPLE VALUE_TYPEs. A repo can be simultaneously:
- `SKILL` (has reusable LLM capability)
- `PLUGIN` (has CLI interface)
- `KNOWLEDGE` (has excellent README)

**Handling:**
1. content-validator-agent assigns ALL applicable VALUE_TYPEs (comma-separated)
2. ingest-router-agent routes to ALL destinations
3. Primary VALUE_TYPE determines ticket metadata label
4. Each destination agent receives a CIV delivery receipt

**Example:**
```
CIV-2026-03-17-042
VALUE_TYPES: SKILL, KNOWLEDGE
Primary: SKILL
Destinations:
  â†’ ecosystem/skills/new_skill/ (skill-creator-agent)
  â†’ knowledge/ai_techniques/ (knowledge-curator-agent)
```

---

## UPDATE: content-validator-agent ADDITION

content-validator-agent now ALSO performs VALUE_TYPE assessment:

Old responsibility:
  - Check quality (1-10 score)
  - Check for spam/malicious content

New responsibility (added):
  - Assess VALUE_TYPE using signal checklist above
  - Write VALUE_TYPE tags to CIV ticket
  - Flag MULTI-VALUE content for dual-routing

Updated output to ingest-router-agent includes:
```
VALIDATION RESULT
Quality score: 8/10
Safety: PASS
VALUE_TYPE: WORKFLOW, KNOWLEDGE
Primary value: WORKFLOW
Priority destinations: [workflows/, knowledge/]
Rationale: Contains step-by-step agent protocol with flowchart
```

---

## UPDATE: ingest-router-agent ADDITION

ingest-router-agent replaces simple classification table with VALUE_TYPE routing:

Decision logic (in order):
1. Read VALUE_TYPE from content-validator output
2. For each VALUE_TYPE, look up destination in ROUTING MATRIX
3. **CHECK FIRST: Does resource already exist at destination?**
   - NO â†’ proceed with normal routing (CREATE)
   - YES â†’ enter CONFLICT RESOLUTION FLOW (see section above)
   - NEVER route without this check
4. On CREATE: move to destination, write delivery receipt
5. On CONFLICT: write CONFLICT DETECTED output â†’ route to training-agent, not destination
6. Update ticket to INGESTED (CREATE) or ENRICHMENT_PENDING (CONFLICT)
7. All destinations confirmed before ticket close

If VALUE_TYPE = UNKNOWN:
  â†’ Hold content in QUARANTINE/vetted/ 
  â†’ Alert intake-chief-agent for manual VALUE_TYPE assessment
  â†’ SLA: must be resolved within 2 corp cycles

---

## EXAMPLES â€” Real Content Through the Pipeline

### Example 1: GitHub repo "LangGraph-agent-patterns"
```
INPUT TYPE: REPO
vet_repo.ps1: PASS (score 92)
VALUE_TYPE assessment:
  âœ“ KNOWLEDGE (excellent research README)
  âœ“ SKILL (reusable agent patterns in Python)
  âœ— PLUGIN (no CLI interface)
  âœ— MCP_SERVER (no MCP protocol)
ROUTE TO:
  â†’ skills/ (skill-creator-agent wraps patterns)
  â†’ knowledge/ai_frameworks/ (knowledge-curator indexes)
```

### Example 2: document "Company AI Governance Policy 2026.pdf"
```
INPUT TYPE: DOCUMENT
content-validator: PASS (score 9)
VALUE_TYPE assessment:
  âœ— KNOWLEDGE (partial â€” too policy-specific)
  âœ— SKILL
  âœ“ RULE_POLICY (defines MUST/PROHIBITED behaviors for AI systems)
ROUTE TO:
  â†’ rule-builder-agent reviews for conflict
  â†’ draft to brain/corp/rules/ai_governance_external.md
  â†’ COO notified for approval
```

### Example 3: web article "How to build an MCP server in TypeScript"
```
INPUT TYPE: WEB_CONTENT
content-validator: PASS (score 7)
VALUE_TYPE assessment:
  âœ“ KNOWLEDGE (technical reference)
  âœ“ WORKFLOW (contains step-by-step tutorial)
  âœ— MCP_SERVER (article about MCP, not an MCP impl)
ROUTE TO:
  â†’ knowledge/mcp_development/ (knowledge-curator)
  â†’ workflows/mcp-server-build-guide.md (archivist-agent)
```

### Example 4: PS1 script "monitor-agent-performance.ps1"
```
INPUT TYPE: PLUGIN (code file)
vet_repo.ps1: PASS (35KB script)
VALUE_TYPE assessment:
  âœ— SKILL
  âœ— PLUGIN (no integration interface)
  âœ“ TOOL_SCRIPT (standalone automation script)
ROUTE TO:
  â†’ scripts/monitor-agent-performance.ps1 (sysadmin-agent catalogs)
  â†’ scripts catalog updated
```

