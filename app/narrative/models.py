from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class NarrativeItem:
    """
    Represents one computed figure prepared for narrative generation.
    """

    section: str

    title: str

    value: str

    limit: str

    status: str

    utilization: str | None = None


@dataclass(slots=True, frozen=True)
class NarrativeContext:
    """
    Context passed to the narrative generator.
    """

    fund_name: str

    items: list[NarrativeItem]

@dataclass(slots=True, frozen=True)
class NarrativeResult:
    """
    Result returned by a narrative generator.
    """

    content: str

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None