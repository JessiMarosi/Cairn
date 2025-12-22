from __future__ import annotations

from pathlib import Path

from cairn_core.projects.load import load_project


def introspect_project(root: Path):
    """
    Phase 4 public API.

    This stub intentionally enforces the Phase 3 gate (load_project) and
    defers introspection implementation until subsequent steps.
    """
    # Phase 3 is the authoritative gate; propagate its errors unchanged.
    load_project(root)

    raise NotImplementedError("Phase 4 introspection is not implemented yet.")
