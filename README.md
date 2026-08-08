# Data Quality Agent

Data Quality Agent is an automated data reliability assistant for analytics and machine learning datasets. It profiles datasets, detects quality problems, scores pipeline health, explains likely root causes, and recommends concrete remediation steps.

## Highlights

- Detects schema drift, missing values, duplicate primary keys, freshness failures, volume anomalies, numeric outliers, and invalid negative values
- Produces structured agent reports with quality score, status, likely causes, recommended next steps, and trace output
- FastAPI backend with interactive docs
- Built-in dashboard for live demos
- Deterministic sample datasets with realistic data quality failures
- Pytest coverage for agent behavior and API contracts
- Dockerfile and GitHub Actions workflow

## Tech Stack

- Python 3.11+
- FastAPI
- Pandas
- NumPy
- Pydantic
- Pytest

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:8000/dashboard`

## Run Tests

```bash
python -m pytest
```

## Docker

```bash
docker build -t data-quality-agent .
docker run --rm -p 8000:8000 data-quality-agent
```

## Example API Calls

```bash
curl http://127.0.0.1:8000/datasets
curl http://127.0.0.1:8000/datasets/orders_daily/profile
curl -X POST http://127.0.0.1:8000/datasets/orders_daily/quality-report
```

## Project Structure

```text
app/
  agent.py       Report scoring, likely-cause analysis, and recommendations
  checks.py      Data quality checks
  data.py        Deterministic sample datasets and metadata
  dashboard.py   Built-in demo UI
  main.py        FastAPI routes
  models.py      API and report models
  profiler.py    Dataset profiling logic
docs/
  architecture.md
  spec.md
tests/
  test_agent.py
  test_api.py
```

## Resume Summary

Built an agentic data quality monitoring platform that profiles datasets, detects schema drift, missingness, duplicates, freshness failures, volume anomalies, and outliers, then generates scored reports with likely root causes and remediation steps through a FastAPI API and interactive dashboard.
