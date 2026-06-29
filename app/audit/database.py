from __future__ import annotations
import sqlite3
from pathlib import Path


class AuditDatabase:
    """
    SQLite database used for audit logging.
    """

    def __init__(
        self,
        database_path: Path,
    ) -> None:

        self._database_path = database_path

        self._connection: sqlite3.Connection | None = None

    def connect(
        self,
    ) -> sqlite3.Connection:
        """
        Open SQLite connection.
        """

        if self._connection is None:

            self._database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._connection = sqlite3.connect(
                self._database_path,
            )

            self._connection.row_factory = (
                sqlite3.Row
            )

        return self._connection

    def initialize(
        self,
    ) -> None:
        """
        Create audit tables if they do not exist.
        """

        connection = self.connect()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_event
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event_type TEXT NOT NULL,

                status TEXT NOT NULL,

                trigger_name TEXT NOT NULL,

                message TEXT,

                payload TEXT,

                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    def get_connection(
        self,
    ) -> sqlite3.Connection:
        """
        Return active SQLite connection.
        """

        return self.connect()

    def close(
        self,
    ) -> None:
        """
        Close SQLite connection.
        """

        if self._connection is not None:

            self._connection.close()

            self._connection = None