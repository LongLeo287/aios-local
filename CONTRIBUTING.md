# 🤝 Joining the Syndicate (Contributing to OmniClaw)

First off, thank you for considering contributing to **OmniClaw**. 

Whether you are here to architect a new Department (Custom Agent), optimize the Master Router, or fortify our Zero-Trust shields, you are now part of the OmniClaw workforce. This document serves as your Corporate Handbook for submitting code, reporting bugs, and expanding the syndicate.

---

## 🏢 1. Routing Your Directives (Issues & Bugs)

Before writing any code, we need to ensure your efforts are routed to the correct department.

*   **Security Vulnerabilities:** Do NOT open a public issue. Route immediately to **Dept 10 (Strix Security)** by following the instructions in our `SECURITY.md` file.
*   **Bug Reports (Core & Agents):** Use the GitHub Issue tracker. Provide clear steps to reproduce, terminal logs, and specify which Department/Agent failed.
*   **Feature Requests & Strategic Proposals:** Route to **Dept 05 (Strategic Planning)** by opening a thread in the [Discussions tab](../../discussions). Pitch your idea before you spend hours coding it.

---

## 🛠️ 2. The Development Workflow

To submit code to the OmniClaw kernel, strictly follow this protocol:

### Step 1: Fork & Branch
1. Fork the repository to your local machine.
2. Create a logically named branch based on your target area:
   * `core/router-optimization` (For Master Router updates)
   * `dept-99/new-image-agent` (For creating a new Department)
   * `ops/memory-leak-fix` (For bug fixes and maintenance)

### Step 2: Adhere to the 3-Tier Plugin Protocol
OmniClaw is a monolithic hub-and-spoke system. We deeply care about RAM and startup times.
*   **Do NOT** cram heavy imports (like `torch`, `puppeteer`, `cv2`) into the global `aios` core.
*   If your Agent requires heavy libraries, build it as a **Tier-2 Lazy-Load Plugin**. It must be sandboxed and include a teardown function to flush RAM after execution. 
*   *Reference:* Read the [Tier-2 Plugin Development Guide](https://github.com/LongLeo287/aios-local/wiki) on our Wiki.

### Step 3: Zero-Trust Local Environment
Before you even think about committing:
*   Ensure **NO API KEYS**, `.env` files, or proprietary data are hardcoded.
*   Run the local Ops script to sanitize your workspace. The `omniclaw_cleaner.py` daemon should ideally sweep your temporary files.

---

## 🤖 3. Forging a New Department (Adding Agents)

We highly encourage developers to expand the syndicate by building new, specialized Agents. If you are submitting a new Department:

1.  **Single Responsibility:** Your Agent must do exactly *one* thing exceptionally well. Do not build "Swiss-Army Knife" agents.
2.  **Stateless Execution:** Your Agent must inherit from `BaseAgent`. It should receive a payload, execute, return the pure Markdown result, and immediately flush its variables.
3.  **Documentation:** You must update the `brain/corp/org_chart.yaml` and provide a brief SOP for your new Agent.

---

## 📜 4. The Pull Request Protocol (Dept 09 - Content Review)

When you are ready to merge your code into the Master branch:

1. Open a Pull Request (PR) against the `main` branch.
2. Title your PR clearly (e.g., `feat(dept-42): add advanced financial analysis agent`).
3. Fill out the provided PR template, explaining *what* you changed and *why* it benefits the OmniClaw OS.
4. **Code Review:** Your PR will be audited by the Core Team (acting as **Dept 09 - Content Review**). We will check for memory leaks, Zero-Trust compliance, and prompt injection vulnerabilities.

---
<div align="center">
  <i>"Code with precision. Execute with autonomy."</i><br>
  <b>Welcome to OmniClaw.</b>
</div>
