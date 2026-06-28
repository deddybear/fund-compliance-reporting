from __future__ import annotations
from decimal import Decimal
from pathlib import Path
from app.computation.models import FigureResult
from app.reconciliation.comparator import Comparator
from app.reconciliation.loader import ReconciliationLoader
from app.reconciliation.models import ReconciliationResult


class ReconciliationEngine:
    """
    Reconcile computed figures against the official answer key.
    """

    def __init__(
        self,
        loader: ReconciliationLoader,
        comparator: Comparator,
    ) -> None:
        self._loader = loader
        self._comparator = comparator

    def reconcile(
        self,
        answer_key: Path,
        computed_figures: list[FigureResult],
        tolerance: Decimal = Decimal("0"),
    ) -> ReconciliationResult:
        """
        Reconcile computed figures with the expected answer key.
        """

        expected_figures = self._loader.load(
            answer_key,
        )

        return self._comparator.compare(
            expected=expected_figures,
            actual=computed_figures,
            tolerance=tolerance,
        )
