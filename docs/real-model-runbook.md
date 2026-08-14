# Real Model Runbook

This generated artifact defines the evidence gate for a future real OpenAI-compatible tool-calling run. It does not claim that a paid model run has already been completed.

## Purpose

Define the exact evidence gate for converting the existing mocked tool-calling telemetry into a public, resume-safe real OpenAI-compatible model run once provider credentials are explicitly supplied.

## Current Status

| Metric | Value |
| --- | ---: |
| Current real model runs | 0 |
| Current mocked model calls | 2 |
| Current mocked tokens | 360 |
| Prompt version | `tool-agent-v3` |
| Implemented agent capabilities | 13 |
| Allowed agent tools | 9 |

## Agent Routes

- `/business-data/agent-report`
- `/datasets/{dataset_id}/agent-report`
- `/postgres/support-tickets/agent-report`

## Run Commands

### start_api

Start the FastAPI app with an explicit OpenAI-compatible model key.

```bash
OPENAI_API_KEY=$OPENAI_API_KEY uvicorn app.main:app --reload
```

### run_builtin_agent

Execute the tool-calling agent on a deterministic dataset.

```bash
curl -X POST http://127.0.0.1:8000/datasets/orders_daily/agent-report
```

### run_business_csv_agent

Execute the tool-calling agent on anonymized business-shaped CSV data.

```bash
curl -X POST http://127.0.0.1:8000/business-data/agent-report -F file=@sample.csv -F dataset_name='Replay Dataset' -F owner='reviewer' -F primary_key='id'
```

### inspect_trace

Inspect sanitized trace, tool calls, final report attachment, and telemetry summary.

```bash
curl http://127.0.0.1:8000/runs/<trace_id>
```

### capture_real_model_evidence

Capture a redacted real-model run artifact from the local API and verify it against the evidence gate.

```bash
python scripts/capture_real_model_run.py --dataset-id orders_daily --write
```

## Evidence Fields

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

## Acceptance Criteria

- Agent status is not DISABLED.
- At least two model calls are recorded.
- At least three tool calls are recorded.
- The strategy tool and final report tool are both used.
- A deterministic QualityReport is attached.
- Report verification passes or lists explicit issues.
- Token count, estimated cost, latency, prompt version, provider, and model are recorded.
- No raw prompt, uploaded rows, credentials, customer identifiers, or secrets are published.

## Safety Gates

- Do not commit OPENAI_API_KEY or provider credentials.
- Do not publish raw request prompts or raw uploaded business rows.
- Use anonymized or synthetic-but-business-shaped CSV data for public artifacts.
- Store only telemetry summaries and redacted report evidence.
- Keep deterministic report verification as the source of truth.

## Resume Upgrade Rules

| Metric | Current value | Minimum before claim | Claim when met |
| --- | ---: | ---: | --- |
| real_model_runs | 0 | 1 | executed a real OpenAI-compatible tool-calling run with public redacted telemetry |
| real_model_tool_calls | 0 | 3 | real model selected multiple tools before finalizing a verified report |

## Resume-Safe Summary

Published a CI-verified real-model runbook with 5 run commands, 15 evidence fields, 8 acceptance criteria, and 5 safety gates without claiming a paid model run yet.

## Not Claimed

- real OpenAI model run completed
- paid model benchmark results
- real model accuracy improvement
- production model traffic
- raw prompts published
