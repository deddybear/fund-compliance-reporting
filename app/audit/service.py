from __future__ import annotations

from datetime import datetime
from typing import Any

from app.audit.models import AuditEvent
from app.audit.models import AuditResult
from app.audit.repository import AuditRepository


class AuditService:
    """
    High-level service for writing audit events.

    This service hides the underlying persistence layer
    (SQLite, PostgreSQL, etc.) from the rest of the
    application.
    """

    def __init__(
        self,
        repository: AuditRepository,
    ) -> None:

        self._repository = repository

    def log(
        self,
        *,
        event_type: str,
        status: str,
        trigger_name: str,
        message: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> AuditResult:
        """
        Record an audit event.
        """

        event = AuditEvent(
            event_type=event_type,
            status=status,
            trigger_name=trigger_name,
            message=message,
            payload=payload,
            created_at=datetime.utcnow(),
        )

        return self._repository.insert(
            event,
        )

    def get_events(
        self,
    ) -> list[AuditEvent]:
        """
        Retrieve all persisted audit events.
        """

        return self._repository.find_all()