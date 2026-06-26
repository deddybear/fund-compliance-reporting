from pathlib import Path
from typing import Any

import yaml


class ConfigurationLoader:
    """Load methodology configuration from YAML files."""

    def load(self, path: Path) -> dict[str, Any]:
        """
        Load a YAML configuration file.

        Args:
            path: Path to the configuration file.

        Returns:
            Parsed YAML as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file extension is invalid.
        """

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        if path.suffix not in {".yaml", ".yml"}:
            raise ValueError("Configuration file must be a YAML file.")

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError("Configuration must be a YAML mapping.")

        return data