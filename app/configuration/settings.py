import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str


def load_settings() -> Settings:
    """Load application settings from environment variables."""
    load_dotenv()
    
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
        neo4j_username=os.getenv("NEO4J_USERNAME", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "password"),
    )