# Data Quality Agent Architecture

Data Quality Agent is a small data reliability platform that profiles analytics datasets, runs quality checks, explains likely root causes, and recommends remediation steps.

## Components

- **FastAPI service** exposes dataset catalog, profiling, quality report, health, and dashboard routes.
- **Profiler** summarizes row count, column count, dtypes, missingness, uniqueness, and sample values.
- **Quality check runner** detects schema drift, missing values, duplicate primary keys, freshness SLA misses, numeric outliers, negative business values, and volume anomalies.
- **Agent layer** converts check results into a scored quality report with likely causes, next steps, and an agent trace.
- **Dashboard** provides a runnable UI for recruiters and interviewers without a separate frontend build step.

## Agent Flow

1. Load dataset metadata and sample records.
2. Profile all columns.
3. Run contract, completeness, uniqueness, freshness, volume, and domain checks.
4. Score the dataset according to severity-weighted findings.
5. Infer likely causes from check signatures.
6. Rank recommendations and return a structured quality report.

## Why It Is Resume-Ready

The project demonstrates practical data engineering skills, API design, pandas-based analysis, production-minded data quality checks, and agentic explanation. It is deterministic and free to run locally, which makes it easy to demo during internship interviews.
