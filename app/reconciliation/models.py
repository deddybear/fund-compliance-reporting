from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExpectedFigure:
    """
    Expected figure loaded from the answer key.
    """
    metric_mapping: str
    section: str
    metric: str
    value: Decimal
    limit: str
    utilization: str
    status: str

@dataclass(frozen=True)
class ReconciliationItem:
    """
    Comparison between expected and actual figure.
    """

    section: str

    figure: str

    expected_value: Decimal
    actual_value: Decimal

    expected_status: str
    actual_status: str

    matched: bool

    difference: Decimal

@dataclass(frozen=True)
class ReconciliationResult:
    """
    Result of reconciliation process.
    """

    items: list[ReconciliationItem]

    @property
    def passed(self) -> bool:
        """
        True if every figure matched.
        """

        return all(
            item.matched
            for item in self.items
        )

    @property
    def failed(self) -> bool:
        """
        True if any figure failed reconciliation.
        """

        return not self.passed

    @property
    def matched_count(self) -> int:
        """
        Number of matched figures.
        """

        return sum(
            1
            for item in self.items
            if item.matched
        )

    @property
    def failed_count(self) -> int:
        """
        Number of unmatched figures.
        """

        return sum(
            1
            for item in self.items
            if not item.matched
        )
