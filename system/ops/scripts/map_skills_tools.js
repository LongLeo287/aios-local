const fs = require('fs');
const path = require('path');

const configPath = 'd:\\AI OS CORP\\AI OS\\.openclaw\\openclaw.json';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

config.agents.list = config.agents.list.map(agent => {
  if (agent.id === 'main') {
    // Supervisor gets full access manually managed via UI or explicitly defined here.
    return agent;
  }

  // Base capabilities for ALL AI OS Agents
  let tools = ['read', 'write', 'process', 'memory_search', 'memory_get', 'sessions_send'];
  let skills = ['aios-memory', 'aios-corp-flows'];

  // Add specialization tools based on role/semantic keywords
  const idStr = agent.id.toLowerCase();
  const isCSuiteOrManager = idStr.includes('ceo') || idStr.includes('coo') || idStr.includes('cfo') || idStr.includes('manager') || idStr.includes('chief') || idStr.includes('pmo');

  if (idStr.includes('architect') || idStr.includes('devops') || idStr.includes('engineer') || idStr.includes('it-')) {
    // Engineering focus
    tools.push('edit', 'apply_patch', 'cmd');
    skills.push('claude-code', 'aios-docs');
  } 
  
  if (idStr.includes('security') || idStr.includes('strix') || idStr.includes('monitor')) {
    // Security focus
    tools.push('web_search', 'cmd');
    skills.push('agent-shield');
  } 
  
  if (idStr.includes('research') || idStr.includes('web') || idStr.includes('content') || idStr.includes('growth')) {
    // Info Gather focus
    tools.push('web_search', 'web_fetch', 'browser');
    skills.push('browser');
  }

  if (isCSuiteOrManager) {
    // Management focus
    tools.push('sessions_list', 'sessions_spawn', 'sessions_history', 'subagents');
    skills.push('aios-subagents', 'aios-workflows', 'agents.me');
  }

  // Deduplicate using Set
  agent.tools = [...new Set(tools)];
  agent.skills = [...new Set(skills)];

  return agent;
});

fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log('Mapped custom Skills & Tools for all agents.');
