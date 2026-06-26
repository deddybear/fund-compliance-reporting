from pathlib import Path
from typing import cast, LiteralString
from neo4j import Query
from neo4j import Driver


class CypherRunner:
    """
    Execute Cypher scripts against Neo4j.

    This class is intentionally unaware of the execution order.
    It only executes the script that is provided.
    """

    def __init__(self, driver: Driver) -> None:
        self._driver = driver


    """
    Execute a single Cypher script.
    
    Args:
        script: Path to the .cypher file.
    """
    def execute(self, script: Path) -> None:
        if not script.exists():
            raise FileNotFoundError(script)
    
        if script.suffix != ".cypher":
            raise ValueError(f"{script} is not a Cypher script.")
    
        raw = script.read_text(encoding="utf-8").strip()
    
        if not raw:
            return
    
        # Split berdasarkan ';' lalu buang statement kosong/komentar
        statements = [
            s.strip()
            for s in raw.split(";")
            if s.strip() and not s.strip().startswith("//")
        ]
    
        print(f"[GRAPH] Executing : {script.name} ({len(statements)} statement(s))")
    
        with self._driver.session() as session:
            for stmt in statements:
                query = Query(cast(LiteralString, stmt))
                print(f"[GRAPH] Query : {query}")
                session.run(query).consume()
    
        print(f"[GRAPH] Completed {script.name}")