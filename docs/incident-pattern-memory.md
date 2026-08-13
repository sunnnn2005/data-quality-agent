# Incident Pattern Memory

This generated artifact proves that dataset memory can retrieve recurring incident patterns from sanitized traces. It is a reproducible local case study, not evidence of external production incidents.

| Pattern ID | Title | Recurrence count | Supporting checks | Evidence trace IDs |
| --- | --- | ---: | --- | --- |
| `incident_pattern_1` | Business-rule validation is not separating exceptional transactions from standard facts. | 2 | negative_amount, numeric_outliers | run_33ef7c1d033d405e, run_9e5e331d816444cd |
| `incident_pattern_2` | Source API or transform logic is producing incomplete fields for required analytics columns. | 2 | missing_values | run_33ef7c1d033d405e, run_9e5e331d816444cd |
| `incident_pattern_3` | The ingestion pipeline may be replaying events without idempotent merge logic. | 2 | duplicate_primary_key | run_33ef7c1d033d405e, run_9e5e331d816444cd |

## Summary

Generated dataset memory that retrieved 3 recurring incident patterns from 2 sanitized support-ticket traces.

## Not Claimed

- external production incidents
- enterprise incident database
- customer-validated root causes
