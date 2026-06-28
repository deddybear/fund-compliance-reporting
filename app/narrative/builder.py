from __future__ import annotations

from app.computation.models import FigureResult
from app.narrative.models import (
    NarrativeContext,
    NarrativeItem,
)


class NarrativeBuilder:
    """
    Builds a narrative context from computed figures.
    """

    def build(
        self,
        fund_name: str,
        figures: list[FigureResult],
    ) -> NarrativeContext:

        items: list[NarrativeItem] = []

        for figure in figures:

            items.append(
                NarrativeItem(
                    section=figure.section,
                    title=figure.figure,
                    value=self._format_value(
                        figure.value,
                    ),
                    limit=figure.limit,
                    status=figure.status,
                    utilization=self._format_utilization(
                        figure.utilization,
                    ),
                )
            )

        return NarrativeContext(
            fund_name=fund_name,
            items=items,
        )

    @staticmethod
    def _format_value(
        value,
    ) -> str:

        return str(value)

    @staticmethod
    def _format_utilization(
        utilization,
    ) -> str | None:

        if utilization is None:
            return None

        return str(utilization)