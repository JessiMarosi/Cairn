"""
Phase 3 tests for loading an existing Cairn project from disk.
"""

import pytest
from pathlib import Path

from cairn_core.projects.load import load_project, ProjectLoadError


def test_load_project_manifest_missing(tmp_path: Path) -> None:
    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_missing"


def test_load_project_manifest_not_file(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.mkdir()

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_not_file"


def test_load_project_manifest_invalid_yaml(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text("not: [valid: yaml", encoding="utf-8")

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_invalid_yaml"


def test_load_project_manifest_schema_unsupported(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text("schema_version: '999'\n", encoding="utf-8")

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_schema_unsupported"


def test_load_project_manifest_missing_field(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text(
        "schema_version: '0.1'\n",
        encoding="utf-8",
    )

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_missing_field"


def test_load_project_manifest_invalid_field(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text(
        "schema_version: '0.1'\n"
        "project_id: 12345\n",
        encoding="utf-8",
    )

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_invalid_field"
