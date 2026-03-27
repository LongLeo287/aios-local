const fs = require('fs');
const path = require('path');

const configPath = 'd:\\AI OS CORP\\AI OS\\.openclaw\\openclaw.json';
const configData = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// The exact absolute path to the main shared workspace where all our 87 skills live
const sharedWorkspace = "d:\\AI OS CORP\\AI OS\\.openclaw\\workspace";

let updatedCount = 0;

if (configData.agents && Array.isArray(configData.agents.list)) {
  configData.agents.list.forEach(agent => {
    // Inject the shared workspace path globally for every agent 
    // to bypass the OpenClaw default "workspace-${id}" isolation logic
    if (agent.workspace !== sharedWorkspace) {
      agent.workspace = sharedWorkspace;
      updatedCount++;
    }
  });
}

// Write back maintaining formatting
fs.writeFileSync(configPath, JSON.stringify(configData, null, 2));
console.log(`\nSuccessfully linked shared Master Workspace for ${updatedCount} micro-agents.`);
