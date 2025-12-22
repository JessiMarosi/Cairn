from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from cairn_core.projects.context import ProjectContext


@dataclass(frozen=True, slots=True)
class ProjectLoadError(Exception):
    code: str
    message: str
    cause: Exception | None = None

    def __str__(self) -> str:
        return self.message


def load_project(root: Path) -> ProjectContext:
    manifest_path = root / ".cairn" / "manifest.yaml"

    if not manifest_path.exists():
        raise ProjectLoadError(
            code="manifest_missing",
            message="Project manifest not found at .cairn/manifest.yaml",
        )

    if not manifest_path.is_file():
        raise ProjectLoadError(
            code="manifest_not_file",
            message="Project manifest path is not a file",
        )

    try:
        raw = manifest_path.read_text(encoding="utf-8")
        _data = yaml.safe_load(raw)
    except Exception as e:  # noqa: BLE001
        raise ProjectLoadError(
            code="manifest_invalid_yaml",
            message="Project manifest is not valid YAML",
            cause=e,
        ) from e

    if not isinstance(_data, dict):
        raise NotImplementedError

    schema_version = _data.get("schema_version")
    if schema_version != "0.1":
        raise ProjectLoadError(
            code="manifest_schema_unsupported",
            message="Unsupported manifest schema_version",
        )

    # Missing required field check (must happen before type validation)
    if _data.get("project_id") is None:
        raise ProjectLoadError(
            code="manifest_missing_field",
            message="Missing required manifest field: project_id",
        )

    # Invalid field (project_id must be a string)
    if not isinstance(_data.get("project_id"), str):
        raise ProjectLoadError(
            code="manifest_invalid_field",
            message="Invalid manifest field: project_id",
        )

    return ProjectContext(
        root=root,
        manifest_path=manifest_path,
        project_id=_data["project_id"],
        schema_version=_data["schema_version"],
    )
