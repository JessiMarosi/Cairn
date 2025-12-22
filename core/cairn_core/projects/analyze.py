from __future__ import annotations

from pathlib import Path

from cairn_core.projects.analysis import AnalysisMarkers, ProjectAnalysis
from cairn_core.projects.introspect import introspect_project
from cairn_core.projects.load import load_project


def analyze_project(root: Path) -> ProjectAnalysis:
    """
    Phase 5 entrypoint (partial).

    Must:
    - enforce Phase 3 + Phase 4 gates
    - be deterministic and side-effect free
    - return ProjectAnalysis
    """
    project = load_project(root)
    intro = introspect_project(root)

    # Minimal deterministic derived fields (will be fully tested/expanded in later steps).
    relative_paths = tuple(intro.relative_paths)

    markers = AnalysisMarkers(
        has_readme=False,
        has_pyproject=False,
        has_requirements=False,
    )

    return ProjectAnalysis(
        project=project,
        introspection=intro,
        entry_count=intro.entry_count,
        relative_paths=relative_paths,
        extension_counts={},
        dir_counts={},
        max_depth=0,
        markers=markers,
    )
