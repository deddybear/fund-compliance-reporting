from __future__ import annotations

from app.graph.renderer_models import (
    GraphEdge,
    GraphNode,
    GraphRenderData,
)


class GraphBuilder:
    """
    Build GraphRenderData from Neo4j query results.
    """

    def build(
        self,
        *,
        title: str,
        graph: dict,
    ) -> GraphRenderData:

        render_data = GraphRenderData(
            title=title,
        )

        #
        # Nodes
        #
        for node in graph.get(
            "nodes",
            [],
        ):

            render_data.nodes.append(

                GraphNode(
                    id=str(node.id),
                    label=self._label(node),
                    properties=dict(node),
                )

            )

        #
        # Relationships
        #
        for relationship in graph.get(
            "relationships",
            [],
        ):

            render_data.edges.append(

                GraphEdge(
                    source=str(
                        relationship.start_node.id,
                    ),
                    target=str(
                        relationship.end_node.id,
                    ),
                    relationship=relationship.type,
                )

            )

        return render_data

    @staticmethod
    def _label(
        node,
    ) -> str:
        """
        Determine the display label of a Neo4j node.
        """

        properties = dict(node)

        for key in (
            "name",
            "title",
            "figure",
            "metric",
            "id",
        ):
            if key in properties:
                return str(
                    properties[key]
                )

        return ":".join(
            list(node.labels)
        )