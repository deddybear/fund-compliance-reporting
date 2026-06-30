from __future__ import annotations

from pathlib import Path

from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    Spacer,
)

from app.computation.models import ComputationResult
from app.narrative.pdf.styles import PDFStyles


class GraphsBuilder:
    """
    Render traceability graphs into the PDF.
    """

    def __init__(
        self,
        styles: PDFStyles,
    ) -> None:

        self._styles = styles

    def build(
        self,
        story: list,
        computation: ComputationResult,
    ) -> None:

        story.append(
            Spacer(
                1,
                0.8 * cm,
            )
        )

        story.append(
            Paragraph(
                "Traceability Graphs",
                self._styles.heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.3 * cm,
            )
        )

        for figure in computation.figures:

            image_path = (
                Path("storage/graphs")
                / f"{figure.metric_id}.png"
            )

            if not image_path.exists():
                continue

            story.append(
                Paragraph(
                    figure.figure,
                    self._styles.subheading,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.15 * cm,
                )
            )

            story.append(
                Image(
                    str(image_path),
                    width=16 * cm,
                    height=9 * cm,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.5 * cm,
                )
            )