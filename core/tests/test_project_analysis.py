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


def test_analyze_extension_counts(tmp_path: Path) -> None:
    """
    Phase 5 must compute extension_counts deterministically.

    Rules:
    - Use the last suffix (Path.suffix), lowercased.
    - Files with no suffix use "" as the key.
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    (tmp_path / "readme.MD").write_text("x", encoding="utf-8")
    (tmp_path / "script.py").write_text("x", encoding="utf-8")
    (tmp_path / "archive.tar.gz").write_text("x", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("x", encoding="utf-8")

    analysis = analyze_project(tmp_path)

    assert analysis.extension_counts[".md"] == 1
    assert analysis.extension_counts[".py"] == 1
    assert analysis.extension_counts[".gz"] == 1
    assert analysis.extension_counts[""] == 1
