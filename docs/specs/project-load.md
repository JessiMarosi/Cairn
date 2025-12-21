# Cairn Project Load Specification (Phase 3)

## Status
Draft (Phase 3 – Read-Side APIs)

## Purpose
Define the authoritative behavior for loading and validating an existing Cairn project
from disk via its manifest file.

This phase introduces **read-only project initialization**.

## Scope
- Load `.cairn/manifest.yaml`
- Validate schema version
- Parse manifest deterministically
- Construct an in-memory ProjectContext
- Reject invalid, malformed, or incompatible projects

## Non-Goals
- No filesystem writes
- No project mutation
- No auto-repair or migration
- No plugin loading
- No UI concerns

## Canonical Paths
- Manifest: `.cairn/manifest.yaml`

## Required Behaviors (High-Level)
- Fail if manifest does not exist
- Fail if manifest is not valid YAML
- Fail if required fields are missing
- Fail if schema_version is unsupported
- Do not infer or default missing data
- Preserve exact stored values where valid

## Open Questions
(None — must be resolved before implementation)

