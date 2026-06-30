from __future__ import annotations
from datetime import datetime
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Spacer,
)

from reportlab.lib.units import cm
from app.narrative.models import NarrativeResult
from app.narrative.pdf.styles import PDFStyles


class CoverBuilder:
    """
    Builds the PDF cover page.
    """

    def __init__(
        self,
        styles: PDFStyles,
    ) -> None:

        self._styles = styles

    def build(
        self,
        story: list,
        fund_name: str,
        narrative: NarrativeResult,
    ) -> None:
        """
        Build cover page.
        """

        #
        # Top spacing
        #
        story.append(
            Spacer(
                1,
                3.5 * cm,
            )
        )

        #
        # Fund Name
        #
        story.append(
            Paragraph(
                fund_name,
                self._styles.cover_title,
            )
        )

        #
        # Report Title
        #
        story.append(
            Paragraph(
                "Portfolio Compliance Report",
                self._styles.cover_subtitle,
            )
        )

        story.append(
            Spacer(
                1,
                1.5 * cm,
            )
        )

        #
        # White Space
        #
        story.append(
            Paragraph(
                "",
                self._styles.metadata,
            )
        )

        story.append(
            Paragraph(
                "",
                self._styles.metadata,
            )
        )

        story.append(
            Spacer(
                1,
                1 * cm,
            )
        )

        #
        # Generated Time
        #
        story.append(
            Paragraph(
                "<b>Generated</b>",
                self._styles.metadata,
            )
        )

        story.append(
            Paragraph(
                datetime.now().strftime(
                    "%d %B %Y %H:%M"
                ),
                self._styles.metadata,
            )
        )

        story.append(
            Spacer(
                1,
                0.8 * cm,
            )
        )

        #
        # OpenAI Model
        #
        # story.append(
        #     Paragraph(
        #         "<b>AI Model</b>",
        #         self._styles.metadata,
        #     )
        # )

        # story.append(
        #     Paragraph(
        #         narrative.model,
        #         self._styles.metadata,
        #     )
        # )

        #
        # Token Information
        #
        # if narrative.total_tokens is not None:

        #     story.append(
        #         Spacer(
        #             1,
        #             0.8 * cm,
        #         )
        #     )

        #     story.append(
        #         Paragraph(
        #             "<b>Total Tokens</b>",
        #             self._styles.metadata,
        #         )
        #     )

        #     story.append(
        #         Paragraph(
        #             str(
        #                 narrative.total_tokens
        #             ),
        #             self._styles.metadata,
        #         )
        #     )

        #
        # Next page
        #
        story.append(
            PageBreak()
        )