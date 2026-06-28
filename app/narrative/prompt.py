from __future__ import annotations
from app.narrative.models import NarrativeContext


class PromptBuilder:
    """
    Builds prompts for the narrative generator.
    """

    SYSTEM_PROMPT = """
You are a senior investment compliance analyst.

Your task is to prepare a professional portfolio compliance report.

Instructions:

- Use only the supplied computed figures.
- Never invent numbers.
- Explain both compliant and non-compliant metrics.
- Write concise professional English.
- Produce PDF.
- Do not use tables.
- Organize the report into logical sections.
- Finish with an executive summary.
""".strip()

    def build(
        self,
        context: NarrativeContext,
    ) -> tuple[str, str]:
        """
        Build system and user prompts.
        """

        return (
            self.SYSTEM_PROMPT,
            self._build_user_prompt(
                context,
            ),
        )

    def _build_user_prompt(
        self,
        context: NarrativeContext,
    ) -> str:

        lines: list[str] = []

        lines.append(
            f"Fund Name: {context.fund_name}"
        )

        lines.append("")
        lines.append(
            "Computed Figures:"
        )
        lines.append("")

        current_section = ""

        for item in context.items:

            if item.section != current_section:

                current_section = item.section

                lines.append(
                    f"## {current_section}"
                )

            line = (
                f"- {item.title}: "
                f"{item.value}"
            )

            if item.limit:

                line += (
                    f" | Limit: {item.limit}"
                )

            if item.utilization:

                line += (
                    f" | Utilization: {item.utilization}"
                )

            line += (
                f" | Status: {item.status}"
            )

            lines.append(line)

        lines.append("")
        lines.append(
            "Generate a professional compliance narrative in Markdown."
        )

        return "\n".join(lines)
