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


def introspect_project(root: Path) -> ProjectIntrospection:
    # Phase 3 gate: MUST run first; errors propagate unchanged.
    project = load_project(root)

    # Stub until traversal is implemented in later steps.
    raise NotImplementedError
