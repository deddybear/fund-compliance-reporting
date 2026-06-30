// =====================================================
// Metric -> Rule
// =====================================================

MATCH (m:Metric {id:"singapore_government_securities"})
MATCH (r:Rule {id:"singapore_government_securities"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"mas_bills"})
MATCH (r:Rule {id:"mas_bills"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"investment_grade_corporate_bonds"})
MATCH (r:Rule {id:"investment_grade_corporate_bonds"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"high_yield_bonds"})
MATCH (r:Rule {id:"high_yield_bonds"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"foreign_currency_bonds"})
MATCH (r:Rule {id:"foreign_currency_bonds"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"structured_credit"})
MATCH (r:Rule {id:"structured_credit"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"cash_and_cash_equivalents"})
MATCH (r:Rule {id:"cash_and_cash_equivalents"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"aggregate_non_ig_exposure"})
MATCH (r:Rule {id:"aggregate_non_ig_exposure"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"single_issuer_concentration"})
MATCH (r:Rule {id:"single_issuer_concentration"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"gre_concentration"})
MATCH (r:Rule {id:"gre_concentration"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"liquidity_ratio"})
MATCH (r:Rule {id:"liquidity_ratio"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"duration"})
MATCH (r:Rule {id:"duration"})
MERGE (m)-[:HAS_RULE]->(r);

MATCH (m:Metric {id:"dv01"})
MATCH (r:Rule {id:"dv01"})
MERGE (m)-[:HAS_RULE]->(r);

// =====================================================
// Rule -> Citation
// =====================================================

MATCH (r:Rule {id:"singapore_government_securities"})
MATCH (c:Citation {id:"singapore_government_securities"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"mas_bills"})
MATCH (c:Citation {id:"mas_bills"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"investment_grade_corporate_bonds"})
MATCH (c:Citation {id:"investment_grade_corporate_bonds"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"high_yield_bonds"})
MATCH (c:Citation {id:"high_yield_bonds"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"foreign_currency_bonds"})
MATCH (c:Citation {id:"foreign_currency_bonds"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"structured_credit"})
MATCH (c:Citation {id:"structured_credit"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"cash_and_cash_equivalents"})
MATCH (c:Citation {id:"cash_and_cash_equivalents"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"aggregate_non_ig_exposure"})
MATCH (c:Citation {id:"aggregate_non_ig_exposure"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"single_issuer_concentration"})
MATCH (c:Citation {id:"single_issuer_concentration"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"gre_concentration"})
MATCH (c:Citation {id:"gre_concentration"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"liquidity_ratio"})
MATCH (c:Citation {id:"liquidity_ratio"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"duration"})
MATCH (c:Citation {id:"duration"})
MERGE (r)-[:HAS_CITATION]->(c);

MATCH (r:Rule {id:"dv01"})
MATCH (c:Citation {id:"dv01"})
MERGE (r)-[:HAS_CITATION]->(c);