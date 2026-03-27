import os
import json
import yaml

ROOT_DIR = os.environ.get("AOS_ROOT", ".")

def create_skill():
    skill_dir = os.path.join(ROOT_DIR, "ecosystem", "skills", "ontology_auditor")
    os.makedirs(skill_dir, exist_ok=True)
    skill_md = os.path.join(skill_dir, "SKILL.md")

    content = """---
name: ontology_auditor
description: SiÃªu ká»¹ nÄƒng quÃ©t rÃ¡c vÅ© trá»¥, Ä‘Ã³ng gÃ³i vÅ© khÃ­ má»“ cÃ´i vÃ  render láº¡i Org Graph.
version: 1.0.0
author: Antigravity
owner_dept: monitoring_inspection
---
# ONTOLOGY AUDITOR (MA TRáº¬N TIáº¾N HÃ“A)

**KÃ­ch hoáº¡t:** Khi Sáº¿p hoáº·c há»‡ thá»‘ng yÃªu cáº§u "Dá»n dáº¹p", "QuÃ©t rÃ¡c", "Render Org Graph".
**HÃ nh Ä‘á»™ng:** Cháº¡y ká»‹ch báº£n `python system/ops/scripts/ontology_auditor.py`.
**Káº¿t quáº£:** Dá»n sáº¡ch cÃ¡c Agent, Workflow, Skill, Plugin má»“ cÃ´i vÃ  Ã©p chÃºng vÃ o Ä‘Ãºng vá»‹ trÃ­ trÃªn Äá»“ thá»‹ nháº­n thá»©c.

## CÃ¡ch dÃ¹ng (Cho SRE-Agent)
Má»Ÿ terminal vÃ  gÃµ:
```bash
python "<AI_OS_ROOT>\\system\\ops\\scripts\\ontology_auditor.py"
```
"""
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(content)

def register_skill():
    registry = os.path.join(ROOT_DIR, "ecosystem", "skills", "SKILL_REGISTRY.json")
    try:
        with open(registry, "r", encoding="utf-8") as f:
            data = json.load(f)

        new_skill = {
            "id": "ontology_auditor",
            "name": "Ontology Auditor Suite",
            "path": "skills/ontology_auditor/SKILL.md",
            "tier": 1,
            "source": "AI OS Core",
            "license": "Internal",
            "status": "ACTIVE",
            "installed_cycle": 19,
            "tags": ["ontology", "system-integrity", "deep-scan", "auto-equip"],
            "trigger": "manual or auto (cron) to maintain zero unlinked files"
        }

        # Check if exists
        exists = False
        for s in data.get("ecosystem", {}).get("skills", []):
            if s.get("id") == "ontology_auditor":
                exists = True
                break

        if not exists:
            data["ecosystem"]["skills"].append(new_skill)
            data["ecosystem"]["metadata"]["total_skills"] = len(data["ecosystem"]["skills"])
            data["ecosystem"]["metadata"]["last_updated"] = "2026-03-26"

            with open(registry, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Registered ontology_auditor in JSON")
    except Exception as e:
        print(f"Error JSON: {e}")

def create_workflow():
    wf_path = os.path.join(ROOT_DIR, "system", "ops", "workflows", "script-integration-flow.md")
    content = """# Department: registry_capability
# THUáº¬T TOÃN Tá»° TIáº¾N HÃ“A (SCRIPT INTEGRATION FLOW)
**Chu ká»³ Ã¡p dá»¥ng:** Báº¥t ká»ƒ khi nÃ o cÃ³ Má»˜T FILE PYTHON (`.py`) hoáº·c Powershell (`.ps1`) má»›i Ä‘Æ°á»£c sinh ra trong AI OS.

## Má»¤C ÄÃCH
Tuyá»‡t Ä‘á»‘i cáº¥m Ä‘á»ƒ ká»‹ch báº£n code xong dÃ¹ng má»™t láº§n rá»“i vá»©t. File Code sau khi nghiá»‡m thu thÃ nh cÃ´ng pháº£i Ä‘Æ°á»£c TÃCH Há»¢P VÃ€O Há»† THá»NG Ä‘á»ƒ tÃ¡i sá»­ dá»¥ng. ÄÃ¢y lÃ  Quy trÃ¬nh Tá»± Tiáº¿n HÃ³a.

## CÃC BÆ¯á»šC KHáº®C NHáº¬P Báº®T BUá»˜C:
1. **CHUáº¨N KIá»‚M (CODE VETTING):**
   - Äáº£m báº£o script cháº¡y khÃ´ng cÃ³ lá»—i (Exit 0).
   - Di chuyá»ƒn script vÃ o `system/ops/scripts/` (hoáº·c thÆ° má»¥c tÆ°Æ¡ng á»©ng).

2. **GÃ“I Ká»¸ NÄ‚NG (Bá»ŒC BULLET):**
   - DÃ¹ng lá»‡nh `write_to_file` táº¡o thÆ° má»¥c `ecosystem/skills/[ten_script]/`.
   - Táº¡o file `[ten_script]/SKILL.md` (Ghi chÃº rÃµ rÃ ng cÃ¡ch Agent khÃ¡c gá»i file nÃ y).

3. **KHAI SINH VÃ€O Sá»” CÃI (REGISTRY):**
   - Cáº­p nháº­t thÃ´ng tin mÅ©i Skill nÃ y vÃ o Sá»• cÃ¡i `ecosystem/skills/SKILL_REGISTRY.json`.
   - Cáº­p nháº­t Automation náº¿u script cáº§n cháº¡y ngáº§m vÃ o `system/automations/AUTOMATION_REGISTRY.yaml`.

4. **PHÃ‚N PHÃT VÅ¨ KHÃ (WEAPON EQUIP):**
   - Chá»‰nh sá»­a file cáº¥u hÃ¬nh YAML cá»§a PhÃ²ng Ban (`brain/corp/departments/[dept_name].yaml`).
   - ThÃªm ID cá»§a Skill/Automation nÃ y vÃ o máº£ng `tools_and_capabilities/skills`.

5. **ÄÃ“NG ÄINH Báº¢N Äá»’:**
   - Cháº¡y `python system/ops/scripts/org_mapper.py` Ä‘á»ƒ nhÃºng Tool má»›i vÃ o Máº¡ng LÆ°á»›i Nháº­n Thá»©c.
"""
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write(content)

def update_automation():
    auto_path = os.path.join(ROOT_DIR, "system", "automations", "AUTOMATION_REGISTRY.yaml")
    try:
        with open(auto_path, 'r', encoding='utf-8') as f:
            auto_data = yaml.safe_load(f)

        if "ontology_sweep" not in auto_data["automations"]:
            auto_data["automations"]["ontology_sweep"] = {
                "type": "cron",
                "path": "system/ops/scripts/ontology_auditor.py",
                "status": "active",
                "owner": "sre-agent",
                "description": "Cháº¡y tá»± Ä‘á»™ng quÃ©t rÃ¡c dá»¯ liá»‡u má»—i chiá»u Thá»© SÃ¡u. Duy trÃ¬ Zero Unlinked Entities."
            }
            with open(auto_path, 'w', encoding='utf-8') as f:
                yaml.dump(auto_data, f, sort_keys=False, allow_unicode=True)
            print("Updated AUTOMATION_REGISTRY.yaml")
    except Exception as e:
        print(f"Error YAML: {e}")

if __name__ == "__main__":
    create_skill()
    register_skill()
    create_workflow()
    update_automation()
    print("DONE SETUP PHASE 19")

