const fs = require('fs');
const path = require('path');

const rootDir = 'd:\\AI OS CORP\\AI OS';
const agentsDir = path.join(rootDir, '.openclaw', 'agents');
const brainAgentsDir = path.join(rootDir, 'brain', 'agents');
const openClawJsonPath = path.join(rootDir, '.openclaw', 'openclaw.json');

// Exact mappings from brain/shared-context/AGENTS.md Skills Assignment Matrix
const skillMatrix = {
  'antigravity': ['context_manager', 'reasoning_engine', 'smart_memory', 'cosmic_memory', 'cognitive_reflector', 'cognitive_evolver', 'proposal_engine', 'llm_router', 'skill_generator'],
  'claude_code': ['shell_assistant', 'reasoning_engine', 'context_manager', 'resilience_engine', 'production_qa', 'diagnostics_engine', 'tools_hub', 'repo_analyst'],
  'orchestrator_pro': ['orchestrator_pro', 'context_manager', 'reasoning_engine', 'notification_bridge', 'project_intake_agent', 'hitl_gateway_enforcer'],
  'frontend-agent': ['shadcn_ui_reference', 'tailwindcss_reference', 'antd_reference', 'fsd_architectural_linter', 'accessibility_grounding', 'visual_excellence'],
  'backend-architect-agent': ['supabase_agent_skills', 'supabase_postgres_best_practices', 'edge_compute_patterns', 'reasoning_engine'],
  'ai-ml-agent': ['llm_router', 'neural_memory', 'insight_engine', 'cost_manager_skill'],
  'sre-agent': ['performance_profiler', 'diagnostics_engine', 'notification_bridge', 'edge_compute_patterns'],
  'mobile-agent': ['Android_APK_Modification', 'reasoning_engine', 'shell_assistant'],
  'ui-ux-agent': ['ui-ux-pro-max', 'visual_excellence', 'accessibility_grounding'],
  'devops-agent': ['edge_compute_patterns', 'shell_assistant', 'resilience_engine'],
  'data-agent': ['insight_engine', 'neural_memory', 'sheets_skill', 'sheets_performance_optimization'],
  'content-agent': ['seo-aeo-optimization', 'web_intelligence', 'channel_manager', 'multi-source-aggregation', 'video-extraction'],
  'web_researcher': ['web_intelligence', 'mem0_plugin', 'firecrawl-cli', 'context_manager'],
  'web-agent': ['gas_skill', 'sheets_skill', 'pos_event_sourcing_auditor', 'shell_assistant', 'reasoning_engine'],
  'security-engineer-agent': ['security_shield', 'cybersecurity', 'security_scanning_reference', 'skill_sentry'],
  'strix-agent': ['security_shield', 'cybersecurity', 'security_scanning_reference', 'skill_sentry'],
  'knowledge-agent': ['knowledge_navigator', 'knowledge_enricher', 'neural_memory', 'smart_memory'],
  'archivist': ['archivist', 'knowledge_enricher', 'context_manager'],
  'cognitive_reflector': ['cognitive_reflector', 'insight_engine', 'cosmic_memory'],
  'channel-agent': ['channel_manager', 'notification_bridge'],
  'growth-agent': ['seo-aeo-optimization', 'web_intelligence', 'channel_manager', 'insight_engine'],
  'crm-agent': ['insight_engine', 'reasoning_engine', 'notification_bridge'],
  'finance-agent': ['insight_engine', 'reasoning_engine', 'sheets_skill'],
  'legal-agent': ['reasoning_engine', 'security_scanning_reference'],
  'hr-agent': ['reasoning_engine', 'project_intake_agent'],
  'prompt-engineer-agent': ['reasoning_engine', 'insight_engine']
};

const agents = fs.readdirSync(agentsDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

// 1. Sync IDENTITY.md from brain/agents/*.md exactly 1:1
agents.forEach(agentId => {
  if (agentId === 'main') return;

  const sourceFile = path.join(brainAgentsDir, `${agentId}.md`);
  const workspaceDir = path.join(agentsDir, agentId, 'workspace');
  const targetFile = path.join(workspaceDir, 'IDENTITY.md');
  const agentsMdTarget = path.join(workspaceDir, 'AGENTS.md');
  const toolsMdTarget = path.join(workspaceDir, 'TOOLS.md');

  if (fs.existsSync(sourceFile)) {
    const content = fs.readFileSync(sourceFile, 'utf8');
    fs.writeFileSync(targetFile, content); // Perfect 1:1 sync
    
    const toolsRegex = /## Tools Available\n([\s\S]*?)(?=\n##|$)/;
    const toolsMatch = content.match(toolsRegex);
    if (toolsMatch) {
       fs.writeFileSync(toolsMdTarget, `# Tools Specifically Delegated to ${agentId}\n\n${toolsMatch[1]}\n\n(Extracted directly from original AI OS agent specs)`);
    } else {
       fs.writeFileSync(toolsMdTarget, `# TOOLS FOR ${agentId}\n\nRefer to IDENTITY.md for tool availability. Ensure to query the SKILL_REGISTRY.json before engaging unrecognized commands.`);
    }

    fs.writeFileSync(agentsMdTarget, `# HIERARCHY FOR ${agentId}\n\nRefer to \`brain/shared-context/AGENTS.md\` for exact reporting lines and escalation matrices. See IDENTITY.md to check if you are a Dept Head.`);
    console.log(`[OK] Copied exact AI OS Profile to ${agentId}`);
  }
});

// 2. Map skills in openclaw.json EXACTLY based on the AGENTS matrix
const config = JSON.parse(fs.readFileSync(openClawJsonPath, 'utf8'));

config.agents.list = config.agents.list.map(agent => {
  if (agent.id === 'main') return agent;
  
  if (skillMatrix[agent.id]) {
    // Preserve existing array and inject new exact skills
    agent.skills = [...new Set([...(agent.skills || []), ...skillMatrix[agent.id]])];
  }
  return agent;
});

fs.writeFileSync(openClawJsonPath, JSON.stringify(config, null, 2));
console.log(`[OK] Force-fed pure AI OS Skill Matrix into OpenClaw config.`);
