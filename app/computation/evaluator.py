
from __future__ import annotations

from decimal import Decimal
from typing import Any


class LimitEvaluator:
    """
    Evaluate a computed value against configured limits.
    """

    def evaluate(
        self,
        value: Decimal,
        status_values: dict[str, str],
        minimum: Decimal | None = None,
        maximum: Decimal | None = None,
    ) -> str:
        """
        Evaluate a value against optional minimum and/or maximum limits.

        Args:
            value:
                Computed value.

            status_values:
                Status values defined in configuration.

            minimum:
                Optional minimum limit.

            maximum:
                Optional maximum limit.

        Returns:
            Evaluation status.
        """

        if minimum is not None:
            if value < minimum:
                return status_values["fail"]

            if value == minimum:
                return status_values.get(
                    "warning",
                    status_values["pass"],
                )

        if maximum is not None:
            if value > maximum:
                return status_values["fail"]

            if value == maximum:
                return status_values.get(
                    "warning",
                    status_values["pass"],
                )

        return status_values["pass"]
