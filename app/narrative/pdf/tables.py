from __future__ import annotations
import re
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from typing import Any
from app.computation.models import ComputationResult
from app.reconciliation.models import ReconciliationResult
from app.narrative.pdf.styles import PDFStyles
from app.narrative.pdf.utilization import UtilizationCalculator
from app.reconciliation.mapping import to_display_name


class TablesBuilder:
    """
    Builds all PDF tables.

    Currently:
    - Computed Figures
    - Reconciliation
    """

    def __init__(
        self,
        styles: PDFStyles,
        utilization : UtilizationCalculator
    ) -> None:
        self._utilization = utilization
        self._styles = styles

    # ---------------------------------------------------------
    # Computed Figures
    # ---------------------------------------------------------

    def build_computed_figures(
        self,
        story: list,
        computation: ComputationResult,
    ) -> None:

        story.append(
            Paragraph(
                "Computed Figures",
                self._styles.heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.3 * cm,
            )
        )

        rows: list[list[Any]] = [
            [
                "Section",
                "Figure",
                "Value",
                "Limit",
                "Utilization",
                "Status",
            ]
        ]

        for figure in computation.figures:

            utilization = self._utilization.calculate(
                value=figure.value,
                minimum=figure.minimum,
                maximum=figure.maximum,
            )

            rows.append(
                [
                    Paragraph(
                        figure.section,
                        self._styles.body_left,
                    ),
                    Paragraph(
                        to_display_name(figure.figure),
                        self._styles.body_left,
                    ),
                    Paragraph(
                        self._format_decimal(
                            figure.value
                        ),
                        self._styles.body,
                    ),
                    Paragraph(
                        figure.limit,
                        self._styles.body,
                    ),
                    Paragraph(
                        self._format_utilization(
                            utilization,
                        ),
                        self._styles.body,
                    ),
                    Paragraph(
                        figure.status,
                        self._styles.status_style(
                            figure.status,
                        ),
                    ),
                ]
            )

        table = Table(
            rows,
            colWidths=[
                3.2 * cm,
                6.0 * cm,
                2.2 * cm,
                2.4 * cm,
                3.0 * cm,
                2.2 * cm,
            ],
        )

        table.setStyle(
            self._default_table_style()
        )

        story.append(table)

    # ---------------------------------------------------------
    # Reconciliation
    # ---------------------------------------------------------

    def build_reconciliation(
        self,
        story: list,
        reconciliation: ReconciliationResult,
    ) -> None:

        story.append(
            Spacer(
                1,
                0.8 * cm,
            )
        )

        story.append(
            Paragraph(
                "Reconciliation",
                self._styles.heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.3 * cm,
            )
        )

        rows : list[list[Any]] = [
            [
                "Figure",
                "Expected",
                "Actual",
                "Matched",
            ]
        ]

        for item in reconciliation.items:

            rows.append(
                [
                    Paragraph(
                        item.figure,
                        self._styles.body_left,
                    ),
                    Paragraph(
                        self._format_decimal(
                            item.expected_value
                        ),
                        self._styles.body,
                    ),
                    Paragraph(
                        self._format_decimal(
                            item.actual_value
                        ),
                        self._styles.body,
                    ),
                    Paragraph(
                        "PASS"
                        if item.matched
                        else "FAIL",
                        self._styles.status_style(
                            "PASS"
                            if item.matched
                            else "FAIL",
                        ),
                    ),
                ]
            )

        table = Table(
            rows,
            colWidths=[
                9 * cm,
                2.5 * cm,
                2.5 * cm,
                3 * cm,
            ],
        )

        table.setStyle(
            self._default_table_style()
        )

        story.append(table)

        story.append(
            Spacer(
                1,
                0.4 * cm,
            )
        )

        summary = (
            f"<b>Matched:</b> "
            f"{reconciliation.matched_count}"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            f"<b>Failed:</b> "
            f"{reconciliation.failed_count}"
        )

        story.append(
            Paragraph(
                summary,
                self._styles.body_left,
            )
        )

    # ---------------------------------------------------------
    # Shared Style
    # ---------------------------------------------------------

    @staticmethod
    def _default_table_style() -> TableStyle:

        return TableStyle(
            [

                #
                # Header
                #
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#163A5F"),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    8,
                ),

                #
                # Body
                #
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.whitesmoke,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "ALIGN",
                    (2, 1),
                    (-1, -1),
                    "CENTER",
                ),

            ]
        )

    # ---------------------------------------------------------
    # Formatter
    # ---------------------------------------------------------

    @staticmethod
    def _format_decimal(
        value,
    ) -> str:

        if isinstance(
            value,
            Decimal,
        ):

            return format(
                value.normalize(),
                "f",
            )

        return str(value)
    

    @staticmethod
    def _format_utilization(
        value: Decimal | None,
    ) -> str:

        if value is None:
            return "-"

        return f"{value.quantize(Decimal('0.1'))}%"
    
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