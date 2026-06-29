from __future__ import annotations
import json
from datetime import datetime
from app.audit.database import AuditDatabase
from app.audit.models import AuditEvent
from app.audit.models import AuditResult


class AuditRepository:
    """
    Repository responsible for persisting audit events.
    """

    def __init__(
        self,
        database: AuditDatabase,
    ) -> None:

        self._database = database

    def insert(
        self,
        event: AuditEvent,
    ) -> AuditResult:
        """
        Persist an audit event.
        """

        connection = self._database.get_connection()

        cursor = connection.cursor()

        try:

            created_at = (
                event.created_at
                or datetime.utcnow()
            )

            cursor.execute(
                """
                INSERT INTO audit_event
                (
                    event_type,
                    status,
                    trigger_name,
                    message,
                    payload,
                    created_at
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    event.event_type,
                    event.status,
                    event.trigger_name,
                    event.message,
                    json.dumps(
                        event.payload
                        or {},
                        default=str,
                    ),
                    created_at.isoformat(),
                ),
            )

            connection.commit()

            return AuditResult(
                success=True,
                event_id=cursor.lastrowid,
            )

        except Exception as exc:

            connection.rollback()

            return AuditResult(
                success=False,
                error_message=str(exc),
            )

    def find_all(
        self,
    ) -> list[AuditEvent]:
        """
        Retrieve all audit events.
        """

        connection = self._database.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                event_type,
                status,
                trigger_name,
                message,
                payload,
                created_at
            FROM audit_event
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()

        events: list[AuditEvent] = []

        for row in rows:

            events.append(

                AuditEvent(

                    event_type=row["event_type"],

                    status=row["status"],

                    trigger_name=row["trigger_name"],

                    message=row["message"],

                    payload=json.loads(
                        row["payload"]
                    )
                    if row["payload"]
                    else {},

                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    ),

                )

            )

        return events