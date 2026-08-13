# Changelog

## Unreleased

- Added a public feedback log that tracks external feedback and confirmed users from an honest zero baseline.
- Added a human-readable resume evidence page for verified signals, current public metrics, resume-safe wording, and explicitly not-claimed outcomes.
- Added a public outcome evidence manifest that maps resume claims to URLs for the demo, release, container image, CI tests, verified artifact, report guardrails, and adoption baseline.
- Added CI verification for the outcome evidence manifest so resume claims cannot quietly drift into unsupported user, feedback, or enterprise adoption claims.
- Added deterministic report verification guardrails for evidence support, known column references, sensitive evidence values, unsupported LLM evidence, recommended actions, and score bounds.
- Exposed verification status in API reports, incident Markdown exports, and sanitized run traces.
- Increased the verified test suite from 42 to 46 tests.

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

- `46` automated tests passing locally and in GitHub Actions.
- Support-ticket demo verifies `FAIL` status, quality score `24`, row count `8`, four expected check categories, and four source-cited business-rule references.
- Default path runs without paid APIs, secrets, or external model calls.
