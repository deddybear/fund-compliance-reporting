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
                    id=node.element_id,
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
                    source=relationship.start_node.element_id,
                    target=relationship.end_node.element_id,
                    relationship=relationship.type,
                )
            )

        return render_data

    @staticmethod
    def _label(
        node,
    ) -> str:
        """
        Determine display label.
        """

        properties = dict(node)
        labels = set(node.labels)

        #
        # Metric
        #
        if "Metric" in labels:

            return properties.get(
                "name",
                properties.get("id", "Metric"),
            )

        #
        # Rule
        #
        if "Rule" in labels:

            minimum = properties.get("minimum")
            maximum = properties.get("maximum")

            if minimum is not None and maximum is not None:
                return (
                    "Rule\n"
                    f"{minimum}% – {maximum}%"
                )

            if minimum is not None:
                return (
                    "Rule\n"
                    f"Minimum {minimum}%"
                )

            if maximum is not None:
                return (
                    "Rule\n"
                    f"Maximum {maximum}%"
                )

            return "Rule"

        #
        # Citation
        #
        if "Citation" in labels:

            document = properties.get(
                "source_document",
                "Document",
            )

            #
            # Remove extension for cleaner graph.
            #
            if "." in document:
                document = document.rsplit(".", 1)[0]

            page = properties.get(
                "page",
                "-",
            )

            return (
                "Citation\n"
                f"{document}\n"
                f"Page {page}"
            )

        #
        # Profile
        #
        if "Profile" in labels:

            return (
                "Profile\n"
                + properties.get(
                    "name",
                    "",
                )
            )

        #
        # Method
        #
        if "Method" in labels:

            return (
                "Method\n"
                + properties.get(
                    "name",
                    "",
                )
            )

        #
        # Fallback
        #
        return properties.get(
            "name",
            properties.get(
                "id",
                next(iter(labels), "Node"),
            ),
        )