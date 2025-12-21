from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectLoadError(Exception):
    code: str
    message: str
    cause: Exception | None = None

    def __str__(self) -> str:
        return self.message


def load_project(root: Path):
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

    raise NotImplementedError
