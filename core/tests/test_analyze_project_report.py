from __future__ import annotations

from pathlib import Path

from cairn_core.projects.analyze import analyze_project, analyze_project_report
from cairn_core.projects.init import init_project
from cairn_core.reporting.build import build_report_from_analysis
from cairn_core.serialization import to_json_str


def test_analyze_project_report_matches_builder(tmp_path: Path) -> None:
    init_project(tmp_path, "test-project")

    analysis = analyze_project(tmp_path)
    expected = build_report_from_analysis(analysis)

    actual = analyze_project_report(tmp_path)

    assert to_json_str(actual) == to_json_str(expected)
