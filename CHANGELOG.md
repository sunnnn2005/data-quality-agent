# Changelog

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
- Evaluation harness for three deterministic data-quality scenarios.
- Public feedback issue template for demo users and contributors.

### Verified

- `39` automated tests passing locally and in GitHub Actions.
- Support-ticket demo verifies `FAIL` status, quality score `24`, row count `8`, four expected check categories, and four source-cited business-rule references.
- Default path runs without paid APIs, secrets, or external model calls.
