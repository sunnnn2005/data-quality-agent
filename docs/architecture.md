# Architecture

Data Quality Agent is a local-first data reliability agent. It profiles datasets, runs deterministic quality checks, converts failures into typed findings, and returns a structured report with likely causes and next steps.

The default implementation uses in-memory sample datasets. That keeps the system inspectable, reproducible, and safe to run without credentials or private data. An optional OpenAI-compatible advisor can be enabled with `OPENAI_API_KEY` to generate a structured risk assessment from redacted evidence.

## Runtime Loop

```text
DatasetSummary + DataFrame
  -> DatasetProfiler
  -> QualityCheckRunner
  -> QualityFinding[]
  -> score/status
  -> likely causes
  -> optional LLMDataQualityAdvisor
  -> QualityReport
```

The agent is deliberately not implemented as a single free-form prompt. Each step has an explicit typed boundary so behavior can be tested and extended.

## Components

### API Layer

`app/main.py` exposes the FastAPI surface:

- health checks
- dataset catalog
- dataset metadata lookup
- column profiling
- quality report generation
- dashboard rendering

The API returns Pydantic models rather than ad hoc dictionaries.

### Model Layer

`app/models.py` defines the contracts used across the runtime:

- `DatasetSummary`
- `ColumnProfile`
- `DatasetProfile`
- `QualityFinding`
- `LLMAssessment`
- `QualityReport`

These models are the public shape of the system.

### Data Layer

`app/data.py` contains deterministic sample datasets and dataset metadata. The sample datasets intentionally include quality failures so tests can assert specific behavior.

### Profiling Layer

`app/profiler.py` creates column-level profiles:

- dtype
- missing count
- missing rate
- uniqueness
- sample values

### Check Layer

`app/checks.py` runs deterministic quality checks:

- schema drift
- missing values
- duplicate primary keys
- freshness SLA
- numeric outliers
- invalid negative values
- volume anomalies

### Agent Layer

`app/agent.py` coordinates profiling, check execution, scoring, likely-cause generation, and next-step recommendation.

### LLM Advisor Layer

`app/llm.py` is an optional model-integration boundary. It demonstrates:

- OpenAI-compatible Chat Completions API usage
- prompt design for strict JSON output
- sensitive-field redaction before model calls
- timeout, retry, and invalid-output handling
- cost estimation from token usage
- lightweight model-output evaluation against the deterministic findings

The model does not replace the rule engine. It can only summarize and prioritize evidence already produced by typed checks.

### Dashboard Layer

`app/dashboard.py` provides a zero-build demo UI. It is intentionally simple so the backend remains the source of truth.

## Extension Points

Good extension points:

- add deterministic datasets in `app/data.py`
- add isolated checks in `app/checks.py`
- add scoring rules in `app/agent.py`
- add report export helpers
- add API tests for new behavior

Avoid mixing these layers in one large change. A good PR should usually update one dataset, one check, one report behavior, or one dashboard interaction.

## Operational Boundaries

Data Quality Agent does not:

- connect to a warehouse by default
- upload data
- call external model providers unless `OPENAI_API_KEY` is explicitly configured
- require paid APIs
- require secrets

Any future integration with warehouse or file upload workflows should preserve read-only defaults and include tests for failure behavior.

## Test Strategy

The tests verify both the agent loop and the API contract:

- known datasets produce expected findings
- score/status reflects severity-weighted findings
- unknown datasets return 404
- profiles include column-level summaries
- the dashboard renders
- the API returns typed reports
- the optional LLM advisor can be skipped safely
- structured LLM assessments can be attached to reports

The project should remain runnable with:

```bash
python -m pytest
```
