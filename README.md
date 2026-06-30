# Fund Compliance Engine

A deterministic Fund Compliance Engine that validates portfolio holdings against configurable investment guidelines.

The engine computes portfolio metrics, evaluates compliance limits, generates reconciliation results, provides traceability through a Neo4j knowledge graph, and produces a PDF compliance report.


# Project Structure

```
FUND-COMPLIANCE-REPORTING
│
├── app/
│   Core application source code implementing the complete compliance pipeline.
│
│   ├── audit/
│   │   Audit event generation and logging.
│   │
│   ├── computation/
│   │   Deterministic computation engine for portfolio figures and compliance evaluation.
│   │
│   ├── configuration/
│   │   Configuration loader and profile management.
│   │
│   ├── graph/
│   │   Knowledge Graph services, repositories, renderers, and visualization utilities.
│   │
│   ├── holdings/
│   │   CSV ingestion and portfolio holding models.
│   │
│   ├── narrative/
│   │   PDF report generation and report builders.
│   │
│   ├── reconciliation/
│   │   Validation of computed figures against expected results.
│   │
│   ├── traceability/
│   │   Traceability service connecting computed figures to graph evidence.
│   │
│   ├── bootstrap.py
│   │   Dependency initialization.
│   │
│   └── pipeline.py
│       Main application workflow.
│
├── configs/
│   Compliance methodology profiles.
│
├── data/
│   Runtime input datasets used by the application.
│
├── docs/
│   Project documentation including architecture, methodology, workflow, and design decisions.
│
├── sample_docs/
│   Sample documents used for demonstration and testing.
│
├── schema/
│   Database schema and Neo4j Knowledge Graph initialization scripts.
│
│   ├── db/
│   │   Relational database schema.
│   │
│   └── graphs/
│       Cypher scripts for creating the Knowledge Graph.
│
├── storage/
│   Runtime generated artifacts.
│
│   ├── db/
│   │   Local database storage.
│   │
│   ├── graphs/
│   │   Generated graph visualizations.
│   │
│   └── reports/
│       Generated compliance reports.
│
├── Dockerfile
│   Docker image definition.
│
├── docker-compose.yml
│   Multi-container application configuration.
│
├── main.py
│   Application entry point.
│
├── pyproject.toml
│   Python project configuration and dependencies.
│
└── README.md
    Project documentation.
```

### PROFILE

The `PROFILE` environment variable specifies which compliance methodology the engine will use during execution.

Each profile corresponds to a YAML configuration file located in the `configs/` directory. These configuration files define the complete compliance methodology, including:

- Asset classification rules
- Compliance limits and thresholds
- Aggregation methods
- Evaluation logic
- Reporting options
- Traceability requirements
- Reconciliation settings

For example:

```env
PROFILE=firm_a
```

will load:

```
configs/firm_a.yaml
```

Similarly,

```env
PROFILE=firm_b
```

will load:

```
configs/firm_b.yaml
```

To use a different methodology, simply create a new configuration file (for example, `firm_c.yaml`) under the `configs/` directory and update the `PROFILE` environment variable accordingly.

```env
PROFILE=firm_c
```

No source code changes are required when switching between supported compliance methodologies.

# Using Docker

## Prerequisites

Before running the application, ensure the following software is installed:

- Docker 24+
- Docker Compose v2+

---

## 1. Configure Environment Variables

Copy the example environment file.

```bash
cp .env.example .env
```

Edit the `.env` file if necessary.

Example:

```env
PROFILE=firm_a
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
OPENAI_API_KEY=your_key_api
OPENAI_API_MODEL=gpt-5.4-mini

```

---

## 2. Start the Application

```bash
docker compose up
```

or run in detached mode

```bash
docker compose up -d
```

---

## 4. Input Files

The application expects the following input files:

```
configs/
    firm_a.yaml
    firm_b.yaml

data/
    sample_holdings.csv
```

The compliance profile is selected using the `PROFILE` environment variable.

Example:

```env
PROFILE=firm_a
```

or

```env
PROFILE=firm_b
```

---

## 5. Generated Output

After execution, generated artifacts can be found under:

```
storage/

├── reports/
│   Generated compliance PDF reports
│
├── graphs/
│   Knowledge graph visualizations
│
└── db/
    Local database artifacts (if applicable)
```

---

## 6. Stop the Application

```bash
docker compose down
```

To also remove volumes:

```bash
docker compose down -v
```