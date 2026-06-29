from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(slots=True)
class ComputedFigure:
    """
    Represents one computed compliance figure.
    """

    section: str
    figure: str

    value: Decimal

    limit: str

    status: str

    utilization: Decimal | None = None

    graph_path: str | None = None

    citation: str | None = None

@dataclass(slots=True, frozen=True)
class FigureResult:
    """
    Represents one computed figure produced by the computation engine.
    """

    section: str
    figure: str

    value: Decimal

    minimum: Decimal | None
    maximum: Decimal | None

    limit: str

    status: str

    utilization: Decimal | None = None

    graph_path: str | None = None

    citation: str | None = None

@dataclass(slots=True)
class ComputationResult:
    """
    Aggregated computation output produced by the
    ComputationEngine.
    """

    figures: list[FigureResult] = field(
        default_factory=list
    )

