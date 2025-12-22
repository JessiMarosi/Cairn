from __future__ import annotations

from collections import Counter
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

    relative_paths = tuple(intro.relative_paths)

    ext_counter: Counter[str] = Counter()
    for rel in relative_paths:
        full_path = root / Path(rel)
        if not full_path.is_file():
            continue

        suffix = Path(rel).suffix.lower()
        ext_counter[suffix] += 1

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
        extension_counts=dict(ext_counter),
        dir_counts={},
        max_depth=0,
        markers=markers,
    )
