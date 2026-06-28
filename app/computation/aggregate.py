from __future__ import annotations
from decimal import Decimal
from typing import Any
from app.computation.base import BaseCalculator
from app.computation.evaluator import LimitEvaluator
from app.computation.models import FigureResult
from app.holdings.models import Holding


class AggregateCalculator(BaseCalculator):
    """
    Computes aggregate portfolio exposure metrics.
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
        """
        Compute Aggregate Non-Investment Grade Exposure.
        """

        total_market_value = self.total_market_value(
            holdings
        )

        non_ig_asset_classes = set(
            configuration["classification"][
                "non_investment_grade_asset_classes"
            ]
        )

        non_ig_market_value = self._non_ig_market_value(
            holdings=holdings,
            asset_classes=non_ig_asset_classes,
        )

        percentage = self.calculate_percentage(
            numerator=non_ig_market_value,
            denominator=total_market_value,
        )

        limit = configuration["limits"][
            "aggregate_non_ig_exposure"
        ]

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=percentage,
            status_values=configuration["evaluation"]["status_values"],
            minimum=minimum,
            maximum=maximum,
        )

        result = self.build_result(
            section="Aggregate",
            figure="Aggregate Non-IG Exposure",
            value=percentage,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

        return [result]

    @staticmethod
    def _non_ig_market_value(
        holdings: list[Holding],
        asset_classes: set[str],
    ) -> Decimal:
        """
        Sum the market value of all non-investment grade holdings.
        """

        return sum(
            (
                holding.market_value_sgd
                for holding in holdings
                if holding.asset_class in asset_classes
            ),
            start=Decimal("0"),
        )