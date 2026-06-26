
from __future__ import annotations

from decimal import Decimal
from typing import Any


class LimitEvaluator:
    """
    Evaluate a computed value against configured limits.
    """

    def __init__(
        self,
        evaluation_config: dict[str, Any],
    ) -> None:
        self._status = evaluation_config["status_values"]

    def evaluate(
        self,
        value: Decimal,
        minimum: Decimal | None = None,
        maximum: Decimal | None = None,
    ) -> str:
        """
        Evaluate a value against optional minimum and/or maximum limits.
        """

        if minimum is not None:
            if value < minimum:
                return self._status["fail"]

            if value == minimum:
                return self._status["warning"]

        if maximum is not None:
            if value > maximum:
                return self._status["fail"]

            if value == maximum:
                return self._status["warning"]

        return self._status["pass"]

