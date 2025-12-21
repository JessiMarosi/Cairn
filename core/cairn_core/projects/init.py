"""
Project initialization primitives.

This module defines the public interface for creating
new Cairn projects. No side effects are permitted at
import time.
"""

from dataclasses import dataclass
from pathlib import Path


def _validate_project_name(name: str) -> None:
    """
    Validate project_name per spec (Option A).

    Rules:
    - length 1–64
    - allowed chars: ASCII letters, digits, space, '-', '_'
    - cannot start or end with whitespace
    - no control characters
    - stored exactly as provided (no normalization/slugging)
    """
    if not isinstance(name, str):
        raise ValueError("Project name must be a string.")

    if len(name) < 1 or len(name) > 64:
        raise ValueError("Project name must be 1–64 characters long.")

    if name[0].isspace() or name[-1].isspace():
        raise ValueError("Project name cannot start or end with whitespace.")

    for ch in name:
        code = ord(ch)

        # Reject non-ASCII
        if code > 127:
            raise ValueError("Project name must contain ASCII characters only.")

        # Reject ASCII control chars (0–31 and 127)
        if code < 32 or code == 127:
            raise ValueError("Project name cannot contain control characters.")

        # Allowed: letters, digits, space, '-', '_'
        if ch == " " or ch == "-" or ch == "_":
            continue
        if ch.isalnum():
            continue

        raise ValueError(
            "Project name contains invalid characters. "
            "Allowed: letters, digits, space, '-', '_'."
        )


@dataclass(frozen=True)
class ProjectContext:
    """
    Immutable description of a Cairn project.

    This object represents validated, on-disk state.
    """
    root: Path
    name: str
    schema_version: str
    created_at: str


def init_project(
    path: Path,
    name: str,
    *,
    force: bool = False,
) -> ProjectContext:
    """
    Initialize a new Cairn project at the given path.

    This function is intentionally unimplemented.
    It defines the contract only.
    """
    # Resolve the path but do not create anything
    project_root = path.expanduser().resolve()

    # Validate project name first (pure validation)
    _validate_project_name(name)

    if not project_root.exists():
        raise ValueError(f"Project root does not exist: {project_root}")

    if not project_root.is_dir():
        raise ValueError(f"Project root is not a directory: {project_root}")

    # Reject already-initialized projects explicitly
    manifest_path = project_root / ".cairn" / "manifest.yaml"
    if manifest_path.exists():
        raise ValueError(
            f"Project already initialized (manifest exists): {manifest_path}"
        )

    # Directory must be empty
    try:
        next(project_root.iterdir())
        raise ValueError(f"Project root is not empty: {project_root}")
    except StopIteration:
        pass  # directory is empty
