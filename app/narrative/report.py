from __future__ import annotations
from pathlib import Path
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from app.computation.models import ComputationResult
from app.narrative.models import NarrativeResult
from app.reconciliation.models import ReconciliationResult
from app.narrative.pdf.styles import PDFStyles
from app.narrative.pdf.cover import CoverBuilder
from app.narrative.pdf.tables import TablesBuilder
from app.narrative.pdf.narrative import NarrativeBuilder
from app.narrative.pdf.footer import FooterBuilder
from app.narrative.markdown.builder import write_markdown
from app.narrative.pdf.utilization import UtilizationCalculator
from app.graph.image_service import GraphImageService

class ReportWriter:
    """
    Writes generated narrative reports to disk.
    """

    def __init__(
            self, 
            utilization: UtilizationCalculator,
            graph_image: GraphImageService,
        ) -> None:

        self.styles = PDFStyles()

        self._utilization = utilization
        self._graph_image = graph_image

        self.cover = CoverBuilder(
            self.styles,
        )

        self.tables = TablesBuilder(
            self.styles,
            self._utilization,
        )

        self.narrative = NarrativeBuilder(
            self.styles,
        )

        self.footer = FooterBuilder(
            self.styles,
        )
        
        

    def markdown(
        self,
        result: NarrativeResult,
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

        output_path = write_markdown(
            self=self,
            native_result=result,
            output_path=output_path
        )

        return output_path
    
    def pdf(
        self,
        *,
        fund_name: str,
        narrative: NarrativeResult,
        computation: ComputationResult,
        reconciliation: ReconciliationResult,
        output_path: Path,
    ) -> Path:
        """
        Generate PDF report.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = SimpleDocTemplate(
            str(output_path),
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
        )

        story: list = []

        #
        # Cover
        #
        self.cover.build(
            story=story,
            fund_name=fund_name,
            narrative=narrative,
        )

        #
        # Computed Figures
        #
        self.tables.build_computed_figures(
            story=story,
            computation=computation,
        )

        #
        # Reconciliation
        #
        self.tables.build_reconciliation(
            story=story,
            reconciliation=reconciliation,
        )

        #
        # AI Narrative
        #
        self.narrative.build(
            story=story,
            narrative=narrative,
        )

        #
        # Render PDF
        #
        document.build(
            story,
            onFirstPage=self.footer.draw,
            onLaterPages=self.footer.draw,
        )

        return output_path

