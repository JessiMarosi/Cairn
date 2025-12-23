from __future__ import annotations

import pytest

from cairn_core.policy.evaluate import evaluate_policy
from cairn_core.policy.schema import PolicyPack, PolicyPackMeta
from cairn_core.reporting.schema import AnalysisSnapshot


def test_evaluate_policy_stub_raises_not_implemented_on_valid_inputs() -> None:
    policy = PolicyPack(
        meta=PolicyPackMeta(policy_pack_id="test-pack", version="0.0.1"),
        rules=(),
    )

    analysis = AnalysisSnapshot(
        entry_count=0,
        dir_count=0,
        max_depth=0,
        files=(),
        dirs=(),
        ext_counts={},
        has_readme=False,
        has_pyproject=False,
        has_requirements=False,
        cairn_aware=True,
    )

    with pytest.raises(NotImplementedError):
        evaluate_policy(policy, analysis)
