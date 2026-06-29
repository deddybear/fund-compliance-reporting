from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class GraphNode:
    """
    Represents a graph node to be rendered.
    """

    id: str
    label: str
    properties: dict[str, str] = field(
        default_factory=dict,
    )


@dataclass(slots=True, frozen=True)
class GraphEdge:
    """
    Represents a relationship between two nodes.
    """

    source: str
    target: str
    relationship: str


@dataclass(slots=True)
class GraphRenderData:
    """
    Complete graph representation used by the renderer.

    This object is independent of Neo4j and NetworkX.
    """

    title: str

    nodes: list[GraphNode] = field(
        default_factory=list,
    )

    edges: list[GraphEdge] = field(
        default_factory=list,
    )