const fs = require('fs');
const path = require('path');

const root = 'd:\\AI OS CORP\\AI OS';
const workspaceSkills = path.join(root, '.openclaw\\workspace\\skills');
const allSkillsFile = path.join(root, 'all_skills.txt');

// Read all_skills.txt with UTF-16LE encoding (PowerShell default)
const content = fs.readFileSync(allSkillsFile, 'utf16le');
const allSkillPaths = content.split('\n').map(p => p.trim()).filter(p => p.endsWith('SKILL.md'));

const missingSkills = [
  "agent-browser-clawdbot", "agents.me", "browser", "channel_manager", "claude-code",
  "cognitive_reflector", "context_manager", "cosmic_memory", "cybersecurity",
  "edge_compute_patterns", "firecrawl-cli", "insight_engine", "mem0_plugin",
  "notification_bridge", "openclaw-github-assistant", "reasoning_engine",
  "security_scanning_reference", "security_shield", "seo-aeo-optimization",
  "skill_sentry", "supabase_agent_skills", "supabase_postgres_best_practices",
  "system-resource-monitor", "web_intelligence"
];

const manualMap = {
  'firecrawl-cli': 'firecrawl-automation',
  'mem0_plugin': 'mem0-automation',
  'claude-code': 'claude-code-expert',
  'agent-browser-clawdbot': 'agent-browser',
  'openclaw-github-assistant': 'github-issues'
};

let copied = 0;

for (const skill of missingSkills) {
  const destDir = path.join(workspaceSkills, skill);
  const destPath = path.join(destDir, 'SKILL.md');
  
  // Try to find exact match in brain/skills
  let matchedPath = allSkillPaths.find(p => p.toLowerCase().includes(`brain\\skills\\${skill.toLowerCase()}\\skill.md`));
  
  // Try to find manual mapped match
  if (!matchedPath && manualMap[skill]) {
    matchedPath = allSkillPaths.find(p => p.toLowerCase().includes(`\\${manualMap[skill].toLowerCase()}\\skill.md`));
  }
  
  // Try to find sub-match across plugins
  if (!matchedPath) {
    matchedPath = allSkillPaths.find(p => p.toLowerCase().includes(`\\${skill.toLowerCase()}\\skill.md`));
  }
  
  // Flexible match ignoring dashes/underscores
  if (!matchedPath) {
    const flexSkill = skill.replace(/[-_]/g, '');
    matchedPath = allSkillPaths.find(p => {
      const parts = p.split('\\');
      if (parts.length < 2) return false;
      const folder = parts[parts.length - 2].replace(/[-_]/g, '').toLowerCase();
      return folder.includes(flexSkill.toLowerCase());
    });
  }
  
  if (matchedPath && fs.existsSync(matchedPath)) {
    // Overwrite the placeholder
    if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, {recursive: true});
    fs.copyFileSync(matchedPath, destPath);
    console.log(`[OK] Mapped 1:1 -> ${skill} from ${matchedPath}`);
    copied++;
  } else {
    console.log(`[WARN] Not found authentic source for: ${skill}`);
  }
}

console.log(`\nSuccessfully restored authentic SKILL.md for ${copied}/${missingSkills.length} skills.`);
