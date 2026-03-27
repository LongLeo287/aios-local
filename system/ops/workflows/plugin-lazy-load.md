# plugin-lazy-load.md — Tier 2 Plugin Lazy Load Workflow
# Version: 1.0 | Created: 2026-03-27 | Authority: Tier 1 (Registry-Manager-Agent)

---

## PURPOSE

Workflow này định nghĩa cách kích hoạt (lazy-load) các plugin Tier 2 trong AI OS theo đúng kiến trúc 3-Tier:

- **Tier 1** (LightRAG, Firecrawl, Mem0, CrewAI): Luôn load — không cần workflow này
- **Tier 2** (specialized plugins): **CHỈ** kích hoạt khi task thực sự cần — đây là workflow đó
- **Tier 3** (blacklisted): Không bao giờ dùng

---

## TRIGGER CONDITIONS

Kích hoạt workflow này khi:
- Agent cần tool không thuộc Tier 1
- Task type = IMAGE | EXCEL | PDF-RENDER | OCR | AUDIO | VIDEO-EDIT
- CEO request plugin cụ thể không đang chạy

---

## EXECUTION STEPS

### Step 1: Identify Required Plugin
```
- Đọc task type từ blackboard.json hoặc event_bus task payload
- Map task type → plugin ID từ SKILL_REGISTRY.json (filter tier=2)
- Confirm plugin is NOT in Tier 3 blacklist
```

### Step 2: Sandbox Init
```
# Start plugin in isolated process
python system/ops/scripts/plugin_sandbox.py start --plugin <plugin_id>

# Check: plugin started successfully?
IF success → proceed to Step 3
IF fail → escalate to CEO + use Tier 1 fallback if available
```

### Step 3: Execute Task
```
# Call plugin via adapter
from ecosystem.plugins.<plugin_id>.<adapter> import get_plugin
plugin = get_plugin()
result = plugin.run(task_payload)

# Store result in telemetry/receipts/
```

### Step 4: Teardown
```
# Always teardown after use (NEVER leave Tier 2 running idle)
python system/ops/scripts/plugin_sandbox.py stop --plugin <plugin_id>

# Log: "Plugin <id> teardown complete"
# Update STATUS.json: plugin_active = false
```

---

## PLUGIN MAP (Tier 2 Examples)

| Task Type | Plugin | Adapter |
|-----------|--------|---------|
| Image generation | minimax-mcp | minimax_adapter |
| Video editing | tai-video | tai_video_adapter |
| Web scraping (complex) | scrapling-mcp | scrapling_adapter |
| PDF extraction | notebooklm | notebooklm_adapter |

---

## ON FAILURE
- Log error to telemetry/receipts/errors/
- Never crash parent process — plugin runs in subprocess
- Fallback: Use Tier 1 equivalent (e.g., Firecrawl for web)
- Escalate to CEO via Telegram if no fallback available

---

## RELATED
- Plugin Registry: `ecosystem/plugins/plugin-catalog.md`
- Skill Registry: `ecosystem/skills/SKILL_REGISTRY.json`
- GEMINI.md `[RULE-TIER-01]` (3-Tier Architecture)
