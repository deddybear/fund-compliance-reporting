from __future__ import annotations

from app.traceability.models import Traceability
from app.traceability.registry import TRACEABILITY_REGISTRY


class TraceabilityRepository:
    """
    Repository responsible for retrieving traceability metadata.

    For now the data source is the in-memory registry.
    Later this repository will be migrated to Neo4j without
    affecting callers.
    """

    def get(
        self,
        figure: str,
    ) -> Traceability | None:
        """
        Retrieve traceability metadata for a figure.

        Returns
        -------
        Traceability | None
            Traceability metadata if found.
        """

        return TRACEABILITY_REGISTRY.get(
            figure,
        )

    def exists(
        self,
        figure: str,
    ) -> bool:
        """
        Check whether traceability exists.
        """

        return figure in TRACEABILITY_REGISTRY

    def all(self) -> dict[str, Traceability]:
        """
        Return all registered traceability entries.

        Mainly useful for debugging or testing.
        """

        return TRACEABILITY_REGISTRY.copy()