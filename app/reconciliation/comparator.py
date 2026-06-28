from __future__ import annotations
from decimal import Decimal
from app.computation.models import FigureResult
from app.reconciliation.mapping import to_display_name
from app.reconciliation.models import (
    ExpectedFigure,
    ReconciliationItem,
    ReconciliationResult,
)


class Comparator:
    """
    Compare computed figures against the expected answer key.
    """

    def compare(
        self,
        expected: list[ExpectedFigure],
        actual: list[FigureResult],
        tolerance: Decimal = Decimal("0"),
    ) -> ReconciliationResult:
        """
        Compare expected and computed figures.

        Args:
            expected:
                Figures loaded from answer key.

            actual:
                Figures produced by ComputationEngine.

            tolerance:
                Numeric tolerance allowed for value comparison.

        Returns:
            ReconciliationResult.
        """

        # actual_lookup: dict[str, FigureResult] = {
        #     figure.figure: figure
        #     for figure in actual
        # }

        actual_lookup = {
            to_display_name(figure.figure): figure
            for figure in actual
        }
        items: list[ReconciliationItem] = []

        for expected_figure in expected:

            actual_figure = actual_lookup.get(
                expected_figure.metric
            )

            #
            # Figure missing
            #
            if actual_figure is None:

                items.append(
                    ReconciliationItem(
                        section=expected_figure.section,
                        figure=expected_figure.metric,
                        expected_value=expected_figure.value,
                        actual_value=Decimal("0"),
                        expected_status=expected_figure.status,
                        actual_status="MISSING",
                        difference=expected_figure.value,
                        matched=False,
                    )
                )

                continue

            difference = abs(
                expected_figure.value
                - actual_figure.value
            )

            matched = (
                difference <= tolerance
                and expected_figure.status.strip().upper()
                == actual_figure.status.strip().upper()
            )

            items.append(
                ReconciliationItem(
                    section=expected_figure.section,
                    figure=expected_figure.metric,
                    expected_value=expected_figure.value,
                    actual_value=actual_figure.value,
                    expected_status=expected_figure.status,
                    actual_status=actual_figure.status,
                    difference=difference,
                    matched=matched,
                )
            )

        return ReconciliationResult(
            items=items
        )

