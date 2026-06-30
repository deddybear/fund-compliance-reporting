from __future__ import annotations
from decimal import Decimal
from typing import Any
from app.computation.base import BaseCalculator
from app.computation.evaluator import LimitEvaluator
from app.computation.models import FigureResult
from app.holdings.models import Holding


class LiquidityCalculator(BaseCalculator):
    """
    Computes portfolio liquidity metrics.
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
        Compute portfolio liquidity ratio.
        """

        total_market_value = self.total_market_value(
            holdings
        )

        liquidity_asset_classes = set(
            configuration["classification"][
                "liquidity_asset_classes"
            ]
        )

        liquidity_market_value = self._liquidity_market_value(
            holdings=holdings,
            asset_classes=liquidity_asset_classes,
        )

        liquidity_ratio = self.calculate_percentage(
            numerator=liquidity_market_value,
            denominator=total_market_value,
        )

        limit = configuration["limits"][
            "liquidity_ratio"
        ]

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=liquidity_ratio,
            status_values=configuration["evaluation"]["status_values"],
            minimum=minimum,
            maximum=maximum,
        )

        result = self.build_result(
            graph_path=None,
            metric_id="liquidity_ratio",
            section="Liquidity",
            figure="Liquidity Ratio",
            value=liquidity_ratio,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

        return [result]

    @staticmethod
    def _liquidity_market_value(
        holdings: list[Holding],
        asset_classes: set[str],
    ) -> Decimal:
        """
        Calculate the market value of liquidity assets.
        """

        return sum(
            (
                holding.market_value_sgd
                for holding in holdings
                if holding.asset_class in asset_classes
            ),
            start=Decimal("0"),
        )
