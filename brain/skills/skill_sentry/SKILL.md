---
name: skill_sentry
version: 1.0
tier: 2
category: security
description: SkillSentry 9-layer security scanner — mandatory before any new plugin/skill
exposed_functions:
  - scan
  - scan_message
  - quick_check
dependencies:
  - notification_bridge
---

# Skill Sentry

## Purpose
Port of the SkillSentry 9-layer security scanner into AI OS native skill.
MANDATORY before activating any new plugin or skill.

## Risk Score Thresholds
| Score | Verdict | Action |
|-------|---------|--------|
| 80-100 | SAFE | Proceed normally |
| 60-79 | LOW | Proceed with monitoring |
| 40-59 | MEDIUM | Warning logged |
| 20-39 | HIGH | Block + notify Antigravity |
| 0-19 | CRITICAL | Hard block + immediate user alert |

## Exposed Functions

### scan(target: str, target_type: str) → dict
```
target:      URL, file path, or directory path
target_type: "repo_url" | "local_dir" | "skill_file"

Runs all 9 layers, returns:
{
  "score": 85,
  "verdict": "SAFE",
  "layers": {
    "layer_1_behavior_chains": {"score": 100, "findings": []},
    "layer_2_evasion":         {"score": 90,  "findings": []},
    "layer_3_base64":          {"score": 100, "findings": []},
    "layer_4_prompt_injection":{"score": 100, "findings": []},
    "layer_5_risk_score":      {"score": 80,  "findings": []},
    "layer_6_alerts":          {"triggered": false},
    "layer_7_network":         {"score": 90,  "findings": []},
    "layer_8_dependencies":    {"score": 75,  "findings": []},
    "layer_9_compliance":      {"score": 80,  "findings": []}
  },
  "findings": [...],
  "recommendation": "ALLOW"
}
```

### scan_message(text: str, user_id: str) → dict
```
Fast scan for channel bridge messages (layers 2 + 4 only)
Returns: {"clean": bool, "reason": str}
```

### quick_check(text: str) → dict
```
Instant check for most common patterns (layers 2 + 4)
Used inline without full scan overhead
Returns: {"safe": bool, "flags": [str]}
```

## Critical Behavior Chains (Layer 1)
```python
DANGEROUS_CHAINS = {
    ("READ_SENSITIVE", "NETWORK_SEND"):     ("Data Exfiltration",     "CRITICAL", -90),
    ("NETWORK_SEND",   "FILE_DELETE"):      ("Upload & Cover Tracks",  "CRITICAL", -85),
    ("BASE64_EXEC",    "EXEC_DYNAMIC"):     ("Obfuscated Execution",   "CRITICAL", -85),
    ("READ", "NETWORK", "DELETE"):          ("Full Exfil Chain",       "CRITICAL", -100),
    ("INSTALL_PKG",    "EXEC_DYNAMIC"):     ("Supply Chain Attack",    "HIGH",     -50),
}
```

## Governance
- Score < 40: Auto-block + log to telemetry/security/
- Score < 20: Hard block + call notification_bridge → dashboard alert
- Cannot be disabled or bypassed by any agent or user command
- Applies to: plugins/, REMOTE/claws/, knowledge/repos/, channels/ messages
