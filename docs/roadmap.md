# Cairn Roadmap

## Overview

This roadmap outlines the phased development of Cairn.  
The goal is to build a stable, local-first developer workbench with strong security guarantees and a modular architecture that can evolve without major rewrites.

Cairn prioritizes correctness, transparency, and long-term maintainability over rapid feature expansion.

---

## v0.1 — Foundation (Initial Release)

**Objective:**  
Establish a solid, auditable core with explicit projects, security boundaries, and a minimal end-to-end workflow.

### Core
- Explicit on-disk project creation and loading
- Project validation against schema
- Basic project metadata handling
- Clear separation between core logic and UI

### Security
- Mandatory local login (single-user)
- Session lifecycle (lock, unlock, timeout)
- Authentication scaffolding (password flow only; MFA stubbed)
- Clear auth → crypto → workspace boundaries

### Projects
- Create/open project from disk
- Enforce project directory structure
- Read/write project configuration files
- Project-level security configuration (parsed, not enforced yet)

### Annotations
- Annotation data model
- Write/read annotations to project directory
- Link annotations to files and line numbers
- Query annotations by project and source

### Policy
- Policy loader (unsigned, local only)
- Policy schema validation
- Effective-policy evaluation logic (no enforcement yet)

### Desktop
- Tauri application shell
- Project open/create UI
- Login gate before workspace access
- Minimal navigation (Projects → Workbench)

### Non-Goals for v0.1
- No AI model integration
- No code execution
- No plugins
- No collaboration features
- No enterprise enforcement

---

## v0.2 — Usability & Core Capability

**Objective:**  
Make Cairn usable day-to-day for individual developers while preserving security and clarity.

### AI Integration
- Local model integration (LLaMA/Kimi)
- External API integration (Claude, user-supplied key)
- Model routing abstraction
- Per-project model enable/disable

### Workbench
- Primary AI interaction module
- Inline actions (accept, annotate, copy)
- Annotation-first interaction flow
- Search and filter annotations

### Security
- MFA support (TOTP)
- Recovery key generation and rotation
- Encrypted project storage option
- Action-based MFA gating (execute, export)

### Testing / Sandbox
- Safe code execution sandbox
- Explicit “Test Code” action
- Latency measurement for test runs only

---

## v0.3 — Governance & Extensibility

**Objective:**  
Prepare Cairn for professional and organizational use.

### Enterprise / Managed Mode
- Signed policy file support
- Role-based access control
- Policy enforcement for:
  - modules
  - execution
  - exports
  - model usage

### Auditing
- Mandatory audit logging (policy-controlled)
- Audit viewer module
- Exportable audit reports

### Plugins
- Structured plugin API (capability-based)
- Plugin discovery and loading
- Plugin sandboxing

---

## v1.0 — Stability & Trust

**Objective:**  
Deliver a stable, documented, trustworthy developer infrastructure tool.

### Stability
- Backward-compatible project schema
- Migration tooling for schema updates
- Performance optimization

### Documentation
- Full user documentation
- Security model documentation
- Threat model publication
- Contribution guidelines finalized

### UX Polish
- Refined navigation and layout
- Keyboard shortcuts
- Accessibility improvements

---

## Guiding Principles

- Local-first by default
- No required cloud accounts
- Explicit user control over data
- Transparent behavior
- Modular, auditable architecture
- Security is a feature, not an add-on

---

## Notes

This roadmap is intentionally conservative.  
Features move forward only when they can be implemented without compromising security, clarity, or maintainability.
