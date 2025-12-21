# Project Schema Specification

## Overview

This document defines the on-disk project schema used by Cairn.

A Cairn project is an explicit, filesystem-based unit that contains source code, configuration, annotations, audit artifacts, and optional debugging output. The project directory is the authoritative source of truth for project state.

Projects are designed to be portable, auditable, and human-readable by default.

---

## Design Principles

- Explicit on-disk representation
- Portable as a single directory
- Human-readable configuration formats
- Versioned schema with migration support
- Git-friendly by default
- Clear separation of concerns
- No hidden or implicit state

---

## Project Root Layout

A Cairn project is a directory with the following structure:

<project_root>/
- project.yaml
- security.yaml
- models.yaml
- code/
- annotations/
- audit/
- debug/
- plugins/

Cairn may create this structure during project creation.  
When opening an existing project, Cairn must validate the presence and structure of required files and directories.

---

## Required Files

### project.yaml

Defines project identity and metadata.

Required fields:

schema_version: "1.0"  
project_id: "<unique-id>"  
name: "<project-name>"  
created_at: "<ISO-8601 timestamp>"  
last_modified: "<ISO-8601 timestamp>"  

owner:
  type: "user"  
  id: "<owner-identifier>"  

Optional fields:

description: "<short description>"  

tags:
- "<tag>"

Notes:
- project_id must remain stable for the lifetime of the project.
- last_modified should update when Cairn writes structured artifacts.

---

### security.yaml

Defines project-level security preferences. These may be restricted or overridden by policy.

Recommended structure:

encryption:
  enabled: false  
  scope: "project"  
  provider: "default"  

authentication:
  require_mfa_on_open: false  
  require_mfa_on_execute: true  
  require_mfa_on_export: true  

data_controls:
  allow_export: true  
  allow_copy_to_clipboard: true  
  redact_secrets_before_api: true  

Notes:
- Encryption preferences may be forced by organizational policy.
- MFA requirements here act as minimums; policy may enforce stricter rules.

---

### models.yaml

Defines which AI models are available to the project and how they are configured.

Recommended structure:

models:
  claude:
    enabled: false  
    mode: "api"  

  llama:
    enabled: true  
    mode: "local"  
    model_path: "./models/llama"  

  kimi:
    enabled: false  
    mode: "local"  
    model_path: "./models/kimi"  

routing:
  strategy: "default"  

Notes:
- API credentials must never be stored in this file.
- Model enablement is always subject to effective policy.

---

## Project Directories

### code/

Contains user source code and related assets.

Notes:
- Cairn must not rewrite user files unless explicitly requested.
- Language-specific structure is not enforced.

---

### annotations/

Stores AI-generated and user-authored annotations.

Each annotation record must include:
- annotation_id
- created_at
- source (module name)
- author ("user", "system", or model identifier)
- content

Optional fields:
- file_path (project-relative)
- line_start
- line_end
- tags
- links to related annotations

Annotations should be append-only where possible to preserve history.

---

### audit/

Stores audit events and audit reports.

Audit records should include:
- timestamp
- module or source
- action type
- outcome (success or failure)
- minimal contextual metadata

Notes:
- Audit logs should avoid capturing full source code or sensitive content.
- Retention and export behavior may be governed by policy.

---

### debug/

Stores debugging artifacts such as:
- stack traces
- test outputs
- execution logs
- temporary analysis files

Notes:
- Debug artifacts may be ephemeral unless retention is required by policy.

---

### plugins/

Contains project-scoped plugins where permitted.

Notes:
- Plugin execution is subject to policy.
- Plugins must declare capabilities.
- Plugins must not access authentication or cryptographic material.

---

## Validation Rules

When opening a project, Cairn must:

- Validate schema_version compatibility
- Verify required files exist
- Validate YAML structure and required fields
- Fail closed on malformed or missing configuration
- Surface validation errors clearly to the user

---

## Schema Versioning and Migration

- schema_version identifies the expected project format.
- Backward compatibility should be maintained within a major version.
- Breaking changes require explicit migration tooling.
- Migration must be deterministic and auditable.

---

## Portability

A Cairn project directory is portable as a unit.

Moving or copying the directory preserves project state, subject to:
- encryption settings
- effective policy restrictions
- availability of local model resources

---

## Security Notes

- Project configuration files must not contain credentials or secret keys.
- Sensitive artifacts may be encrypted depending on configuration and policy.
- Projects do not bypass authentication, policy, or cryptographic boundaries.

---

## Summary

Cairn projects are explicit, auditable, and portable units of work.  
All project behavior flows from the on-disk schema combined with effective policy evaluation.
