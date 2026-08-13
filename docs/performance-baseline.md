# Performance Baseline

This generated artifact measures local FastAPI `TestClient` endpoint latency for built-in sample data. It is useful as a CI regression baseline and does not claim hosted production performance.

## Summary

| Metric | Value |
| --- | ---: |
| Benchmarks | 2 |
| Passed | 2 |
| Failed | 0 |
| Status | `PASS` |

## Benchmarks

| Check | Method | Path | Iterations | Avg ms | P95 ms | Max P95 ms | Passed |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| quality_report_local_baseline | `POST` | `/datasets/orders_daily/quality-report` | 12 | 1.737 | 1.89 | 80.0 | True |
| profile_local_baseline | `GET` | `/datasets/orders_daily/profile` | 12 | 1.162 | 1.261 | 40.0 | True |

## Resume-Safe Summary

Published a CI-verified local performance baseline for 2 core FastAPI report/profile routes using 24 measured endpoint calls over built-in sample data.

## Not Claimed

- No production latency SLA is claimed.
- No hosted traffic benchmark is claimed.
- No external load test is claimed.
