from __future__ import annotations

import pytest

from cairn_core.projects.introspect import ProjectIntrospection, introspect_project


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


def test_introspect_returns_project_introspection_on_valid_project(tmp_path):
    """
    Phase 4 Step 8: first real behavior.
    For a valid project, introspect_project must return ProjectIntrospection
    (and must NOT raise NotImplementedError).
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    # Contract check: public API advertises ProjectIntrospection return type.
    # With `from __future__ import annotations`, this may be stored as a string.
    assert introspect_project.__annotations__.get("return") in (
        "ProjectIntrospection",
        ProjectIntrospection,
    )

    result = introspect_project(tmp_path)
    assert isinstance(result, ProjectIntrospection)


def test_introspect_depth_exceeded_is_error(tmp_path):
    """
    Spec: If visiting an entry would exceed MAX_DEPTH, introspection MUST fail with
    code 'introspection_scan_limit_exceeded'.
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    # Build a nested directory chain deeper than MAX_DEPTH (25).
    # root is depth 0; a child under root is depth 1.
    cur = tmp_path
    for i in range(27):  # deterministic exceed
        cur = cur / f"d{i}"
        cur.mkdir()

    with pytest.raises(Exception) as excinfo:
        introspect_project(tmp_path)

    err = excinfo.value
    assert hasattr(err, "code")
    assert err.code == "introspection_scan_limit_exceeded"


def test_introspect_symlink_is_error(tmp_path):
    """
    Spec: Symlinks must be rejected immediately (fail-fast) with
    code 'introspect_symlink_detected'.

    NOTE (Windows): Creating symlinks may require Developer Mode or admin privileges.
    If symlink creation is not permitted, the test is skipped.
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    target = tmp_path / "real_dir"
    target.mkdir()
    link = tmp_path / "link_dir"

    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as e:
        pytest.skip(f"Symlink creation not permitted on this system: {e}")

    with pytest.raises(Exception) as excinfo:
        introspect_project(tmp_path)

    err = excinfo.value
    assert hasattr(err, "code")
    assert err.code == "introspect_symlink_detected"


def test_introspect_records_entry_count(tmp_path):
    """
    Step 12: Introspection must record a deterministic count of visited entries.

    We only assert the count is a positive integer (exact value may evolve).
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    result = introspect_project(tmp_path)

    assert isinstance(result.entry_count, int)
    assert result.entry_count > 0


def test_introspect_records_sorted_relative_paths(tmp_path):
    """
    Step 13/14/16: Introspection must expose deterministic traversal order as relative paths,
    sorted lexicographically, MUST NOT include the project root itself ("."),
    and must not contain duplicates.
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    # Create deterministic entries to assert ordering against.
    (tmp_path / "z.txt").write_text("z", encoding="utf-8")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "m").mkdir()
    (tmp_path / "m" / "b.txt").write_text("b", encoding="utf-8")

    result = introspect_project(tmp_path)

    rels = result.relative_paths
    assert isinstance(rels, list)
    assert all(isinstance(x, str) for x in rels)

    # Root must NOT appear
    assert "." not in rels

    expected_subset = ["a.txt", "m", "m/b.txt", "z.txt"]
    for p in expected_subset:
        assert p in rels

    # Global deterministic ordering
    assert rels == sorted(rels)

    # No duplicates
    assert len(rels) == len(set(rels))


def test_introspect_excludes_dunder_pycache(tmp_path):
    """
    Step 17: Introspection must exclude __pycache__ directories and their contents.
    """
    from cairn_core.projects.init import init_project

    init_project(tmp_path, "test-project")

    cache_dir = tmp_path / "__pycache__"
    cache_dir.mkdir()
    (cache_dir / "junk.pyc").write_bytes(b"\x00\x01\x02")

    result = introspect_project(tmp_path)

    assert "__pycache__" not in result.relative_paths
    assert "__pycache__/junk.pyc" not in result.relative_paths
