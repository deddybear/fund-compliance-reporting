from __future__ import annotations
from typing import Any
from app.computation.aggregate import AggregateCalculator
from app.computation.allocation import AllocationCalculator
from app.computation.concentration import ConcentrationCalculator
from app.computation.liquidity import LiquidityCalculator
from app.computation.market_risk import MarketRiskCalculator
from app.computation.models import ComputationResult
from app.traceability.builder import TraceabilityBuilder
from app.holdings.models import Holding


class ComputationEngine:
    """
    Orchestrates all portfolio computation calculators.
    """

    def __init__(
        self,
        allocation: AllocationCalculator,
        aggregate: AggregateCalculator,
        concentration: ConcentrationCalculator,
        liquidity: LiquidityCalculator,
        market_risk: MarketRiskCalculator,
        traceability: TraceabilityBuilder,
    ) -> None:
        self._calculators = [
            allocation,
            aggregate,
            concentration,
            liquidity,
            market_risk,
        ]

        self._traceability = traceability

    def compute(
        self,
        holdings: list[Holding],
        configuration: dict[str, Any],
    ) -> ComputationResult:
        """
        Execute all portfolio calculators and combine
        their results.
        """

        figures = []

        for calculator in self._calculators:
            figures.extend(
                calculator.compute(
                    holdings=holdings,
                    configuration=configuration,
                )
            )

        #
        # Attach graph path and citation
        #
        figures = self._traceability.enrich(
            figures,
        )    

        return ComputationResult(
            figures=figures,
        )

