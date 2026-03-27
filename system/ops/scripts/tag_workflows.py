import os

WORKFLOW_DIR = r"<AI_OS_ROOT>\system\ops\workflows"

DEPT_KEYWORDS = {
    "engineering": ["deploy", "code", "dev", "tech", "ci-cd"],
    "qa_testing": ["qa", "test", "security", "vet"],
    "marketing": ["market", "content-marketing", "seo"],
    "hr_people": ["agent-auto-create", "agent-hire", "recruiting", "profile"],
    "operations": ["daily-cycle", "sync", "learning-loop", "pre-session"],
    "registry_capability": ["skill-discovery", "knowledge-ingest", "doc-registry"],
    "monitoring_inspection": ["bot-reporting", "hud", "ping"],
    "content_intake": ["intake", "civ"],
    "content_review": ["review", "distribute", "knowledge-distribution"],
    "strategy": ["strategy", "planning", "retro"]
}

def guess_dept(filename):
    lower_name = filename.lower()
    for dept, keywords in DEPT_KEYWORDS.items():
        if any(kw in lower_name for kw in keywords):
            return dept
    # Default fallback
    return "operations"

def main():
    if not os.path.exists(WORKFLOW_DIR):
        print(f"Cannot find {WORKFLOW_DIR}")
        return

    tagged_count = 0
    for file in os.listdir(WORKFLOW_DIR):
        if not file.endswith(".md"):
            continue

        filepath = os.path.join(WORKFLOW_DIR, file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue

        # Check if already tagged
        if "# Department:" in content[:1000]:
            continue

        dept = guess_dept(file)

        # Prepend the tag
        new_content = f"# Department: {dept}\n" + content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        tagged_count += 1
        print(f"Tagged {file} -> {dept}")

    print(f"Successfully auto-tagged {tagged_count} workflows.")

if __name__ == "__main__":
    main()
