from __future__ import annotations

from decimal import Decimal


class UtilizationCalculator:
    """
    Computes utilization against configured limits.
    """

    def calculate(
        self,
        *,
        value: Decimal,
        minimum: Decimal | None,
        maximum: Decimal | None,
    ) -> Decimal | None:

        #
        # Range
        #
        if minimum is not None and maximum is not None:

            if value < minimum:
                return (value / minimum) * Decimal("100")

            return (value / maximum) * Decimal("100")

        #
        # Upper bound
        #
        if maximum is not None:

            return (value / maximum) * Decimal("100")

        #
        # Lower bound
        #
        if minimum is not None:

            return (value / minimum) * Decimal("100")

        return None