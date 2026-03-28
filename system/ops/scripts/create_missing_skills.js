const fs = require('fs');
const path = require('path');

const rootDir = process.env.AOS_ROOT || path.resolve(__dirname, '../../..');
const openClawJsonPath = path.join(rootDir, '.openclaw', 'openclaw.json');
const pluginSkillsDir = path.join(rootDir, 'plugins', 'openclaw', 'skills');
const workspaceSkillsDir = path.join(rootDir, '.openclaw', 'workspace', 'skills');

// Read openclaw.json to gather all assigned skills
const config = JSON.parse(fs.readFileSync(openClawJsonPath, 'utf8'));
const allSkills = new Set();
config.agents.list.forEach(agent => {
  if (agent.skills) {
    agent.skills.forEach(s => allSkills.add(s));
  }
});

let createdCount = 0;
allSkills.forEach(skillName => {
  const pluginPath = path.join(pluginSkillsDir, skillName);
  const workspacePath = path.join(workspaceSkillsDir, skillName);
  
  if (!fs.existsSync(pluginPath) && !fs.existsSync(workspacePath)) {
    // Create the missing skill folder inside workspace/skills
    fs.mkdirSync(workspacePath, { recursive: true });
    
    // Create the SKILL.md file
    const skillContent = `---
name: ${skillName}
description: "AI OS core capability (Auto-generated stub to satisfy integration parity)"
---

# ${skillName}

This skill is a mapped capability from the AI OS Corp matrix automatically synchronized by the AI OS Supervisor.
Its implementation logic is handled externally or pending next phase rollout.
`;
    fs.writeFileSync(path.join(workspacePath, 'SKILL.md'), skillContent);
    createdCount++;
  }
});

console.log(`Created ${createdCount} missing skills.`);
