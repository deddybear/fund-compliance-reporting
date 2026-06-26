# Knowledge Graph Design

## Status

Draft

---

# 1. Purpose

This document defines the knowledge graph model used by the compliance reporting platform.

The graph serves as the system of record for:

- Investment guideline knowledge
- Portfolio holdings
- Compliance limits
- Risk metrics
- Provenance metadata

The primary objective is to support:

- Deterministic figure computation
- Explainable graph traversal
- Full traceability
- Human review workflows
- Multi-firm methodology support

The knowledge graph is implemented using Neo4j.

---

# 2. Design Principles

## 2.1 Graph as System of Record

All approved regulatory knowledge SHALL be stored in the Knowledge Graph.

The computation engine MUST consume graph data rather than re-reading source documents.

---

## 2.2 Provenance by Default

Every extracted node and relationship MUST retain provenance metadata.

Required provenance attributes:

- source_document
- page_number
- chunk_id
- extraction_confidence
- graph_version

---

## 2.3 Human-Governed Knowledge

No extracted graph content may be used for computation until approved through the Graph Review Gate.

---

## 2.4 Explainable Traversal

Every reported figure MUST be explainable through graph traversal.

Required traceability chain:

```text
Reported Figure
        ↓
Computed Figure
        ↓
Knowledge Graph Path
        ↓
Source Citation
        ↓
Guideline Document
```

---

## 2.5 Versioned Knowledge

The graph SHALL support versioning.

Each approved graph snapshot SHALL receive a unique graph version identifier.

Example:

```text
graph_v1
graph_v2
graph_v3
```

Historical versions remain available for audit and reconciliation purposes.

---

# 3. Graph Scope

The graph contains two categories of information:

## Regulatory Knowledge

Derived from:

```text
sample_fund_guidelines.pdf
```

Includes:

- Asset classes
- Exposure limits
- Concentration rules
- Risk constraints
- Compliance thresholds
- Breach actions

---

## Portfolio Knowledge

Derived from:

```text
sample_holdings.csv
```

Includes:

- Holdings
- Issuers
- Parent issuers
- Ratings
- Market values
- Asset classifications

---

# 4. Node Types

## Fund

Represents a managed investment fund.

Example:

```text
Fund
 └── Sample Fixed Income Fund
```

### Properties

| Property | Type |
|----------|------|
| fund_id | string |
| name | string |
| graph_version | string |

---

## Holding

Represents a portfolio position.

### Properties

| Property | Type |
|----------|------|
| holding_id | string |
| security_name | string |
| market_value | decimal |
| currency | string |
| rating | string |
| graph_version | string |

---

## Issuer

Represents a legal issuer.

### Properties

| Property | Type |
|----------|------|
| issuer_id | string |
| issuer_name | string |
| graph_version | string |

---

## ParentIssuer

Represents an issuer group.

### Properties

| Property | Type |
|----------|------|
| parent_id | string |
| parent_name | string |
| graph_version | string |

---

## AssetClass

Represents regulatory asset classifications.

Examples:

```text
Investment Grade
Non-Investment Grade
Cash
Government Bond
Corporate Bond
```

### Properties

| Property | Type |
|----------|------|
| asset_class_id | string |
| name | string |
| graph_version | string |

---

## Limit

Represents a compliance limit.

Examples:

```text
Maximum Non-Investment Grade Exposure
Maximum Single Issuer Exposure
```

### Properties

| Property | Type |
|----------|------|
| limit_id | string |
| name | string |
| threshold | decimal |
| unit | string |
| graph_version | string |

---

## Metric

Represents a computed compliance metric.

Examples:

```text
Aggregate Non-Investment Grade Exposure
Portfolio Duration
Single Issuer Exposure
```

### Properties

| Property | Type |
|----------|------|
| metric_id | string |
| name | string |
| graph_version | string |

---

## BreachAction

Represents actions required when limits are exceeded.

### Properties

| Property | Type |
|----------|------|
| action_id | string |
| description | string |
| severity | string |
| graph_version | string |

---

## SourceDocument

Represents imported source files.

Examples:

```text
sample_fund_guidelines.pdf
sample_holdings.csv
```

### Properties

| Property | Type |
|----------|------|
| document_id | string |
| filename | string |
| sha256_hash | string |
| ingestion_timestamp | datetime |

---

## SourceCitation

Represents provenance references.

### Properties

| Property | Type |
|----------|------|
| citation_id | string |
| page_number | integer |
| chunk_id | string |
| extraction_confidence | decimal |

---

# 5. Relationship Types

## Fund Relationships

```text
(Fund)-[:HOLDS]->(Holding)
```

---

## Issuer Relationships

```text
(Holding)-[:ISSUED_BY]->(Issuer)

(Issuer)-[:PART_OF]->(ParentIssuer)
```

---

## Classification Relationships

```text
(Holding)-[:CLASSIFIED_AS]->(AssetClass)
```

---

## Compliance Relationships

```text
(AssetClass)-[:SUBJECT_TO]->(Limit)

(Metric)-[:EVALUATES]->(Limit)

(Limit)-[:VIOLATION_ACTION]->(BreachAction)
```

---

## Provenance Relationships

```text
(Node)-[:CITED_BY]->(SourceCitation)

(SourceCitation)-[:FROM_DOCUMENT]->(SourceDocument)
```

---

# 6. Provenance Model

All extracted knowledge MUST be traceable to source documents.

Example:

```text
AssetClass
      ↓
SourceCitation
      ↓
sample_fund_guidelines.pdf
```

Example citation metadata:

```json
{
  "page_number": 4,
  "chunk_id": "chunk_012",
  "extraction_confidence": 0.98
}
```

---

# 7. Graph Review Workflow

Only approved graph content may be used by the computation engine.

Workflow:

```text
Guideline Document
        ↓
Draft Graph
        ↓
Graph Review Gate
        ↓
Approved Graph
        ↓
Knowledge Graph
```

---

## Reviewer Actions

Reviewers may:

- Approve
- Reject
- Correct entities
- Correct relationships

All reviewer actions generate audit events.

---

## Approval Requirement

The computation engine MUST reject:

```text
Draft Graph
```

The computation engine MAY consume:

```text
Approved Graph
```

---

# 8. Example Graph Traversal

Example compliance question:

> What is the aggregate non-investment-grade exposure?

Traversal:

```text
Fund
 ↓
Holding
 ↓
AssetClass
 ↓
Non-Investment Grade
```

Pseudo-query:

```cypher
MATCH (f:Fund)-[:HOLDS]->(h:Holding)
      -[:CLASSIFIED_AS]->(ac:AssetClass)
WHERE ac.name = "Non-Investment Grade"

RETURN SUM(h.market_value)
```

---

# 9. Figure Traceability Example

Example reported figure:

```text
Aggregate Non-Investment Grade Exposure = 15.0%
```

Traceability path:

```text
Reported Figure
        ↓
Metric
        ↓
Holding
        ↓
AssetClass
        ↓
Source Citation
        ↓
sample_fund_guidelines.pdf
```

This traceability chain is required for publication.

---

# 10. Governance Rules

## Rule 1

All graph content MUST have provenance.

---

## Rule 2

All graph content MUST belong to a graph version.

---

## Rule 3

Only approved graph versions MAY be used for computation.

---

## Rule 4

Reviewer modifications MUST generate audit events.

---

## Rule 5

Deleted graph elements SHOULD be soft-retired and retained for audit purposes.

---

## Rule 6

Every published figure MUST resolve to:

```text
Figure
    →
Graph Path
    →
Source Citation
    →
Source Document
```

---

# 11. Summary

The Knowledge Graph serves as the central system of record for compliance reporting.

The graph provides:

- Structured regulatory knowledge
- Portfolio relationships
- Provenance tracking
- Human governance controls
- Explainable traversal paths
- Deterministic computation support

By combining graph storage, provenance metadata, and review workflows, the platform ensures that all reported figures remain explainable, traceable, reproducible, and auditable.