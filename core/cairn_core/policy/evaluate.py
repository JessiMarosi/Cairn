from __future__ import annotations

from typing import Tuple

from cairn_core.policy.schema import PolicyPack, Rule
from cairn_core.reporting.schema import AnalysisSnapshot, Evidence, Finding, RemediationLink, StandardsLink


class PolicyEvaluationError(Exception):
    """
    Phase 7 error base class.

    All Phase 7 evaluation-specific errors MUST derive from this type and expose a
    stable string code via .code.
    """
    code: str

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def evaluate_policy(policy: PolicyPack, analysis: AnalysisSnapshot) -> Tuple[Finding, ...]:
    """
    Phase 7 entrypoint.

    Must:
    - be deterministic and side-effect free
    - evaluate enabled rules only (policy is the authority)
    - return findings sorted deterministically (severity then rule_id)
    - never generate narrative text
    """
    raise NotImplementedError
