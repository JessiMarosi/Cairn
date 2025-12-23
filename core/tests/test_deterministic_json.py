import pytest

from cairn_core.serialization import to_json_str, SerializationError
from cairn_core.policy import PolicyPack, PolicyPackMeta
from cairn_core.reporting import (
    CairnReport,
    ReportMeta,
    PolicyPin,
    AnalysisSnapshot,
)


def test_json_is_deterministic_for_policy_pack():
    meta = PolicyPackMeta(policy_pack_id="x", version="1.0.0")
    pack = PolicyPack(meta=meta)

    s1 = to_json_str(pack)
    s2 = to_json_str(pack)

    assert s1 == s2
    assert s1.endswith("\n")


def test_json_is_deterministic_for_report():
    report = CairnReport(
        meta=ReportMeta(generated_at="2025-12-22T00:00:00Z"),
        policy=PolicyPin(policy_pack_id="x", version="1.0.0", schema_version="1.0"),
        project_ref="proj",
        analysis=AnalysisSnapshot(entry_count=1, dir_count=0, max_depth=0),
    )

    s1 = to_json_str(report)
    s2 = to_json_str(report)
    assert s1 == s2


def test_unsupported_type_raises_coded_error():
    class Bad:
        pass

    with pytest.raises(SerializationError) as excinfo:
        to_json_str({"x": Bad()})

    assert excinfo.value.code == "json_unsupported_type"


def test_non_string_key_raises_coded_error():
    with pytest.raises(SerializationError) as excinfo:
        to_json_str({1: "x"})  # type: ignore[dict-item]

    assert excinfo.value.code == "json_key_not_string"
