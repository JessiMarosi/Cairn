"""
Project initialization primitives.

This module defines the public interface for creating
new Cairn projects. No side effects are permitted at
import time.
"""

from dataclasses import dataclass
from pathlib import Path


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
    raise NotImplementedError("Project initialization not implemented yet.")
