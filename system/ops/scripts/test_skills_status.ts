import { buildWorkspaceSkillStatus } from "./plugins/openclaw/src/agents/skills-status.js";
import { loadConfig } from "./plugins/openclaw/src/config/config.js";

const cfg = loadConfig();
const workspaceDir = cfg.agents?.[0]?.workspace || "d:\\AI OS CORP\\AI OS\\.openclaw\\workspace";

console.log("Testing with workspaceDir:", workspaceDir);
const report = buildWorkspaceSkillStatus(workspaceDir, { config: cfg });

const targetSkills = [
  "aios-memory",
  "aios-corp-flows",
  "aios-subagents",
  "aios-workflows",
  "agents.me",
  "context_manager",
  "reasoning_engine",
  "skill_sentry",
  "cognitive_reflector",
  "insight_engine",
  "channel_manager"
];

for (const skill of report.skills) {
  if (targetSkills.includes(skill.name) || targetSkills.includes(skill.skillKey)) {
    console.log(`Found: name="${skill.name}", skillKey="${skill.skillKey}", source="${skill.source}"`);
  }
}
