from __future__ import annotations
import re
from decimal import Decimal

from app.computation.models import ComputationResult
from app.narrative.models import FirewallResult



class NumberRule:
    """
    Validate that every computed figure appearing in the
    narrative matches the deterministic computation result.

    Strategy

        Figure
            ↓
        Find metric in narrative
            ↓
        Extract nearby text
            ↓
        Extract numbers
            ↓
        Compare against expected value
    """

    WINDOW_SIZE = 180

    NUMBER_PATTERN = re.compile(
        r"\d[\d,]*(?:\.\d+)?(?:[eE][+-]?\d+)?"
    )

    TOLERANCE = Decimal("0.01")

    def validate(
        self,
        *,
        computation: ComputationResult,
        narrative: str,
        result: FirewallResult,
    ) -> None:

        narrative_lower = narrative.lower()

        for figure in computation.figures:

            metric = figure.figure.lower()

            #
            # Locate metric inside narrative.
            #
            index = narrative_lower.find(metric)

            if index < 0:
                #
                # MetricRule will report this.
                #
                continue

            #
            # Extract local context only.
            #
            window = narrative[
                index : index + self.WINDOW_SIZE
            ]

            values = self._extract_numbers(
                window,
            )

            if not values:

                result.add_issue(
                    rule="NumberRule",
                    message=(
                        f"No numeric value found near "
                        f"metric '{figure.figure}'."
                    ),
                    actual=window,
                )

                continue

            expected = self._normalize(
                figure.value,
            )

            matched = any(
                abs(
                    expected - value
                )
                <= self.TOLERANCE
                for value in values
            )

            if not matched:

                result.add_issue(
                    rule="NumberRule",
                    message=(
                        f"Metric '{figure.figure}' "
                        f"expected {expected} "
                        f"but found {values}."
                    ),
                    actual=window,
                )
            

    def _extract_numbers(
        self,
        text: str,
    ) -> list[Decimal]:

        values: list[Decimal] = []

        for raw in self.NUMBER_PATTERN.findall(
            text
        ):

            try:

                values.append(
                    self._normalize(raw)
                )

            except Exception:

                continue

        return values

    def _normalize(
        self,
        value: str | Decimal,
    ) -> Decimal:

        if isinstance(
            value,
            Decimal,
        ):
            return value

        cleaned = (
            str(value)
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        return Decimal(cleaned)



class MetricRule:
    """
    Validate that every computed metric is mentioned
    somewhere in the generated narrative.
    """

    def validate(
        self,
        *,
        computation: ComputationResult,
        narrative: str,
        result: FirewallResult,
    ) -> None:

        normalized_text = self._normalize(
            narrative,
        )

        for figure in computation.figures:

            metric = self._normalize(
                figure.figure,
            )

            if metric not in normalized_text:

                result.add_issue(
                    rule="MetricRule",
                    message=(
                        f"Metric '{figure.figure}' "
                        "not found in narrative."
                    ),
                    expected=figure.figure,
                )

    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize text for metric matching.

        Example

            singapore_government_securities
                ↓
            singapore government securities

            Portfolio-Modified-Duration
                ↓
            portfolio modified duration
        """

        text = text.lower()

        text = text.replace("_", " ")

        text = text.replace("-", " ")

        #
        # Remove punctuation.
        #
        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
        )

        #
        # Collapse multiple spaces.
        #
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()


class StatusRule:
    """
    Validate that PASS / FAIL status is consistent.
    """

    def validate(
        self,
        *,
        computation: ComputationResult,
        narrative: str,
        result: FirewallResult,
    ) -> None:

        lower_text = narrative.lower()

        for figure in computation.figures:

            status = figure.status.upper()

            if status == "PASS":

                if (
                    "breach" in lower_text
                    and figure.figure.lower() in lower_text
                ):

                    result.add_issue(
                        rule="StatusRule",
                        message="Narrative indicates breach for a PASS figure.",
                        expected="PASS",
                        actual="BREACH",
                    )

            elif status == "FAIL":

                if (
                    "compliant" in lower_text
                    and figure.figure.lower() in lower_text
                ):

                    result.add_issue(
                        rule="StatusRule",
                        message="Narrative indicates compliant for a FAIL figure.",
                        expected="FAIL",
                        actual="COMPLIANT",
                    )


class CitationRule:
    """
    Validate that every figure contains traceability
    metadata before narrative publication.
    """

    def validate(
        self,
        *,
        computation: ComputationResult,
        narrative: str,
        result: FirewallResult,
    ) -> None:

        for figure in computation.figures:

            if figure.citation is None:

                result.add_issue(
                    rule="CitationRule",
                    message="Missing citation.",
                    expected=figure.figure,
                )

            if figure.graph_path is None:

                result.add_issue(
                    rule="CitationRule",
                    message="Missing graph path.",
                    expected=figure.figure,
                )
