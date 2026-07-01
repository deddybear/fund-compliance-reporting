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

---

# Workflow

```
                     Fund Guideline PDF
                            │
                            ▼
                  Knowledge Graph (Neo4j)
                            ▲
                            │
        Cypher Schema Initialization Scripts
                            │
                            ▼
                    Portfolio Holdings CSV
                            │
                            ▼
              Deterministic Computation Engine
                            │
                            ▼
         Traceability + Reconciliation Engine
                            │
                            ▼
              PDF Compliance Report Generation
```

---

# Configure Environment

Copy the example environment file.

```bash
cp .env.example .env
```

Edit the `.env` file and configure the required environment variables.

Example:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

OPENAI_API_KEY=your_openai_api_key
OPENAI_API_MODEL=gpt-5.4-mini
```

| Variable | Description |
|----------|-------------|
| `NEO4J_URI` | URI of the Neo4j database. |
| `NEO4J_USERNAME` | Neo4j username. |
| `NEO4J_PASSWORD` | Neo4j password. |
| `OPENAI_API_KEY` | OpenAI API key used for narrative generation. |
| `OPENAI_API_MODEL` | OpenAI model used by the application. |

> **Note**
>
> The compliance methodology is **not** configured through environment variables. It is selected using the `--profile` command-line argument when starting the application.

---

# Start the Application

## 1. Start Neo4j

Start the Neo4j container.

```bash
docker compose up -d
```

## 2. Install Dependencies

```bash
uv sync
```

---

## 3. Run the Application

Run the application by specifying the compliance profile.

### Firm A

```bash
uv run python main.py --profile firm_a
```

### Firm B

```bash
uv run python main.py --profile firm_b
```

The `--profile` argument determines which compliance methodology is loaded from the `configs/` directory.

For example:

```bash
uv run python main.py --profile firm_a
```

loads:

```
configs/firm_a.yaml
```

while:

```bash
uv run python main.py --profile firm_b
```

loads:

```
configs/firm_b.yaml
```

To add a new compliance methodology, create a new configuration file (for example, `firm_c.yaml`) under the `configs/` directory and run:

```bash
uv run python main.py --profile firm_c
```