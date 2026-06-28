from __future__ import annotations
from app.computation.aggregate import AggregateCalculator
from app.computation.allocation import AllocationCalculator
from app.computation.concentration import ConcentrationCalculator
from app.computation.engine import ComputationEngine
from app.computation.evaluator import LimitEvaluator
from app.computation.liquidity import LiquidityCalculator
from app.computation.market_risk import MarketRiskCalculator
from app.configuration.loader import ConfigurationLoader
from app.configuration.settings import load_settings
from app.graph.cypher_runner import CypherRunner
from app.graph.database import Neo4jDatabase
from app.holdings.loader import HoldingsLoader
from app.reconciliation.loader import ReconciliationLoader
from app.reconciliation.comparator import Comparator
from app.reconciliation.engine import ReconciliationEngine
from app.narrative.builder import NarrativeBuilder
from app.narrative.prompt import PromptBuilder
from app.narrative.report import ReportWriter
from app.narrative.openai_generator import OpenAINarrativeGenerator



class Bootstrap:
    """
    Build and wire all application dependencies.
    """

    def __init__(self) -> None:

        #
        # Settings
        #
        self.settings = load_settings()

        #
        # Neo4j
        #
        self.database = Neo4jDatabase(
            settings=self.settings,
        )

        self.database.connect()
        self.database.verify()

        self.cypher_runner = CypherRunner(
            driver=self.database.get_driver(),
        )

        #
        # Loaders
        #
        self.configuration_loader = ConfigurationLoader()

        self.holdings_loader = HoldingsLoader()

        #
        # Shared services
        #
        self.limit_evaluator = LimitEvaluator()

        #
        # Calculators
        #
        self.allocation_calculator = AllocationCalculator(
            evaluator=self.limit_evaluator,
        )

        self.aggregate_calculator = AggregateCalculator(
            evaluator=self.limit_evaluator,
        )

        self.concentration_calculator = ConcentrationCalculator(
            evaluator=self.limit_evaluator,
        )

        self.liquidity_calculator = LiquidityCalculator(
            evaluator=self.limit_evaluator,
        )

        self.market_risk_calculator = MarketRiskCalculator(
            evaluator=self.limit_evaluator,
        )

        #
        # Engine
        #
        self.computation_engine = ComputationEngine(
            allocation=self.allocation_calculator,
            aggregate=self.aggregate_calculator,
            concentration=self.concentration_calculator,
            liquidity=self.liquidity_calculator,
            market_risk=self.market_risk_calculator,
        )

        #
        # Reconciliation
        #
        self.reconciliation_loader = ReconciliationLoader()
        
        self.reconciliation_comparator = Comparator()
        
        self.reconciliation_engine = ReconciliationEngine(
            loader=self.reconciliation_loader,
            comparator=self.reconciliation_comparator,
        )

        self.prompt_builder = PromptBuilder()
        
        self.narrative_builder = NarrativeBuilder()
        
        self.narrative_generator = OpenAINarrativeGenerator(
            api_key=self.settings.openai_api_key,
            model=self.settings.openai_model,
            prompt_builder=self.prompt_builder,
        )
        
        self.report_writer = ReportWriter()


    def shutdown(self) -> None:
        """
        Release application resources.
        """

        self.database.close()

