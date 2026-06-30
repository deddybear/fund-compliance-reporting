from __future__ import annotations

from app.graph.query_service import GraphQueryService
from app.traceability.models import Citation
from app.traceability.models import Traceability
from app.traceability.repository import TraceabilityRepository
from neo4j.graph import Path


class Neo4jTraceabilityRepository(
    TraceabilityRepository,
):

    def __init__(
        self,
        graph: GraphQueryService,
    ) -> None:

        self._graph = graph

    @staticmethod
    def _convert_path(
        path: Path,
    ) -> list[dict]:

        result = []

        nodes = list(path.nodes)
        relationships = list(path.relationships)

        for i, node in enumerate(nodes):

            label = list(node.labels)[0]

            result.append(
                {
                    "type": "node",
                    "label": label,
                    **dict(node),
                }
            )

            if i < len(relationships):

                result.append(
                    {
                        "type": "relationship",
                        "label": relationships[i].type,
                    }
                )

        return result

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
        rule = result["rule"]
        citation = result["citation"]
        
        # print(rule, metric, citation)


        maximum = rule.get('maximum')
        minimum = rule.get('minimum', 0) 

        if minimum == 0:
            graph_path = f"{metric['name']} -> Rule : Max {maximum}% -> {citation['source_document']} - Page : {citation['page']}"
        else :
            graph_path = f"{metric['name']} -> Rule : {minimum}% - {maximum}% -> {citation['source_document']} - Page : {citation['page']}"

        return Traceability(
            graph_path=graph_path,
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