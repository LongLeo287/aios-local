const fs = require('fs');
const path = require('path');

const rootDir = 'd:\\AI OS CORP\\AI OS';
const activationFile = path.join(rootDir, 'brain', 'agents', 'activation_status.json');
const openClawJsonPath = path.join(rootDir, '.openclaw', 'openclaw.json');
const agentsDir = path.join(rootDir, '.openclaw', 'agents');
const defaultWorkspace = path.join(rootDir, '.openclaw', 'workspace');

// Read existing agents
const activationData = JSON.parse(fs.readFileSync(activationFile, 'utf8'));
const allAgents = [];

['c_suite', 'tier1_core', 'tier2_operational', 'tier3_specialized'].forEach(tier => {
  for (const [id, data] of Object.entries(activationData[tier])) {
    allAgents.push({ 
      id, 
      name: `${id} (${data.status})`, 
      description: data.notes,
      tier: tier
    });
  }
});

// Update openclaw.json
const openClawData = JSON.parse(fs.readFileSync(openClawJsonPath, 'utf8'));
openClawData.agents.list = [{ id: 'main', name: 'Giám sát cục bộ (Supervisor)' }, ...allAgents.map(a => ({ id: a.id, name: `${a.id} - ${a.description} (${a.tier})` }))];
fs.writeFileSync(openClawJsonPath, JSON.stringify(openClawData, null, 2));

// Create workspace folders and copy files
allAgents.forEach(agent => {
  const workspacePath = path.join(agentsDir, agent.id, 'workspace');
  if (!fs.existsSync(workspacePath)) {
    fs.mkdirSync(workspacePath, { recursive: true });
  }
  
  // Copy default .md files with customized contents
  const mdFiles = fs.readdirSync(defaultWorkspace).filter(f => f.endsWith('.md'));
  mdFiles.forEach(file => {
    const src = path.join(defaultWorkspace, file);
    const dest = path.join(workspacePath, file);
    
    let content = fs.readFileSync(src, 'utf8');
    
    // Tailor the IDENTITY.md
    if (file === 'IDENTITY.md') {
        content = `# IDENTITY.md - Who Am I?\n\n- **Name:** ${agent.id}\n- **Creature:** AI OS Corp Agent - Tier: ${agent.tier}\n- **Role:** ${agent.description}\n- **Vibe:** Highly specialized component of the AI OS ecosystem.\n\nThis agent is part of the formal AI OS Agent hierarchy.\n`;
    }
    
    // Tailor the TOOLS.md
    if (file === 'TOOLS.md') {
        content = `# TOOLS.md\n\nThis customized workspace grants the ${agent.id} agent specific tool permissions appropriate for: ${agent.description}. It overrides the default system tools to maintain bounded authority.`;
    }
    
    // Tailor the AGENTS.md
    if (file === 'AGENTS.md') {
        content = `# AGENTS.md\n\nAs the ${agent.id}, you cooperate with other agents in ${agent.tier}. \nYour scope of operation is tailored towards ${agent.description}.`;
    }
    
    fs.writeFileSync(dest, content);
  });
});

console.log(`Successfully synced ${allAgents.length} agents to OpenClaw workspaces!`);
