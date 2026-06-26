from pathlib import Path

from app.graph.cypher_runner import CypherRunner


class GraphBootstrap:
    """
    Initialize the Neo4j Knowledge Graph.

    Responsible for executing the required Cypher scripts
    in the correct order.
    """

    def __init__(
        self,
        runner: CypherRunner,
        scripts_directory: Path,
    ) -> None:
        self._runner = runner
        self._scripts_directory = scripts_directory

    def initialize(self) -> None:
        scripts = (
            "01_constraints.cypher",
            "02_indexes.cypher",
            # "03_schema.cypher",
        )

        for script in scripts:
            self._runner.execute(
                self._scripts_directory / script
            )