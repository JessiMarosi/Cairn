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
