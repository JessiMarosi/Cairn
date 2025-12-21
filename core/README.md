# Cairn Core

## Overview

Cairn Core is the security-critical engine of Cairn.  
It implements all project management, authentication, cryptography, policy evaluation, annotation handling, and audit logging.

The Core is designed to be deterministic, testable, and independent of any user interface.  
All security guarantees provided by Cairn originate here.

---

## Responsibilities

Cairn Core is responsible for:

- Creating, opening, and validating projects
- Enforcing authentication and session lifecycle
- Managing cryptographic operations and key handling
- Evaluating effective policy (user, project, organization)
- Persisting annotations and audit events
- Enforcing module and action restrictions
- Providing a stable API boundary to the desktop application
- Ensuring fail-closed behavior on security-relevant errors

---

## Non-Responsibilities

Cairn Core must **not**:

- Render user interfaces
- Store plaintext secrets
- Perform network operations unless explicitly enabled
- Make assumptions about user intent
- Bypass policy or authentication requirements
- Execute untrusted code without sandbox mediation

---

## Design Principles

- Local-first by default
- Deterministic behavior
- Explicit inputs and outputs
- Fail closed on error
- Clear subsystem boundaries
- No implicit global state
- Security decisions centralized in Core

---

## Core Structure

The Core is organized into focused subsystems:

- `projects/`  
  Project creation, loading, validation, and context management

- `auth/`  
  Authentication, session lifecycle, MFA hooks, and recovery mechanisms

- `crypto/`  
  Key derivation, encryption/decryption, and secret handling

- `policy/`  
  Policy loading, validation, and effective-policy evaluation

- `annotations/`  
  Annotation models, persistence, linking, and querying

- `logging/`  
  Audit logging and diagnostic event recording

Each subsystem exposes a narrow API and must not depend on UI concerns.

---

## API Boundary

Cairn Core exposes functionality through explicit APIs intended to be consumed by the desktop application or other trusted callers.

Key rules:

- All inputs must be validated
- All outputs must be explicit
- Errors must be descriptive but not leak sensitive data
- No subsystem may bypass another subsystem’s responsibilities

The desktop application must treat Core as the authoritative source for all decisions.

---

## Session Model

- Authentication establishes a session
- Sessions are time-bound and idle-expiring
- Cryptographic keys are scoped to the session
- Locking a session invalidates access to protected artifacts
- Unlocking requires re-authentication or recovery mechanisms

Session state must never be persisted insecurely.

---

## Policy Enforcement

Policy evaluation occurs within Core and governs:

- Available modules
- Allowed actions
- External service usage
- Code execution permissions
- Data export and sharing
- Plugin capabilities

Policy evaluation follows a most-restrictive-wins model and must fail closed.

---

## Audit Logging

Cairn Core records audit events for security-relevant actions.

Audit events must:

- Be append-only where possible
- Avoid capturing unnecessary sensitive content
- Include timestamps, action types, and outcomes
- Be queryable by the desktop application
- Respect policy-defined retention and export rules

Audit logging must not be bypassable.

---

## Error Handling

- Invalid input must be rejected
- Security-related failures must fail closed
- Errors must be surfaced clearly to the caller
- Sensitive information must never be included in error messages
- Diagnostic events may be recorded locally for troubleshooting

---

## Testing Expectations

Core code must be:

- Unit-testable without a UI
- Deterministic under test conditions
- Covered by automated tests for:
  - schema validation
  - policy evaluation
  - authentication flows
  - encryption boundaries
  - audit logging

Security-critical logic must not rely on manual testing alone.

---

## Future Extensions

Planned future responsibilities (phased):

- Secure execution sandbox integration
- Model orchestration and routing
- Plugin capability enforcement
- Enterprise-grade policy enforcement
- Stronger audit integrity and report signing

These features must integrate without weakening existing guarantees.

---

## Summary

Cairn Core is the trusted foundation of Cairn.

All security, policy, and data integrity guarantees originate here.  
No feature should be implemented in Cairn unless it can be enforced and validated by the Core.
