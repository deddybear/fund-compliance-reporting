# Graph Review Workflow

## Status

Draft

---

# 1. Purpose

This document defines the governance process for reviewing and approving graph content before it becomes available for compliance computation.

The review workflow exists to ensure that:

- Extracted knowledge is accurate
- Provenance is preserved
- Graph relationships are valid
- Human oversight is enforced
- Only trusted graph versions are used for reporting

This workflow implements the **Graph Review Gate** described in RFC-001.

---

# 2. Objectives

The Graph Review Workflow aims to:

1. Prevent unverified knowledge from entering production.
2. Ensure all graph entities have provenance.
3. Ensure all graph relationships are logically valid.
4. Maintain a complete audit trail of reviewer actions.
5. Support versioned graph publication.

---

# 3. Review Lifecycle

The review lifecycle consists of five stages.

```text
  Source Documents
        ↓
    Draft Graph
        ↓
    Human Review
        ↓
   Approved Graph
        ↓
Production Knowledge Graph
```

---

# 4. Workflow States

## State 1 — Draft

Graph content has been extracted but has not yet been reviewed.

Characteristics:

- Not trusted
- Not available for computation
- Editable by reviewers

Example:

```text
Status: DRAFT
Version: graph_v5
```

---

## State 2 — In Review

The graph is actively being reviewed.

Characteristics:

- Assigned to reviewer
- Under validation
- Pending decision

Example:

```text
Status: IN_REVIEW
Assigned Reviewer: reviewer_01
```

---

## State 3 — Approved

The graph has passed review.

Characteristics:

- Trusted
- Available for computation
- Eligible for publication

Example:

```text
Status: APPROVED
Version: graph_v5
```

---

## State 4 — Rejected

The graph contains issues requiring correction.

Characteristics:

- Not available for computation
- Returned for remediation

Example:

```text
Status: REJECTED
Reason: Incorrect issuer relationship
```

---

## State 5 — Archived

Historical graph version retained for audit purposes.

Characteristics:

- Immutable
- Read-only
- Retained for traceability

---

# 5. Reviewer Responsibilities

Reviewers are responsible for validating extracted graph content.

---

## Entity Validation

Reviewers verify:

- Entity names
- Entity types
- Entity attributes
- Classification accuracy

Example:

```text
Holding
    ↓
Corporate Bond
```

Verify that the classification is correct.

---

## Relationship Validation

Reviewers verify:

- Relationship direction
- Relationship semantics
- Relationship completeness

Example:

```text
Holding
    ↓
ISSUED_BY
    ↓
Issuer
```

The relationship must accurately represent the source document.

---

## Provenance Validation

Reviewers verify:

- Source document reference
- Page number
- Chunk identifier
- Extraction confidence

Every extracted node and relationship must have provenance.

---

## Regulatory Validation

Reviewers verify:

- Limits
- Thresholds
- Breach actions
- Regulatory interpretations

against the original guideline document.

---

# 6. Reviewer Actions

Reviewers may perform the following actions.

---

## Approve

The graph content is accepted without modification.

Result:

```text
Draft Graph
        ↓
Approved Graph
```

Audit Event:

```text
GRAPH_APPROVED
```

---

## Reject

The graph content is rejected.

Result:

```text
Draft Graph
        ↓
Rejected Graph
```

Audit Event:

```text
GRAPH_REJECTED
```

---

## Correct

The reviewer modifies graph content before approval.

Examples:

- Correct entity labels
- Correct relationships
- Correct classifications
- Correct provenance metadata

Audit Event:

```text
GRAPH_CORRECTED
```

---

## Publish

An approved graph version becomes active.

Audit Event:

```text
GRAPH_PUBLISHED
```

---

# 7. Validation Checklist

Reviewers should validate the following.

| Check | Description |
|---------|---------|
| Entity Completeness | Required entities exist |
| Relationship Accuracy | Relationships match source material |
| Provenance Completeness | Citation metadata exists |
| Classification Accuracy | Asset classes are correct |
| Limit Accuracy | Thresholds match guidelines |
| Breach Action Accuracy | Escalation rules are correct |
| Version Metadata | Graph version assigned |
| Duplicate Detection | Duplicate nodes removed |

---

# 8. Version Management

Every approved graph receives a unique version identifier.

Example:

```text
graph_v1
graph_v2
graph_v3
```

---

## Version Promotion

```text
Draft Graph
        ↓
Review
        ↓
Approved Graph
        ↓
Published Graph
```

Only published versions may be used by the computation engine.

---

## Version Retention

Historical versions are preserved.

Example:

```text
graph_v1
graph_v2
graph_v3
graph_v4
```

Older versions remain available for:

- Audits
- Reconciliation
- Investigations
- Historical reporting

---

# 9. Computation Guardrail

The computation engine MUST only operate on approved graph versions.

Allowed:

```text
APPROVED
PUBLISHED
```

Not Allowed:

```text
DRAFT
REJECTED
```

---

## Validation Rule

Before computation begins:

```text
IF graph.status != APPROVED
THEN reject computation request
```

---

# 10. Audit Requirements

Every review action generates an immutable audit event.

Examples:

| Event | Description |
|---------|---------|
| GRAPH_REVIEW_REQUESTED | Review initiated |
| GRAPH_CORRECTED | Reviewer modified graph |
| GRAPH_APPROVED | Graph approved |
| GRAPH_REJECTED | Graph rejected |
| GRAPH_PUBLISHED | Graph activated |

---

## Append-Only Rule

Audit events MUST NOT be:

- Updated
- Deleted
- Overwritten

Corrections are recorded as new events.

Example:

```text
GRAPH_APPROVED
        ↓
GRAPH_CORRECTED
        ↓
GRAPH_APPROVED
```

---

# 11. Example Review Scenario

Example:

```text
sample_fund_guidelines.pdf
        ↓
Draft Graph
```

Extracted Relationship:

```text
Holding
    ↓
CLASSIFIED_AS
    ↓
Investment Grade
```

Reviewer discovers:

```text
Holding
    ↓
CLASSIFIED_AS
    ↓
Non-Investment Grade
```

Reviewer action:

```text
GRAPH_CORRECTED
```

Result:

```text
Corrected Graph
        ↓
GRAPH_APPROVED
        ↓
GRAPH_PUBLISHED
```

---

# 12. Summary

The Graph Review Workflow ensures that all graph content is validated before becoming available for compliance computation.

The workflow provides:

- Human governance
- Provenance verification
- Version control
- Computation safeguards
- Full auditability

By enforcing mandatory review and approval, the system guarantees that only trusted graph knowledge contributes to reported compliance figures.