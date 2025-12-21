# Cairn Architecture

## Overview

Cairn is a local-first, cross-platform developer workbench designed as developer infrastructure software.  
It is built as a desktop application with a modular tool architecture, explicit on-disk projects, and security boundaries that protect user data by default.

This document describes the high-level architecture, component boundaries, and data flow.

---

## Goals

- Local-first operation with explicit user control over data
- Cross-platform desktop delivery (Windows, macOS, Linux)
- Clear security boundaries between authentication, cryptography, and workspace access
- Modular tools that can be enabled, restricted, or audited independently
- Transparent, auditable behavior with explicit on-disk artifacts
- Enterprise-ready controls via local policy enforcement (optional)

---

## Non-Goals

- No required cloud accounts or centralized identity
- No default telemetry
- No implicit background uploads of user data
- No plugin execution with unrestricted privileges

---

## High-Level Components

Cairn consists of two primary layers:

1. Desktop (UI Shell)
2. Core (Engine)

### Desktop (Tauri)

Responsibilities:
- User interface and navigation
- Authentication gate (login UX)
- Project selection and opening
- Display of tool modules (Workbench, Debug, Audit, etc.)
- Presentation-layer filtering/search over annotations and logs
- Invoking Core services via a stable boundary (IPC)

Non-responsibilities:
- Implementing cryptography
- Storing secrets
- Directly reading/writing project content except through Core APIs

### Core (Engine)

Responsibilities:
- Project management (create/open/validate)
- Authentication and session lifecycle
- Cryptography and encryption boundaries
- Policy evaluation (personal or enterprise)
- Annotation and audit data models and persistence
- Model orchestration abstraction (future phases)
- Execution sandbox abstraction (future phases)

The Core is designed to be testable, deterministic, and independent of UI concerns.

---

## Core Subsystems

The Core is organized into subsystems with explicit boundaries.

### Projects

Purpose:
- Manage explicit on-disk projects

Responsibilities:
- Create project directory structure
- Load and validate project files (`project.yaml`, `security.yaml`, `models.yaml`)
- Provide normalized project context to other subsystems
- Enforce schema versioning rules

Interfaces (illustrative):
- `create_project(path, metadata)`
- `open_project(path)`
- `validate_project(path)`
- `get_project_context(project_id)`

### Authentication

Purpose:
- Mandatory local login with a secure session model

Responsibilities:
- Enrollment (initial setup) and login flows
- Password verification (no plaintext storage)
- Session token creation and expiration
- Lock/unlock behavior and idle timeout
- MFA integration (phased; stubbed early)
- Recovery key integration (phased)

Constraints:
- Authentication never directly reads or writes project content

Interfaces (illustrative):
- `enroll_user(user_id, password, mfa_config?)`
- `login(user_id, password)`
- `lock_session()`
- `unlock_session(credentials)`
- `get_session_state()`

### Crypto

Purpose:
- Provide encryption/decryption services and key management

Responsibilities:
- Key derivation from authentication material
- Encryption of sensitive artifacts (project or workspace scope)
- Secure handling of secrets in memory where possible

Constraints:
- Crypto never implements UI, never stores plaintext secrets on disk
- Crypto does not decide policy; it is invoked by authorized workflows

Interfaces (illustrative):
- `derive_keys(session)`
- `encrypt(path_or_bytes)`
- `decrypt(path_or_bytes)`

### Policy

Purpose:
- Determine effective restrictions and allowances

Responsibilities:
- Load personal, project, and enterprise policy sources
- Validate policy structure
- Evaluate effective controls using precedence rules
- Provide policy decisions to other subsystems (modules, export, execution, models)

Precedence:
1. Organization/system policy (if present)
2. User policy/preferences
3. Project configuration

Rule:
- Most restrictive wins

Interfaces (illustrative):
- `load_policy_sources()`
- `evaluate_effective_policy(project_context, user_context)`
- `is_allowed(action, context)`

### Annotations

Purpose:
- Persist and query AI and user annotations

Responsibilities:
- Annotation data model
- Write/read annotations to `annotations/`
- Query/filter by module, file, line, tags, timestamps
- Link annotations across modules (e.g., Debug → Audit)

Interfaces (illustrative):
- `add_annotation(project_id, annotation)`
- `query_annotations(project_id, filters)`
- `link_annotations(project_id, from_id, to_id)`

### Auditing

Purpose:
- Create an auditable record of security-relevant and tool-relevant actions

Responsibilities:
- Append-only audit events in `audit/`
- Support filtered queries and report generation (phased)
- Ensure audit logging can be policy-enforced (enterprise)

Audit events should include:
- timestamp
- module/source
- action type
- subject (project/file reference when applicable)
- outcome (success/failure)
- minimal metadata (avoid unnecessary content capture)

Interfaces (illustrative):
- `record_event(project_id, event)`
- `query_events(project_id, filters)`

### Execution Sandbox (Phased)

Purpose:
- Safely execute user code in a controlled environment

Responsibilities:
- Provide isolated execution environment
- Control filesystem/network access based on policy
- Capture output artifacts to `debug/` or `audit/` as appropriate
- Expose latency measurements for test runs only

This subsystem is intentionally deferred until security and policy foundations are stable.

### Model Orchestration (Phased)

Purpose:
- Route prompts/tasks to configured models

Responsibilities:
- Model adapter interfaces (local and external)
- Task routing and aggregation logic
- Per-project model enable/disable and configuration
- Optional caching of responses (policy-controlled)

This subsystem must respect policy controls for external APIs and redaction rules.

---

## Modular Tool Architecture

Cairn is presented as a set of isolated tools/modules. Each module has:
- explicit entry
- isolated state
- policy-controlled access
- dedicated logs/artifacts where applicable

Initial modules:
- Projects
- Workbench
- Debug
- Audit
- Collaboration (phased)
- Test/Sandbox (phased)
- Security (settings, enrollment, recovery)

Modules should never bypass Core boundaries. All file access is mediated by Core APIs.

---

## Data Flow

### Startup
1. Desktop starts
2. Desktop requests session state from Core
3. If no active session, Desktop shows login gate
4. On successful login, Core issues a session token

### Project Open
1. Desktop requests project open
2. Core validates project schema and security configuration
3. Core evaluates effective policy for the project context
4. Desktop renders allowed modules and restrictions

### Annotation Write
1. User triggers an action (e.g., annotate suggestion)
2. Desktop calls Core `add_annotation`
3. Core persists annotation under `annotations/`
4. Core optionally records an audit event (policy-controlled)

### Audit View
1. Desktop requests audit events
2. Core returns filtered results
3. Desktop renders audit module UI

---

## Security Boundaries

Cairn enforces a strict separation:

- Auth unlocks access to crypto keys (session-scoped)
- Crypto unlocks access to protected workspace artifacts
- Workspace access is mediated by policy and module permissions

Principles:
- No secrets in UI logs
- No plaintext passwords stored
- No network use unless explicitly configured and allowed by policy
- No plugin execution without declared capabilities and policy approval

---

## Enterprise / Managed Mode

Managed mode is enabled by the presence of an organization policy source.

Characteristics:
- Policy restrictions cannot be overridden by users or projects
- Role-based access can be enforced locally
- Audit logging can be mandatory
- External API usage can be blocked or constrained

Policy distribution is local and offline-capable (e.g., signed policy bundle).

---

## Logging and Observability

Cairn uses:
- Append-only audit logs for security-relevant events
- Tool-specific logs and artifacts under the project directory
- Minimal operational logs for troubleshooting (kept local)

Logging is designed to support transparency without capturing unnecessary sensitive content.

---

## Versioning and Compatibility

- Project schema versions are explicit (`schema_version`)
- Core maintains backward compatibility where possible
- Breaking schema changes require migration tooling
- Policy schema versions are explicit (`policy_version`)

---

## Repository Structure (Recommended)

- `core/` contains the Core engine and tests
- `desktop/` contains the Tauri application
- `docs/` contains specifications and design documents
- `.github/` contains CI and templates

---

## Notes

This architecture is intentionally conservative.  
Subsystems (especially execution and model routing) must be introduced only after the security and policy boundaries are proven stable.
