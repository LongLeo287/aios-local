const fs = require('fs');
const path = require('path');

const configPath = path.join(process.env.AOS_ROOT || path.resolve(__dirname, '../../..'), '.openclaw', 'openclaw.json');
const configData = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// The Cognitive Pack: Universal power-ups that don't violate specialty
const cognitivePack = [
  "context_manager",
  "reasoning_engine",
  "skill_sentry",
  "cognitive_reflector",
  "insight_engine",
  "channel_manager"
];

let updatedCount = 0;

if (configData.agents && Array.isArray(configData.agents.list)) {
  configData.agents.list.forEach(agent => {
    // Only augment agents that already have a localized skills restrictor (allowlist)
    if (Array.isArray(agent.skills)) {
      const originalLength = agent.skills.length;
      
      cognitivePack.forEach(skill => {
        if (!agent.skills.includes(skill)) {
          agent.skills.push(skill);
        }
      });
      
      if (agent.skills.length > originalLength) {
        updatedCount++;
        console.log(`[OK] Augmented Agent: ${agent.id} (Total Skills: ${agent.skills.length})`);
      }
    }
  });
}

// Write back maintaining formatting
fs.writeFileSync(configPath, JSON.stringify(configData, null, 2));
console.log(`\nSuccessfully injected Cognitive Power-Ups for ${updatedCount} micro-agents.`);
