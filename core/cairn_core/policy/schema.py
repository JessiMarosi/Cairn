from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple


# -----------------------------
# Core primitives (locked)
# -----------------------------

SchemaVersion = Literal["1.0"]

# Severity is deterministic and finite — no arbitrary strings.
Severity = Literal["info", "low", "medium", "high", "critical"]

# Rule behavior must be conservative and bounded.
RuleKind = Literal[
    # Static checks against Phase 5 analysis outputs:
    "analysis_marker_present",
    "analysis_marker_missing",
    "analysis_extension_count_at_least",
    "analysis_extension_count_at_most",
    "analysis_max_depth_at_most",
    "analysis_dir_count_at_least",
    "analysis_entry_count_at_most",
]

# Optional: policy “target environments” (not per-user personalization).
TargetEnv = Literal["general", "enterprise", "regulated", "high_security"]


@dataclass(frozen=True)
class StandardsRef:
    """
    References an external standard/control. This is metadata only; it must NOT change decisions.
    """
    scheme: str  # e.g., "NIST", "CIS", "ISO27001", "OWASP"
    ref: str     # e.g., "NIST SP 800-53: AC-2"
    url: Optional[str] = None


@dataclass(frozen=True)
class JurisdictionScope:
    """
    High-level scope metadata to support 'lawful by construction' constraints.
    This must remain broad: do not encode legal advice, only applicability boundaries.
    """
    regions: Tuple[str, ...] = ()      # e.g., ("US", "EU")
    excluded_regions: Tuple[str, ...] = ()
    notes: Optional[str] = None        # e.g., "General guidance; consult counsel for local law."


@dataclass(frozen=True)
class RemediationRef:
    """
    Points to a curated remediation project (Phase 8) by stable ID.
    """
    project_id: str                    # e.g., "remediate/add_readme"
    safe_by_default: bool = True       # non-destructive default
    dry_run_supported: bool = True


@dataclass(frozen=True)
class Rule:
    """
    Deterministic policy rule definition.

    - No code execution embedded here.
    - 'params' is constrained by 'kind' (validated later in Phase 7).
    - 'recommendation' is NOT free-form; it must be a short, controlled string.
      If you want richer wording, that belongs to Phase 9 (explain-only layer).
    """
    rule_id: str                       # stable unique ID, e.g., "proj.readme.required"
    title: str                         # short, human-readable
    kind: RuleKind
    severity: Severity

    # Deterministic gating:
    enabled: bool = True
    target_envs: Tuple[TargetEnv, ...] = ("general",)

    # Parameters for the rule kind (validated later):
    params: Dict[str, Any] = field(default_factory=dict)

    # Controlled remediation linkage:
    remediation: Tuple[RemediationRef, ...] = ()

    # Standards metadata (non-decision):
    standards: Tuple[StandardsRef, ...] = ()

    # Audit fields:
    rationale: str = ""                # factual justification, not narrative
    references: Tuple[str, ...] = ()   # internal doc refs, ticket refs, etc.


@dataclass(frozen=True)
class SeverityModel:
    """
    Defines the severity scale and any deterministic normalization rules.
    """
    schema: Literal["fixed_scale_v1"] = "fixed_scale_v1"
    allowed: Tuple[Severity, ...] = ("info", "low", "medium", "high", "critical")


@dataclass(frozen=True)
class PolicyPackMeta:
    """
    Identity + provenance. Must be sufficient for audit pinning.
    """
    policy_pack_id: str                # stable identifier, e.g., "cairn-default"
    version: str                       # semver-like string, e.g., "1.2.0"
    schema_version: SchemaVersion = "1.0"

    published_date: Optional[str] = None   # ISO date string "YYYY-MM-DD"
    author: Optional[str] = None
    description: Optional[str] = None

    jurisdiction: JurisdictionScope = JurisdictionScope()
    standards_profile: Tuple[StandardsRef, ...] = ()

    # Compatibility:
    min_cairn_version: Optional[str] = None

    # Audit pinning:
    content_hash_alg: Literal["sha256"] = "sha256"
    content_hash: Optional[str] = None     # computed at load time later (Phase 10)


@dataclass(frozen=True)
class PolicyPack:
    """
    Full policy pack. This is the central decision authority input.
    """
    meta: PolicyPackMeta
    severity_model: SeverityModel = SeverityModel()
    rules: Tuple[Rule, ...] = ()
