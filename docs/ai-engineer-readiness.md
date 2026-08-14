# AI Engineer Readiness

This generated artifact explains why the project is relevant for AI Engineer Intern applications while keeping outcome claims honest.

## Summary

This project demonstrates AI Engineer intern readiness through API integration, tool calling, structured output, guardrails, observability, evaluation, and real business-data connectors; it does not yet claim production users or accepted real-model benchmark runs.

## Resume Bullet

Built an OpenAI-compatible data-quality LLM agent for CSV and read-only PostgreSQL business data, with 9 controlled tools, dynamic tool selection, structured reports, trace/cost telemetry, deterministic guardrails, safe fallback, and CI-verified evidence artifacts.

## Skill Signals

| Signal | Status | Evidence |
| --- | --- | --- |
| OpenAI-compatible chat-completions integration | `implemented` | app/llm.py supports OPENAI_API_KEY, OPENAI_BASE_URL, model selection, retries, timeouts, JSON response parsing, and cost estimation. |
| LLM tool calling with feedback loop | `implemented` | app/tool_agent.py lets the model choose from 9 allowed tools, appends tool results back into messages, and loops until final answer or max step budget. |
| Real business-data interface | `implemented` | FastAPI exposes /business-data/agent-report for CSV exports and /postgres/support-tickets/agent-report for a read-only PostgreSQL table. |
| Structured AI output | `implemented` | AgentRunReport and QualityReport are Pydantic response models with findings, hypotheses, recommendations, evidence, verification, telemetry, and trace_id. |
| Deterministic report guardrails | `implemented` | ReportVerifier checks evidence support, known columns, sensitive terms, unsupported LLM evidence, action coverage, and score bounds. |
| Model observability and cost awareness | `implemented` | Agent evaluation records model, provider, prompt version, latency, token usage, estimated cost, retry budget, distinct tools, duplicate tools, and final report attachment. |
| Safe LLM degradation | `implemented` | Without OPENAI_API_KEY, the agent returns DISABLED with an explicit fallback instead of crashing the API. |
| Agent evaluation harness | `implemented` | evals/scenarios.jsonl and app/evals.py measure status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, and latency. |
| Source-cited retrieval for domain rules | `partial` | retrieve_business_rules gives the LLM source-cited local Markdown business rules for support-ticket constraints. |
| Accepted real-model run evidence | `not_claimed` | Real-model runbook and capture gate exist, but accepted_real_model_run_count is still 0 until a redacted OpenAI-compatible run is captured. |

## Evidence Counts

| Metric | Value |
| --- | ---: |
| Agent Readiness Implemented | 16 |
| Capability Matrix Implemented | 13 |
| Allowed Tools | 9 |
| Business Replay Rows | 8 |
| Business Replay Findings | 5 |
| Real Model Run Commands | 5 |
| Real Model Capture Required Fields | 17 |
| Real Model Capture Accepted Runs | 0 |
| Application Evidence Links | 50 |

## Resume-Safe Lines

- Built an OpenAI-compatible data-quality LLM agent for CSV and read-only PostgreSQL business data, with 9 controlled tools, dynamic tool selection, structured reports, trace/cost telemetry, deterministic guardrails, safe fallback, and CI-verified evidence artifacts.
- Explained LLM decisions through tool-call traces, evidence-backed findings, verification status, prompt version, token usage, latency, and estimated cost fields.

## Not Resume-Safe Yet

- Do not claim production users.
- Do not claim customer feedback.
- Do not claim accepted real-model benchmark runs until accepted_real_model_run_count is greater than 0.
- Do not claim embedding-based RAG until a vector retrieval layer is implemented.
