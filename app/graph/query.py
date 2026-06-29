from __future__ import annotations

from typing import Any, LiteralString, cast
from neo4j import Driver
from neo4j import Query
from neo4j import Record


class GraphQueryService:
    """
    Generic Neo4j query service.

    This service is responsible only for executing Cypher
    queries and returning Neo4j records.

    Business logic should remain inside repositories.
    """

    def __init__(
        self,
        driver: Driver,
    ) -> None:

        self._driver = driver

    def one(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> Record | None:
        """
        Execute a query expected to return
        at most one record.
        """

        with self._driver.session() as session:

            result = session.run(
                Query(cast(LiteralString, cypher)),
                parameters or {},
            )

            return result.single()

    def all(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[Record]:
        """
        Execute a query returning multiple records.
        """

        with self._driver.session() as session:

            result = session.run(
                 Query(cast(LiteralString, cypher)),
                parameters or {},
            )

            return list(result)

    def scalar(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute a query and return the first column
        of the first record.
        """

        record = self.one(
            cypher=cypher,
            parameters=parameters,
        )

        if record is None:
            return None

        return record[0]

    def exists(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> bool:
        """
        Execute a query and determine whether
        at least one record exists.
        """

        record = self.one(
            cypher=cypher,
            parameters=parameters,
        )

        return record is not None

    def execute(
        self,
        cypher: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """
        Execute write/update/delete query.
        """

        with self._driver.session() as session:

            session.run(
                 Query(cast(LiteralString, cypher)),
                parameters or {},
            ).consume()