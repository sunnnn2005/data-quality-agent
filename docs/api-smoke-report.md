# API Smoke Report

This generated artifact verifies core FastAPI routes with `TestClient`. It proves local endpoint behavior without claiming production traffic.

## Summary

| Metric | Value |
| --- | ---: |
| Checks | 6 |
| Passed | 6 |
| Failed | 0 |
| Status | `PASS` |

## Route Checks

| Check | Method | Path | Status | Passed |
| --- | --- | --- | ---: | --- |
| health | `GET` | `/health` | 200 | True |
| dataset_catalog | `GET` | `/datasets` | 200 | True |
| profile | `GET` | `/datasets/orders_daily/profile` | 200 | True |
| quality_report | `POST` | `/datasets/orders_daily/quality-report` | 200 | True |
| agent_report_disabled_fallback | `POST` | `/datasets/orders_daily/agent-report` | 200 | True |
| incident_markdown | `POST` | `/datasets/orders_daily/incident-report.md` | 200 | True |

## Resume-Safe Summary

Published a CI-verified API smoke report covering 6 FastAPI routes for health, catalog, profiling, deterministic report, disabled agent fallback, and incident Markdown export.

## Not Claimed

- No production uptime SLA is claimed.
- No external traffic volume is claimed.
- No hosted API usage is claimed.
