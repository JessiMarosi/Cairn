from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from cairn_core.projects.context import ProjectContext
from cairn_core.projects.introspect import ProjectIntrospection


@dataclass(frozen=True)
class AnalysisMarkers:
    has_readme: bool
    has_pyproject: bool
    has_requirements: bool


@dataclass(frozen=True)
class ProjectAnalysis:
    project: ProjectContext
    introspection: ProjectIntrospection

    entry_count: int
    relative_paths: Tuple[str, ...]

    extension_counts: Dict[str, int]
    dir_counts: Dict[str, int]
    max_depth: int

    markers: AnalysisMarkers
