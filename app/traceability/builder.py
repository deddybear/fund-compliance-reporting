from __future__ import annotations

from app.computation.models import FigureResult
from app.traceability.service import TraceabilityService


class TraceabilityBuilder:
    """
    Enrich computed figures with traceability metadata.

    This builder is intentionally unaware of where the
    traceability data comes from. It delegates lookup to
    TraceabilityService.
    """

    def __init__(
        self,
        service: TraceabilityService,
    ) -> None:

        self._service = service

    def enrich(
        self,
        figures: list[FigureResult],
    ) -> list[FigureResult]:

        enriched: list[FigureResult] = []

        for figure in figures:

            traceability = self._service.find(
                figure.metric_id
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
                    metric_id=figure.metric_id,
                    section=figure.section,
                    figure=figure.figure,
                    value=figure.value,
                    limit=figure.limit,
                    status=figure.status,
                    utilization=figure.utilization,
                    graph_path=traceability.graph_path,
                    citation=str(traceability.citation),
                    minimum=figure.minimum,
                    maximum=figure.maximum,
                )

            )

        return enriched