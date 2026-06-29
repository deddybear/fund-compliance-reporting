from __future__ import annotations
from pathlib import Path
from app.computation.aggregate import AggregateCalculator
from app.computation.allocation import AllocationCalculator
from app.computation.concentration import ConcentrationCalculator
from app.computation.engine import ComputationEngine
from app.computation.evaluator import LimitEvaluator
from app.computation.liquidity import LiquidityCalculator
from app.computation.market_risk import MarketRiskCalculator
from app.configuration.loader import ConfigurationLoader
from app.configuration.settings import load_settings
# from app.graph.cypher_runner import CypherRunner
from app.graph.graph_builder import GraphBuilder
from app.graph.networkx_renderer import NetworkXRenderer
from app.graph.query_service import GraphQueryService
from app.graph.database import Neo4jDatabase
from app.graph.graph_loader import GraphLoader
from app.graph.query_service import GraphQueryService
from app.traceability.neo4j_traceability_repository import (
    Neo4jTraceabilityRepository,
)
from app.graph.image_service import GraphImageService
from app.holdings.loader import HoldingsLoader
from app.reconciliation.loader import ReconciliationLoader
from app.reconciliation.comparator import Comparator
from app.reconciliation.engine import ReconciliationEngine
from app.narrative.builder import NarrativeBuilder
from app.narrative.firewall import NarrativeFirewall
from app.narrative.prompt import PromptBuilder
from app.narrative.report import ReportWriter
from app.narrative.openai_generator import OpenAINarrativeGenerator
from app.traceability.builder import TraceabilityBuilder
from app.audit.database import AuditDatabase
from app.audit.repository import AuditRepository
from app.audit.service import AuditService
from app.narrative.pdf.utilization import UtilizationCalculator
from app.traceability.repository import TraceabilityRepository
from app.traceability.service import TraceabilityService


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
        self.databaseNeo4jDatabase = Neo4jDatabase(
            settings=self.settings,
        )

        self.databaseNeo4jDatabase.connect()
        self.databaseNeo4jDatabase.verify()

        # self.cypher_runner = CypherRunner(
        #     driver=self.databaseNeo4jDatabase.get_driver(),
        # )

        self.graph_loader = GraphLoader(
            driver=self.databaseNeo4jDatabase.get_driver(),
        )

        self.graph_query_service = GraphQueryService(
            driver=self.databaseNeo4jDatabase.get_driver(),
        )

        #
        # Graph Rendering
        #
        self.graph_query_service = GraphQueryService(
            driver=self.databaseNeo4jDatabase.get_driver(),
        )

        self.graph_builder = GraphBuilder()

        self.graph_renderer = NetworkXRenderer()

        self.graph_image_service = GraphImageService(
            query=self.graph_query_service,
            builder=self.graph_builder,
            renderer=self.graph_renderer,
        )

        #
        # Audit
        #
        self.audit_database = AuditDatabase(
            database_path=Path(
                "storage/audit/audit.db"
            ),
        )

        self.audit_database.initialize()

        self.audit_repository = AuditRepository(
            database=self.audit_database,
        )

        self.audit_service = AuditService(
            repository=self.audit_repository,
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

        self.traceability_repository = Neo4jTraceabilityRepository(
            graph=self.graph_query_service,
        )

        self.traceability_service = TraceabilityService(
            repository=self.traceability_repository,
        )
        
        self.traceability_builder = TraceabilityBuilder(
            service=self.traceability_service,
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
            traceability=self.traceability_builder,
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
        self.narrative_firewall= NarrativeFirewall()
        
        self.narrative_generator = OpenAINarrativeGenerator(
            api_key=self.settings.openai_api_key,
            model=self.settings.openai_model,
            prompt_builder=self.prompt_builder,
            firewall=self.narrative_firewall
        )

        self.utilization_calculator = UtilizationCalculator()
        
        self.report_writer = ReportWriter(
            utilization=self.utilization_calculator,
            graph_image=self.graph_image_service
        )


    def shutdown(self) -> None:
        """
        Release application resources.
        """

        self.databaseNeo4jDatabase.close()
        self.audit_database.close()

