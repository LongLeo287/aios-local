const fs = require('fs');
const path = require('path');

const configPath = 'd:\\AI OS CORP\\AI OS\\.openclaw\\openclaw.json';
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

let fixedCount = 0;
config.agents.list = config.agents.list.map(agent => {
  if (agent.id === 'main') return agent;

  // If tools is an array of strings, it's the old invalid format
  if (Array.isArray(agent.tools)) {
    agent.tools = {
      allow: agent.tools // Explicitly allow ONLY these tools
    };
    fixedCount++;
  }
  return agent;
});

if (fixedCount > 0) {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`[OK] Converted tool arrays to strict AgentToolsConfig objects for ${fixedCount} agents.`);
} else {
  console.log('No agents needed tool schema fixing.');
}
