# Changelog

## Unreleased

## v0.2.0 - 2026-08-13

- Added machine-readable feedback metrics for public feedback issues, reproducible reports, confirmed external users, bug feedback, and feature feedback.
- Added a scheduled public evidence health workflow that checks the live demo, release page, business-impact artifact, outcome evidence manifest, adoption metrics, feedback metrics, and PostgreSQL agent route evidence.
- Added a CI-verified business impact artifact that quantifies support-ticket issue categories, affected columns, and recommended actions for resume evidence.
- Added append-only adoption history tracking for stars, forks, watchers, issues, release, commit, and test count.
- Added a public feedback log that tracks external feedback and confirmed users from an honest zero baseline.
- Added a human-readable resume evidence page for verified signals, current public metrics, resume-safe wording, and explicitly not-claimed outcomes.
- Added a public outcome evidence manifest that maps resume claims to URLs for the demo, release, container image, CI tests, verified artifact, report guardrails, and adoption baseline.
- Added a PostgreSQL-backed LLM agent route at `/postgres/support-tickets/agent-report` that reuses the read-only support-ticket adapter and safely falls back when no model key is configured.
- Added CI verification for the outcome evidence manifest so resume claims cannot quietly drift into unsupported user, feedback, or enterprise adoption claims.
- Added deterministic report verification guardrails for evidence support, known column references, sensitive evidence values, unsupported LLM evidence, recommended actions, and score bounds.
- Exposed verification status in API reports, incident Markdown exports, and sanitized run traces.
- Increased the verified test suite from 47 to 52 tests.

## v0.1.0 - 2026-08-13

Initial public release of Data Quality Agent.

### Added

- Public GitHub Pages demo for a reproducible support-ticket data-quality case study.
- CI-verified support-ticket artifact at `docs/verified-support-ticket-result.json`.
- FastAPI endpoints for deterministic reports, uploaded CSV reports, LLM agent reports, run traces, and a read-only PostgreSQL support-ticket demo.
- OpenAI-compatible LLM tool-calling agent with adaptive strategy selection, multi-step replanning tests, and deterministic report attachment.
- Source-cited business-rule retrieval for support-ticket findings.
- Bounded CSV upload path with row, column, and file-size limits.
- Optional read-only PostgreSQL adapter with write-operation rejection, row-limit enforcement, statement timeout, and mocked CI tests.
- Docker Compose demo that seeds a PostgreSQL support-ticket table and exposes the database-backed quality report endpoint.
- Ticket-ready Markdown incident report export for data incident workflows.
- Evaluation harness for three deterministic data-quality scenarios.
- Public feedback issue template for demo users and contributors.
- Public adoption metrics baseline for stars, forks, issues, release, and container evidence.

### Verified

- `47` automated tests passing locally and in GitHub Actions.
- Support-ticket demo verifies `FAIL` status, quality score `24`, row count `8`, four expected check categories, and four source-cited business-rule references.
- Default path runs without paid APIs, secrets, or external model calls.
