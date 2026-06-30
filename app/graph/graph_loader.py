from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from neo4j import Driver


class GraphLoader:
    """
    Load a methodology configuration into Neo4j.

    Current responsibility:

    - Profile
    - Metric
    - Rule

    Relationship creation will be expanded
    incrementally during Sprint 2.
    """

    def __init__(
        self,
        driver: Driver,
    ) -> None:

        self._driver = driver

    def load(
        self,
        configuration_path: Path,
    ) -> None:

        with configuration_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            configuration = yaml.safe_load(
                file,
            )

        with self._driver.session() as session:

            self._load_profile(
                session,
                configuration,
            )

            self._load_metrics(
                session,
                configuration,
            )

            self._load_rules(
                session,
                configuration,
            )

            self._load_citations(
                session,
                configuration,
            )

            self._load_relationships(
                session,
                configuration,
            )

    # ---------------------------------------------------------

    @staticmethod
    def _load_profile(
        session,
        configuration: dict[str, Any],
    ) -> None:

        profile = configuration["profile"]

        session.run(
            """
            MERGE (p:Profile {name:$name})

            SET p.version=$version,
                p.description=$description
            """,
            name=profile["name"],
            version=profile["version"],
            description=profile["description"],
        )

    # ---------------------------------------------------------

    @staticmethod
    def _load_metrics(
        session,
        configuration: dict[str, Any],
    ) -> None:

        allocation = configuration["classification"][
            "allocation"
        ]

        for metric_id, metric_name in allocation.items():

            session.run(
                """
                MERGE (m:Metric {id:$id})

                SET m.name=$name,
                    m.section='Allocation'
                """,
                id=metric_id,
                name=metric_name,
            )

        session.run(
            """
            MERGE (m:Metric {
                id:'aggregate_non_ig_exposure'
            })

            SET m.name='Aggregate Non-IG Exposure',
                m.section='Aggregate'
            """
        )

        session.run(
            """
            MERGE (m:Metric {
                id:'single_issuer_concentration'
            })

            SET m.name='Single Issuer Concentration',
                m.section='Concentration'
            """
        )

        session.run(
            """
            MERGE (m:Metric {
                id:'gre_concentration'
            })

            SET m.name='GRE Concentration',
                m.section='Concentration'
            """
        )

        session.run(
            """
            MERGE (m:Metric {
                id:'liquidity_ratio'
            })

            SET m.name='Liquidity Ratio',
                m.section='Liquidity'
            """
        )

        session.run(
            """
            MERGE (m:Metric {
                id:'duration'
            })

            SET m.name='Portfolio Modified Duration',
                m.section='Market Risk'
            """
        )

        session.run(
            """
            MERGE (m:Metric {
                id:'dv01'
            })

            SET m.name='Portfolio DV01',
                m.section='Market Risk'
            """
        )

    # ---------------------------------------------------------

    @staticmethod
    def _load_rules(
        session,
        configuration: dict[str, Any],
    ) -> None:

        limits = configuration["limits"]

        for category, values in limits.items():

            if isinstance(values, dict):

                #
                # Asset Allocation
                #
                if all(
                    isinstance(v, dict)
                    for v in values.values()
                ):

                    for metric_id, rule in values.items():

                        session.run(
                            """
                            MERGE (r:Rule {id:$id})

                            SET
                                r.minimum=$minimum,
                                r.maximum=$maximum
                            """,
                            id=metric_id,
                            minimum=rule.get("min"),
                            maximum=rule.get("max"),
                        )

                #
                # Single Rule
                #
                else:

                    session.run(
                        """
                        MERGE (r:Rule {id:$id})

                        SET
                            r.minimum=$minimum,
                            r.maximum=$maximum
                        """,
                        id=category,
                        minimum=values.get("min"),
                        maximum=values.get("max"),
                    )

    @staticmethod
    def _load_citations(
        session,
        configuration: dict[str, Any],
    ) -> None:

        #
        # TODO:
        # nanti source document berasal dari parser PDF
        #

        metrics = []

        allocation = configuration["classification"]["allocation"]

        metrics.extend(
            allocation.keys()
        )

        metrics.extend(
            [
                "aggregate_non_ig_exposure",
                "single_issuer_concentration",
                "gre_concentration",
                "liquidity_ratio",
                "duration",
                "dv01",
            ]
        )

        for metric_id in metrics:

            session.run(
                """
                MERGE (c:Citation {id:$id})

                SET
                    c.source_document='sample_guideline.pdf',
                    c.page=1,
                    c.chunk_id=$id,
                    c.summary=$id
                """,
                id=metric_id,
            )

    @staticmethod
    def _load_relationships(
        session,
        configuration: dict[str, Any],
    ) -> None:

        profile = configuration["profile"]["name"]
    
        allocation = configuration["classification"]["allocation"]
    
        metric_ids = list(
            allocation.keys()
        )
    
        metric_ids.extend(
            [
                "aggregate_non_ig_exposure",
                "single_issuer_concentration",
                "gre_concentration",
                "liquidity_ratio",
                "duration",
                "dv01",
            ]
        )
    
        for metric_id in metric_ids:
        
            #
            # Profile -> Metric
            #
            session.run(
                """
                MATCH (p:Profile {name:$profile})
                MATCH (m:Metric {id:$metric})
    
                MERGE (p)-[:USES]->(m)
                """,
                profile=profile,
                metric=metric_id,
            )
    
            #
            # Metric -> Rule
            #
            session.run(
                """
                MATCH (m:Metric {id:$metric})
                MATCH (r:Rule {id:$metric})
    
                MERGE (m)-[:HAS_RULE]->(r)
                """,
                metric=metric_id,
            )
    
            #
            # Rule -> Citation
            #
            session.run(
                """
                MATCH (r:Rule {id:$metric})
                MATCH (c:Citation {id:$metric})
    
                MERGE (r)-[:HAS_CITATION]->(c)
                """,
                metric=metric_id,
            )