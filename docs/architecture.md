# Architecture

Data Quality Agent is a local-first data reliability agent. It profiles datasets, runs deterministic quality checks, converts failures into typed findings, and returns a structured report with likely causes and next steps.

The default implementation uses in-memory sample datasets. That keeps the system inspectable, reproducible, and safe to run without credentials or private data. The business-data upload path accepts bounded CSV exports with explicit owner, primary-key, and expected-column context. An optional OpenAI-compatible tool-calling agent can be enabled with `OPENAI_API_KEY` to inspect dataset evidence through explicit tools.

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

Optional LLM tool loop:

User request
  -> LLMDataQualityAgent
  -> tool choice: get_dataset_contract | select_quality_strategy | profile_dataset | run_quality_checks | build_quality_report
  -> tool results
  -> re-plan from observed results
  -> final answer + AgentRunReport
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
- `AgentToolCall`
- `AgentRunReport`
- `QualityReport`

These models are the public shape of the system.

### Data Layer

`app/data.py` contains deterministic sample datasets and dataset metadata. The sample datasets intentionally include quality failures so tests can assert specific behavior.

`app/business_data.py` adapts real CSV exports into the same `DatasetSummary + DataFrame` contract. It validates file type, file size, row count, column count, and primary-key presence before analysis.

`app/business_rules.py` retrieves source-cited business rules from `docs/business-rules/`. The default implementation uses deterministic keyword and check-name matching so CI can run without paid embedding APIs. Future vector search can replace the retrieval implementation while keeping the `BusinessRuleReference` report contract stable.

`app/postgres_adapter.py` provides an optional read-only PostgreSQL adapter for real business tables. It is disabled by default, requires explicit environment configuration, rejects write operations, requires bounded `SELECT` queries, caps row limits, sets a statement timeout, and reuses the same `DatasetSummary + DataFrame` contract used by built-in and CSV datasets.

`docker-compose.yml` and `examples/postgres/init.sql` provide a reproducible local PostgreSQL demo. The compose stack creates a read-only database user, seeds a support-ticket table with realistic quality failures, and exposes `/postgres/support-tickets/quality-report` as an end-to-end database-backed report path.

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

### Tool-Calling Agent Layer

`app/tool_agent.py` implements a true LLM agent loop. It exposes a small toolbox:

- `get_dataset_contract`
- `select_quality_strategy`
- `profile_dataset`
- `run_quality_checks`
- `build_quality_report`

The model decides which tools to call, receives JSON tool results, and must call `build_quality_report` before finalizing. `select_quality_strategy` gives the model a compact planning tool so payment, customer/profile, and generic datasets can trigger different recommended checks. The response includes an `AgentRunReport` with every tool call, result preview, final answer, attached deterministic report, and evaluation flags such as whether the strategy and required report tools were used.

### Verification Layer

`app/verifier.py` adds deterministic guardrails after report generation. It validates that findings are evidence-backed, referenced columns exist, sensitive terms are not exposed in evidence, LLM evidence references map back to actual findings, recommended actions are present, and the quality score stays within contract bounds. Verification results are included in `QualityReport`, incident Markdown exports, and sanitized run traces so reviewers can audit whether a report is safe to share.

### Dashboard Layer

`app/dashboard.py` provides a zero-build demo UI. It is intentionally simple so the backend remains the source of truth.

### Incident Export Layer

`app/incident_export.py` converts structured `QualityReport` objects into ticket-ready Markdown. It separates facts, tool evidence, likely causes, recommended actions, business-rule references, and limitations so reports can move into incident-management workflows without losing the deterministic evidence trail.

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
- persist uploaded CSV files
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
- business-rule retrieval returns source-cited constraints without raw row data
- PostgreSQL adapter rejects write operations and unbounded queries
- PostgreSQL support-ticket endpoint analyzes a read-only adapter-backed table
- incident Markdown export separates facts, evidence, actions, and limitations
- structured LLM assessments can be attached to reports
- the tool-calling agent can be skipped safely without a key
- the tool-calling agent can re-plan across multiple model calls after observing tool results
- dataset shape changes the recommended quality strategy
- mocked tool-call loops attach a deterministic report before final answer
- uploaded CSV business data can be analyzed through deterministic and agent endpoints

The project should remain runnable with:

```bash
python -m pytest
```
