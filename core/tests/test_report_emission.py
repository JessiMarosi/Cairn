from cairn_core.reporting import (
    CairnReport,
    ReportMeta,
    PolicyPin,
    AnalysisSnapshot,
    Finding,
    Evidence,
    render_report_text,
    write_report_json,
    write_report_text,
)
from cairn_core.serialization import to_json_str


def _base_report(findings=()):
    return CairnReport(
        meta=ReportMeta(generated_at="2025-12-22T00:00:00Z", tool_version="0.6.0"),
        policy=PolicyPin(policy_pack_id="pack", version="1.0.0", schema_version="1.0"),
        project_ref="proj",
        analysis=AnalysisSnapshot(
            entry_count=3,
            dir_count=1,
            max_depth=2,
            ext_counts={".py": 2, ".md": 1},
            has_readme=True,
            has_pyproject=False,
            has_requirements=False,
        ),
        findings=findings,
    )


def test_render_report_text_is_deterministic():
    r = _base_report()
    s1 = render_report_text(r)
    s2 = render_report_text(r)
    assert s1 == s2


def test_render_report_text_sorts_ext_counts():
    r = _base_report()
    s = render_report_text(r)
    # .md should appear before .py
    md_idx = s.find("  .md:")
    py_idx = s.find("  .py:")
    assert md_idx != -1 and py_idx != -1
    assert md_idx < py_idx


def test_render_report_text_sorts_findings_deterministically():
    f1 = Finding(rule_id="b.rule", severity="low", title="B", evidence=Evidence({"x": 1}))
    f2 = Finding(rule_id="a.rule", severity="high", title="A", evidence=Evidence({"x": 2}))
    f3 = Finding(rule_id="c.rule", severity="high", title="C", evidence=Evidence({"x": 3}))
    r = _base_report(findings=(f1, f2, f3))

    s = render_report_text(r)

    # High severity should come first; within same severity rule_id sorts ascending.
    first = s.find("rule_id: a.rule")
    second = s.find("rule_id: c.rule")
    third = s.find("rule_id: b.rule")
    assert first != -1 and second != -1 and third != -1
    assert first < second < third


def test_write_report_json_matches_serializer(tmp_path):
    r = _base_report()
    out = tmp_path / "report.json"
    write_report_json(r, out)

    assert out.read_text(encoding="utf-8").endswith("\n")
    assert out.read_text(encoding="utf-8") == to_json_str(r)


def test_write_report_text_writes_utf8_and_newline(tmp_path):
    r = _base_report()
    out = tmp_path / "report.txt"
    write_report_text(r, out)

    data = out.read_text(encoding="utf-8")
    assert data.endswith("\n")
    assert "CAIRN REPORT" in data
    assert "POLICY" in data
    assert "ANALYSIS" in data
    assert "FINDINGS" in data
