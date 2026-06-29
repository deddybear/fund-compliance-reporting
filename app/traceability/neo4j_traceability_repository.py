from __future__ import annotations

from app.graph.query_service import GraphQueryService
from app.traceability.models import Citation
from app.traceability.models import Traceability
from app.traceability.repository import TraceabilityRepository


class Neo4jTraceabilityRepository(
    TraceabilityRepository,
):

    def __init__(
        self,
        graph: GraphQueryService,
    ) -> None:

        self._graph = graph

    def find(
        self,
        metric_id: str,
    ) -> Traceability | None:

        result = self._graph.get_traceability(
            metric_id,
        )

        if result is None:
            return None

        metric = result["metric"]
        citation = result["citation"]

        return Traceability(
            graph_path=metric.get(
                "graph_path",
                "",
            ),
            citation=Citation(
                source_document=citation.get(
                    "source_document",
                    "",
                ),
                page=int(
                    citation.get(
                        "page",
                        0,
                    )
                ),
                chunk_id=citation.get(
                    "chunk_id",
                    "",
                ),
                passage_summary=citation.get(
                    "passage_summary",
                    "",
                ),
            ),
        )