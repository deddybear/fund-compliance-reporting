from __future__ import annotations
from decimal import Decimal
from typing import Any
from app.computation.base import BaseCalculator
from app.computation.evaluator import LimitEvaluator
from app.computation.models import FigureResult
from app.holdings.models import Holding


class AllocationCalculator(BaseCalculator):
    """
    Computes asset allocation figures.
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

        total_market_value = self._total_market_value(
            holdings
        )

        allocation_mapping = configuration[
            "classification"
        ]["allocation"]

        allocation_limits = configuration[
            "limits"
        ]["asset_allocation"]

        figures: list[FigureResult] = []

        for figure_name, asset_class in allocation_mapping.items():

            percentage = self._calculate_allocation(
                holdings=holdings,
                asset_class=asset_class,
                total_market_value=total_market_value,
            )

            limit = allocation_limits[figure_name]

            minimum = self._to_decimal(
                limit.get("min")
            )

            maximum = self._to_decimal(
                limit.get("max")
            )

            status = self._evaluator.evaluate(
                value=percentage,
                status_values=configuration["evaluation"]["status_values"],
                minimum=minimum,
                maximum=maximum,
            )

            figures.append(
                self.build_result(
                    section="Allocation",
                    figure=figure_name,
                    value=percentage,
                    minimum=minimum,
                    maximum=maximum,
                    status=status,
                )
            )

        return figures

    def _total_market_value(
        self,
        holdings: list[Holding],
    ) -> Decimal:

        return sum(
            (
                holding.market_value_sgd
                for holding in holdings
            ),
            start=Decimal("0"),
        )

    def _calculate_allocation(
        self,
        holdings: list[Holding],
        asset_class: str,
        total_market_value: Decimal,
    ) -> Decimal:

        asset_value = sum(
            (
                holding.market_value_sgd
                for holding in holdings
                if holding.asset_class == asset_class
            ),
            start=Decimal("0"),
        )

        if total_market_value == Decimal("0"):
            return Decimal("0")

        return (
            asset_value
            / total_market_value
            * Decimal("100")
        )

    @staticmethod
    def _format_limit(
        minimum: Decimal | None,
        maximum: Decimal | None,
    ) -> str:

        if (
            minimum is not None
            and maximum is not None
        ):
            return f"{minimum}–{maximum}%"

        if maximum is not None:
            return f"≤ {maximum}%"

        if minimum is not None:
            return f"≥ {minimum}%"

        return "-"

    @staticmethod
    def _to_decimal(
        value: Any,
    ) -> Decimal | None:

        if value is None:
            return None

        return Decimal(str(value))

