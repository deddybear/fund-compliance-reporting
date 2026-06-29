from __future__ import annotations
from app.computation.models import ComputationResult
from app.narrative.models import FirewallResult
from app.narrative.rules import (
    CitationRule,
    MetricRule,
    NumberRule,
    StatusRule,
)


class NarrativeFirewall:
    """
    Validates LLM-generated narrative against deterministic
    computation results before publication.
    """

    def __init__(self) -> None:

        self._rules = [

            NumberRule(),

            MetricRule(),

            StatusRule(),

            CitationRule(),

        ]

    def validate(
        self,
        *,
        computation: ComputationResult,
        narrative: str,
    ) -> FirewallResult:
        """
        Execute every firewall rule.

        Returns
        -------
        FirewallResult
            Validation result containing any detected issues.
        """

        result = FirewallResult()

        for rule in self._rules:

            rule.validate(
                computation=computation,
                narrative=narrative,
                result=result,
            )

        return result

