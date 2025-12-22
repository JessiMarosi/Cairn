from __future__ import annotations

from pathlib import Path

import pytest

from cairn_core.projects.analyze import analyze_project


def test_analyze_propagates_phase3_errors(tmp_path: Path) -> None:
    """
    Phase 5 must enforce the Phase 3 gate.
    If the project is invalid (e.g., missing manifest), the Phase 3 error must propagate unchanged.
    """
    with pytest.raises(Exception) as excinfo:
        analyze_project(tmp_path)

    err = excinfo.value
    assert hasattr(err, "code"), (
        f"Expected a Phase 3-style exception with .code, got: {type(err)!r}"
    )
    assert err.code == "manifest_missing"


def test_analyze_returns_projectanalysis_for_valid_project(tmp_path: Path) -> None:
    """
    For a valid project, Phase 5 must return a ProjectAnalysis object.
    """
    from cairn_core.projects.init import init_project
    from cairn_core.projects.analysis import ProjectAnalysis

    init_project(tmp_path, "test-project")

    analysis = analyze_project(tmp_path)
    assert isinstance(analysis, ProjectAnalysis)
