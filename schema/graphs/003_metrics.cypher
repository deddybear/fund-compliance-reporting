// =====================================================
// Metrics
// =====================================================

MERGE (:Metric {
    id: "singapore_government_securities",
    name: "Singapore Government Securities",
    section: "Allocation"
});

MERGE (:Metric {
    id: "mas_bills",
    name: "MAS Bills",
    section: "Allocation"
});

MERGE (:Metric {
    id: "investment_grade_corporate_bonds",
    name: "Investment Grade Corporate Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "high_yield_bonds",
    name: "High Yield Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "foreign_currency_bonds",
    name: "Foreign Currency Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "structured_credit",
    name: "Structured Credit",
    section: "Allocation"
});

MERGE (:Metric {
    id: "cash_and_cash_equivalents",
    name: "Cash & Cash Equivalents",
    section: "Allocation"
});

MERGE (:Metric {
    id: "aggregate_non_ig_exposure",
    name: "Aggregate Non-IG Exposure",
    section: "Aggregate"
});

MERGE (:Metric {
    id: "single_issuer_concentration",
    name: "Single Issuer Concentration",
    section: "Concentration"
});

MERGE (:Metric {
    id: "gre_concentration",
    name: "GRE Concentration",
    section: "Concentration"
});

MERGE (:Metric {
    id: "liquidity_ratio",
    name: "Liquidity Ratio",
    section: "Liquidity"
});

MERGE (:Metric {
    id: "duration",
    name: "Portfolio Modified Duration",
    section: "Market Risk"
});

MERGE (:Metric {
    id: "dv01",
    name: "Portfolio DV01",
    section: "Market Risk"
});