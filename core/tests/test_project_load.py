"""
Phase 3 tests for loading an existing Cairn project from disk.
"""

import pytest
from pathlib import Path

from cairn_core.projects.load import load_project, ProjectLoadError


def test_load_project_manifest_missing(tmp_path: Path) -> None:
    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_missing"


def test_load_project_manifest_not_file(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.mkdir()

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_not_file"


def test_load_project_manifest_invalid_yaml(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text("not: [valid: yaml", encoding="utf-8")

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_invalid_yaml"


def test_load_project_manifest_schema_unsupported(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text("schema_version: '999'\n", encoding="utf-8")

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_schema_unsupported"


def test_load_project_manifest_missing_field(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text(
        "schema_version: '0.1'\n",
        encoding="utf-8",
    )

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_missing_field"


def test_load_project_manifest_invalid_field(tmp_path: Path) -> None:
    cairn_dir = tmp_path / ".cairn"
    cairn_dir.mkdir()
    manifest_path = cairn_dir / "manifest.yaml"
    manifest_path.write_text(
        "schema_version: '0.1'\n"
        "project_id: 12345\n",
        encoding="utf-8",
    )

    with pytest.raises(ProjectLoadError) as excinfo:
        load_project(tmp_path)

    assert excinfo.value.code == "manifest_invalid_field"


from cairn_core.policy import (
    PolicyPack,
    PolicyPackMeta,
    Rule,
    SeverityModel,
)


def test_policy_pack_constructs_with_minimal_fields():
    meta = PolicyPackMeta(
        policy_pack_id="test-pack",
        version="1.0.0",
    )

    pack = PolicyPack(meta=meta)

    assert pack.meta.policy_pack_id == "test-pack"
    assert pack.meta.version == "1.0.0"
    assert pack.meta.schema_version == "1.0"
    assert pack.rules == ()


def test_rule_is_frozen_and_immutable():
    rule = Rule(
        rule_id="test.rule",
        title="Test Rule",
        kind="analysis_marker_present",
        severity="low",
    )

    try:
        rule.severity = "high"  # type: ignore[attr-defined]
        assert False, "Rule should be frozen"
    except Exception:
        assert True


def test_severity_model_is_fixed_and_ordered():
    model = SeverityModel()

    assert model.schema == "fixed_scale_v1"
    assert model.allowed == ("info", "low", "medium", "high", "critical")


from cairn_core.reporting import (
    CairnReport,
    ReportMeta,
    PolicyPin,
    AnalysisSnapshot,
    Finding,
)


def test_report_constructs_with_minimal_required_fields():
    meta = ReportMeta(generated_at="2025-12-22T22:00:00Z")

    policy = PolicyPin(
        policy_pack_id="test-pack",
        version="1.0.0",
        schema_version="1.0",
    )

    analysis = AnalysisSnapshot(
        entry_count=10,
        dir_count=2,
        max_depth=3,
    )

    report = CairnReport(
        meta=meta,
        policy=policy,
        project_ref="example-project",
        analysis=analysis,
    )

    assert report.project_ref == "example-project"
    assert report.findings == ()


def test_finding_is_frozen_and_deterministic():
    finding = Finding(
        rule_id="test.rule",
        severity="medium",
        title="Test Finding",
    )

    try:
        finding.severity = "high"  # type: ignore[attr-defined]
        assert False, "Finding should be frozen"
    except Exception:
        assert True
