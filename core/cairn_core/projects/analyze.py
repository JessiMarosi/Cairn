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

    # ---- extension_counts ----
    ext_counter: Counter[str] = Counter()
    for rel in relative_paths:
        full_path = root / Path(rel)
        if not full_path.is_file():
            continue

        suffix = Path(rel).suffix.lower()
        ext_counter[suffix] += 1

    # ---- dir_counts ----
    dir_counter: Counter[str] = Counter()
    for rel in relative_paths:
        full_path = root / Path(rel)
        if not full_path.is_file():
            continue

        # Normalize for Windows paths
        rel_norm = rel.replace("\\", "/")

        # Exclude Cairn internal metadata
        if rel_norm.startswith(".cairn/"):
            continue

        # Group files by top-level directory; root files count under ""
        head, sep, _tail = rel_norm.partition("/")
        top = "" if sep == "" else head
        dir_counter[top] += 1

    # ---- max_depth ----
    max_depth = 0
    for rel in relative_paths:
        full_path = root / Path(rel)
        if not full_path.is_file():
            continue

        # Normalize for Windows paths
        rel_norm = rel.replace("\\", "/")

        # Exclude Cairn internal metadata
        if rel_norm.startswith(".cairn/"):
            continue

        # Depth = number of directories in the relative path
        parts = rel_norm.split("/")
        depth = len(parts) - 1  # root file => 0
        if depth > max_depth:
            max_depth = depth

    # ---- markers ----
    has_readme = False
    has_pyproject = False
    has_requirements = False

    for rel in relative_paths:
        rel_norm = rel.replace("\\", "/")

        # Ignore internal metadata
        if rel_norm == ".cairn" or rel_norm.startswith(".cairn/"):
            continue

        # Only root-level files count for markers
        if "/" in rel_norm:
            continue

        name = rel_norm.lower()

        if name == "pyproject.toml":
            has_pyproject = True
        elif name == "requirements.txt":
            has_requirements = True
        else:
            # README.* at root (case-insensitive)
            if name.startswith("readme") and (len(name) == 6 or name[6] == "."):
                has_readme = True

    markers = AnalysisMarkers(
        has_readme=has_readme,
        has_pyproject=has_pyproject,
        has_requirements=has_requirements,
    )

    return ProjectAnalysis(
        project=project,
        introspection=intro,
        entry_count=intro.entry_count,
        relative_paths=relative_paths,
        extension_counts=dict(ext_counter),
        dir_counts=dict(dir_counter),
        max_depth=max_depth,
        markers=markers,
    )
