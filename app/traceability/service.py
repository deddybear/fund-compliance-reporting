from __future__ import annotations

from app.traceability.models import Traceability
from app.traceability.repository import TraceabilityRepository


class TraceabilityService:
    """
    Application service responsible for providing traceability
    metadata to the computation/reporting pipeline.
    """

    def __init__(
        self,
        repository: TraceabilityRepository,
    ) -> None:

        self._repository = repository

    def get(
        self,
        figure: str,
    ) -> Traceability | None:
        """
        Retrieve traceability information for a computed figure.
        """

        return self._repository.get(
            figure,
        )

    def require(
        self,
        figure: str,
    ) -> Traceability:
        """
        Retrieve traceability information.

        Raises
        ------
        KeyError
            If traceability metadata is missing.
        """

        traceability = self._repository.get(
            figure,
        )

        if traceability is None:
            raise KeyError(
                f"Traceability not found for figure '{figure}'."
            )

        return traceability

    def exists(
        self,
        figure: str,
    ) -> bool:
        """
        Check whether traceability metadata exists.
        """

        return self._repository.exists(
            figure,
        )