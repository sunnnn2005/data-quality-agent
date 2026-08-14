# Agent Capability Matrix

This generated artifact maps Data Quality Agent against a practical LLM-agent checklist. It is intentionally conservative: implemented capabilities are separated from partial, planned, and not-claimed work.

## Summary

| Metric | Value |
| --- | ---: |
| Implemented capabilities | 13 |
| Partial maturity areas | 4 |
| Planned capabilities | 1 |
| Not-claimed areas | 1 |
| Allowed tools | 9 |

## Agent Definition

LLM decision-making + controlled tools + stateful loop + dynamic path + bounded permissions + evidence-backed output.

## Tool Allowlist

- `get_dataset_contract`
- `profile_dataset`
- `select_quality_strategy`
- `retrieve_dataset_memory`
- `inspect_primary_key_integrity`
- `analyze_numeric_distribution`
- `run_quality_checks`
- `retrieve_business_rules`
- `build_quality_report`

## Capability Matrix

| Checklist question | Status | Evidence | Next step |
| --- | --- | --- | --- |
| Does the agent have a bounded task goal? | implemented | LLMDataQualityAgent.run asks the model to investigate one dataset and determine quality status, primary risks, and remediation actions. |  |
| Does the LLM choose the next step instead of following a fixed path? | implemented | The Chat Completions loop exposes tools with tool_choice=auto, and model-selected tool calls determine which toolbox function runs next. |  |
| Are there multiple structured tools with a whitelist? | implemented | 9 allowed tools: get_dataset_contract, profile_dataset, select_quality_strategy, retrieve_dataset_memory, inspect_primary_key_integrity, analyze_numeric_distribution, run_quality_checks, retrieve_business_rules, build_quality_report. |  |
| Are tool results fed back to the LLM? | implemented | Each tool result is appended as a role=tool message before the next model call. |  |
| Can different input shapes trigger different plans? | implemented | select_quality_strategy returned 7 checks for orders_daily: schema_required_columns, missing_values, volume_anomaly, duplicate_primary_key, freshness_sla, negative_amount, numeric_outliers. |  |
| Does the agent preserve task state and evidence? | implemented | AgentRunReport stores status, final_answer, tool_calls, quality_report, evaluation, and trace_id; RunTraceStore persists sanitized run traces when TRACE_DB_PATH is configured. |  |
| Does the loop know when to stop? | implemented | The loop stops when the model returns no tool calls, when build_quality_report attaches a final report, or after six rounds. |  |
| Are tool and database permissions bounded? | implemented | Tool dispatch rejects unknown tools, PostgreSQL is read-only, and 3 unsafe SQL examples are rejected. |  |
| Does the system degrade safely when the model is unavailable? | implemented | Without OPENAI_API_KEY, the agent returns status=DISABLED instead of failing the API. |  |
| Does the model receive summaries instead of full private tables? | implemented | LLM prompt payloads contain dataset metadata, column profiles, redacted samples, and finding evidence rather than raw uploaded files. |  |
| Is the final output structured and machine-verifiable? | implemented | QualityReport and AgentRunReport are Pydantic response models exposed through FastAPI and OpenAPI. |  |
| Are facts, hypotheses, recommendations, and limitations separable? | implemented | QualityReport separates findings, likely_causes, root_cause_hypotheses, recommended_next_steps, verification, and llm_assessment. |  |
| Are final reports checked by deterministic code? | implemented | ReportVerifier checks finding evidence, known columns, sensitive terms, LLM evidence support, recommended actions, and score bounds. |  |
| Can reviewer inspect traces, model metadata, latency, cost, and fallback status? | partial | Run traces, prompt_version, model_call_count, token/cost telemetry, and fallback status exist, but there is no production monitoring dashboard. | Add persisted per-model-call telemetry for real model runs and expose aggregate latency/cost dashboards. |
| Does memory influence future reasoning? | partial | retrieve_dataset_memory gives the LLM prior sanitized traces and recurring incident patterns, but accepted feedback labels do not yet tune ranking. | Use accepted/needs-review hypothesis feedback to adjust root-cause ranking in later runs. |
| Does the agent retrieve external knowledge? | partial | retrieve_business_rules provides source-cited local Markdown business rules, but there is no embedding/vector search layer yet. | Add optional embedding-backed retrieval with permission filtering and source citations. |
| Is there an eval suite proving agent value? | partial | The repo has deterministic scenario evals, fallback tests, and tool-planning coverage, but no large labeled real-world eval set. | Add 20-30 labeled business-data scenarios measuring tool-choice accuracy, false positives, evidence support, latency, and cost. |
| Are risky actions gated by human approval? | planned | The current agent is read-only and recommends actions; it does not execute writes or send tickets. | Add an approval boundary before generated SQL, ticket creation, or notification actions. |
| Is there production usage or external user proof? | not_claimed | The public metrics intentionally show zero confirmed external users and no enterprise production deployment claim. |  |

## Resume-Safe Summary

Published a CI-verified agent capability matrix showing 13 implemented LLM-agent capabilities, 4 partial maturity areas, 9 allowed tools, safe fallback, read-only business-data boundaries, and no inflated production-user claims.

## Not Claimed

- external users
- customer feedback
- enterprise production deployment
- paid model benchmark results
- autonomous write actions
