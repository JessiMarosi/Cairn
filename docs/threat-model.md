# Threat Model

## Overview

This document defines the threat model for Cairn.

It identifies the assets Cairn is designed to protect, the primary threat actors, trust boundaries, attack surfaces, and explicit assumptions and non-goals. This threat model informs architectural, policy, and implementation decisions throughout the project.

Cairn is designed as local-first developer infrastructure software. External services are optional and explicitly configured.

---

## Assets

Cairn is responsible for protecting the confidentiality and integrity of the following assets:

- Project source code and related files
- Project metadata and configuration
- Annotations (AI-generated and user-authored)
- Audit logs and security-relevant records
- Authentication material:
  - password verifiers (hashed)
  - MFA secrets (where enabled)
  - recovery materials (where enabled)
- Encryption keys derived during active sessions
- API credentials provided by the user for external model providers
- Policy files and enforcement state

---

## Security Goals

Cairn is designed to meet the following security goals:

1. Prevent unauthorized access to projects and sensitive artifacts.
2. Require explicit local authentication before accessing protected data.
3. Ensure cryptographic material is inaccessible to the UI, plugins, and untrusted modules.
4. Enforce policy restrictions deterministically and transparently.
5. Provide auditable records of sensitive actions.
6. Minimize accidental data exfiltration through default behavior.
7. Fail closed when security-relevant errors occur.

---

## Threat Actors

Cairn considers the following threat actors:

- A non-administrative attacker with access to the local machine
- A malicious or careless user on a shared workstation
- Malware operating under the user’s OS account
- An attacker who gains access to project directories via filesystem theft or backup leakage
- A malicious or misconfigured plugin
- Risks introduced by external services when explicitly enabled:
  - service-side logging or retention
  - network interception if system trust is compromised

---

## Trust Boundaries

Cairn enforces strict trust boundaries:

- The desktop UI is untrusted with respect to secrets.
- The Core engine is trusted to implement security-critical logic.
- Authentication unlocks sessions but does not directly access project data.
- Cryptography is isolated and invoked only through authorized workflows.
- Policy restricts behavior; it does not grant access.
- Plugins are untrusted and capability-restricted.
- External services are outside the trust boundary.

---

## Attack Surfaces and Mitigations

### Local Filesystem

Risks:
- Theft of project directories
- Tampering with configuration or audit files
- Downgrade of security settings via file modification

Mitigations:
- Explicit schema validation on load
- Policy-enforced restrictions overriding project settings
- Optional encryption of sensitive artifacts
- Append-only audit logging where feasible
- Clear user-visible validation errors

---

### Authentication and Session Handling

Risks:
- Weak password handling
- Session token reuse or theft
- Inadequate lock or timeout behavior
- Recovery mechanisms weakening security

Mitigations:
- Salted, memory-hard password hashing
- Short-lived session tokens with idle timeout
- Explicit lock and unlock flows
- MFA gating for high-risk actions
- Recovery mechanisms that do not bypass primary controls

---

### Policy Enforcement

Risks:
- Policy bypass through malformed configuration
- Conflicting policy sources producing undefined behavior

Mitigations:
- Schema validation for all policy sources
- Deterministic precedence rules
- Most-restrictive-wins evaluation
- Fail-closed behavior on policy parsing errors
- User-visible indication of managed mode

---

### External Model APIs (Optional)

Risks:
- Unintentional data exfiltration
- Leakage of sensitive code or secrets
- API key compromise

Mitigations:
- External APIs disabled by default
- Explicit per-project enablement
- Policy ability to disable external services entirely
- Redaction controls where applicable
- Local-only storage of API credentials
- Clear user indication when external services are used

---

### Plugin System (Phased)

Risks:
- Arbitrary code execution
- Unauthorized network access
- Access to sensitive project data or secrets

Mitigations:
- Plugins disabled by default
- Explicit capability declarations
- Policy-controlled enablement
- Deny-by-default privileges
- No access to authentication or cryptographic material
- Optional sandboxing in later phases

---

### Code Execution and Sandbox (Phased)

Risks:
- Execution of untrusted code
- Host system compromise
- Data destruction or exfiltration

Mitigations:
- Execution disabled by default
- Policy-controlled enablement
- Sandboxed execution environment
- MFA gating for execution actions
- Audit logging of execution attempts

---

## Out-of-Scope Threats and Assumptions

Cairn does not attempt to defend against:

- An attacker with full administrative or root access
- A fully compromised operating system or kernel
- Hardware attacks or physical forensic extraction
- Data exfiltration occurring outside Cairn’s control (e.g., manual file copying)
- Behavior of third-party services after data is transmitted to them

Cairn assumes:

- The underlying operating system enforces basic user isolation
- Users and organizations configure their environment appropriately
- Physical access to unlocked devices is trusted

---

## Security Posture Summary

Default posture:

- Local-first and offline-capable
- No required cloud identity
- No implicit external network communication
- Explicit project boundaries
- Strong separation between UI, Core, and plugins
- Policy-enforced restrictions in managed environments

---

## Roadmap-Aligned Enhancements

Planned security enhancements include:

- TOTP-based MFA
- Recovery key mechanisms
- Encrypted project artifacts
- Signed policy enforcement
- Stronger audit integrity and report signing
- Plugin sandboxing
- Secure execution environments

---

## Summary

This threat model defines the security boundaries and assumptions under which Cairn operates.

All future features must be evaluated against this model to ensure they do not weaken Cairn’s security posture or violate its local-first, user-controlled design principles.
