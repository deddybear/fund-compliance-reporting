from pathlib import Path
from decimal import Decimal
from app.bootstrap import Bootstrap
from app.computation.models import ComputationResult
from app.reconciliation.models import ReconciliationResult
from app.narrative.models import NarrativeResult
from app.audit.events import AuditEventType
from app.audit.events import AuditStatus

class Pipeline:
    """
        End-to-end application pipeline.

        Configuration
              ↓
          Holdings
              ↓
         Computation
              ↓
       Reconciliation
              ↓
       Narrative (LLM)
              ↓
         PDF Report
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

        self._bootstrap.audit_service.log(
            event_type=AuditEventType.CONFIGURATION_LOADED,
            status=AuditStatus.SUCCESS,
            trigger_name="Pipeline.run",
            message="Configuration loaded successfully.",
            payload={
                "configuration_file": str(configuration_path),
            },
        )

        holdings = (
            self._bootstrap.holdings_loader.load(
                holdings_path,
            )
        )

        self._bootstrap.audit_service.log(
            event_type=AuditEventType.CONFIGURATION_LOADED,
            status=AuditStatus.SUCCESS,
            trigger_name="Pipeline.run",
            message="Holdings loaded successfully.",
            payload={
                "holdings_file": str(holdings_path),
                "holding_count": len(holdings),
            },
        )

        computation = (
            self._bootstrap.computation_engine.compute(
                holdings=holdings,
                configuration=configuration,
            )
        )

        self._bootstrap.audit_service.log(
            event_type=AuditEventType.COMPUTATION_COMPLETED,
            status=AuditStatus.SUCCESS,
            trigger_name="Pipeline.run",
            message="Portfolio computation completed.",
            payload={
                "figure_count": len(computation.figures),
            },
        )


        reconciliation = (
            self._bootstrap.reconciliation_engine.reconcile(
                answer_key=answer_key_path,
                computed_figures=computation.figures,
                tolerance=Decimal("0.01"),
            )
        )

        self._bootstrap.audit_service.log(
                event_type=AuditEventType.RECONCILIATION_COMPLETED,
                status=AuditStatus.SUCCESS,
                trigger_name="Pipeline.run",
                message="Reconciliation completed.",
                payload={
                    "matched": reconciliation.matched_count,
                    "failed": reconciliation.failed_count,
                    "passed": reconciliation.passed,
                },
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
                computation=computation,
            )
        )

        self._bootstrap.audit_service.log(
            event_type=AuditEventType.NARRATIVE_GENERATED,
            status=AuditStatus.SUCCESS,
            trigger_name="Pipeline.run",
            message="Narrative generated successfully.",
            payload={
                "model": narrative.model,
                "total_tokens": narrative.total_tokens,
            },
        )
        #
        # Markdown Report
        #
        # report_path = (
        #     self._bootstrap.report_writer.write_markdown(
        #         result=narrative,
        #         output_path=Path(
        #             "storage/reports/compliance_report.pdf"
        #         ),
        #     )
        # )


        report_path = (
            self._bootstrap.report_writer.pdf(
                fund_name=configuration["profile"]["description"],
                narrative=narrative,
                computation=computation,
                reconciliation=reconciliation,
                output_path=Path(
                        f"storage/reports/compliance_report_{configuration["profile"]["name"]}.pdf"
                ),
            )
        )

        self._bootstrap.audit_service.log(
            event_type=AuditEventType.REPORT_GENERATED,
            status=AuditStatus.SUCCESS,
            trigger_name="Pipeline.run",
            message="Compliance report generated.",
            payload={
                "output_file": str(report_path),
            },
        )

        return (
            computation,
            reconciliation,
            narrative,
            report_path,
        )
            

