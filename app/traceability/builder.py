from __future__ import annotations

from app.computation.models import FigureResult
from app.traceability.registry import TRACEABILITY_REGISTRY


class TraceabilityBuilder:
    """
    Enrich computed figures with traceability metadata.

    This builder attaches:

        - graph_path
        - citation

    to every computed figure using the
    TRACEABILITY_REGISTRY.
    """

    def enrich(
        self,
        figures: list[FigureResult],
    ) -> list[FigureResult]:

        enriched: list[FigureResult] = []

        for figure in figures:

            traceability = (
                TRACEABILITY_REGISTRY.get(
                    figure.figure,
                )
            )

            #
            # Figure not registered.
            #
            if traceability is None:

                enriched.append(
                    figure,
                )

                continue

            enriched.append(

                FigureResult(
                    section=figure.section,
                    figure=figure.figure,
                    value=figure.value,
                    limit=figure.limit,
                    status=figure.status,
                    utilization=figure.utilization,
                    graph_path=traceability.graph_path,
                    citation=str(traceability.citation),
                    minimum=figure.minimum,
                    maximum=figure.maximum
                )

            )

        return enriched