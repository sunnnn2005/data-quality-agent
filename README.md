# Data Quality Agent

[![test](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml/badge.svg)](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Data Quality Agent is a local-first data reliability agent. It profiles a dataset, runs contract and quality checks, assigns severity, and returns a structured report with likely causes and recommended next steps.

The project is designed to keep the data-quality loop visible. There is no hidden external model call in the default path. The agent produces typed findings, a quality score, and an explicit trace of the checks it ran.

![Data Quality Agent dashboard](docs/assets/data-quality-dashboard.png)

## The Model

Data Quality Agent is built around five objects:

- **DatasetSummary**: owner, primary key, expected columns, freshness metadata, and description.
- **DatasetProfile**: row count, column count, dtypes, missingness, uniqueness, and sample values.
- **QualityFinding**: one failing check with severity, evidence, and remediation.
- **QualityReport**: score, status, findings, likely causes, next steps, and trace.
- **CheckRunner**: the deterministic tool that applies quality checks.

The point is not to generate a vague "data looks bad" paragraph. The report is structured enough to test, diff, export, or attach to a data incident ticket.

## How It Works

1. Load dataset metadata and records.
2. Build a column-level profile.
3. Run schema, freshness, completeness, uniqueness, volume, domain, and outlier checks.
4. Convert failed checks into typed findings.
5. Apply severity-weighted scoring.
6. Infer likely causes from the pattern of failures.
7. Return a report with remediation steps and an agent trace.

The sample datasets are intentionally small and deterministic. They are not mock data for its own sake; they make the agent behavior reproducible and testable.

## Why This Exists

Data quality systems often show a failing check but leave the operator to reconstruct the story. This project explores a compact agent loop for data reliability:

```text
dataset -> profile -> checks -> findings -> likely causes -> action plan
```

It is closer to a small internal data platform tool than a notebook. The backend exposes API contracts, the dashboard shows the report, and tests verify the agent's decisions.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000/dashboard`
- API docs: `http://127.0.0.1:8000/docs`

Run a report:

```bash
curl -X POST http://127.0.0.1:8000/datasets/orders_daily/quality-report
```

## API Surface

```text
GET  /health
GET  /datasets
GET  /datasets/{dataset_id}
GET  /datasets/{dataset_id}/profile
POST /datasets/{dataset_id}/quality-report
GET  /dashboard
```

## Checks

The default runner includes:

- Required-column checks
- Unexpected-column/schema drift checks
- Missing-value checks
- Duplicate primary-key checks
- Freshness SLA checks
- Numeric outlier checks
- Negative business-value checks
- Volume baseline checks

Each check returns evidence instead of only a boolean. That makes the output easier to inspect and the tests more meaningful.

## Development

```bash
python -m pytest
```

Docker:

```bash
docker build -t data-quality-agent .
docker run --rm -p 8000:8000 data-quality-agent
```

## Contributing

Contributions are welcome. Good starter tasks are labeled [`good first issue`](https://github.com/sunnnn2005/data-quality-agent/labels/good%20first%20issue), and broader tasks are labeled [`help wanted`](https://github.com/sunnnn2005/data-quality-agent/labels/help%20wanted).

Useful first contributions:

- Add one deterministic dataset scenario
- Add one quality check
- Add one test for an edge case
- Improve dashboard accessibility
- Improve documentation or examples

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md) before opening a pull request.

## Repository Layout

```text
app/
  agent.py       Report scoring and likely-cause analysis
  checks.py      Deterministic data-quality checks
  data.py        Local datasets and contracts
  dashboard.py   Demo UI
  main.py        FastAPI routes
  models.py      Typed report contracts
  profiler.py    Column-level profiling
docs/
  architecture.md
  spec.md
tests/
  test_agent.py
  test_api.py
```

## Safety and Scope

Data Quality Agent runs on local deterministic datasets. It does not connect to a warehouse, upload data, or call external model providers. Future warehouse or CSV integrations should be explicit adapters with read-only defaults and tests.

## Roadmap

See [ROADMAP.md](ROADMAP.md) and the open issues for planned work.

## License

MIT
