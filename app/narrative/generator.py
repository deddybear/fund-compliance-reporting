from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.narrative.models import NarrativeContext, NarrativeResult


class NarrativeGenerator(ABC):
    """
    Abstract interface for narrative generation.

    Implementations may use OpenAI, Gemini, Claude,
    or any other language model.
    """

    @abstractmethod
    def generate(
        self,
        context: NarrativeContext,
    ) -> NarrativeResult:
        """
        Generate a narrative from the supplied context.
        """
        raise NotImplementedError