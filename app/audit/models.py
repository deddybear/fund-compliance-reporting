from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class AuditEvent:
    """
    Represents a single audit event generated during
    execution of the compliance pipeline.
    """

    event_type: str

    status: str

    trigger_name: str

    message: str | None = None

    payload: dict[str, Any] | None = None

    created_at: datetime | None = None


@dataclass(slots=True, frozen=True)
class AuditResult:
    """
    Result returned after persisting an audit event.
    """

    success: bool

    event_id: int | None = None

    error_message: str | None = None