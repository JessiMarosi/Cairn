# Phase 4 Spec: Project Introspection

## Status
- Phase: 4
- State: DRAFT (not implemented)
- Last updated: 2025-12-21

## Purpose
Define a read-only, deterministic introspection pass over an existing Cairn project on disk. Introspection derives metadata from filesystem structure and file metadata only (no content parsing beyond manifest handled in Phase 3).

## Scope (In / Out)

### In scope
- Read-only inspection of a project root that already passes `load_project(root)`
- Derive deterministic metadata from on-disk structure and file metadata
- Hard-coded exclusion rules for common non-project directories (e.g., `.git/`, `node_modules/`)
- Stable ordering of all returned collections (sorted)
- Strict scan limits to prevent runaway traversal

### Out of scope (non-goals)
- No writes, repairs, migrations, or normalization
- No plugin execution
- No UI
- No network calls
- No inference/guessing from file contents
- No reading arbitrary file contents (metadata only)

## Preconditions
- Phase 3 `load_project(root) -> ProjectContext` is the authoritative gate.
- Introspection MUST call `load_project(root)` first and MUST NOT duplicate Phase 3 validation.

## Public API

### Module + Function (public)
- Module: `core/cairn_core/projects/introspect.py`
- Function: `introspect_project(root: Path) -> ProjectIntrospection`

### Behavior overview
1. Call `load_project(root)` and obtain `ProjectContext`
2. Inspect filesystem under:
   - `root/` (top-level structure)
   - `root/.cairn/` (Cairn internal directory)
3. Return derived metadata only, in a deterministic structure

## Data Model

### ProjectIntrospection (derived-only)
Fields (v0):
- `context: ProjectContext`
- `cairn_dir_exists: bool`
- `manifest_size_bytes: int`
- `manifest_mtime_ns: int`
- `tree: ProjectTreeSummary`

### ProjectTreeSummary
Fields (v0):
- `file_count: int`
- `dir_count: int`
- `total_size_bytes: int`
- `top_level_entries: tuple[str, ...]`  (sorted, relative names)
- `cairn_entries: tuple[str, ...]`      (sorted, relative names)
- `ignored_paths: tuple[str, ...]`      (sorted, relative paths excluded)

### Scan accounting semantics (MUST)
- Definitions:
  - A **directory** is any non-symlink filesystem entry for which `Path.is_dir()` is true.
  - A **file** is any non-symlink filesystem entry for which `Path.is_file()` is true.
  - Symlinks are never counted (traversal fails on encounter per spec).
- Counting rules:
  - `dir_count` includes the project `root` directory itself (depth 0).
  - `file_count` counts all visited files under `root`, including files within `.cairn/` (unless excluded).
  - Excluded directories and their contents MUST NOT be visited and MUST NOT contribute to `file_count`, `dir_count`, or `total_size_bytes`.
- Size rules:
  - `total_size_bytes` is the sum of `st_size` for each counted file.
  - Directories do not contribute to `total_size_bytes`.
- Failure behavior:
  - If a permission or I/O error occurs on any visited entry, introspection MUST fail immediately.
  - On failure, no partial counts are returned (exception raised).

## Determinism Rules (MUST)
- No reliance on OS directory enumeration order
- All lists/tuples must be sorted lexicographically
- Use relative paths (POSIX-style or explicit normalization rule must be chosen)
- Use integer timestamps (e.g., `st_mtime_ns`) rather than formatted date strings
- Do not use current time
- No nondeterministic data sources

## Path ordering & normalization (MUST)
- All paths exposed in introspection outputs MUST be:
  - Relative to the project `root`
  - Normalized to use forward slashes (`/`) as separators
- Ordering:
  - All path lists and entry tuples MUST be sorted lexicographically by their normalized string form.
- Case handling:
  - Path case MUST be preserved exactly as reported by the filesystem.
  - No case folding or normalization is performed, even on case-insensitive filesystems.
- Stability guarantee:
  - Given the same on-disk project state, introspection output MUST be byte-for-byte identical across runs on the same platform.

## Safety Rules (MUST)
- Do not follow symlinks (v0 default), or define exact symlink policy here
- Never read file contents (metadata only)
- Never traverse outside `root` (no `..` escapes; resolve and enforce)

### Filesystem traversal rules (MUST)
- Traversal is rooted at `root` and MUST NOT access paths outside `root` (even via symlinks).
- Symlinks:
  - Introspection MUST NOT follow symlinks (neither to files nor directories).
  - If a symlink is encountered during traversal, introspection MUST raise `introspection_symlink_disallowed`.
- Depth counting:
  - `root` is depth `0`.
  - An entry directly under `root/` is depth `1`.
  - If visiting an entry would exceed `MAX_DEPTH`, introspection MUST fail with `introspection_scan_limit_exceeded`.
- Exclusion application:
  - Exclusions apply to directory names anywhere in the tree.
  - If a directory is excluded, it (and all descendants) MUST NOT be visited or counted.
  - Excluded paths MUST be recorded in `ignored_paths` as normalized relative paths.

## Exclusion Rules (v0)
Exclude these directories anywhere they appear:
- `.git/`
- `.venv/`, `venv/`
- `node_modules/`
- `__pycache__/`
- `.mypy_cache/`
- `.pytest_cache/`

## Scan Limits (v0)
- `MAX_FILES = 50000`
- `MAX_DEPTH = 25`

If a limit is exceeded, introspection must fail with a deterministic error code.

## Error Model

### Phase 3 errors
All Phase 3 errors propagate unchanged (do not wrap or remap).

### Phase 4 errors (new)
- `introspection_scan_limit_exceeded`
- `introspection_permission_denied`
- `introspection_io_error`
- `introspection_symlink_disallowed` (if applicable)

### Error representation (MUST)
- Introspection errors are raised as Python exceptions.
- Each Phase 4 error exception MUST expose a stable `code: str` matching one of the Phase 4 error codes listed above.
- Phase 3 errors MUST propagate unchanged (no wrapping, no remapping).
- Exception messages are developer-facing and may change; tests MUST assert on `code` (and on exception type only if specified).

## Test Requirements
Add `core/tests/test_project_introspect.py` with coverage for:
- Happy path introspection returns stable, sorted results
- Exclusions are applied deterministically
- Limit exceeded produces `introspection_scan_limit_exceeded`
- Permissions errors map to `introspection_permission_denied` (platform-conditional)
- Symlink behavior matches spec

## Compatibility Guarantees
- Phase 3 behavior and `ProjectContext` remain unchanged in Phase 4
- Phase 4 output is additive; future fields must be optional or versioned
