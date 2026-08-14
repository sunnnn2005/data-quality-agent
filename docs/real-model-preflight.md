# Real Model Preflight

This generated artifact checks whether the project can safely run a real OpenAI-compatible LLM tool-calling pass. It never executes a paid model call and never prints provider credentials.

## Current Status

| Metric | Value |
| --- | ---: |
| Execution status | `not_ready` |
| Real model run executed by preflight | False |
| Ready checks | 3 |
| Total checks | 5 |
| Blocked checks | 2 |

## Checks

| Check | Ready | Evidence |
| --- | --- | --- |
| `openai_api_key_configured` | False | `"OPENAI_API_KEY is not configured in the environment."` |
| `local_api_health` | False | `{"error_type": "URLError", "name": "local_api_health", "ready": false, "status": "unavailable", "url": "http://127.0.0.1:8000/health"}` |
| `business_csv_sample_available` | True | `"examples/support_tickets.csv"` |
| `business_agent_route_documented` | True | `["/business-data/agent-report", "/datasets/{dataset_id}/agent-report", "/postgres/support-tickets/agent-report"]` |
| `redacted_capture_gate_ready` | True | `{"capture_required_field_count": 17, "requires_raw_prompt_logged_false": true}` |

## Blocked Checks

- `openai_api_key_configured`
- `local_api_health`

## Next Capture Command

```bash
Start the API with OPENAI_API_KEY, then rerun this preflight.
```

## Resume-Safe Summary

Published a real-model preflight gate that checks API readiness, provider-key presence, business CSV sample availability, documented agent routes, and redacted telemetry requirements before any real LLM run is claimed.

## Not Claimed

- real model run completed by this preflight
- provider credential value
- raw prompt contents
- raw business rows
- production model traffic
