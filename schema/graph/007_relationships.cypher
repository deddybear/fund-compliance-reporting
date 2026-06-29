MATCH (p:Profile {name:"firm_a"})
MATCH (g:Guideline {id:"guideline_allocation"})
MERGE (p)-[:HAS_GUIDELINE]->(g);

MATCH (p:Profile {name:"firm_b"})
MATCH (g:Guideline {id:"guideline_allocation"})
MERGE (p)-[:HAS_GUIDELINE]->(g);

MATCH (g:Guideline {id:"guideline_allocation"})
MATCH (m:Metric {section:"Allocation"})
MERGE (g)-[:DEFINES]->(m);

MATCH (g:Guideline {id:"guideline_aggregate"})
MATCH (m:Metric {id:"aggregate_non_ig"})
MERGE (g)-[:DEFINES]->(m);

MATCH (g:Guideline {id:"guideline_concentration"})
MATCH (m:Metric)
WHERE m.section = "Concentration"
MERGE (g)-[:DEFINES]->(m);

MATCH (g:Guideline {id:"guideline_liquidity"})
MATCH (m:Metric {id:"liquidity_ratio"})
MERGE (g)-[:DEFINES]->(m);

MATCH (g:Guideline {id:"guideline_market_risk"})
MATCH (m:Metric)
WHERE m.section = "Market Risk"
MERGE (g)-[:DEFINES]->(m);