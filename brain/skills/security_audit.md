---
name: Security Audit Skill
description: Capability to analyze and evaluate the security level of a bookmark list.
---

# Security Audit Skill 🛡️

This skill allows the Agent to perform in-depth security checks on the user's bookmark system.

## Execution Steps:
1. **URL Collection:** Get the list of URLs from the specified bookmarks.
2. **Protocol Check:** Classify links not using HTTPS.
3. **Domain Analysis:** Cross-reference with `link_safety_rules.md` to find spoofing or phishing signs.
4. **Shortened Link Decoding:** Use APIs or Requests to get the real destination of shortened links.
5. **Permission Audit:** (If authorized) List sensitive permissions that the domain holds on the browser.
6. **Reporting:** Export a detailed "Security Health" report and suggest actions (Block, Delete, Revoke).

## Requirements:
- Access to the rules file: `link_safety_rules.md`.
- Use `SecurityService.js` and `PrivacyService.js` in the extension.
- Adhere to Privacy-First principles; do not store personal data.
