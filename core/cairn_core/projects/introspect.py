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

    NOTE: Fields will be filled in during later steps as traversal is implemented.
    Keep this dataclass minimal and only add fields that are validated by tests.
    """

    project: ProjectContext
    entry_count: int
    relative_paths: list[str]


def _iter_tree_deterministic(root: Path, *, max_depth: int) -> list[Path]:
    """
    Deterministic directory traversal (foundation for Phase 4).

    - Stable lexicographic ordering within each directory.
    - Rejects symlinks immediately (fail-fast).
    - Enforces max_depth (root is depth 0).
    - Excludes __pycache__ directories and their contents.
    """
    if max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    out: list[Path] = []

    def walk_dir(dir_path: Path, depth: int) -> None:
        # Exclusion: ignore __pycache__ entirely (dir and contents).
        if dir_path.name == "__pycache__":
            return

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
            # We only fail if there *exists* a child entry we would visit.
            # (If directory is empty, there's nothing to exceed.)
            try:
                # NOTE: Excluded children (like __pycache__) still "exist" on disk,
                # but we still consider their presence as "a child exists".
                has_child = any(dir_path.iterdir())
            except OSError as e:
                raise ProjectIntrospectError(
                    code="introspect_io_error",
                    message=f"Failed to read directory: {dir_path} ({e})",
                ) from e

            if has_child:
                raise ProjectIntrospectError(
                    code="introspection_scan_limit_exceeded",
                    message=f"Traversal depth limit exceeded at: {dir_path}",
                )
            return

        # Deterministic ordering: sort by name only (filesystem case preserved).
        try:
            children = sorted(dir_path.iterdir(), key=lambda p: p.name)
        except OSError as e:
            raise ProjectIntrospectError(
                code="introspect_io_error",
                message=f"Failed to read directory: {dir_path} ({e})",
            ) from e

        for child in children:
            # Exclusion: ignore __pycache__ entirely (dir and contents).
            if child.name == "__pycache__":
                continue

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
    """
    Phase 4:
    - Phase 3 gate MUST run first; errors propagate unchanged.
    - Must enforce traversal max depth, raising code 'introspection_scan_limit_exceeded'.
    - For a valid project (within limits), must return ProjectIntrospection.
    """
    project = load_project(root)

    entries = _iter_tree_deterministic(root, max_depth=_DEFAULT_MAX_DEPTH)

    # Convert to relative POSIX paths and EXCLUDE the root entry "."
    relative_paths: list[str] = []
    for p in entries:
        rp = p.relative_to(root).as_posix()
        if rp == ".":
            continue
        relative_paths.append(rp)

    return ProjectIntrospection(
        project=project,
        entry_count=len(entries),
        relative_paths=relative_paths,
    )
