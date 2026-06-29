from __future__ import annotations

from pathlib import Path


def available_profiles() -> list[str]:
    """
    Discover all available configuration profiles.
    """

    config_directory = Path("configs")

    return sorted(
        config_file.stem
        for config_file in config_directory.glob("*.yaml")
    )


def profile_exists(
    profile: str,
) -> bool:
    """
    Check whether a configuration profile exists.
    """

    return profile in available_profiles()