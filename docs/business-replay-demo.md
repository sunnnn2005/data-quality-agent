# Business Replay Demo

This generated artifact proves the business-data path can replay an anonymized support-ticket CSV and produce a verified deterministic report. It does not claim real company data, external users, or customer feedback.

## Dataset

| Field | Value |
| --- | --- |
| Path | `examples/support_tickets.csv` |
| Rows | 8 |
| Columns | 6 |
| Primary key | `ticket_id` |
| Contains real company data | `False` |
| Contains PII | `False` |

## Replay Command

```bash
curl -X POST http://127.0.0.1:8000/business-data/quality-report -F file=@examples/support_tickets.csv -F dataset_name='Support Tickets Replay' -F owner='support-ops' -F primary_key='ticket_id' -F expected_columns='ticket_id,team,priority,status,amount,created_at'
```

## Verified Report Summary

| Metric | Value |
| --- | ---: |
| Status | `FAIL` |
| Quality score | 24 |
| Findings | 5 |
| Failed check types | 4 |
| Business-rule references | 4 |
| Root-cause hypotheses | 3 |
| Recommended actions | 5 |
| Verification passed | `True` |

## Checks

- `duplicate_primary_key`
- `missing_values`
- `negative_amount`
- `numeric_outliers`

## Root-Cause Hypotheses

- Business-rule validation is not separating exceptional transactions from standard facts. (`confidence=0.71`, checks=negative_amount, numeric_outliers)
- The ingestion pipeline may be replaying events without idempotent merge logic. (`confidence=0.65`, checks=duplicate_primary_key)
- Source API or transform logic is producing incomplete fields for required analytics columns. (`confidence=0.63`, checks=missing_values)

## Resume-Safe Summary

Published a reproducible business-shaped CSV replay demo that verifies 8 rows, 5 findings, 4 failed check types, 4 business-rule references, 3 root-cause hypotheses, and deterministic report verification.

## Not Claimed

- real company data
- external user replay
- customer feedback
- production incident resolved
