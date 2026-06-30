from __future__ import annotations
from decimal import Decimal
from typing import Any
from app.computation.models import FigureResult
from collections import defaultdict 
from collections.abc import Callable
from app.holdings.models import Holding


class BaseCalculator:
    """
    Base class for all computation calculators.
    """

    @staticmethod
    def total_market_value(
        holdings: list[Holding],
    ) -> Decimal:
        """
        Calculate the total market value of the portfolio.
        """
        return sum(
            (
                holding.market_value_sgd
                for holding in holdings
            ),
            start=Decimal("0"),
        )

    @staticmethod
    def to_decimal(
        value: Any,
    ) -> Decimal | None:
        """
        Convert a value to Decimal.
        """
        if value is None:
            return None

        return Decimal(str(value))

    @staticmethod
    def format_limit(
        minimum: Decimal | None,
        maximum: Decimal | None,
    ) -> str:
        """
        Format limit for reporting.
        """

        if minimum is not None and maximum is not None:
            return f"{minimum}–{maximum}%"

        if minimum is not None:
            return f"≥ {minimum}%"

        if maximum is not None:
            return f"≤ {maximum}%"

        return "-"

    def build_result(
        self,
        *,
        metric_id: str,
        section: str,
        figure: str,
        value: Decimal,
        minimum: Decimal | None,
        maximum: Decimal | None,
        status: str,
        graph_path: None,
        citation: str = "",
        utilization: Decimal | None = None,
    ) -> FigureResult:
        """
        Build a standardized FigureResult.
        """

        return FigureResult(
            metric_id=metric_id,
            section=section,
            figure=figure,
            value=value,
            limit=self.format_limit(
                minimum,
                maximum,
            ),
            minimum=minimum,
            maximum=maximum,
            status=status,
            graph_path=graph_path,
            citation=citation,
            utilization=utilization,
        )

    @staticmethod
    def calculate_percentage(
        numerator: Decimal,
        denominator: Decimal,
    ) -> Decimal:
        """
        Calculate a percentage value.
        """

        if denominator == Decimal("0"):
            return Decimal("0")

        return (
            numerator
            / denominator
            * Decimal("100")
        )

    @staticmethod
    def group_market_value_by_issuer(
        holdings: list[Holding],
        key_selector: Callable[[Holding], str],
    ) -> dict[str, Decimal]:
        """
        Group market value by a selected key
        (issuer_name, parent_issuer, etc.).
        """

        grouped: defaultdict[str, Decimal] = defaultdict(
            lambda: Decimal("0")
        )

        for holding in holdings:
            grouped[
                key_selector(holding)
            ] += holding.market_value_sgd

        return dict(grouped)

    @staticmethod
    def _build_selector(
        source: str,
    ) -> Callable[[Holding], str]:

        if source == "issuer":
            return lambda h: h.issuer_name

        if source == "parent_issuer":
            return lambda h: h.parent_issuer

        raise ValueError(
            f"Unsupported grouping source: {source}"
        )
