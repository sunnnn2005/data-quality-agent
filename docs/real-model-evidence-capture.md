# Real Model Evidence Capture

This generated artifact defines and verifies the public-safe capture format for real LLM agent runs. It keeps the current baseline honest until a redacted real run is available.

## Current Status

| Metric | Value |
| --- | ---: |
| Evaluated runs | 0 |
| Accepted real model runs | 0 |
| Rejected real model runs | 0 |
| Runbook evidence fields | 15 |
| Capture required fields | 17 |
| Blocked outcome claims | 4 |

## Required Capture Fields

- `trace_id`
- `provider`
- `model`
- `prompt_version`
- `dataset_id`
- `model_call_count`
- `tool_call_count`
- `distinct_tool_count`
- `used_strategy_tool`
- `used_required_report_tool`
- `final_report_attached`
- `total_tokens`
- `estimated_cost_usd`
- `latency_ms`
- `verification_passed`
- `redaction_status`
- `raw_prompt_logged`

## Claimable Metrics

| Metric | Claimable | Current value | Minimum before claim | Evidence rule |
| --- | --- | ---: | ---: | --- |
| real_model_runs | False | 0 | 1 | At least one accepted real OpenAI-compatible model run is captured. |
| real_model_tool_calling_runs | False | 0 | 1 | The accepted real model run used multiple whitelisted tools. |
| real_model_verified_reports | False | 0 | 1 | The accepted real model run produced a verified report with attached evidence. |
| real_model_cost_tracked_runs | False | 0 | 1 | The accepted real model run recorded token, cost, and latency telemetry. |

## Accepted Runs

- None yet.

## Rejected Runs

- None.

## Blocked Outcome Claims

- `real_model_runs`
- `real_model_tool_calling_runs`
- `real_model_verified_reports`
- `real_model_cost_tracked_runs`

## Resume-Safe Summary

Published a CI-verified real-model evidence capture gate requiring redacted trace, provider, model, prompt version, tool calls, token usage, estimated cost, latency, and report verification before claiming a real LLM agent run.

## Not Claimed

- real OpenAI model run completed
- paid model benchmark results
- real model accuracy improvement
- production model traffic
- raw prompts published
