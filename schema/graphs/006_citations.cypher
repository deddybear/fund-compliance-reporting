// =====================================================
// Citations
// =====================================================

MERGE (:Citation {
    id: "singapore_government_securities",
    source_document: "sample_fund_guidelines.pdf",
    page: 1,
    chunk_id: "singapore_government_securities",
    summary: "Singapore Government Securities (AAA-rated only) allocation must remain between 20% and 60% of NAV."
});

MERGE (:Citation {
    id: "mas_bills",
    source_document: "sample_fund_guidelines.pdf",
    page: 1,
    chunk_id: "mas_bills",
    summary: "MAS Bills may be held up to 40% of NAV as liquidity buffer."
});

MERGE (:Citation {
    id: "investment_grade_corporate_bonds",
    source_document: "sample_fund_guidelines.pdf",
    page: 1,
    chunk_id: "investment_grade_corporate_bonds",
    summary: "Investment Grade Corporate Bonds allocation must remain between 10% and 50%."
});

MERGE (:Citation {
    id: "high_yield_bonds",
    source_document: "sample_fund_guidelines.pdf",
    page: 1,
    chunk_id: "high_yield_bonds",
    summary: "High Yield Bonds allocation must not exceed 15%."
});

MERGE (:Citation {
    id: "foreign_currency_bonds",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "foreign_currency_bonds",
    summary: "Foreign Currency Bonds must be fully currency hedged and limited to 20%."
});

MERGE (:Citation {
    id: "structured_credit",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "structured_credit",
    summary: "Structured Credit limited to AAA tranches and maximum 10%."
});

MERGE (:Citation {
    id: "cash_and_cash_equivalents",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "cash_and_cash_equivalents",
    summary: "Cash and Cash Equivalents must remain between 5% and 25%."
});

MERGE (:Citation {
    id: "aggregate_non_ig_exposure",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "aggregate_non_ig_exposure",
    summary: "Aggregate exposure to High Yield Bonds and Structured Credit must not exceed 20%."
});

MERGE (:Citation {
    id: "single_issuer_concentration",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "single_issuer_concentration",
    summary: "Single issuer concentration must not exceed 8%."
});

MERGE (:Citation {
    id: "gre_concentration",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "gre_concentration",
    summary: "GRE concentration must not exceed 12%."
});

MERGE (:Citation {
    id: "liquidity_ratio",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "liquidity_ratio",
    summary: "Liquid assets must constitute at least 25%."
});

MERGE (:Citation {
    id: "duration",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "duration",
    summary: "Portfolio Modified Duration must remain between 2 and 6.5 years."
});

MERGE (:Citation {
    id: "dv01",
    source_document: "sample_fund_guidelines.pdf",
    page: 2,
    chunk_id: "dv01",
    summary: "Portfolio DV01 must not exceed SGD 85,000."
});