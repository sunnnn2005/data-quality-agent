# Agent Maturity Audit

Map the project against a practical 20-point LLM agent maturity checklist so resume claims stay evidence-backed and weak areas remain explicit.

## Summary

| Metric | Value |
| --- | ---: |
| Audit rows | 20 |
| Implemented areas | 14 |
| Partial areas | 5 |
| Not-claimed areas | 1 |
| Allowed tools | 9 |
| AI Engineer signals | 8 |
| Accepted real-model runs | 0 |

## Checklist

| Area | Status | Evidence | Resume Signal |
| --- | --- | --- | --- |
| Task goal | implemented | The agent investigates one dataset and returns quality status, risks, root-cause hypotheses, and remediation actions. | bounded AI task definition |
| LLM decision-making | implemented | The Chat Completions tool loop uses tool_choice=auto so the model chooses the next tool from the allowlist. | LLM-driven tool selection |
| Controlled tools | implemented | The toolbox exposes 9 structured allowlisted tools and rejects unknown tool names. | safe tool calling |
| Agent loop | implemented | Tool results are appended as role=tool messages before the next model step. | multi-step agent execution |
| Dynamic execution path | implemented | The strategy tool chooses different checks for transaction, support-ticket, customer, and generic tables. | adaptive data-quality investigation |
| State management | implemented | AgentRunReport stores status, final answer, tool calls, attached report, evaluation, and trace_id. | stateful agent reporting |
| Planning and replanning | partial | The model can inspect strategy, profile, memory, checks, and report tools iteratively, but there is no explicit editable plan object yet. | agent planning roadmap |
| Termination conditions | implemented | The loop stops on final model answer, attached quality report, disabled model fallback, or max-round budget. | bounded autonomous loop |
| Permissions and safety | implemented | The agent is read-only, uses a tool allowlist, limits database access, redacts sensitive fields, and verifies final reports. | AI safety boundary |
| Error handling and fallback | implemented | Missing OPENAI_API_KEY returns a structured DISABLED fallback instead of failing the API. | production-minded fallback |
| Context management | implemented | The model receives dataset metadata, profiles, redacted samples, and finding evidence rather than full private tables. | privacy-aware prompting |
| Memory | partial | The agent can retrieve sanitized prior traces and recurring incident patterns, but feedback labels do not yet update ranking. | dataset memory |
| RAG | partial | The agent retrieves source-cited local business rules, but embedding/vector search is not implemented yet. | source-cited retrieval |
| Structured output | implemented | QualityReport and AgentRunReport are Pydantic models with findings, hypotheses, evidence, telemetry, and verification. | machine-verifiable AI output |
| Fact/inference separation | implemented | The report separates findings, likely causes, root-cause hypotheses, recommended actions, evidence, and limitations. | evidence-backed reasoning |
| Guardrails and verification | implemented | ReportVerifier checks evidence support, known fields, sensitive terms, unsupported LLM evidence, and score bounds. | deterministic AI guardrails |
| Observability | partial | Trace ids, tool-call previews, fallback status, latency, token/cost fields, and SQLite trace persistence exist, but there is no full monitoring dashboard. | agent observability |
| Evaluation | partial | Scenario evals cover status accuracy, finding recall, evidence support, fallback, report-tool usage, and latency. | agent evaluation harness |
| Deployment and versioning | implemented | The repo publishes a FastAPI app, Docker image, public demo docs, OpenAPI artifact, CI, release notes, and public evidence checks. | shipping discipline |
| Real-model production evidence | not_claimed | The repo has a real-model runbook, capture gate, and preflight, but accepted_real_model_run_count is still 0. | blocked until real model evidence |

## Next Upgrades

- Planning and replanning: Add a compact plan state with current hypothesis, next tool, and stop reason after each loop.
- Memory: Use accepted and needs-review hypothesis labels to adjust later root-cause ranking.
- RAG: Add optional embedding-backed retrieval for larger business-rule and incident documents.
- Observability: Expose aggregate latency, cost, retry, and per-tool success metrics in a dashboard.
- Evaluation: Add a larger labeled eval set for tool-choice accuracy, false positives, evidence support, and cost.
- Real-model production evidence: Run one explicit paid or approved OpenAI-compatible trace, redact it, and pass the capture verifier.

## Resume-Safe Summary

Published a 20-point LLM agent maturity audit with 14 implemented areas, 5 partial areas, 9 controlled tools, structured output, guardrails, traceability, and an explicit zero accepted-real-model-run boundary.

## Not Claimed

- production users
- customer feedback
- enterprise deployment
- embedding-backed RAG
- accepted real-model benchmark run
- autonomous write actions
