from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Tuple

from cairn_core.reporting.schema import CairnReport, Finding
from cairn_core.serialization import to_json_bytes


# Deterministic severity ordering (lowest -> highest)
_SEV_ORDER = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _sort_findings(findings: Tuple[Finding, ...]) -> Tuple[Finding, ...]:
    # Deterministic: sort by severity (descending), then rule_id, then title
    return tuple(
        sorted(
            findings,
            key=lambda f: (-_SEV_ORDER.get(f.severity, 99), f.rule_id, f.title),
        )
    )


def render_report_text(report: CairnReport) -> str:
    """
    Deterministic, non-improvisational, human-readable rendering.

    Rules:
    - fixed section order
    - stable sorting
    - no free-form advice, no creative language
    """
    findings = _sort_findings(report.findings)

    lines: list[str] = []

    # Header
    lines.append("CAIRN REPORT")
    lines.append(f"schema_version: {report.meta.report_schema_version}")
    lines.append(f"generated_at: {report.meta.generated_at or ''}")
    lines.append(f"tool_version: {report.meta.tool_version or ''}")
    lines.append("")

    # Policy pin
    lines.append("POLICY")
    lines.append(f"policy_pack_id: {report.policy.policy_pack_id}")
    lines.append(f"version: {report.policy.version}")
    lines.append(f"schema_version: {report.policy.schema_version}")
    lines.append(f"content_hash_alg: {report.policy.content_hash_alg}")
    lines.append(f"content_hash: {report.policy.content_hash or ''}")
    lines.append("")

    # Project ref
    lines.append("PROJECT")
    lines.append(f"project_ref: {report.project_ref}")
    lines.append("")

    # Analysis snapshot
    a = report.analysis
    lines.append("ANALYSIS")
    lines.append(f"entry_count: {a.entry_count}")
    lines.append(f"dir_count: {a.dir_count}")
    lines.append(f"max_depth: {a.max_depth}")
    lines.append(f"has_readme: {a.has_readme}")
    lines.append(f"has_pyproject: {a.has_pyproject}")
    lines.append(f"has_requirements: {a.has_requirements}")
    lines.append(f"cairn_aware: {a.cairn_aware}")

    # ext_counts: stable ordering by extension
    lines.append("ext_counts:")
    for ext in sorted(a.ext_counts.keys()):
        lines.append(f"  {ext}: {a.ext_counts[ext]}")
    lines.append("")

    # Findings
    lines.append("FINDINGS")
    lines.append(f"count: {len(findings)}")
    lines.append("")

    if not findings:
        lines.append("(none)")
        lines.append("")
        return "\n".join(lines)

    for idx, f in enumerate(findings, start=1):
        lines.append(f"[{idx}] rule_id: {f.rule_id}")
        lines.append(f"    severity: {f.severity}")
        lines.append(f"    title: {f.title}")
        lines.append(f"    rationale: {f.rationale}")

        # evidence: stable ordering by key
        ev = f.evidence.items
        lines.append("    evidence:")
        for k in sorted(ev.keys()):
            lines.append(f"      {k}: {ev[k]}")

        # remediation: stable ordering by project_id
        lines.append("    remediation:")
        if f.remediation:
            for r in sorted(f.remediation, key=lambda x: x.project_id):
                lines.append(
                    f"      - project_id: {r.project_id} | safe_by_default: {r.safe_by_default} | dry_run_supported: {r.dry_run_supported}"
                )
        else:
            lines.append("      (none)")

        # standards: stable ordering by (scheme, ref)
        lines.append("    standards:")
        if f.standards:
            for s in sorted(f.standards, key=lambda x: (x.scheme, x.ref)):
                lines.append(f"      - {s.scheme}: {s.ref}" + (f" | {s.url}" if s.url else ""))
        else:
            lines.append("      (none)")

        lines.append("")

    return "\n".join(lines)


def write_report_json(report: CairnReport, path: str | Path) -> None:
    """
    Deterministic JSON emission (single-authority serializer).
    """
    p = Path(path)
    p.write_bytes(to_json_bytes(report))


def write_report_text(report: CairnReport, path: str | Path) -> None:
    """
    Deterministic text emission (UTF-8, newline normalized).
    """
    p = Path(path)
    text = render_report_text(report)
    if not text.endswith("\n"):
        text += "\n"
    p.write_text(text, encoding="utf-8", newline="\n")
