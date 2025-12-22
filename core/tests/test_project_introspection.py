from __future__ import annotations

import pytest

from cairn_core.projects.introspect import introspect_project


def test_introspect_propagates_phase3_errors(tmp_path):
    """
    Phase 4 must enforce the Phase 3 gate.
    If the project is invalid (e.g., missing manifest), the Phase 3 error must propagate unchanged.
    """
    with pytest.raises(Exception) as excinfo:
        introspect_project(tmp_path)

    err = excinfo.value
    assert hasattr(err, "code"), (
        f"Expected a Phase 3-style exception with .code, got: {type(err)!r}"
    )
    assert err.code == "manifest_missing"


def test_introspect_stub_raises_not_implemented_on_valid_project(tmp_path):
    """
    For a valid project, Phase 4 currently stubs and must raise NotImplementedError
    (until traversal is implemented).
    """
    from cairn_core.projects.init import init_project

    # Phase 2 init signature is: (path, name, *, force=False)
    init_project(tmp_path, "test-project")

    with pytest.raises(NotImplementedError):
        introspect_project(tmp_path)
