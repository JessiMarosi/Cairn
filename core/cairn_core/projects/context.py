from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectContext:
    root: Path
    manifest_path: Path
    project_id: str
    schema_version: str
