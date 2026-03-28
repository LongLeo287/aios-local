# Security Policy

<div align="center">

[**Xem Phiên Bản Tiếng Việt (Vietnamese)**](SECURITY-vn.md)

</div>

---

## 🛡️ The OmniClaw Zero-Trust Commitment

OmniClaw is built on a strict **Zero-Trust Architecture**. Our core philosophy is that your local machine is a fortress, and no data—especially API keys, environment variables, or proprietary source code—should ever leave it without explicit, manual authorization. 

The system utilizes automated background daemons (`omniclaw_cleaner.py`) and specialized agents (**Dept 10 - Strix Security**) to sanitize memory, rewrite git histories, and purge ephemeral data after every session.

## Supported Versions

We actively provide security updates and patches for the following versions of the OmniClaw Core:

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| 12.0.x  | :white_check_mark: | Current Active Cycle |
| < 12.0  | :x:                | Deprecated (Pre-Rebrand) |

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability, a sandbox escape, or a scenario where an Agent bypasses the Zero-Trust local containment, please **DO NOT** open a public GitHub Issue. 

Publicly disclosing a vulnerability could put other users' local instances at risk before a patch can be deployed.

**Please report it directly to our Security Department (Dept 10):**
1. Navigate to the **[Security tab](../../security/advisories)** in this repository.
2. Click **Report a vulnerability** to open a private advisory.
3. Provide a detailed summary of the exploit, including steps to reproduce the bypass.

*Alternatively, if you prefer email, please reach out to the project maintainers directly.*

### Triage & Resolution Process
1. **Intake:** Dept 10 will acknowledge receipt of your vulnerability report within 48 hours.
2. **Investigation:** Our core team will isolate the issue and verify the sandbox escape or data leak.
3. **Eradication:** A hotfix will be developed and pushed to the `main` branch. 
4. **Disclosure:** Once the patch is confirmed and distributed, we will publicly disclose the vulnerability and appropriately credit you for the discovery.

---
*“Trust nothing. Verify everything. Purge the rest.”* — **Dept 10 (Strix Security)**
