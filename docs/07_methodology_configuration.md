# Methodology Configuration Design

## Status

Draft

---

# 1. Purpose

This document defines the methodology configuration framework used by the compliance reporting platform.

The configuration framework enables multiple firms to use the same computation engine while applying different reporting methodologies.

The primary objective is to support methodology changes through configuration rather than source code modifications.

---

# 2. Objectives

The configuration framework must:

* Support multiple firms
* Support multiple reporting methodologies
* Eliminate methodology-specific code branches
* Enable runtime configuration switching
* Preserve deterministic computation
* Maintain auditability

---

# 3. Design Principles

## 3.1 Configuration Over Code

Methodology differences SHALL be represented in configuration files.

The computation engine SHALL remain unchanged when switching methodologies.

Example:

```text
Firm A
    ↓
firm_a.yaml

Firm B
    ↓
firm_b.yaml
```

The same engine executes both methodologies.

---

## 3.2 Deterministic Behavior

A methodology profile MUST produce identical outputs when executed against identical inputs.

Required inputs:

* Holdings dataset
* Approved graph version
* Methodology profile

---

## 3.3 Versioned Configurations

Every methodology profile MUST be versioned.

Example:

```text
firm_a_v1
firm_a_v2
firm_b_v1
```

Historical versions remain available for:

* Audit investigations
* Reconciliation
* Historical reporting

---

## 3.4 Auditable Selection

Every configuration selection MUST generate an audit event.

Example:

```text
CONFIG_PROFILE_LOADED
```

Captured metadata:

* Profile name
* Profile version
* Configuration hash
* Timestamp

---

# 4. Configuration Architecture

The configuration layer sits between the Knowledge Graph and Computation Engine.

```text
Approved Knowledge Graph
            ↓

Methodology Configuration
            ↓

Deterministic Computation Engine
            ↓

Computed Figures
```

The configuration layer controls computational behavior.

---

# 5. Configuration Structure

Example directory structure:

```text
configs/
├── firm_a.yaml
├── firm_b.yaml
└── shared.yaml
```

---

## Shared Configuration

Contains common definitions:

* Asset class mappings
* Rating mappings
* Standard calculation settings

---

## Firm Configuration

Contains methodology-specific rules.

Examples:

* Exposure limits
* Concentration limits
* Breach thresholds
* Reporting labels

---

# 6. Configuration Categories

The platform supports the following configuration categories.

---

## Regulatory Limits

Defines compliance thresholds.

Example:

```yaml
limits:
  max_non_investment_grade: 20
  max_single_issuer: 10
```

---

## Asset Classification Rules

Defines asset class mappings.

Example:

```yaml
asset_classes:
  investment_grade:
    - AAA
    - AA
    - A
    - BBB

  non_investment_grade:
    - BB
    - B
    - CCC
```

---

## Aggregation Rules

Defines how exposures are aggregated.

Example:

```yaml
aggregation:
  issuer_level: parent_issuer
```

Possible values:

```text
issuer
parent_issuer
```

---

## Compliance Evaluation Rules

Defines pass/fail logic.

Example:

```yaml
evaluation:
  threshold_operator: less_than_or_equal
```

---

## Reporting Rules

Controls report output formatting.

Example:

```yaml
reporting:
  percentage_precision: 2
```

---

# 7. Example Methodology Profiles

---

## Firm A

```yaml
profile:
  name: firm_a
  version: 1.0

limits:
  max_non_investment_grade: 20

aggregation:
  issuer_level: issuer
```

---

## Firm B

```yaml
profile:
  name: firm_b
  version: 1.0

limits:
  max_non_investment_grade: 15

aggregation:
  issuer_level: parent_issuer
```

---

## Outcome

The same holdings data may produce different compliance results.

Example:

```text
Exposure = 18%
```

Firm A:

```text
Limit = 20%
Result = PASS
```

Firm B:

```text
Limit = 15%
Result = BREACH
```

No source code modifications are required.

---

# 8. Configuration Loading

Configuration is loaded at runtime.

Workflow:

```text
Execution Request
        ↓
Load Profile
        ↓
Validate Configuration
        ↓
Execute Computation
```

---

## Example

```python
engine.run(
    graph_version="graph_v5",
    methodology="firm_a"
)
```

Runtime selection:

```text
firm_a.yaml
```

---

# 9. Configuration Validation

Configurations MUST be validated before execution.

Required checks:

* Required sections exist
* Values are valid
* Thresholds are numeric
* Asset mappings are complete
* Version metadata exists

---

## Invalid Example

```yaml
limits:
  max_non_investment_grade: abc
```

Result:

```text
CONFIGURATION_VALIDATION_FAILED
```

---

# 10. Methodology Switching

Methodology switching occurs by changing configuration only.

Example:

```text
Before:
firm_a.yaml

After:
firm_b.yaml
```

The computation engine remains unchanged.

---

## Required Property

The following operation MUST NOT require source code changes:

```text
Firm A
        ↓
Firm B
```

This requirement is one of the core architectural principles of the platform.

---

# 11. Audit Requirements

Every configuration action generates audit events.

Examples:

| Event                    | Description                     |
| ------------------------ | ------------------------------- |
| CONFIG_PROFILE_LOADED    | Configuration selected          |
| CONFIG_VALIDATED         | Configuration passed validation |
| CONFIG_VALIDATION_FAILED | Configuration invalid           |
| CONFIG_VERSION_CHANGED   | Active profile changed          |

All events are written to the append-only audit log.

---

# 12. Security Considerations

Configuration files SHALL be version controlled.

Configuration files SHOULD be immutable after release.

Only authorized users SHOULD be allowed to publish new methodology profiles.

Configuration modifications SHOULD require review and approval.

---

# 13. Governance Rules

Rule 1

Methodology behavior MUST be defined in configuration.

---

Rule 2

Methodology switching MUST NOT require source code modification.

---

Rule 3

Configurations MUST be versioned.

---

Rule 4

Configurations MUST be validated before execution.

---

Rule 5

Configuration selection MUST be auditable.

---

# 14. Summary

The Methodology Configuration Framework enables the platform to support multiple reporting methodologies while preserving deterministic computation.

The framework provides:

* Runtime methodology switching
* Configuration-driven behavior
* Versioned methodology profiles
* Auditability
* Deterministic execution

By externalizing methodology rules into configuration files, the platform can support multiple firms without introducing methodology-specific source code.
