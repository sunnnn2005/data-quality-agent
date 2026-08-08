# Spec: Data Quality Agent

## Objective
Build a data quality monitoring agent that simulates a large-company analytics or data platform internship project. The system profiles datasets, detects quality failures, explains likely causes, and recommends remediation actions in a structured report.

Target users are data analysts, data scientists, data engineers, and ML platform interviewers reviewing whether this project demonstrates data quality, validation, analytics, and agentic reasoning.

## Tech Stack
- Python 3.12
- FastAPI
- Pydantic
- pandas and NumPy
- pytest
- In-memory deterministic sample datasets and baseline schemas
- Optional future warehouse connector boundary, but default behavior must run without external services

## Commands
- Create venv: `python3.12 -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r requirements.txt -r requirements-dev.txt`
- Run API: `uvicorn app.main:app --reload`
- Test: `python -m pytest`
- Docker: `docker build -t data-quality-agent . && docker run -p 8002:8000 data-quality-agent`

## Project Structure
- `app/main.py`: FastAPI entrypoint and routes
- `app/models.py`: dataset and report schemas
- `app/data.py`: sample datasets, baselines, and freshness metadata
- `app/checks.py`: profiling, missingness, duplicates, schema drift, outliers, freshness checks
- `app/agent.py`: report generation and remediation reasoning
- `app/dashboard.py`: static data platform dashboard
- `tests/`: unit and API tests
- `docs/`: architecture and usage documentation

## Code Style
Keep checks pure and composable:

```python
def run_quality_checks(dataset: DatasetSnapshot, baseline: DatasetBaseline) -> list[QualityFinding]:
    frame = pd.DataFrame(dataset.rows)
    return [
        *check_schema(frame, baseline),
        *check_missing_values(frame),
        *check_duplicates(frame, baseline.primary_key),
    ]
```

## Testing Strategy
- Unit tests for schema drift, missing values, duplicates, outliers, freshness, and scoring.
- API tests for dataset listing, profiling, quality report generation, and dashboard rendering.
- Tests must run without network, secrets, Docker, or external databases.

## Boundaries
- Always: use deterministic sample datasets, make findings explainable, validate incoming records.
- Ask first: adding paid data warehouse connectors, external storage, or authentication.
- Never: commit private data, require paid APIs, claim production warehouse integration unless implemented.

## Success Criteria
- A user can run the API locally and open `/dashboard`.
- At least three datasets produce meaningful and distinct data quality reports.
- Reports include score, severity, findings, evidence, likely causes, and remediation steps.
- Tests pass in CI and locally.
- README clearly explains large-company internship relevance and resume bullets.
