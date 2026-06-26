from pathlib import Path
from app.graph.database import Neo4jDatabase
from app.settings import load_settings
from app.graph.cypher_runner import CypherRunner
from app.graph.bootstrap import GraphBootstrap
from app.config.loader import ConfigurationLoader
from app.holdings.loader import HoldingsLoader

class Pipeline:

    def run(self) -> None:
        print("[BOOT] Initializing pipeline...")

        settings = load_settings()

        database = Neo4jDatabase(settings)

        print("[GRAPH] Connecting to Neo4j...")

        database.connect()

        database.verify()

        print("[GRAPH] Connected successfully.")

        runner = CypherRunner(database.driver())

        bootstrap = GraphBootstrap(
            runner=runner,
            scripts_directory=Path("neo4j")
        )

        bootstrap.initialize()
        
        database.close()

        print("[CONFIG] Initzialation Loader")

        loader = ConfigurationLoader()

        config = loader.load(
            Path("configs/firm_a.yaml")
        )

        print(
            f"[CONFIG] Loaded configuration: {config['profile']['name']}"
        )

        holdings_loader = HoldingsLoader()

        holdings = holdings_loader.load(
            Path("sample_docs/sample_holdings.csv")
        )
        
        print(
            f"[HOLDINGS] Loaded {len(holdings)} instruments."
        )
