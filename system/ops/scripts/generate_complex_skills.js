const fs = require('fs');
const path = require('path');

const workspaceSkills = 'd:\\AI OS CORP\\AI OS\\.openclaw\\workspace\\skills';

const skillsToGenerate = {
  "agents.me": {
    "name": "agents-me",
    "description": "This skill should be used when the user asks to manage focus state, control background ambient noise, or interact with the Agents.me focus API to optimize the workstation environment for prolonged deep work."
  },
  "edge_compute_patterns": {
    "name": "edge-compute-patterns",
    "description": "This skill should be used when the user asks to evaluate, design, or scaffold Edge computing infrastructure such as Cloudflare Workers, Vercel Edge Functions, or Supabase Edge. It provides architectural patterns and constraints for Edge-first capabilities."
  },
  "security_scanning_reference": {
    "name": "security-scanning-reference",
    "description": "This skill should be used when the user asks to consult security scanning standards (SAST/DAST), trigger a code vulnerability audit, or verify codebase compliance against OWASP top 10 within the CI/CD pipeline."
  },
  "system-resource-monitor": {
    "name": "system-resource-monitor",
    "description": "This skill should be used when the user asks to monitor local host metrics, diagnose CPU/RAM spikes, or verify that the active AI OS containers are operating within configured resource limits."
  }
};

const templates = {
  "agents.me": `## Purpose
Interact with the Agents.me workspace API to control ambient sound, focus states, and neuro-stimulation tracking.

## When to Use This Skill
- When initializing a deep work session requiring focus optimization.
- To toggle ambient audio parameters based on cognitive load.

## Core Capabilities
1. **Focus State Tracking**: Logging Pomodoro or uninterrupted work blocks.
2. **Audio Sync**: Interfacing with the ambient sound generator.

## Main Workflow
1. Check current audio/focus status via \`GET /api/v1/workspace/status\`.
2. Determine cognitive load based on the user's task pipeline.
3. Apply optimal ambient profile.

## Known Pitfalls
- Do not interrupt the user with audio state changes during typing bursts.`,

  "edge_compute_patterns": `## Purpose
Provide architectural review and scaffolding for Edge-based deployments.

## When to Use This Skill
- Scaffolding new Supabase Edge Functions.
- Refactoring Node.js heavy routes into Cloudflare Workers / Vercel Edge.

## Core Capabilities
1. **V8 Isolate Compliance Checking**: Ensure code does not use unsupported Node.js modules (e.g. \`fs\`, \`child_process\`).
2. **Latency Optimization**: Recommend geo-distributed caching strategies.

## Main Workflow
1. Analyze the input route or function.
2. Flag any Node-specific dependencies.
3. Suggest isomorphic or Web-API compliant alternatives.

## Known Pitfalls
- Forgetting that Edge environments have strict execution time limits (e.g. 10ms CPU time on CF Workers free tier).
- Relying on persistent state across requests.`,

  "security_scanning_reference": `## Purpose
Consult and enforce DAST/SAST vulnerability checking.

## When to Use This Skill
- During the \`[Verifying]\` or \`[Execution]\` phases when pushing new backend logic.
- When evaluating a 3rd party package for dependency vulnerabilities.

## Core Capabilities
1. **Dependency Analysis**: Cross-reference packages against NIST/CVE databases.
2. **Static Code Review**: Check for SQLi, XSS, and hardcoded secrets.

## Main Workflow
1. Parse the target codebase.
2. Apply regex and semantic scanning for known anti-patterns.
3. Generate a security manifest block.

## Known Pitfalls
- False positives on test files containing hardcoded mock tokens.`,

  "system-resource-monitor": `## Purpose
Diagnostic monitoring of CPU, memory, and disk I/O on the host machine.

## When to Use This Skill
- The Supervisor detects lag or timeout errors from Docker or Local endpoints.
- Optimizing memory footprint of heavy LLM context windows.

## Core Capabilities
1. **System Triage**: Read cross-platform metrics (via WMI/PowerShell on Windows, \`top\` on Unix).
2. **Process Tree Mapping**: Identify the exact PID causing resource starvation.

## Main Workflow
1. Invoke the host shell to retrieve top consuming processes.
2. Map PIDs to AI OS modules (e.g., LightRAG, Postgres, OpenClaw Agent).
3. Recommend cleanup or restart actions.

## Known Pitfalls
- Over-polling the system can cause observational overhead.`
};

for (const [skillId, meta] of Object.entries(skillsToGenerate)) {
  const destDir = path.join(workspaceSkills, skillId);
  const destPath = path.join(destDir, 'SKILL.md');
  
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, {recursive: true});
  
  const content = `---
name: ${meta.name}
description: "${meta.description}"
tier: 2
category: system
---

# ${meta.name.toUpperCase().replace(/-/g, ' ')}

${templates[skillId]}

---
*Generated via Skill Creator Ultra workflow format*
`;

  fs.writeFileSync(destPath, content);
  console.log(`[OK] Generated Anthropic-compliant Skill for ${skillId}`);
}
