from __future__ import annotations

from app.traceability.models import Citation
from app.traceability.models import Traceability


TRACEABILITY_REGISTRY: dict[str, Traceability] = {

    #
    # Allocation
    #
    "singapore_government_securities": Traceability(
        graph_path=(
            "(AssetClass:SingaporeGovernmentSecurities)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:singapore_government_securities)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=3,
            chunk_id="allocation_sgs",
            passage_summary=(
                "Singapore Government Securities allocation."
            ),
        ),
    ),

    "mas_bills": Traceability(
        graph_path=(
            "(AssetClass:MASBills)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:mas_bills)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=3,
            chunk_id="allocation_mas",
            passage_summary=(
                "MAS Bills allocation."
            ),
        ),
    ),

    "investment_grade_corporate_bonds": Traceability(
        graph_path=(
            "(AssetClass:InvestmentGrade)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:investment_grade_corporate_bonds)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=3,
            chunk_id="allocation_ig",
            passage_summary=(
                "Investment grade allocation."
            ),
        ),
    ),

    "high_yield_bonds": Traceability(
        graph_path=(
            "(AssetClass:HighYield)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:high_yield_bonds)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=4,
            chunk_id="allocation_hy",
            passage_summary=(
                "High Yield allocation."
            ),
        ),
    ),

    "foreign_currency_bonds": Traceability(
        graph_path=(
            "(AssetClass:ForeignCurrencyBond)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:foreign_currency_bonds)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=4,
            chunk_id="allocation_fx",
            passage_summary=(
                "Foreign Currency Bond allocation."
            ),
        ),
    ),

    "structured_credit": Traceability(
        graph_path=(
            "(AssetClass:StructuredCredit)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:structured_credit)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=4,
            chunk_id="allocation_sc",
            passage_summary=(
                "Structured Credit allocation."
            ),
        ),
    ),

    "cash_and_cash_equivalents": Traceability(
        graph_path=(
            "(AssetClass:Cash)"
            "-[:CONTRIBUTES_TO]->"
            "(Allocation:cash_and_cash_equivalents)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=5,
            chunk_id="allocation_cash",
            passage_summary=(
                "Cash allocation."
            ),
        ),
    ),

    #
    # Aggregate
    #
    "Aggregate Non-IG Exposure": Traceability(
        graph_path=(
            "(AssetClass:HighYield)"
            "-[:CONTRIBUTES_TO]->"
            "(Aggregate:non_ig)"
            "<-[:CONTRIBUTES_TO]-"
            "(AssetClass:StructuredCredit)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=4,
            chunk_id="aggregate_non_ig",
            passage_summary=(
                "Aggregate non-investment-grade exposure cap."
            ),
        ),
    ),

    #
    # Concentration
    #
    "Single Issuer Concentration": Traceability(
        graph_path=(
            "(Issuer)"
            "-[:ISSUED]->"
            "(Instrument)"
            "-[:CONTRIBUTES_TO]->"
            "(Concentration:single_issuer)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=5,
            chunk_id="single_issuer",
            passage_summary=(
                "Largest single issuer concentration."
            ),
        ),
    ),

    "GRE Concentration": Traceability(
        graph_path=(
            "(Issuer:GRE)"
            "-[:ISSUED]->"
            "(Instrument)"
            "-[:CONTRIBUTES_TO]->"
            "(Concentration:gre)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=5,
            chunk_id="gre_concentration",
            passage_summary=(
                "Largest Government Related Entity concentration."
            ),
        ),
    ),

    #
    # Liquidity
    #
    "Liquidity Ratio": Traceability(
        graph_path=(
            "(Asset)"
            "-[:QUALIFIES_AS]->"
            "(LiquidAsset)"
            "-[:CONTRIBUTES_TO]->"
            "(Liquidity:ratio)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=6,
            chunk_id="liquidity_ratio",
            passage_summary=(
                "Liquidity ratio calculation."
            ),
        ),
    ),

    #
    # Market Risk
    #
    "Portfolio Modified Duration": Traceability(
        graph_path=(
            "(Holding)"
            "-[:CONTRIBUTES_TO]->"
            "(MarketRisk:modified_duration)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=7,
            chunk_id="duration",
            passage_summary=(
                "Portfolio modified duration."
            ),
        ),
    ),

    "Portfolio DV01": Traceability(
        graph_path=(
            "(Holding)"
            "-[:CONTRIBUTES_TO]->"
            "(MarketRisk:dv01)"
        ),
        citation=Citation(
            source_document="sample_fund_guidelines.pdf",
            page=7,
            chunk_id="dv01",
            passage_summary=(
                "Portfolio DV01."
            ),
        ),
    ),
}