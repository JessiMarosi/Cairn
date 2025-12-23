from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, Tuple

# Keep report schema version explicit and finite.
ReportSchemaVersion = Literal["1.0"]

# Reuse the same finite severity scale as policy.
Severity = Literal["info", "low", "medium", "high", "critical"]


@dataclass(frozen=True)
class ReportMeta:
    """
    Report identity. This must be sufficient for audit reproducibility.

    NOTE:
    - generated_at is a string to avoid timezone/serialization drift.
    - tool_version is optional until we pin it in Phase 10/11.
    """
    report_schema_version: ReportSchemaVersion = "1.0"
    generated_at: Optional[str] = None     # ISO-8601 string, e.g. "2025-12-22T22:15:03-05:00"
    tool_version: Optional[str] = None     # e.g., "0.6.0"


@dataclass(frozen=True)
class PolicyPin:
    """
    Policy identity and pinning info included with every report.
    content_hash may be None until Phase 10 computes/locks it.
    """
    policy_pack_id: str
    version: str
    schema_version: str                   # e.g., "1.0"
    content_hash_alg: Literal["sha256"] = "sha256"
    content_hash: Optional[str] = None


@dataclass(frozen=True)
class AnalysisSnapshot:
    """
    Snapshot of deterministic Phase 5 analysis outputs.
    Keep this stable and conservative: counts, paths, markers, depth.

    IMPORTANT:
    - relative paths only (no absolute paths) to improve portability.
    - do not include file contents.
    """
    entry_count: int
    dir_count: int
    max_depth: int

    # relative paths
    files: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ()

    # extension -> count (store as plain dict; JSON-friendly)
    ext_counts: Dict[str, int] = field(default_factory=dict)

    # markers (deterministic booleans)
    has_readme: bool = False
    has_pyproject: bool = False
    has_requirements: bool = False

    # explicit note that .cairn rules were respected (Phase 5 guarantee)
    cairn_aware: bool = True


@dataclass(frozen=True)
class Evidence:
    """
    Deterministic evidence payload.
    Keys should be stable and documented by the rule kind.

    Examples:
      {"marker": "README", "present": False}
      {"ext": ".py", "count": 12, "min_required": 1}
    """
    items: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RemediationLink:
    """
    Links a finding to a curated remediation project (Phase 8).
    """
    project_id: str
    safe_by_default: bool = True
    dry_run_supported: bool = True


@dataclass(frozen=True)
class StandardsLink:
    """
    Standards metadata only; never used as decision logic.
    """
    scheme: str        # e.g. "NIST", "CIS", "ISO27001", "OWASP"
    ref: str           # e.g. "CIS 1.1"
    url: Optional[str] = None


@dataclass(frozen=True)
class Finding:
    """
    A single deterministic policy outcome.

    No free-form recommendation text.
    Any friendly explanation belongs to Phase 9 (explain-only).
    """
    rule_id: str
    severity: Severity
    title: str

    # Deterministic evidence for audit/replay
    evidence: Evidence = Evidence()

    # Optional remediation references (curated)
    remediation: Tuple[RemediationLink, ...] = ()

    # Optional standards metadata
    standards: Tuple[StandardsLink, ...] = ()

    # Stable, controlled rationale field (factual, not narrative)
    rationale: str = ""


@dataclass(frozen=True)
class CairnReport:
    """
    The canonical report artifact for Phase 6+.

    - policy pinning required
    - analysis snapshot required
    - findings may be empty (e.g., “no issues”)
    """
    meta: ReportMeta
    policy: PolicyPin

    # "project_ref" is a display-safe identifier (relative path, repo name, etc.)
    project_ref: str

    analysis: AnalysisSnapshot
    findings: Tuple[Finding, ...] = ()
