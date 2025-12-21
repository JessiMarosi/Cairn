# Policy Schema Specification

## Overview

This document defines the policy schema used by Cairn to enforce organizational and system-level controls.

Policies are optional and local-first. When present, they restrict behavior on the local system without requiring a backend service or cloud identity.

Policy enforcement is deterministic, transparent, and auditable. Policies restrict capabilities; they do not grant access.

---

## Design Principles

- Local enforcement only
- Offline-capable
- Explicit and declarative
- Most-restrictive-wins evaluation
- Transparent to users
- No embedded credentials or secrets
- Policies restrict behavior; they never elevate privilege

---

## Policy Sources and Precedence

Cairn evaluates policy sources in the following order:

1. Organization / System Policy  
2. User Policy (local preferences)  
3. Project Configuration  

When multiple policies apply, the most restrictive effective rule is enforced.

---

## Policy Distribution and Integrity

Policies may be distributed as a signed bundle:

- cairn_policy.yaml  
- cairn_policy.sig  

If a signature is present, Cairn must verify the policy before applying it.  
Unsigned or invalid policies must be ignored and recorded as a local diagnostic event.

---

## Policy Versioning

Every policy must declare a version:

policy_version: "1.0"

Unsupported policy versions must be ignored and surfaced to the user.

---

## Top-Level Structure

policy_version: "1.0"

organization:
  name: "<Organization Name>"
  policy_id: "<unique-policy-id>"
  issued_at: "<ISO-8601 timestamp>"

roles: {}
authentication: {}
modules: {}
models: {}
execution: {}
data_controls: {}
plugins: {}
auditing: {}
projects: {}

All sections are optional unless otherwise specified.

---

## Roles (RBAC)

Roles define categories of allowed actions. Role assignment is implementation-specific and out of scope for this schema.

roles:
  viewer:
    description: "Read-only access"
  developer:
    description: "Standard development access"
  debugger:
    description: "Debugging access"
  auditor:
    description: "Audit access"
  admin:
    description: "Administrative access"

---

## Authentication Controls

authentication:
  require_login: true
  require_mfa:
    default: true
    for_modules:
      - audit
      - execute
    for_actions:
      - export
      - change_security_settings

---

## Module Controls

modules:
  projects: true
  workbench: true
  debug: true
  audit: true
  collaboration: false
  execute: false
  security: true

---

## Model Controls

models:
  allow_external_apis: false
  allowed_models:
    - llama
    - kimi
  external_api_rules:
    redact_secrets_before_api: true

---

## Execution Controls

execution:
  allow_code_execution: false
  require_mfa_for_execution: true
  sandbox:
    allow_network: false
    allow_filesystem_write: false

---

## Data Handling Controls

data_controls:
  allow_export: false
  allow_copy_to_clipboard: false
  allow_external_sharing: false

---

## Plugin Controls

plugins:
  enabled: false
  allowed_capabilities:
    - read_annotations
    - add_annotations
  allow_network: false

---

## Auditing Controls

auditing:
  enabled: true
  retention_days: 365
  require_signed_reports: false
  mandatory_events:
    - login
    - project_open
    - export_attempt
    - execution_attempt

---

## Project Controls

projects:
  require_encryption: true
  allow_personal_projects: false
  shared_project_access: "role-based"

---

## Enforcement Requirements

- Policies override user and project configuration
- Disallowed actions must fail closed
- Policy decisions must be auditable
- Active policy state must be visible to the user (e.g., “Managed Mode”)

---

## Security Notes

- Policies must not contain credentials, secrets, or API keys
- Policies do not authenticate users
- Policies restrict behavior; they never grant new capabilities
