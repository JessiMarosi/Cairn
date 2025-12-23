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


def test_analyze_dir_counts_by_top_level_dir(tmp_path: Path) -> None:
    """
    Phase 5 Step 31:
    dir_counts counts FILES grouped by top-level directory.

    Rules:
    - Root files count under "".
    - Nested files count under their first path segment.
    - Deterministic (same result each run).
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    # Root files
    (tmp_path / "root1.txt").write_text("x", encoding="utf-8")
    (tmp_path / "root2").write_text("x", encoding="utf-8")

    # Nested files
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "sub").mkdir()
    (tmp_path / "docs" / "sub" / "b.md").write_text("x", encoding="utf-8")

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "pkg").mkdir()
    (tmp_path / "src" / "pkg" / "mod.py").write_text("x", encoding="utf-8")

    analysis1 = analyze_project(tmp_path)
    analysis2 = analyze_project(tmp_path)

    expected = {
        "": 2,      # root1.txt, root2
        "docs": 2,  # docs/a.md, docs/sub/b.md
        "src": 2,   # src/main.py, src/pkg/mod.py
    }

    assert analysis1.dir_counts == expected
    assert analysis2.dir_counts == expected
