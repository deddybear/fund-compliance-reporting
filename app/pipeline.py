from pathlib import Path
from decimal import Decimal
from app.bootstrap import Bootstrap
from app.computation.models import ComputationResult
from app.reconciliation.models import ReconciliationResult
from app.narrative.models import NarrativeResult

class Pipeline:
    """
    Complete application pipeline.
    """


    def __init__(
        self,
        bootstrap: Bootstrap,
    ) -> None:
        self._bootstrap = bootstrap

    def run(
        self,
        configuration_path: Path,
        holdings_path: Path,
        answer_key_path: Path,
    ) -> tuple[
        ComputationResult,
        ReconciliationResult,
        NarrativeResult,
        Path,
    ]:

        configuration = (
            self._bootstrap.configuration_loader.load(
                configuration_path,
            )
        )

        holdings = (
            self._bootstrap.holdings_loader.load(
                holdings_path,
            )
        )

        computation = (
            self._bootstrap.computation_engine.compute(
                holdings=holdings,
                configuration=configuration,
            )
        )

        reconciliation = (
            self._bootstrap.reconciliation_engine.reconcile(
                answer_key=answer_key_path,
                computed_figures=computation.figures,
                tolerance=Decimal("0.01"),
            )
        )

        #
        # Narrative Context
        #
        context = (
            self._bootstrap.narrative_builder.build(
                fund_name=configuration["profile"]["description"],
                figures=computation.figures,
            )
        )

        #
        # AI Narrative
        #
        narrative = (
            self._bootstrap.narrative_generator.generate(
                context=context,
            )
        )

        #
        # Markdown Report
        #
        report_path = (
            self._bootstrap.report_writer.write_markdown(
                result=narrative,
                output_path=Path(
                    "output/compliance_report.pdf"
                ),
            )
        )

        return (
            computation,
            reconciliation,
            narrative,
            report_path,
        )
