/*
====================================================
Graph Schema Definition
Compliance Reporting Knowledge Graph
====================================================

This file documents:

1. Node Labels
2. Relationship Types
3. Example Topology

The graph acts as the system of record for:

- Investment Guidelines
- Portfolio Holdings
- Compliance Limits
- Risk Metrics
- Provenance

====================================================
NODE LABELS
====================================================

Fund
Holding
Issuer
ParentIssuer
AssetClass
Limit
Metric
BreachAction
SourceDocument
SourceCitation

====================================================
RELATIONSHIP TYPES
====================================================

HOLDS
ISSUED_BY
PART_OF
CLASSIFIED_AS
SUBJECT_TO
EVALUATES
VIOLATION_ACTION
CITED_BY
FROM_DOCUMENT

====================================================
EXAMPLE GRAPH TOPOLOGY
====================================================

(Fund)-[:HOLDS]->(Holding)

(Holding)-[:ISSUED_BY]->(Issuer)

(Issuer)-[:PART_OF]->(ParentIssuer)

(Holding)-[:CLASSIFIED_AS]->(AssetClass)

(AssetClass)-[:SUBJECT_TO]->(Limit)

(Metric)-[:EVALUATES]->(Limit)

(Limit)-[:VIOLATION_ACTION]->(BreachAction)

(Node)-[:CITED_BY]->(SourceCitation)

(SourceCitation)-[:FROM_DOCUMENT]->(SourceDocument)

====================================================
TRACEABILITY CHAIN
====================================================

Metric
  ↓
Holding
  ↓
AssetClass
  ↓
SourceCitation
  ↓
SourceDocument

====================================================
END OF SCHEMA
====================================================
*/