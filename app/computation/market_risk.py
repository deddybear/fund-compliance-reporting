from __future__ import annotations
from decimal import Decimal
from typing import Any
from app.computation.base import BaseCalculator
from app.computation.evaluator import LimitEvaluator
from app.computation.models import FigureResult
from app.holdings.models import Holding


class MarketRiskCalculator(BaseCalculator):
    """
    Computes portfolio market risk metrics.
    """

    DV01_FACTOR = Decimal("0.0001")

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
            self._compute_duration(
                holdings=holdings,
                configuration=configuration,
                total_market_value=total_market_value,
            ),
            self._compute_dv01(
                holdings=holdings,
                configuration=configuration,
            ),
        ]

    def _compute_duration(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
        total_market_value: Decimal,
    ) -> FigureResult:

        duration = self._portfolio_duration(
            holdings=holdings,
            total_market_value=total_market_value,
        )

        limit = configuration["limits"]["duration"]

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=duration,
            status_values=configuration["evaluation"]["status_values"],
            minimum=minimum,
            maximum=maximum,
        )

        return self.build_result(
            graph_path=None,
            metric_id="duration",
            section="Market Risk",
            figure="Portfolio Modified Duration",
            value=duration,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

    def _compute_dv01(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
    ) -> FigureResult:

        dv01 = self._portfolio_dv01(
            holdings
        )

        limit = configuration["limits"]["dv01"]

        minimum = self.to_decimal(
            limit.get("min")
        )

        maximum = self.to_decimal(
            limit.get("max")
        )

        status = self._evaluator.evaluate(
            value=dv01,
            status_values=configuration["evaluation"]["status_values"],
            minimum=minimum,
            maximum=maximum,
        )

        return self.build_result(
            graph_path=None,
            metric_id="dv01",
            section="Market Risk",
            figure="Portfolio DV01",
            value=dv01,
            minimum=minimum,
            maximum=maximum,
            status=status,
        )

    @staticmethod
    def _portfolio_duration(
        holdings: list[Holding],
        total_market_value: Decimal,
    ) -> Decimal:
        """
        Weighted average modified duration.
        """

        if total_market_value == Decimal("0"):
            return Decimal("0")

        weighted_duration = sum(
            (
                holding.market_value_sgd
                * holding.modified_duration
                for holding in holdings
            ),
            start=Decimal("0"),
        )

        return (
            weighted_duration
            / total_market_value
        )

    @classmethod
    def _portfolio_dv01(
        cls,
        holdings: list[Holding],
    ) -> Decimal:
        """
        NOTE:
        The assignment does not specify the DV01 methodology.

        Industry approximation:

            DV01 =
            Market Value × Modified Duration × 0.0001
        """

        return sum(
            (
                holding.market_value_sgd
                * holding.modified_duration
                * cls.DV01_FACTOR
                for holding in holdings
            ),
            start=Decimal("0"),
        )

