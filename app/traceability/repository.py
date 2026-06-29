from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.traceability.models import Traceability


class TraceabilityRepository(ABC):
    """
    Abstract repository for traceability.
    """

    def find(
        self,
        metric_id: str,
    ) -> Traceability | None:
        pass