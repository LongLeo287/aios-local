const fs = require('fs');
const path = require('path');

const rootDir = 'd:\\AI OS CORP\\AI OS';
const agentsDir = path.join(rootDir, '.openclaw', 'agents');
const openclawDir = path.join(rootDir, '.openclaw');

if (fs.existsSync(agentsDir)) {
  const agents = fs.readdirSync(agentsDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  let movedCount = 0;
  agents.forEach(agentId => {
    if (agentId === 'main') return;
    
    const wrongWorkspaceDir = path.join(agentsDir, agentId, 'workspace');
    const correctWorkspaceDir = path.join(openclawDir, `workspace-${agentId}`);
    
    // If we mistakenly created it in agents/[id]/workspace, move it
    if (fs.existsSync(wrongWorkspaceDir)) {
      // Copy over recursively
      fs.cpSync(wrongWorkspaceDir, correctWorkspaceDir, { recursive: true });
      // Remove old
      fs.rmSync(path.join(agentsDir, agentId), { recursive: true, force: true });
      movedCount++;
    }
  });

  console.log(`Moved ${movedCount} agent workspaces to correct root format (workspace-[id])`);
} else {
  console.log('No agents directory found, nothing to fix.');
}
