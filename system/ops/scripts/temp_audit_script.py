import json
import os

# Read the SKILL_REGISTRY.json file
with open('<AI_OS_ROOT>/brain/shared-context/SKILL_REGISTRY.json', 'r', encoding='utf-8-sig') as f:
    sr = json.load(f)

# Check if entries is a dict or list
entries_raw = sr.get('entries', {})
if isinstance(entries_raw, dict):
    # It's a dict, convert to list of tuples
    entries_list = list(entries_raw.items())
    print(f"Entries is a dict with {len(entries_list)} items")
else:
    # It's already a list
    entries_list = [(e.get('name', 'unknown'), e) for e in entries_raw]
    print(f"Entries is a list with {len(entries_list)} items")

ROOT = os.environ.get("AOS_ROOT", ".")
broken = []
valid = 0

# Check each entry for broken paths
for name, info in entries_list:
    if isinstance(info, dict):
        path = info.get('path', '') or info.get('skill_path', '')
        if path:
            skill_md = os.path.join(ROOT, path, 'SKILL.md')
            if not os.path.isfile(skill_md):
                broken.append((name, path))
                print(f"Broken: {name} -> {path}")
            else:
                valid += 1

print(f"\nTotal: {len(entries_list)}")
print(f"Valid: {valid}")
print(f"Broken paths: {len(broken)}")

# Write to audit file
audit_content = f"""# SKILL_REGISTRY.json Audit Report - 2026-03-24

## Summary
- Total entries: {len(entries_list)}
- Valid paths: {valid}
- Broken paths: {len(broken)}

## Broken Entries
"""

if broken:
    for name, path in broken:
        audit_content += f"- **{name}**: {path}\n"
else:
    audit_content += "- No broken paths found - all SKILL.md files exist at their declared paths\n"

audit_content += """

## Recommendations
1. For broken paths: either update the path or remove the entry
2. Run this audit monthly to catch drift
3. Consider adding a CI check for path validation
"""

os.makedirs('<AI_OS_ROOT>/brain/knowledge/notes', exist_ok=True)
with open('<AI_OS_ROOT>/brain/knowledge/notes/SKILL_REGISTRY_AUDIT-2026-03-24.md', 'w', encoding='utf-8') as f:
    f.write(audit_content)

print("\nAudit report generated successfully.")

