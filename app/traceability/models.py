from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Citation:
    """
    Citation pointing back to the original guideline source.

    Every computed figure should be traceable to the document
    from which its compliance rule originated.
    """

    source_document: str

    page: int

    chunk_id: str

    passage_summary: str


@dataclass(slots=True, frozen=True)
class Traceability:
    """
    Complete traceability metadata for a computed figure.

    Includes:
        - graph traversal path
        - citation back to the original guideline
    """

    graph_path: str

    citation: Citation