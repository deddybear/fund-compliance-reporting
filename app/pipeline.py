from pathlib import Path
from decimal import Decimal
from app.bootstrap import Bootstrap
from app.computation.models import ComputationResult
from app.reconciliation.models import ReconciliationResult

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

        return (
            computation,
            reconciliation,
        )
