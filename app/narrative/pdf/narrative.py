from __future__ import annotations

from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    Spacer,
)

from app.narrative.models import NarrativeResult
from app.narrative.pdf.styles import PDFStyles


class NarrativeBuilder:
    """
    Builds the AI Narrative section.
    """

    def __init__(
        self,
        styles: PDFStyles,
    ) -> None:

        self._styles = styles

    def build(
        self,
        story: list,
        narrative: NarrativeResult,
    ) -> None:
        """
        Build AI Narrative section.
        """

        story.append(
            Paragraph(
                "AI Compliance Narrative",
                self._styles.heading,
            )
        )

        story.append(
            Spacer(
                1,
                0.3 * cm,
            )
        )

        paragraphs = self._split_paragraphs(
            narrative.content,
        )

        for paragraph in paragraphs:

            story.append(
                Paragraph(
                    paragraph,
                    self._styles.body,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.25 * cm,
                )
            )

        #
        # Metadata
        #
        story.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

        # story.append(
        #     Paragraph(
        #         "Generation Metadata",
        #         self._styles.subheading,
        #     )
        # )

        # metadata = [
        #     (
        #         "Model",
        #         narrative.model,
        #     ),
        #     (
        #         "Prompt Tokens",
        #         self._value(
        #             narrative.prompt_tokens,
        #         ),
        #     ),
        #     (
        #         "Completion Tokens",
        #         self._value(
        #             narrative.completion_tokens,
        #         ),
        #     ),
        #     (
        #         "Total Tokens",
        #         self._value(
        #             narrative.total_tokens,
        #         ),
        #     ),
        # ]

        # for label, value in metadata:

        #     story.append(
        #         Paragraph(
        #             f"<b>{label}</b>: {value}",
        #             self._styles.body_left,
        #         )
        #     )

    @staticmethod
    def _split_paragraphs(
        text: str,
    ) -> list[str]:
        """
        Split narrative into paragraphs.
        """

        paragraphs = []

        for paragraph in text.split("\n\n"):

            paragraph = (
                paragraph
                .replace("\n", "<br/>")
                .strip()
            )

            if paragraph:

                paragraphs.append(
                    paragraph,
                )

        return paragraphs

    @staticmethod
    def _value(
        value: int | None,
    ) -> str:

        if value is None:
            return "-"

        return str(value)