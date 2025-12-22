from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cairn_core.projects.context import ProjectContext
from cairn_core.projects.load import load_project


class ProjectIntrospectError(Exception):
    """
    Phase 4 error base class.

    All Phase 4 introspection-specific errors MUST derive from this type and expose a
    stable string code via .code. Phase 3 load errors must propagate unchanged.
    """

    code: str

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class ProjectIntrospection:
    """
    Phase 4 result object.

    NOTE: Fields will be filled in during Step 3+ as traversal is implemented.
    Keep this dataclass minimal for now to avoid inventing fields not yet wired.
    """

    project: ProjectContext


def _iter_tree_deterministic(root: Path, *, max_depth: int) -> list[Path]:
    """
    Deterministic directory traversal (foundation for Phase 4).

    - Stable lexicographic ordering within each directory.
    - Rejects symlinks immediately (fail-fast).
    - Enforces max_depth (root is depth 0).

    NOTE: This helper is intentionally NOT wired into introspect_project() yet.
    """
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    out: list[Path] = []

    def walk_dir(dir_path: Path, depth: int) -> None:
        # Fail-fast on symlinks.
        if dir_path.is_symlink():
            raise ProjectIntrospectError(
                code="introspect_symlink_detected",
                message=f"Symlink encountered: {dir_path}",
            )

        out.append(dir_path)

        # Spec: if visiting an entry would exceed MAX_DEPTH, we MUST fail.
        # root is depth 0; children are depth+1.
        # If we're already at max_depth, any child entry would exceed it.
        if depth >= max_depth:
            try:
                next(dir_path.iterdir(), None)
            except OSError as e:
                raise ProjectIntrospectError(
                    code="introspect_io_error",
                    message=f"Failed to read directory: {dir_path} ({e})",
                ) from e

            raise ProjectIntrospectError(
                code="introspection_scan_limit_exceeded",
                message=f"Traversal depth limit exceeded at: {dir_path}",
            )

        # Deterministic ordering: sort by name only (filesystem case preserved).
        try:
            children = sorted(dir_path.iterdir(), key=lambda p: p.name)
        except OSError as e:
            # Placeholder for later: permissions / IO errors will become Phase 4 codes.
            raise ProjectIntrospectError(
                code="introspect_io_error",
                message=f"Failed to read directory: {dir_path} ({e})",
            ) from e

        for child in children:
            # Reject symlinks at the entry point.
            if child.is_symlink():
                raise ProjectIntrospectError(
                    code="introspect_symlink_detected",
                    message=f"Symlink encountered: {child}",
                )

            if child.is_dir():
                walk_dir(child, depth + 1)
            else:
                out.append(child)

    walk_dir(root, 0)
    return out


_DEFAULT_MAX_DEPTH = 25  # Spec default: MAX_DEPTH = 25


def introspect_project(root: Path) -> ProjectIntrospection:
    # Phase 3 gate: MUST run first; errors propagate unchanged.
    project = load_project(root)

    # Phase 4 traversal wiring (skeleton only). No accounting/exclusions yet.
    _iter_tree_deterministic(root, max_depth=_DEFAULT_MAX_DEPTH)

    # Stub until traversal is fully implemented in later steps.
    raise NotImplementedError
