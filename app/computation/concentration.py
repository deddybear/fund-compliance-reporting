from __future__ import annotations
from decimal import Decimal
from typing import Any, Callable
from app.computation.base import BaseCalculator
from app.computation.evaluator import LimitEvaluator
from app.computation.models import FigureResult
from app.holdings.models import Holding


class ConcentrationCalculator(BaseCalculator):
    """
    Computes issuer concentration metrics.
    """

    def __init__(
        self,
        evaluator: LimitEvaluator,
    ) -> None:
        self._evaluator = evaluator

    def compute(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
    ) -> list[FigureResult]:

        total_market_value = self.total_market_value(
            holdings
        )

        return [
            self._compute_single_issuer(
                holdings=holdings,
                configuration=configuration,
                total_market_value=total_market_value,
            ),
            self._compute_gre(
                holdings=holdings,
                configuration=configuration,
                total_market_value=total_market_value,
            ),
        ]

    def _compute_single_issuer(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
        total_market_value: Decimal,
    ) -> FigureResult:

        limit = configuration["limits"][
            "single_issuer_concentration"
        ]

        excluded = set(
            limit.get("exclude", [])
        )

        filtered_holdings = [
            holding
            for holding in holdings
            if holding.issuer_name not in excluded
        ]

        method = configuration.get(
            "aggregation",
            {},
        ).get(
            "issuer_concentration_method",
            {},
        ).get(
            "source",
            "issuer",
        )

        selector = self._build_selector(
            method
        )

        grouped = self.group_market_value_by_issuer(
            filtered_holdings,
            key_selector=selector,
        )

        maximum_market_value = self._maximum_market_value(
            grouped
        )

        percentage = self.calculate_percentage(
            numerator=maximum_market_value,
            denominator=total_market_value,
        )

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=percentage,
            status_values=configuration["evaluation"][
                "status_values"
            ],
            minimum=minimum,
            maximum=maximum,
        )

        return self.build_result(
            section="Concentration",
            figure="Single Issuer Concentration",
            value=percentage,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

    def _compute_gre(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
        total_market_value: Decimal,
    ) -> FigureResult:

        gre_types = set(
            configuration["classification"][
                "gre_issuer_types"
            ]
        )

        filtered_holdings = [
            holding
            for holding in holdings
            if holding.issuer_type in gre_types
        ]

        method = configuration.get(
            "aggregation",
            {},
        ).get(
            "gre_concentration_method",
            {},
        ).get(
            "source",
            "issuer",
        )

        selector = self._build_selector(
            method
        )

        grouped = self.group_market_value_by_issuer(
            filtered_holdings,
            key_selector=selector,
        )

        maximum_market_value = self._maximum_market_value(
            grouped
        )

        percentage = self.calculate_percentage(
            numerator=maximum_market_value,
            denominator=total_market_value,
        )

        limit = configuration["limits"][
            "gre_concentration"
        ]

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=percentage,
            status_values=configuration["evaluation"][
                "status_values"
            ],
            minimum=minimum,
            maximum=maximum,
        )

        return self.build_result(
            section="Concentration",
            figure="GRE Concentration",
            value=percentage,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

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

    @staticmethod
    def _maximum_market_value(
        grouped_market_value: dict[str, Decimal],
    ) -> Decimal:

        if not grouped_market_value:
            return Decimal("0")

        return max(
            grouped_market_value.values()
        )

