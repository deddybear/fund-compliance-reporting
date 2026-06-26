from __future__ import annotations

from dataclasses import dataclass
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

    limit: str

    status: str

    utilization: Decimal | None = None

    graph_path: str | None = None

    citation: str | None = None