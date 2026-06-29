MERGE (:Metric {
    id: "allocation_sgs",
    name: "Singapore Government Securities",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_mas",
    name: "MAS Bills",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_ig",
    name: "Investment Grade Corporate Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_hy",
    name: "High Yield Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_fx",
    name: "Foreign Currency Bonds",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_sc",
    name: "Structured Credit",
    section: "Allocation"
});

MERGE (:Metric {
    id: "allocation_cash",
    name: "Cash & Cash Equivalents",
    section: "Allocation"
});

MERGE (:Metric {
    id: "aggregate_non_ig",
    name: "Aggregate Non-IG Exposure",
    section: "Aggregate"
});

MERGE (:Metric {
    id: "single_issuer",
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
    id: "portfolio_duration",
    name: "Portfolio Modified Duration",
    section: "Market Risk"
});

MERGE (:Metric {
    id: "portfolio_dv01",
    name: "Portfolio DV01",
    section: "Market Risk"
});