# Computation Engine Design

## Status

Draft

---

# 1. Purpose

This document defines the architecture and operating principles of the Deterministic Computation Engine.

The Computation Engine is responsible for producing all numerical outputs used within compliance reports.

The engine operates exclusively on approved graph data and configuration-driven methodologies.

The engine serves as the authoritative source for:

* Compliance metrics
* Exposure calculations
* Threshold evaluations
* Breach determinations
* Reconciliation outputs

The engine explicitly excludes all Language Model participation from numerical computation.

---

# 2. Design Goals

The Computation Engine is designed to satisfy the following requirements:

1. Deterministic outputs
2. Reproducible calculations
3. Explainable figures
4. Configuration-driven methodologies
5. Graph-based computation
6. Traceable results
7. Audit-friendly execution

---

# 3. Design Principles

## 3.1 Deterministic by Design

Given:

* Identical graph version
* Identical holdings data
* Identical methodology profile

The engine MUST produce identical outputs.

Example:

```text
Input A
    ↓
Output X

Input A
    ↓
Output X
```

The engine MUST NOT produce different outputs for identical inputs.

---

## 3.2 Graph-Driven Computation

The engine computes figures from the approved Knowledge Graph.

The engine MUST NOT re-interpret source documents.

Approved flow:

```text
Knowledge Graph
        ↓
Computation Engine
        ↓
Computed Figures
```

---

## 3.3 Configuration-Driven Behavior

Calculation methodologies MUST be configurable.

The engine SHALL support:

```text
Firm A Methodology
Firm B Methodology
Firm C Methodology
```

without source code modifications.

---

## 3.4 Explainability First

Every figure MUST be explainable.

Each result must include:

* Figure name
* Inputs used
* Methodology profile
* Graph traversal path
* Source citations

---

# 4. Engine Architecture

The engine consists of five logical layers.

```text
Knowledge Graph
        ↓

Graph Query Layer
        ↓

Calculation Layer
        ↓

Validation Layer
        ↓

Figure Contract Builder
        ↓

Computed Figures
```

---

# 5. Processing Flow

## Step 1 — Load Approved Graph

Only approved graph versions may be used.

Validation:

```text
graph.status == APPROVED
```

Required.

---

## Step 2 — Load Methodology Profile

Example:

```text
configs/firm_a.yaml
```

The methodology profile determines:

* Limits
* Aggregation rules
* Classification mappings
* Threshold handling

---

## Step 3 — Execute Computations

The engine executes deterministic calculations.

Examples:

```text
Aggregate Exposure

Issuer Concentration

Duration

Cash Ratio

Rating Distribution
```

---

## Step 4 — Validate Results

Validation includes:

* Missing values
* Invalid classifications
* Threshold evaluation
* Configuration validation

---

## Step 5 — Build Figure Contracts

Each computed figure is converted into a standard output contract.

---

# 6. Figure Contract

Every computed figure SHALL conform to the following structure.

```json
{
  "figure": "aggregate_non_investment_grade_exposure",
  "value": 15.0,
  "unit": "%",
  "limit": 20.0,
  "status": "PASS",
  "methodology_profile": "firm_a",
  "graph_version": "graph_v5"
}
```

---

# 7. Traceability Contract

Every figure must include traceability information.

Example:

```json
{
  "figure": "aggregate_non_investment_grade_exposure",
  "graph_path": [
    "Fund",
    "Holding",
    "AssetClass",
    "Limit"
  ],
  "source_documents": [
    "sample_fund_guidelines.pdf"
  ]
}
```

---

## Required Traceability Chain

```text
Figure
    ↓
Metric
    ↓
Graph Path
    ↓
Source Citation
    ↓
Source Document
```

Figures that fail traceability validation SHALL be rejected.

---

# 8. Computation Categories

The engine supports multiple categories of calculations.

---

## Exposure Calculations

Examples:

```text
Investment Grade Exposure

Non-Investment Grade Exposure

Cash Exposure
```

---

## Concentration Calculations

Examples:

```text
Single Issuer Exposure

Parent Issuer Exposure
```

---

## Risk Calculations

Examples:

```text
Duration

Spread Duration

Weighted Average Rating
```

---

## Compliance Calculations

Examples:

```text
Threshold Evaluation

Limit Validation

Breach Detection
```

---

# 9. Methodology Switching

Methodology behavior is controlled by configuration.

Example:

```text
Firm A
    ↓
firm_a.yaml

Firm B
    ↓
firm_b.yaml
```

The engine loads configuration at runtime.

No source code modification is required.

---

## Example

Firm A:

```yaml
max_non_investment_grade: 20
```

Firm B:

```yaml
max_non_investment_grade: 15
```

The same holdings data may therefore produce different compliance outcomes.

---

# 10. LLM Boundary

The Computation Engine enforces a strict separation between numerical computation and language models.

---

## Allowed

Language Models MAY:

* Extract guideline content
* Generate narratives

---

## Prohibited

Language Models MUST NOT:

* Calculate figures
* Aggregate values
* Apply thresholds
* Determine breaches
* Modify computed figures
* Perform reconciliation

---

## Approved Architecture

```text
Knowledge Graph
        ↓
Computation Engine
        ↓
Computed Figures
        ↓
Narrative Generator
```

---

## Forbidden Architecture

```text
Knowledge Graph
        ↓
Language Model
        ↓
Computed Figures
```

---

# 11. Error Handling

The engine SHALL reject computation requests when:

* Graph version is not approved
* Configuration is invalid
* Required graph entities are missing
* Traceability validation fails

Example:

```text
ERROR:
Missing AssetClass classification.
```

---

# 12. Audit Requirements

Every computation execution generates audit events.

Examples:

| Event                     | Description            |
| ------------------------- | ---------------------- |
| CONFIG_PROFILE_LOADED     | Methodology selected   |
| FIGURE_COMPUTED           | Figure calculated      |
| FIGURE_COMPUTATION_FAILED | Figure failed          |
| BREACH_DETECTED           | Threshold exceeded     |
| TRACEABILITY_VALIDATED    | Traceability confirmed |
| TRACEABILITY_FAILED       | Traceability failed    |

All events are written to the append-only audit log.

---

# 13. Extensibility Model

New calculations should be added as isolated computation modules.

Example:

```text
engine/
├── exposure.py
├── concentration.py
├── duration.py
├── liquidity.py
└── ratings.py
```

The engine core should remain unchanged when adding new metrics.

---

# 14. Governance Rules

Rule 1

Only approved graph versions may be used.

---

Rule 2

All figures must be traceable.

---

Rule 3

All figures must conform to the Figure Contract.

---

Rule 4

All computations must be deterministic.

---

Rule 5

Language Models must remain outside the computation path.

---

# 15. Summary

The Deterministic Computation Engine is the authoritative source of all report figures.

The engine provides:

* Deterministic calculations
* Configuration-driven methodologies
* Full traceability
* Reconciliation support
* Auditability
* LLM isolation

By separating computation from narrative generation, the architecture ensures that all compliance figures remain reproducible, explainable, and suitable for regulatory reporting.
    