from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

from app.graph.renderer import GraphRenderer
from app.graph.renderer_models import GraphRenderData


class NetworkXRenderer(GraphRenderer):
    """
    Render GraphRenderData into PNG using NetworkX.
    """

    def render(
        self,
        graph: GraphRenderData,
        output_path: Path,
    ) -> Path:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        graph_network = nx.DiGraph()

        #
        # Nodes
        #
        for node in graph.nodes:

            graph_network.add_node(
                node.id,
                label=node.label,
            )

        #
        # Edges
        #
        for edge in graph.edges:

            graph_network.add_edge(
                edge.source,
                edge.target,
                label=edge.relationship,
            )

        #
        # Layout
        #
        positions = nx.spring_layout(
            graph_network,
            seed=42,
        )

        plt.figure(
            figsize=(8, 6),
        )

        #
        # Draw Nodes
        #
        nx.draw_networkx_nodes(
            graph_network,
            positions,
            node_size=2500,
            node_color="#DCEEFF",
            edgecolors="black",
        )

        #
        # Draw Edges
        #
        nx.draw_networkx_edges(
            graph_network,
            positions,
            arrows=True,
            arrowsize=20,
            width=1.5,
        )

        #
        # Node Labels
        #
        node_labels = {

            node: data["label"]

            for node, data
            in graph_network.nodes(data=True)

        }

        nx.draw_networkx_labels(
            graph_network,
            positions,
            labels=node_labels,
            font_size=9,
        )

        #
        # Edge Labels
        #
        edge_labels = nx.get_edge_attributes(
            graph_network,
            "label",
        )

        nx.draw_networkx_edge_labels(
            graph_network,
            positions,
            edge_labels=edge_labels,
            font_size=8,
        )

        plt.title(
            graph.title,
        )

        plt.axis(
            "off",
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=200,
            bbox_inches="tight",
        )

        plt.close()

        return output_path