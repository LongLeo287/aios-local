import os
import sys
import re

if len(sys.argv) < 2:
    print("Missing language argument (1=English, 2=Vietnamese)")
    sys.exit(1)

lang_code = sys.argv[1]
target_lang = "English" if lang_code == '1' else "Vietnamese"
target_lang_upper = target_lang.upper()

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    # Target 1: Headers like "# Language: Vietnamese (user-facing)"
    new_content = re.sub(
        r'(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)? \(user-facing\)', 
        f'<!--LANG-->{target_lang}<!--/LANG--> (user-facing)', 
        new_content, flags=re.IGNORECASE
    )
    
    # Target 2: Markdown Bold Language Rule "Language: **Vietnamese**"
    new_content = re.sub(
        r'Language(:)? \*\*(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)?\*\*', 
        f'Language\\1 **<!--LANG-->{target_lang}<!--/LANG-->**', 
        new_content, flags=re.IGNORECASE
    )

    # Target 3: MASTER_PROMPT table rows "| **Vietnamese** |"
    new_content = re.sub(
        r'\| \*\*(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)?\*\* \|', 
        f'| **<!--LANG-->{target_lang}<!--/LANG-->** |', 
        new_content, flags=re.IGNORECASE
    )

    # Target 4: Rules explicitly stating "VIETNAMESE ONLY" or "ENGLISH ONLY"
    new_content = re.sub(
        r'(?:<!--LANG-->)?(VIETNAMESE|ENGLISH)(?:<!--/LANG-->)? ONLY', 
        f'<!--LANG-->{target_lang_upper}<!--/LANG--> ONLY', 
        new_content
    )

    # Target 5: Specific GEMINI rule "Reporting: Vietnamese to CEO"
    new_content = re.sub(
        r'Reporting:\*\*\s*(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)? to ', 
        f'Reporting:** <!--LANG-->{target_lang}<!--/LANG--> to ', 
        new_content, flags=re.IGNORECASE
    )

    # Target 6: Specific bullet rules "- **Language:** **Vietnamese**."
    new_content = re.sub(
        r'- \*\*Language:\*\* \*\*(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)?\*\*\.', 
        f'- **Language:** **<!--LANG-->{target_lang}<!--/LANG-->**.', 
        new_content, flags=re.IGNORECASE
    )

    # Target 7: Inline paragraph rules "in **Vietnamese**." or "are conducted in **Vietnamese**."
    new_content = re.sub(
        r'in \*\*(?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)?\*\*', 
        f'in **<!--LANG-->{target_lang}<!--/LANG-->**', 
        new_content, flags=re.IGNORECASE
    )
    
    # Target 8: General report actions "... report Vietnamese" (No bolding)
    new_content = re.sub(
        r'report (?:<!--LANG-->)?(Vietnamese|English)(?:<!--/LANG-->)?\b', 
        f'report <!--LANG-->{target_lang}<!--/LANG-->', 
        new_content, flags=re.IGNORECASE
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [+] Synced Language Elements: {os.path.basename(filepath)} -> {target_lang}")

print(f"Applying Cognitive Architecture Language: {target_lang}...")

files_to_check = [
    "GEMINI.md",
    "brain/corp/prompts/master_prompt.md",
    "brain/corp/prompts/runes/brainstorm_prompt.md",
    "brain/corp/prompts/runes/bmad_prompt.md",
    "brain/corp/prompts/runes/decision_log_prompt.md",
    "brain/corp/prompts/runes/execution_receipt_prompt.md",
    "brain/corp/prompts/runes/multi_agent_brainstorm_prompt.md",
    "system/security/rules/AGENTS.md",
    "system/security/rules/MASTER_PROMPT.md",
    "system/security/rules/ORCHESTRATION_SOP.md",
    "system/security/rules/agent_behavior.md",
    "system/security/rules/LEARNING_CYCLE_PROTOCOL.md",
    "brain/corp/rules/manager_rules.md",
    "brain/corp/rules/csuite_rules.md",
    "brain/corp/rules/worker_rules.md",
    "system/security/rules/orchestrator_rules.md",
    "system/security/rules/WORKFLOW.md",
    "system/ops/workflows/DELEGATION_SOP.md"
]

for rel_path in files_to_check:
    process_file(os.path.join(root_dir, rel_path))

print("Language application complete.")
