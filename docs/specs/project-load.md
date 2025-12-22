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

## Public API (Phase 3)

### Function
`load_project(root: Path) -> ProjectContext`

### Input
- `root` is an absolute or relative path to the **project root directory**.

### Output
- Returns a valid `ProjectContext` when `.cairn/manifest.yaml` exists and is valid.

---

## ProjectContext (Phase 3)

`ProjectContext` is the in-memory, read-only representation of a loaded Cairn project.

### Required Fields
- `root: Path`  
  The project root directory passed to `load_project(...)`, preserved exactly.

- `manifest_path: Path`  
  The resolved manifest path: `root/.cairn/manifest.yaml`.

- `project_id: str`  
  The project identifier from the manifest.

- `schema_version: str`  
  The manifest schema version (must be `"0.1"` for Phase 3).

### Notes
- `ProjectContext` is constructed **only after** all Phase 3 validations pass.
- `ProjectContext` construction must not perform filesystem writes.
- The context is immutable for the lifetime of Phase 3.

---

## Error Model
- Raises `ProjectLoadError` (new) for all load-time failures.
- `ProjectLoadError` must include:
  - a stable error code string (e.g., `"manifest_missing"`)
  - a human-readable message
  - optional underlying exception context (not shown to user by default)

## Error Codes (Authoritative)

The following error codes are stable and must be used:

- `manifest_missing`  
  `.cairn/manifest.yaml` does not exist at the resolved project root.

- `manifest_not_file`  
  The manifest path exists but is not a regular file.

- `manifest_invalid_yaml`  
  The manifest file could not be parsed as valid YAML.

- `manifest_schema_unsupported`  
  `schema_version` is present but not supported by this version of Cairn.

- `manifest_missing_field`  
  One or more required manifest fields are missing.

- `manifest_invalid_field`  
  A required field exists but has an invalid type or value.

## Required Behaviors (High-Level)
- Fail if manifest does not exist
- Fail if manifest is not valid YAML
- Fail if required fields are missing
- Fail if schema_version is unsupported
- Do not infer or default missing data
- Preserve exact stored values where valid

## Notes
- This function is read-only (no filesystem writes).
- Manifest path resolution is always `root/.cairn/manifest.yaml`.

## Open Questions
(None — must be resolved before implementation)
