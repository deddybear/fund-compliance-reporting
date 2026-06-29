from __future__ import annotations

from app.traceability.models import Traceability
from app.traceability.repository import TraceabilityRepository


class TraceabilityService:

    def __init__(
        self,
        repository: TraceabilityRepository,
    ) -> None:

        self._repository = repository

    def find(
        self,
        metric_id: str,
    ) -> Traceability | None:

        return self._repository.find(
            metric_id,
        )

    def require(
        self,
        metric_id: str,
    ) -> Traceability:

        traceability = self.find(
            metric_id,
        )

        if traceability is None:
            raise KeyError(
                f"Traceability '{metric_id}' not found."
            )

        return traceability