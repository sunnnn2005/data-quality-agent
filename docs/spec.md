# Specification

Data Quality Agent is a data reliability agent for local experimentation with dataset validation workflows. The core checks are deterministic, and an optional OpenAI-compatible tool-calling agent can inspect datasets with explicit tools before returning a structured answer.

## Purpose

The system turns dataset records and metadata into a structured quality report. It is designed for inspection rather than automation theater: checks are explicit, findings are typed, and scoring can be tested.

## Non-Goals

- No production warehouse connection in the default path.
- No upload of private data.
- No required LLM provider.
- No required external storage.
- No hidden network calls in the default path.

## Functional Requirements

- List available datasets.
- Return dataset metadata by id.
- Generate a column-level profile for a known dataset.
- Generate a quality report for a known dataset.
- Include score, status, findings, likely causes, recommendations, timestamp, and trace.
- Include an `llm_assessment` object that is disabled by default and populated when an OpenAI-compatible provider is configured.
- Generate an optional `agent-report` where the LLM chooses data-quality tools and attaches the deterministic source-of-truth report.
- Return a clear 404 for unknown datasets.
- Render a browser dashboard with the same backend data.

## Runtime Contracts

### DatasetSummary

A dataset summary describes ownership, primary key, expected columns, freshness metadata, and purpose.

### DatasetProfile

A dataset profile summarizes row count, column count, dtypes, missingness, uniqueness, and samples.

### QualityFinding

A finding is one failed or suspicious check. It includes severity, evidence, and a recommended remediation.

### QualityReport

The report is the final output. It should be useful both as JSON and as a source for future markdown/text exports.

### LLMAssessment

The optional LLM assessment includes model/provider metadata, summary, risk level, evidence used, suggested actions, estimated cost, evaluation metadata, and error state. It must remain structured and testable.

### AgentRunReport

The optional agent report includes model-selected tool calls, result previews, final answer, deterministic report attachment, evaluation metadata, and disabled/error states.

## Check Contracts

Current checks are deterministic local functions:

- required columns
- schema drift
- missing values
- duplicate primary keys
- freshness SLA
- numeric outliers
- negative business values
- volume baseline

Future checks should follow the same pattern:

- explicit inputs
- typed findings
- deterministic evidence
- no hidden mutation
- tested edge cases

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
python -m pytest
```

Docker:

```bash
docker build -t data-quality-agent .
docker run --rm -p 8000:8000 data-quality-agent
```

## Quality Bar

- Tests must pass locally and in CI.
- New datasets should be deterministic.
- New report fields should be represented as typed Pydantic models.
- New integrations should not require secrets in the default path.
- Documentation should describe behavior without overstating production readiness.
- LLM features must preserve deterministic fallback behavior and avoid sending sensitive fields.
- Tool-calling features must expose small explicit tools rather than unrestricted code execution.
