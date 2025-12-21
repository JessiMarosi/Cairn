# Cairn Project Initialization Spec (v0)

## Goal
Define the deterministic, auditable on-disk format created by `cairn_core.projects.init.init_project()`.
This document is the source of truth for what gets written to disk and what failure modes are handled.

## Non-Goals
- No networking
- No SaaS accounts
- No plugin install
- No secrets storage (beyond placeholders)
- No AI integration

## Terms
- Project root: the directory the user chooses for a project
- Project ID: stable identifier stored on disk
- Manifest: the canonical project metadata file

## Inputs
`init_project(project_root: Path, project_name: str, created_by: str | None = None) -> ProjectContext`

## Outputs (On-Disk Layout)
Project root contains:

- `.cairn/` (tool-owned; auditable; deterministic)
  - `manifest.yaml` (canonical project metadata)
  - `audit.log` (append-only event log; v0 minimal)
  - `locks/` (reserved)
- `README.md` (human-facing)
- `data/` (user data; not tool-owned; created empty by default)
- `plugins/` (reserved; no execution in v0)

## File Formats

### `.cairn/manifest.yaml` (required)
Minimum fields:
- `schema_version` (string; e.g. "0.1")
- `project_id` (UUIDv4 string)
- `name` (string)
- `created_at` (UTC ISO-8601 string)
- `created_by` (string or null)
- `tool`:
  - `name`: "cairn"
  - `version`: "0.0.0-dev" (placeholder for now)

Rules:
- YAML must be written with stable ordering and stable formatting
- No machine-specific absolute paths inside manifest

### `.cairn/audit.log` (required)
Append-only text file.
First entry records project creation with:
- timestamp (UTC ISO-8601)
- event_type: "project.created"
- project_id

Exact format TBD, but must be deterministic and parseable.

### `README.md` (required)
Contains:
- Project name
- Project ID
- Created timestamp

## Determinism Rules
- All timestamps must be UTC
- UUID generated once at init and persisted
- No environment-dependent fields written (hostnames, usernames unless explicitly `created_by`)
- No hidden state outside project root

## Validation / Preconditions
- `project_root` must exist OR be creatable
- `project_root` must be empty (no files or directories present)
- Initialization MUST fail if `.cairn/manifest.yaml` already exists
- `project_name` rules:
  - length: 1–64 characters
  - allowed characters: ASCII letters (A–Z, a–z), digits (0–9), space, hyphen (-), underscore (_)
  - must not start or end with whitespace
  - no control characters
  - value is stored exactly as provided (no normalization or slugging)


## Failure Behavior
If any write fails:
- Do not leave a partially initialized project
- Best-effort rollback: remove `.cairn/` and any created files in this init call
- Never delete user pre-existing files

## Security Notes
- Treat paths as untrusted input; prevent directory traversal issues
- Use atomic writes for manifest (write temp file then rename)
- File permissions: inherit OS defaults (tightening later)

## Open Questions
- Should we support a `cairn.yaml` at root instead of `.cairn/manifest.yaml`?
