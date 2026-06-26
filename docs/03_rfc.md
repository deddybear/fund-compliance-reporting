# RFC-001: Graph-Based Compliance Reporting Architecture

Author: Dedi Suharman

Status: Informational

Category: Architecture

Created: 2026-06-25

---

# Status of This Memo

This memo documents the architecture and governance model for a graph-based compliance reporting system.

This document is intended to guide implementation and establish normative requirements for deterministic computation, traceability, auditability, and language model governance.

This memo does not specify an Internet standard.

---

# Abstract

This document defines the architecture for a compliance reporting platform that combines investment guideline knowledge, portfolio holdings data, deterministic computation, and narrative generation.

The architecture is designed to satisfy the following objectives:

- Deterministic figure generation
- Graph-based knowledge representation
- Full provenance and traceability
- Configuration-driven methodology switching
- Human review controls
- Append-only audit logging
- Strict separation between numerical computation and language model outputs

The system uses a Knowledge Graph as the system of record and enforces a strict boundary between computational components and language model components.

---

# Table of Contents

1. Introduction
2. Conventions and Definitions
3. Requirements
4. System Architecture
5. Knowledge Graph Requirements
6. Deterministic Computation Requirements
7. LLM Boundary
8. Figure Contract
9. Reconciliation
10. Traceability
11. Narrative Firewall
12. Audit Logging
13. Security Considerations
14. IANA Considerations
15. References

---

# 1. Introduction

Compliance reporting systems require transparency, reproducibility, and auditability.

Investment guidelines frequently contain interconnected concepts including:

- Asset classifications
- Exposure limits
- Concentration thresholds
- Risk constraints
- Escalation procedures

These relationships are difficult to represent and reason about using isolated tabular structures.

The architecture described in this document uses a graph-based representation of regulatory knowledge and portfolio relationships, enabling deterministic figure generation and complete traceability from reported figures back to source documents.

---

# 2. Conventions and Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 and RFC 8174.

## 2.1 Knowledge Graph

A graph representation containing entities, relationships, and provenance metadata derived from investment guidelines and portfolio data.

## 2.2 Computed Figure

A deterministic numerical result produced by the computation engine.

## 2.3 Provenance

Metadata describing the origin of information.

## 2.4 Narrative

Human-readable commentary generated from computed figures.

## 2.5 Methodology Profile

A configuration package defining firm-specific reporting behavior.

---

# 3. Requirements

## R1. Deterministic Outputs

The system MUST produce identical outputs when executed against identical inputs.

## R2. Explainability

Every reported figure MUST be explainable.

## R3. Traceability

Every reported figure MUST be traceable to source material.

## R4. Auditability

The system MUST maintain an append-only audit trail.

## R5. Human Governance

The system MUST support human review before publication of extracted knowledge and generated narratives.

## R6. Methodology Switching

The system MUST support switching methodologies without source code modifications.

## R7. LLM Restrictions

Language models MUST NOT participate in numerical computation.

---

# 4. System Architecture

The architecture consists of the following major components:

1. Ingestion Layer
2. Extraction Layer
3. Graph Review Gate
4. Knowledge Graph
5. Configuration Layer
6. Computation Engine
7. Reconciliation Engine
8. Traceability Validator
9. Narrative Generator
10. Narrative Firewall
11. Narrative Review Gate
12. Audit Log Store

The approved processing flow is:

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

```

---

# 5. Knowledge Graph Requirements

The Knowledge Graph SHALL act as the system of record for guideline-derived knowledge.

The graph MUST support representation of:

- Asset Classes
- Limits
- Thresholds
- Aggregates
- Holdings
- Issuers
- Parent Issuers
- Risk Metrics
- Breach Actions

The graph MUST store provenance metadata for all extracted entities and relationships.

The implementation SHALL use Neo4j.

---

# 6. Deterministic Computation Requirements

All report figures MUST be generated by a deterministic computation engine.

The computation engine MUST:

- Produce reproducible outputs
- Operate only on approved graph data
- Generate traceable figures
- Support methodology configuration

The computation engine MUST NOT invoke language models.

---

# 7. LLM Boundary

## 7.1 Allowed Operations

Language models MAY be used for:

- Generate narrative commentary
- Explain deterministic figures
- Produce executive summary

## 7.2 Prohibited Operations

Language models MUST NOT:

- Parse holdings
- Extract regulatory rules
- Construct Knowledge Graph
- Perform calculations
- Determine compliance
- Detect breaches
- Calculate figures
- Aggregate values
- Perform arithmetic
- Apply limits
- Evaluate thresholds
- Determine breaches
- Reconcile outputs
- Modify computed figures


## 7.3 Approved Architecture

```text

        ┌─────────────────┐
        │ Knowledge Graph │
        └────────┬────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│ Deterministic Computation Engine │
└───────────────┬──────────────────┘
                │
                ▼
      ┌──────────────────┐
      │ Computed Figures │
      └────────┬─────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Narrative Generator │
    └─────────────────────┘

```

## 7.4 Prohibited Architecture

```text

    ┌─────────────────┐
    │ Knowledge Graph │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Language Model  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Computed Figures│
    └─────────────────┘

```

The language model MUST NOT be part of the numerical computation path.

---

# 8. Figure Contract

Every computed figure MUST conform to the following structure.

```json
{
  "figure": "aggregate_non_ig_exposure",
  "value": 15.0,
  "status": "PASS",
  "limit": 20.0,
  "graph_path": "...",
  "citation": {
    "source_document": "...",
    "page": 4
  }
}
```

The figure contract SHALL be used by all downstream validation components.

---

# 9. Reconciliation

The system MUST compare computed outputs against expected outputs.

The reconciliation process MUST produce:

- Expected Value
- Actual Value
- Delta
- Validation Status

Example:

```json
{
  "figure": "aggregate_non_ig_exposure",
  "expected": 15.0,
  "actual": 15.0,
  "delta": 0.0,
  "status": "PASS"
}
```

---

# 10. Traceability

Every figure MUST resolve to:

```text

Figure
    →
Graph Path
    →
Source Document

```

Figures that cannot be traced SHALL be rejected.

Traceability validation MUST be executed before report publication.

---

# 11. Narrative Firewall

The system MUST validate all generated narratives.

Every numerical value appearing in a narrative MUST already exist in the computed figure set.

Narratives containing unauthorized numerical values SHALL be rejected.

This mechanism exists to enforce the LLM Boundary defined in Section 7.

---

# 12. Audit Logging

The system MUST maintain append-only audit records.

Audit records SHALL include:

- Ingestion Events
- Extraction Events
- Review Events
- Computation Events
- Reconciliation Events
- Validation Events
- Publication Events

Audit records MUST NOT be modified or deleted.

Corrections SHALL be recorded as new events.

The implementation SHALL use PostgreSQL.

---

# 13. Security Considerations

Only approved graph versions MAY be used for computation.

Only approved narratives MAY be published.

Configuration files SHOULD be version controlled.

Audit logs SHOULD be immutable.

Access to graph modification operations SHOULD be restricted.

---

# 14. IANA Considerations

This document has no IANA actions.

---

# 15. References

## Normative References

[RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", RFC 2119.

[RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", RFC 8174.

## Informative References

Neo4j Documentation

YAML Specification

Assignment Requirements Document