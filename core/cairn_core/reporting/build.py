from __future__ import annotations

from pathlib import Path

from cairn_core.projects.analysis import ProjectAnalysis
from cairn_core.reporting.schema import (
    AnalysisSnapshot,
    CairnReport,
    PolicyPin,
    ReportMeta,
)

# Deterministic placeholders (no CLI yet; no runtime timestamps)
_DETERMINISTIC_GENERATED_AT = "1970-01-01T00:00:00Z"


def build_report_from_analysis(analysis: ProjectAnalysis) -> CairnReport:
    """
    Phase 6 Step 5: deterministic mapping from Phase 5 ProjectAnalysis
    to Phase 6 CairnReport.

    Constraints:
    - No policy evaluation (Phase 7 responsibility)
    - No dynamic timestamps or environment-dependent values
    - No narrative or free-form advisory text
    """
    meta = ReportMeta(
        generated_at=_DETERMINISTIC_GENERATED_AT,
        tool_version=None,
    )

    policy = PolicyPin(
        policy_pack_id="unassigned",
        version="0.0.0",
        schema_version="1.0",
        content_hash_alg="sha256",
        content_hash=None,
    )

    intro = analysis.introspection

    rels = tuple(intro.relative_paths)

    files = tuple(p for p in rels if "." in Path(p).name)
    dirs = tuple(p for p in rels if "." not in Path(p).name)

    snapshot = AnalysisSnapshot(
        entry_count=analysis.entry_count,
        dir_count=len(dirs),
        max_depth=analysis.max_depth,
        files=files,
        dirs=dirs,
        ext_counts=dict(analysis.extension_counts),
        has_readme=analysis.markers.has_readme,
        has_pyproject=analysis.markers.has_pyproject,
        has_requirements=analysis.markers.has_requirements,
        cairn_aware=True,
    )

    # Display-safe identifier. Deterministic and environment-independent.
    project_ref = analysis.project.project_id

    return CairnReport(
        meta=meta,
        policy=policy,
        project_ref=project_ref,
        analysis=snapshot,
        findings=(),
    )
