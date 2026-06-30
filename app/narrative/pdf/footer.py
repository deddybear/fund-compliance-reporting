from __future__ import annotations

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import cm

from app.narrative.pdf.styles import PDFStyles


class FooterBuilder:
    """
    Draw page header and footer.

    This builder is used as callback for:

        document.build(
            story,
            onFirstPage=footer.draw,
            onLaterPages=footer.draw,
        )
    """

    def __init__(
        self,
        styles: PDFStyles,
    ) -> None:

        self._styles = styles

    def draw(
        self,
        canvas,
        document,
    ) -> None:

        canvas.saveState()

        self._draw_header(
            canvas,
        )

        self._draw_footer(
            canvas,
            document,
        )

        canvas.restoreState()

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    def _draw_header(
        self,
        canvas,
    ) -> None:

        width, height = canvas._pagesize

        #
        # Header line
        #
        canvas.setStrokeColor(
            colors.HexColor("#D9D9D9")
        )

        canvas.line(
            2 * cm,
            height - 2 * cm,
            width - 2 * cm,
            height - 2 * cm,
        )

        #
        # Header title
        #
        canvas.setFont(
            "Helvetica-Bold",
            11,
        )

        canvas.setFillColor(
            colors.HexColor("#163A5F")
        )

        canvas.drawString(
            2 * cm,
            height - 1.5 * cm,
            "Report Income Fund",
        )

    # ---------------------------------------------------------
    # Footer
    # ---------------------------------------------------------

    def _draw_footer(
        self,
        canvas,
        document,
    ) -> None:

        width, _ = canvas._pagesize

        #
        # Footer line
        #
        canvas.setStrokeColor(
            colors.HexColor("#D9D9D9")
        )

        canvas.line(
            2 * cm,
            2 * cm,
            width - 2 * cm,
            2 * cm,
        )

        #
        # Footer text
        #
        canvas.setFillColor(
            colors.grey
        )

        canvas.setFont(
            "Helvetica",
            8,
        )

        #
        # Generated date
        #
        canvas.drawString(
            2 * cm,
            1.4 * cm,
            datetime.now().strftime(
                "%d %B %Y"
            ),
        )


        #
        # Page number
        #
        canvas.drawRightString(
            width - 2 * cm,
            1.4 * cm,
            f"Page {document.page}",
        )