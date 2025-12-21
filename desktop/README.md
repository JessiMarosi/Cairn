# Cairn Desktop

## Overview

Cairn Desktop is the cross-platform desktop application for Cairn.  
It provides the user interface, navigation, and interaction layer while delegating all security-critical logic to the Core engine.

The desktop application is designed to be local-first, offline-capable, and security-aware by default.

---

## Responsibilities

Cairn Desktop is responsible for:

- Rendering the user interface
- Managing application navigation and layout
- Presenting authentication and session state
- Allowing users to create and open projects
- Displaying and interacting with tool modules
- Issuing requests to the Core engine via a stable boundary
- Reflecting effective policy restrictions in the UI

---

## Non-Responsibilities

Cairn Desktop must **not**:

- Implement cryptographic logic
- Store passwords, secrets, or encryption keys
- Bypass authentication or policy enforcement
- Directly manipulate project files
- Perform security-sensitive decisions independently
- Execute user code without Core mediation

All sensitive operations are delegated to the Core engine.

---

## Architecture

Cairn Desktop is implemented using a lightweight desktop framework (e.g., Tauri) with a strict separation between UI and Core.

High-level structure:

- UI layer (views, components, navigation)
- IPC boundary (requests to Core)
- Session-aware state management
- Policy-aware rendering logic

The desktop application treats the Core as the authoritative source for all project, policy, and security decisions.

---

## Application Flow

### Startup

1. Desktop application launches
2. Desktop queries Core for session state
3. If no active session exists, login is required
4. On successful authentication, the workspace becomes accessible

---

### Project Selection

1. User creates or opens a project
2. Desktop requests project validation from Core
3. Core evaluates effective policy
4. Desktop renders only permitted modules and actions

---

### Tool Interaction

1. User interacts with a module (Workbench, Debug, Audit, etc.)
2. Desktop sends a request to Core
3. Core enforces authentication, policy, and security rules
4. Desktop displays results or errors returned by Core

---

## Modules

The desktop application presents Cairn as a collection of isolated modules.

Initial modules include:

- Projects
- Workbench
- Debug
- Audit
- Security (settings and enrollment)

Additional modules may be added in later phases, subject to policy and Core support.

Modules must not share state directly and must not bypass Core APIs.

---

## Policy Awareness

When a policy is active, the desktop application must:

- Indicate managed mode to the user
- Disable or hide restricted modules
- Disable restricted actions
- Display clear error messages when actions are blocked
- Avoid suggesting unavailable capabilities

Policy enforcement is performed by Core; Desktop reflects outcomes.

---

## Security Considerations

- Desktop logs must not include sensitive data
- Secrets must never be rendered in plaintext
- Session expiration and lock state must be clearly indicated
- UI components must not cache sensitive responses longer than necessary
- Clipboard interactions must respect policy restrictions

---

## Platform Support

Cairn Desktop is intended to support:

- Windows
- macOS
- Linux

Platform-specific behavior must not weaken security or bypass policy enforcement.

---

## Development Notes

- UI changes must not require Core changes unless behavior is affected
- Desktop-to-Core communication must use explicit, versioned requests
- UI features must degrade gracefully when restricted by policy
- Debug and developer tooling must be disabled or gated in production builds

---

## Summary

Cairn Desktop is a presentation and interaction layer only.

All security, policy, and data integrity guarantees are provided by the Core engine. The desktop application must faithfully represent those guarantees without attempting to reimplement or weaken them.
