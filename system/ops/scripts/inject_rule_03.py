import os

gemini_path = r"<AI_OS_ROOT>\GEMINI.md"
claude_path = r"<AI_OS_ROOT>\CLAUDE.md"

try:
    with open(gemini_path, "r", encoding="utf-8") as f:
        text1 = f.read()

    rule_gemini = """
**[RULE-ARCH-03]** NATIVE TOOLING & SOP MANDATE:
- MỌI AI OS AGENT KHÔNG ĐƯỢC tự ý tạo file hệ thống (Agent, Skill, Workflow, Project, Rule) thủ công.
- TẤT CẢ quy trình phải thông qua các SOP chuẩn rải rác trong `system/ops/workflows/` (vd: `agent-auto-create.md`, `skill-discovery-auto.md`).
- KHÔNG hứa hẹn suông "Em xin cam kết...", vi phạm luật này là hành vi Anti-System. Im lặng và tuân thủ Luật!
"""

    if "**[RULE-ARCH-03]**" not in text1:
        text1 = text1.replace("**[RULE-CIV-01]**", rule_gemini + "\n**[RULE-CIV-01]**")
        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write(text1)
            print("Injected into GEMINI.md")
except Exception as e:
    print(f"Error GEMINI: {e}")

try:
    with open(claude_path, "r", encoding="utf-8") as f:
        text2 = f.read()

    rule_claude = "- **[RULE-ARCH-03] NATIVE TOOLING & SOP MANDATE**: MỌI AI OS AGENT KHÔNG ĐƯỢC tự ý tạo file (Agent, Skill, Workflow, Rule) thủ công. TẤT CẢ phải thông qua Hệ thống SOP chuẩn trong `system/ops/workflows/`. Vi phạm luật này là hành vi Anti-System. Không hứa hẹn suông, IM LẶNG VÀ TUÂN THỦ LUẬT.\n"

    if "[RULE-ARCH-03]" not in text2:
        # We find the line to replace
        for line in text2.split("\n"):
            if "ecosystem/subagents/mq/" in line:
                text2 = text2.replace(line, line + "\n" + rule_claude)
                with open(claude_path, "w", encoding="utf-8") as f:
                    f.write(text2)
                print("Injected into CLAUDE.md")
                break
except Exception as e:
    print(f"Error CLAUDE: {e}")
