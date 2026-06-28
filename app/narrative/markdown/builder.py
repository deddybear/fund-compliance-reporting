from __future__ import annotations
from pathlib import Path
from app.narrative.models import NarrativeResult

def write_markdown(
        self,
        native_result: NarrativeResult,
        output_path: Path,
    ) -> Path:
        """
        Write the generated narrative as a Markdown file.

        Args:
            result:
                Narrative generation result.

            output_path:
                Destination markdown file.

        Returns:
            Path to the written report.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            native_result.content,
            encoding="utf-8",
        )

        return output_path