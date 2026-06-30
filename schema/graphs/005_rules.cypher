// =====================================================
// Rules
// =====================================================

MERGE (:Rule {
    id: "singapore_government_securities",
    minimum: 20,
    maximum: 60
});

MERGE (:Rule {
    id: "mas_bills",
    minimum: 0,
    maximum: 40
});

MERGE (:Rule {
    id: "investment_grade_corporate_bonds",
    minimum: 10,
    maximum: 50
});

MERGE (:Rule {
    id: "high_yield_bonds",
    minimum: 0,
    maximum: 15
});

MERGE (:Rule {
    id: "foreign_currency_bonds",
    minimum: 0,
    maximum: 20
});

MERGE (:Rule {
    id: "structured_credit",
    minimum: 0,
    maximum: 10
});

MERGE (:Rule {
    id: "cash_and_cash_equivalents",
    minimum: 5,
    maximum: 25
});

MERGE (:Rule {
    id: "aggregate_non_ig_exposure",
    maximum: 20
});

MERGE (:Rule {
    id: "single_issuer_concentration",
    maximum: 8
});

MERGE (:Rule {
    id: "gre_concentration",
    maximum: 12
});

MERGE (:Rule {
    id: "liquidity_ratio",
    minimum: 25
});

MERGE (:Rule {
    id: "duration",
    minimum: 2,
    maximum: 6.5
});

MERGE (:Rule {
    id: "dv01",
    maximum: 85000
});