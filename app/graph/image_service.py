from __future__ import annotations
from pathlib import Path
from app.computation.models import FigureResult
from app.graph.graph_builder import GraphBuilder
from app.graph.networkx_renderer import NetworkXRenderer
from app.graph.query_service import GraphQueryService


class GraphImageService:
    """
    Generate PNG graph for a computed figure.
    """

    def __init__(
        self,
        query: GraphQueryService,
        builder: GraphBuilder,
        renderer: NetworkXRenderer,
    ) -> None:

        self._query = query
        self._builder = builder
        self._renderer = renderer

    def generate(
        self,
        metric_id: str,
        title: str,
        output_path: Path,
    ) -> Path | None:
    
        graph = self._query.get_graph_path(
            metric_id,
        )
    
        if graph is None:
            return None
    
        render_data = self._builder.build(
            title=title,
            graph=graph,
        )
    
        return self._renderer.render(
            render_data,
            output_path,
        )