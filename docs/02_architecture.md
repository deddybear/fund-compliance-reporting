# Architecture Design

## Overview

The system is designed as a deterministic compliance reporting pipeline that combines document-derived regulatory knowledge with portfolio holdings data.

The architecture separates:

1. Knowledge extraction
2. Knowledge storage
3. Deterministic computation
4. Report generation
5. Validation and reconciliation

This separation ensures that language models never participate in numerical calculations, figure generation, or reconciliation logic.

---

# Architecture Principles

## Principle 1 — Deterministic Figures

All report figures are generated exclusively by the computation engine.

The language model is not allowed to:

* Calculate figures
* Round values
* Modify values
* Introduce new values

This guarantees reproducible and auditable outputs.

---

## Principle 2 — Graph-Based Computation

Investment guidelines and holdings data are stored in a unified knowledge graph.

Every reported figure is derived by traversing graph relationships rather than re-reading source documents.

---

## Principle 3 — Human Validation Gates

Two mandatory review gates are enforced:

### Graph Review Gate

Human validation of extracted entities and relationships before they become trusted knowledge.

### Narrative Review Gate

Human approval of generated report narratives before publication.

---

## Principle 4 — Full Traceability

Every figure must resolve to:

```text
Figure → Graph Path → Source Document
```

Figures without traceability are considered invalid.

---

## Principle 5 — Configuration-Driven Methodology

Firm-specific calculation methodologies are externalized into configuration files.

Switching between Firm A and Firm B requires only a configuration change and never a computation engine code modification.

---

# System Components

## 1. Ingestion Layer

Responsible for importing source materials.

### Inputs

* sample_fund_guidelines.pdf
* sample_holdings.csv

### Responsibilities

* Parse source files
* Generate document metadata
* Create ingestion records
* Trigger extraction workflow

---

## 2. Extraction Layer

Responsible for extracting structured knowledge from guideline documents.

### Responsibilities

* Entity extraction
* Relationship extraction
* Confidence scoring
* Provenance assignment

### Output

Draft knowledge graph.

---

## 3. Graph Review Gate

Human validation checkpoint.

### Responsibilities

* Review extracted entities
* Review extracted relationships
* Approve or reject graph versions

Only approved graphs can be promoted to production use.

---

## 4. Knowledge Graph

Technology:

```text
Neo4j
```

### Responsibilities

Store:

* Asset classes
* Limits
* Risk metrics
* Thresholds
* Breach actions
* Owners
* Issuers
* Parent issuers
* Holdings positions

### Additional Responsibilities

Store provenance metadata:

* Source document
* Page number
* Chunk identifier
* Extraction confidence
* Ingestion timestamp

---

## 5. Configuration Layer

Technology:

```text
YAML
```

### Examples

```text
configs/
├── firm_a.yaml
└── firm_b.yaml
```

### Responsibilities

Define:

* Methodology selection
* Asset classification rules
* Aggregation rules
* Concentration rules
* Calculation behavior

This layer enables methodology switching without modifying application code.

---

## 6. Computation Engine

Technology:

```text
Python
```

This is the core component of the system.

### Responsibilities

Compute:

* Asset allocation percentages
* Aggregate non-investment-grade exposure
* Single issuer concentration
* Group concentration
* Liquidity ratio
* Portfolio duration
* DV01-style metrics

### Requirements

* Deterministic
* Reproducible
* Configuration driven
* Graph traversal based

### Output Per Figure

```json
{
  "figure": "...",
  "value": "...",
  "status": "...",
  "limit": "...",
  "graph_path": "...",
  "citation": {...}
}
```

---

## 7. Reconciliation Engine

Technology:

```text
Python
```

### Responsibilities

Compare computed figures against:

```text
firm_A_answer_key.xlsx
```

### Output

```json
{
  "figure": "...",
  "expected": "...",
  "actual": "...",
  "delta": "...",
  "status": "PASS"
}
```

---

## 8. Traceability Validator

### Responsibilities

Verify that every figure can be resolved to:

```text
Figure → Graph Path → Source
```

A figure that cannot be traced is returned as an error.

---

## 9. Narrative Generator

Technology:

```text
LLM API
```

### Responsibilities

Generate human-readable commentary from computed figures.

### Restrictions

The model must not:

* Calculate figures
* Modify figures
* Create figures
* Introduce new numbers

The model only receives pre-computed outputs.

---

## 10. Narrative Firewall

### Responsibilities

Validate narrative content.

The firewall ensures that every numeric value appearing in the narrative already exists in the computed figure dataset.

Any unauthorized number causes validation failure.

---

## 11. Narrative Review Gate

Human approval checkpoint.

### Responsibilities

* Review generated narrative
* Approve publication
* Reject incorrect narratives

---

## 12. Audit Log Store

Technology:

```text
SQLite
```

### Responsibilities

Persist append-only audit records.

Tracked activities include:

* Ingestion
* Extraction
* Reviews
* Computation
* Reconciliation
* Traceability validation
* Narrative generation
* Publication

No audit event may be modified or deleted.

---

# High-Level Data Flow

```text

┌────────────────┐      ┌──────────────┐
│ Guidelines PDF │      │ Holdings CSV │
└────────┬───────┘      └──────┬───────┘
         └──────────┬──────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ Ingestion Layer  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Extraction Layer │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Graph Review Gate│
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Knowledge Graph  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │Configuration Layer│
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Computation Engine│
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Computed Figures │
          └───────┬─────┬────┘
                  │     │
        ┌─────────┘     └──────────┐
        ▼                          ▼
┌─────────────────┐      ┌──────────────────────┐
│ Reconciliation  │      │ Traceability         │
│ Check           │      │ Validation           │
└────────┬────────┘      └──────────┬───────────┘
         └────────────┬─────────────┘
                      │
                      ▼
          ┌─────────────────────┐
          │ Narrative Generator │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │ Narrative Firewall  │
          └─────────┬───────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │ Narrative Review    │
          │ Gate                │
          └─────────┬───────────┘
                    │
                    ▼
             ┌──────────────┐
             │ Final Report │
             └──────────────┘


---

# Deployment Architecture

The solution is deployed using Docker Compose.

```text

+--------------------------------------+
|           Docker Compose             |
+--------------------------------------+
              |
      +-------+-------+
      |               |
      v               v

+------------+   +------------+
| Neo4j      |   | Python App |
| Graph DB   |   | Pipeline   |
+------------+   +------------+
                        |
                        v

                 +-------------+
                 | SQLite  |
                 | Audit Store |
                 +-------------+

```
