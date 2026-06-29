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

    _NON_IG_RATINGS = {
        "BB+",
        "BB",
        "BB-",
        "B+",
        "B",
        "B-",
        "CCC",
        "CC",
        "C",
        "D",
    }

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

        aggregation_config = configuration.get(
            "aggregation",
            {},
        )

        non_ig_config = aggregation_config.get(
            "non_ig_method",
            {},
        )

        method = non_ig_config.get(
            "source",
            "asset_class",
        )

        include_fallen_angels = non_ig_config.get(
            "include_fallen_angels",
            True,
        )

        non_ig_asset_classes = set(
            configuration["classification"][
                "non_investment_grade_asset_classes"
            ]
        )

        non_ig_market_value = self._non_ig_market_value(
            holdings=holdings,
            asset_classes=non_ig_asset_classes,
            method=method,
            include_fallen_angels=include_fallen_angels,
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
            status_values=configuration["evaluation"][
                "status_values"
            ],
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

    def _non_ig_market_value(
        self,
        *,
        holdings: list[Holding],
        asset_classes: set[str],
        method: str,
        include_fallen_angels: bool,
    ) -> Decimal:
        """
        Compute Non-IG market value using the configured methodology.
        """

        if method == "asset_class":
            return self._asset_class_method(
                holdings,
                asset_classes,
            )

        if method == "credit_rating":
            return self._credit_rating_method(
                holdings,
                asset_classes,
                include_fallen_angels,
            )

        raise ValueError(
            f"Unsupported Non-IG methodology: {method}"
        )

    @staticmethod
    def _asset_class_method(
        holdings: list[Holding],
        asset_classes: set[str],
    ) -> Decimal:
        """
        Firm A methodology.
        """

        return sum(
            (
                holding.market_value_sgd
                for holding in holdings
                if holding.asset_class in asset_classes
            ),
            start=Decimal("0"),
        )

    def _credit_rating_method(
        self,
        holdings: list[Holding],
        asset_classes: set[str],
        include_fallen_angels: bool,
    ) -> Decimal:
        """
        Firm B methodology.
        """

        total = Decimal("0")

        for holding in holdings:

            #
            # Structured Credit is always treated as Non-IG.
            #
            if holding.asset_class == "Structured Credit":
                total += holding.market_value_sgd
                continue

            #
            # Current Non-IG rating.
            #
            if holding.credit_rating not in self._NON_IG_RATINGS:
                continue

            #
            # Skip fallen angels when configured.
            #
            if (
                not include_fallen_angels
                and holding.downgraded_from
            ):
                continue

            total += holding.market_value_sgd

        return total