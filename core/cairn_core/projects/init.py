"""
Project initialization primitives.

This module defines the public interface for creating
new Cairn projects. No side effects are permitted at
import time.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import uuid

import yaml


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


def _utc_now_iso8601() -> str:
    """Return current UTC time as ISO-8601 string with 'Z' and no microseconds."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
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

    Phase 2: creates `.cairn/` and writes `.cairn/manifest.yaml`.
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

    # Phase 2 filesystem writes
    cairn_dir = project_root / ".cairn"
    cairn_dir.mkdir(parents=True, exist_ok=False)

    manifest: dict[str, Any] = {
        "schema_version": "0.1",
        "project_id": str(uuid.uuid4()),
        "name": name,
        "created_at": _utc_now_iso8601(),
        "created_by": None,
        "tool": {
            "name": "cairn",
            "version": "0.0.0-dev",
        },
    }

    manifest_yaml = yaml.safe_dump(
        manifest,
        sort_keys=False,
        default_flow_style=False,
        indent=2,
    )

    (cairn_dir / "manifest.yaml").write_text(manifest_yaml, encoding="utf-8")

    return ProjectContext(
        root=project_root,
        name=name,
        schema_version=manifest["schema_version"],
        created_at=manifest["created_at"],
    )
