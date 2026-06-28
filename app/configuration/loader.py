from __future__ import annotations
from pathlib import Path
from typing import Any

import yaml


class ConfigurationLoader:
    """
    Loads portfolio configuration from YAML.
    """

    def load(
        self,
        path: Path,
    ) -> dict[str, Any]:
        """
        Load a YAML configuration file.

        Args:
            path: Configuration YAML path.

        Returns:
            Configuration dictionary.
        """

        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {path}"
            )

        if path.suffix.lower() not in {
            ".yaml",
            ".yml",
        }:
            raise ValueError(
                "Configuration must be a YAML file."
            )

        with path.open(
            mode="r",
            encoding="utf-8",
        ) as file:

            configuration = yaml.safe_load(file)

        if not isinstance(configuration, dict):
            raise ValueError(
                "Invalid configuration format."
            )

        return configuration

