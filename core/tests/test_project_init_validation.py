from __future__ import annotations

from pathlib import Path

import pytest

from cairn_core.projects.init import init_project


def test_init_project_rejects_nonexistent_root(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist"
    with pytest.raises(ValueError, match="Project root does not exist"):
        init_project(missing, "Cairn")


def test_init_project_rejects_file_path(tmp_path: Path) -> None:
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="Project root is not a directory"):
        init_project(file_path, "Cairn")


def test_init_project_rejects_empty_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="1–64 characters"):
        init_project(tmp_path, "")


def test_init_project_rejects_name_with_leading_space(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="cannot start or end with whitespace"):
        init_project(tmp_path, " Cairn")


def test_init_project_rejects_name_with_trailing_space(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="cannot start or end with whitespace"):
        init_project(tmp_path, "Cairn ")


def test_init_project_rejects_name_with_invalid_character(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="invalid characters"):
        init_project(tmp_path, "Cairn:Project")


def test_init_project_rejects_name_with_non_ascii(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="ASCII characters only"):
        init_project(tmp_path, "Cairné")


def test_init_project_rejects_non_empty_directory(tmp_path: Path) -> None:
    (tmp_path / "some_file.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="Project root is not empty"):
        init_project(tmp_path, "Cairn")


def test_init_project_rejects_existing_manifest(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    (cairn_dir / "manifest.yaml").write_text(
        "schema_version: '0.1.0'\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="manifest exists"):
        init_project(tmp_path, "Cairn")


def test_init_project_writes_manifest_when_valid(tmp_path: Path) -> None:
    # Arrange: empty directory + valid name
    project_root = tmp_path
    project_name = "My Project"

    # Act
    init_project(project_root, project_name)

    # Assert: manifest exists
    manifest_path = project_root / ".cairn" / "manifest.yaml"
    assert manifest_path.exists()
    assert manifest_path.is_file()
