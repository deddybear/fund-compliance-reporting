from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from app.graph.renderer_models import GraphRenderData


class GraphRenderer(ABC):
    """
    Abstract renderer for graph visualization.

    Implementations may render using:

        - NetworkX
        - Graphviz
        - Mermaid
        - Cytoscape
        - etc.

    The output is always an image file.
    """

    @abstractmethod
    def render(
        self,
        graph: GraphRenderData,
        output_path: Path,
    ) -> Path:
        """
        Render graph into an image.

        Args:
            graph:
                Graph representation.

            output_path:
                Destination image path.

        Returns
        -------
        Path
            Generated image path.
        """
        raise NotImplementedError