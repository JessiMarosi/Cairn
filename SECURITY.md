# Security Policy

## Supported Versions

Cairn is currently in early development. Security fixes will be applied only to the latest development version.

Older commits and forks may not receive security updates.

---

## Reporting a Vulnerability

If you discover a security vulnerability in Cairn, please **do not** report it publicly via GitHub issues.

Instead, report it responsibly by contacting:

- Email: security@cairn.dev (placeholder)
- Or by opening a **private security advisory** on GitHub

Please include:
- A clear description of the issue
- Steps to reproduce (if applicable)
- Potential impact
- Any relevant logs or screenshots (with sensitive data removed)

---

## Security Scope

Cairn aims to protect:
- Project source code and configuration
- Annotations and audit artifacts
- Authentication and session boundaries
- Policy enforcement mechanisms

Cairn does **not** claim to protect against:
- A fully compromised operating system
- Attackers with administrator/root access
- Physical access to unlocked devices
- Behavior of third-party services once data is sent to them

---

## Security Model Summary

- Local-first by default
- No required cloud identity
- No implicit network communication
- Explicit authentication and session handling
- Policy-driven restrictions in managed environments

Security is a core design goal and is treated as part of the product, not an afterthought.

---

## Disclosure Policy

We ask that security researchers:
- Avoid accessing or modifying data without permission
- Avoid denial-of-service testing
- Allow reasonable time for fixes before public disclosure

We appreciate responsible disclosure and constructive collaboration.
