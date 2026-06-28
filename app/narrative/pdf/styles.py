from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_JUSTIFY,
    TA_LEFT,
)
from reportlab.lib.styles import (
    ParagraphStyle,
    StyleSheet1,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm


class PDFStyles:
    """
    Centralized PDF styles.

    Every PDF component (cover, tables, narrative, footer)
    should use styles from this class.
    """

    def __init__(self) -> None:

        stylesheet = getSampleStyleSheet()

        self.styles: StyleSheet1 = stylesheet

        #
        # Cover
        #
        self.cover_title = ParagraphStyle(
            name="CoverTitle",
            parent=stylesheet["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#163A5F"),
            spaceAfter=0.8 * cm,
        )

        self.cover_subtitle = ParagraphStyle(
            name="CoverSubtitle",
            parent=stylesheet["Heading2"],
            alignment=TA_CENTER,
            fontName="Helvetica",
            fontSize=18,
            leading=24,
            textColor=colors.HexColor("#4F81BD"),
            spaceAfter=1.5 * cm,
        )

        #
        # Heading
        #
        self.heading = ParagraphStyle(
            name="Heading",
            parent=stylesheet["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=24,
            textColor=colors.HexColor("#163A5F"),
            spaceBefore=0.6 * cm,
            spaceAfter=0.3 * cm,
        )

        self.subheading = ParagraphStyle(
            name="SubHeading",
            parent=stylesheet["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2E75B6"),
            spaceBefore=0.4 * cm,
            spaceAfter=0.2 * cm,
        )

        #
        # Body
        #
        self.body = ParagraphStyle(
            name="Body",
            parent=stylesheet["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            alignment=TA_JUSTIFY,
            textColor=colors.black,
        )

        self.body_left = ParagraphStyle(
            name="BodyLeft",
            parent=self.body,
            alignment=TA_LEFT,
        )

        #
        # Metadata
        #
        self.metadata = ParagraphStyle(
            name="Metadata",
            parent=self.body,
            alignment=TA_CENTER,
            fontSize=11,
            leading=18,
        )

        #
        # Footer
        #
        self.footer = ParagraphStyle(
            name="Footer",
            parent=self.body,
            alignment=TA_CENTER,
            fontSize=8,
            textColor=colors.grey,
        )

        #
        # Status
        #
        self.status_pass = ParagraphStyle(
            name="StatusPass",
            parent=self.body,
            alignment=TA_CENTER,
            textColor=colors.green,
            fontName="Helvetica-Bold",
        )

        self.status_warning = ParagraphStyle(
            name="StatusWarning",
            parent=self.body,
            alignment=TA_CENTER,
            textColor=colors.orange,
            fontName="Helvetica-Bold",
        )

        self.status_fail = ParagraphStyle(
            name="StatusFail",
            parent=self.body,
            alignment=TA_CENTER,
            textColor=colors.red,
            fontName="Helvetica-Bold",
        )

    def status_style(
        self,
        status: str,
    ) -> ParagraphStyle:
        """
        Return paragraph style based on status.
        """

        status = status.upper()

        if status == "PASS":
            return self.status_pass

        if status == "WARNING":
            return self.status_warning

        if status == "FAIL":
            return self.status_fail

        return self.body