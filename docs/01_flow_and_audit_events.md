# Flow Design and Audit Event Model

## Purpose

This document defines the end-to-end processing flow, governance controls, and audit event model for the compliance reporting system.

The design emphasizes:

* Deterministic computation
* Human oversight
* Full traceability
* Append-only auditability
* Strict separation between language models and numerical computation

---

# 1. End-to-End Processing Flow

## Current-State (Typical Manual Process)

```text

    Guideline Documents
            +
    Portfolio Holdings
            |
            v

    Manual Interpretation
            |
            v

    Spreadsheet Calculations
            |
            v

    Manual Validation
            |
            v

    Narrative Writing
            |
            v

      Final Report
```

### Challenges

* Manual interpretation is error-prone.
* Calculations are difficult to audit.
* Traceability is limited.
* Methodology changes require significant manual effort.
* Reviewer decisions are often not preserved.

---

## Target-State (Proposed Architecture)

```text

            ┌─────────────────────┐     
            │ Guideline Documents │
            │ Portfolio Holdings  │
            └──────────┬──────────┘      
                       │
                       ▼
              ┌───────────────────┐
              │ Graph Review Gate │
              └────────┬──────────┘
                       │ Approved
                       ▼
          ┌──────────────────────────┐
          │ Approved Knowledge Graph │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Configuration Selection │
          └────────────┬────────────┘
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
         ┌───────────────────────┐
         │Traceability Validation│
         └──────────┬────────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │ Reconciliation Check│
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ Narrative Generation│
          └──────────┬──────────┘
                     │
                     ▼
       ┌────────────────────────────┐
       │ Narrative Firewall Check   │
       └────────────┬───────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Narrative Review Gate│
         └──────────┬───────────┘
                    │ 
                    ▼
            ┌────────────────┐
            │  Final Report  │
            └────────────────┘
```

---

# 2. Human Review Gates

The architecture introduces mandatory human review checkpoints.

These gates ensure that language model outputs cannot directly become published outputs.

---

## Gate 1 — Graph Review Gate

### Purpose

Validate extracted entities and relationships before they become trusted knowledge.

### Inputs

* Extracted entities
* Extracted relationships
* Provenance metadata

### Reviewer Actions

Reviewers may:

* Approve extraction
* Reject extraction
* Correct entities
* Correct relationships

### Outputs

* Approved Graph Version
* Rejected Graph Version

### Audit Requirement

All reviewer actions generate immutable audit events.

---

## Gate 2 — Narrative Review Gate

### Purpose

Validate generated narratives before publication.

### Inputs

* Computed figures
* Generated narrative
* Narrative firewall results

### Reviewer Actions

Reviewers may:

* Approve narrative
* Reject narrative
* Request regeneration

### Outputs

* Published Report
* Rejected Report

### Audit Requirement

All reviewer decisions are recorded in the audit log.

---

# 3. Language Model Boundary

Language models are intentionally restricted.

They assist with extraction and narrative generation but never participate in numerical computation.

---

## Allowed Responsibilities

### Knowledge Extraction

Input:

```text
Guideline Documents
```

Output:

```text
Draft Entities
Draft Relationships
```

### Narrative Generation

Input:

```text
Approved Computed Figures
```

Output:

```text
Human Readable Commentary
```

---

## Prohibited Responsibilities

Language models MUST NOT:

* Calculate figures
* Aggregate values
* Perform arithmetic
* Apply thresholds
* Determine breaches
* Round values
* Reconcile outputs
* Modify computed figures

---

## Approved Processing Pattern

```text

┌──────────────────────────────────────────┐
│            Knowledge Graph               │
│      (Approved Structured Facts)         │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│    Deterministic Computation Engine      │
│  • Rule-based Calculations               │
│  • Formula Execution                     │
│  • Metric Aggregation                    │
└──────────────────┬───────────────────────┘
                   ▼
┌──────────────────────────────────────────┐
│             Computed Figures             │
│      (Verified Quantitative Results)     │
└──────────────────┬───────────────────────┘
                   ▼
┌──────────────────────────────────────────┐
│          Narrative Generator             │
│    (Figures → Human-readable Report)     │
└──────────────────────────────────────────┘

```

---

## Forbidden Processing Pattern



```text
    
┌──────────────────────────┐
│      Knowledge Graph     │
│ (Structured Portfolio    │
│ Facts and Relationships) │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│           LLM            │
│ (Analysis & Computation) │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Computed Figures     │
│ (Metrics and Results)    │
└──────────────────────────┘

```

In this design the language model becomes part of the numerical computation path and therefore violates system requirements.

---

## Boundary Enforcement Mechanisms

The boundary is enforced through:

1. Deterministic Computation Engine
2. Traceability Validation
3. Narrative Firewall Validation

Any figure not produced by the computation engine is rejected.

Any narrative introducing unauthorized values is rejected.

---

# 4. Traceability Model

Every reported figure must be traceable to its source.

Required traceability chain:

```text

    ┌─────────────────┐
    │ Reported Figure │
    └───────┬─────────┘
            │
            ▼
┌──────────────────────────┐
│ Computed Figure Contract │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────┐
│ Knowledge Graph Path │
└───────────┬──────────┘
            │
            ▼
┌─────────────────┐
│ Source Citation │
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│ Guideline Document │
└────────────────────┘

---

## Example

```text

┌──────────────────────────────────────┐
│ Aggregate Non-Investment Grade       │
│ Exposure                             │
└──────────────────┬───────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │     15.0%      │
          └───────┬────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│ Holding → Asset Class → Limit        │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ sample_fund_guidelines.pdf           │
│ Page 4                               │
└──────────────────────────────────────┘

```

---

# 5. Narrative Firewall

The Narrative Firewall prevents language models from introducing unauthorized numerical values.

---

## Validation Rule

Every numerical value appearing in a narrative must already exist within the computed figure dataset.

---

## Example

### Computed Figures

```json
{
  "duration": 5.2,
  "cash_ratio": 4.1
}
```

### Valid Narrative

```text
Portfolio duration is 5.2 years.
Cash ratio is 4.1%.
```

### Invalid Narrative

```text
Portfolio duration is 5.2 years.
Cash ratio is 4.5%.
```

The value `4.5` does not exist in the computed figures and causes validation failure.

---

# 6. Audit Event Catalogue

All significant workflow actions generate audit events.

| Event                      | Trigger                                          | Data Captured                                    | Retention |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------ | --------- |
| DOCUMENT_INGESTED          | Source document imported                         | Document ID, filename, SHA256 hash, timestamp    | 7 years   |
| HOLDINGS_IMPORTED          | Holdings file imported                           | File hash, position count                        | 7 years   |
| GRAPH_IMPORTED             | Graph imported                                   | Node count, edge count, confidence summary       | 7 years   |
| GRAPH_REVIEW_REQUESTED     | Graph submitted for review                       | Graph version, reviewer assignment               | 7 years   |
| GRAPH_CORRECTED            | Reviewer modifies extracted graph                | Reviewer ID, graph version, modification summary | 7 years   |
| GRAPH_APPROVED             | Graph approved                                   | Reviewer ID, approval timestamp                  | 7 years   |
| GRAPH_REJECTED             | Graph rejected                                   | Reviewer ID, rejection reason                    | 7 years   |
| GRAPH_PUBLISHED            | Approved graph activated                         | Graph version, activation timestamp              | 7 years   |
| CONFIG_PROFILE_LOADED      | Firm methodology selected                        | Profile name, version, configuration hash        | 7 years   |
| FIGURE_COMPUTED            | Figure calculated                                | Figure name, value, limit, status                | 7 years   |
| FIGURE_COMPUTATION_FAILED  | Figure calculation failed                        | Figure name, failure reason                      | 7 years   |
| BREACH_DETECTED            | Threshold exceeded                               | Figure, threshold, actual value                  | 7 years   |
| TRACEABILITY_VALIDATED     | Traceability check passed                        | Figure name, graph path, citation                | 7 years   |
| TRACEABILITY_FAILED        | Traceability check failed                        | Figure name, failure reason                      | 7 years   |
| RECONCILIATION_COMPLETED   | Answer key comparison completed                  | Expected value, actual value, delta              | 7 years   |
| RECONCILIATION_FAILED      | Reconciliation mismatch detected                 | Expected value, actual value, delta              | 7 years   |
| REPORT_DATASET_FINALIZED   | Figure dataset approved for narrative generation | Report ID, dataset version                       | 7 years   |
| NARRATIVE_GENERATED        | Narrative generated                              | Prompt version, model version                    | 7 years   |
| FIREWALL_VALIDATED         | Narrative passed validation                      | Report ID, validation result                     | 7 years   |
| FIREWALL_FAILED            | Narrative introduced unauthorized value          | Report ID, offending value                       | 7 years   |
| NARRATIVE_REVIEW_REQUESTED | Narrative submitted for review                   | Reviewer assignment                              | 7 years   |
| NARRATIVE_APPROVED         | Narrative approved                               | Reviewer ID, approval timestamp                  | 7 years   |
| NARRATIVE_REJECTED         | Narrative rejected                               | Reviewer ID, rejection reason                    | 7 years   |
| REPORT_PUBLISHED           | Final report published                           | Report ID, publication timestamp                 | 7 years   |
| REPORT_REJECTED            | Publication rejected                             | Report ID, rejection reason                      | 7 years   |

---

# 7. Append-Only Audit Requirement

The audit log is immutable.

The system MUST NOT:

* Update audit events
* Delete audit events
* Overwrite audit events

Corrections, reversals, and reviewer modifications SHALL be recorded as new events.

---

## Example

```text

    GRAPH_APPROVED
          ↓
    GRAPH_CORRECTED
          ↓
    GRAPH_APPROVED

```

The complete history remains preserved.

---

# 8. Summary

The proposed workflow introduces:

* Human governance through review gates
* Deterministic figure generation
* Strict language model boundaries
* Full traceability
* Narrative validation controls
* Append-only audit logging

Together, these controls ensure that compliance reports remain reproducible, explainable, traceable, and auditable.
