from neo4j import GraphDatabase
from neo4j import Driver
from app.settings import Settings


class Neo4jDatabase:
    """Neo4j database connection manager."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._driver: Driver | None = None

    def connect(self) -> None:
        """Create Neo4j driver."""

        self._driver = GraphDatabase.driver(
            uri=self._settings.neo4j_uri,
            auth=(
                self._settings.neo4j_username,
                self._settings.neo4j_password,
            ),
        )

    def verify(self) -> None:
        """Verify connectivity."""

        if self._driver is None:
            raise RuntimeError("Neo4j driver has not been initialized.")

        self._driver.verify_connectivity()

    def driver(self) -> Driver:
        """Return active driver."""

        if self._driver is None:
            raise RuntimeError("Neo4j driver has not been initialized.")

        return self._driver

    def close(self) -> None:
        """Close Neo4j driver."""

        if self._driver is not None:
            self._driver.close()