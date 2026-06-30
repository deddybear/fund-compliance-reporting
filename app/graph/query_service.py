from __future__ import annotations

from neo4j import Driver


class GraphQueryService:
    """
    Centralized Neo4j query layer.

    Every repository should use this service instead
    of writing Cypher directly.
    """

    def __init__(
        self,
        driver: Driver,
    ) -> None:

        self._driver = driver

    # ---------------------------------------------------------
    # Profile
    # ---------------------------------------------------------

    def get_profile(
        self,
        profile_name: str,
    ) -> dict | None:

        query = """
        MATCH (p:Profile {name:$profile})
        RETURN p
        """

        with self._driver.session() as session:

            record = session.run(
                query,
                profile=profile_name,
            ).single()

        if record is None:
            return None

        return dict(record["p"])

    # ---------------------------------------------------------
    # Metric
    # ---------------------------------------------------------

    def get_metric(
        self,
        metric_id: str,
    ) -> dict | None:

        query = """
        MATCH (m:Metric {id:$metric})
        RETURN m
        """

        with self._driver.session() as session:

            record = session.run(
                query,
                metric=metric_id,
            ).single()

        if record is None:
            return None

        return dict(record["m"])

    # ---------------------------------------------------------
    # Rule
    # ---------------------------------------------------------

    def get_rule(
        self,
        metric_id: str,
    ) -> dict | None:

        query = """
        MATCH (m:Metric {id:$metric})
              -[:HAS_RULE]->
              (r:Rule)
        RETURN r
        """

        with self._driver.session() as session:

            record = session.run(
                query,
                metric=metric_id,
            ).single()

        if record is None:
            return None

        return dict(record["r"])

    # ---------------------------------------------------------
    # Traceability
    # ---------------------------------------------------------

    def get_traceability(
        self,
        metric_id: str,
    ) -> dict | None:

        query = """
        MATCH (m:Metric {id:$metric})

        OPTIONAL MATCH (m)-[:HAS_RULE]->(r:Rule)
        OPTIONAL MATCH (r)-[:HAS_CITATION]->(c:Citation)

        RETURN
            m,
            r,
            c
        """

        with self._driver.session() as session:

            record = session.run(
                query,
                metric=metric_id,
            ).single()

        if record is None:
            return None

        return {
            "metric": dict(record["m"]),
            "rule": dict(record["r"]) if record["r"] else None,
            "citation": dict(record["c"]) if record["c"] else None,
        }

    # ---------------------------------------------------------
    # Graph Path
    # ---------------------------------------------------------

    def get_graph_path(
        self,
        metric_id: str,
    ) -> dict | None:

        query = """
        MATCH p=(m:Metric {id:$metric})
              -[:HAS_RULE]->
              (r:Rule)
              -[:HAS_CITATION]->
              (c:Citation)

        RETURN
            nodes(p) AS nodes,
            relationships(p) AS relationships
        """

        with self._driver.session() as session:

            record = session.run(
                query,
                metric=metric_id,
            ).single()

        if record is None:
            return None

        return {
            "nodes": record["nodes"],
            "relationships": record["relationships"],
        }