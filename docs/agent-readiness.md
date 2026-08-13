# Agent Readiness

This page tracks how close Data Quality Agent is to a mature LLM agent. It is intentionally conservative: implemented capabilities are separated from partial and planned work.

## Implemented

| Capability | Evidence |
| --- | --- |
| LLM chooses among data-quality tools | `app/tool_agent.py` exposes `get_dataset_contract`, `profile_dataset`, `select_quality_strategy`, `run_quality_checks`, and `build_quality_report` as tool-calling functions. |
| Tool results feed back into a multi-step agent loop | `LLMDataQualityAgent.run` appends tool results back into model messages and continues for up to six rounds. |
| Real business data entrypoints | `/business-data/agent-report` accepts bounded CSV exports and `/postgres/support-tickets/agent-report` uses a read-only PostgreSQL adapter. |
| Deterministic report guardrails | `ReportVerifier` validates evidence support, known field references, sensitive evidence, unsupported LLM evidence, recommended actions, and score bounds. |
| Persistent trace audit trail | `TRACE_DB_PATH` enables SQLite persistence for sanitized run traces, allowing `/runs/{trace_id}` records to be recovered after process restart. |
| Dataset memory retrieval | `/datasets/{dataset_id}/memory` retrieves recent sanitized traces, recurring checks, and recurring root-cause titles for a dataset. |
| Evidence-ranked root-cause hypotheses | `QualityReport.root_cause_hypotheses` ranks likely causes by confidence and attaches supporting checks, evidence, and recommended actions. |
| Hypothesis feedback labels | `docs/hypothesis-feedback.json` records accepted and needs-review labels for generated root-cause hypotheses. |
| Safe fallback | When `OPENAI_API_KEY` is not configured, the agent returns a structured `DISABLED` state instead of failing the API. |
| Public evidence | `docs/outcome-evidence.json`, `docs/resume-evidence.md`, and Public Evidence Health verify resume-safe claims. |

## Partial

| Capability | Current state | Next step |
| --- | --- | --- |
| Memory | Dataset-level retrieval exists over sanitized trace summaries. | Add incident-pattern retrieval and use retrieved memory inside the LLM tool loop. |
| RAG | Business-rule retrieval uses local source-cited Markdown rules. | Add optional embedding-backed retrieval with source citations and permission filtering. |
| Observability | Sanitized trace summaries and tool-call previews are available. | Track prompt version, model version, token use, latency breakdown, retries, and estimated cost. |
| Evaluation | Tests cover fallback, tool use, evidence support, and public artifacts. | Add a larger labeled eval set for tool-choice accuracy, finding recall, false positives, and cost. |

## Planned

- Add incident-pattern memory retrieval over previous trace summaries.
- Add a human approval boundary before exporting remediation SQL or ticket actions.
- Add issue-pattern memory retrieval that reuses accepted or needs-review root-cause labels.

## Not Claimed

- External users
- Customer feedback
- Enterprise production deployment
- Paid model benchmark results

## Resume-Safe Wording

- Built an LLM tool-calling data-quality agent with dynamic tool selection, read-only PostgreSQL analysis, dataset memory retrieval, persistent SQLite trace audit logging, evidence-ranked root-cause hypotheses, human-reviewed hypothesis feedback labels, structured report guardrails, and safe model-key fallback.
- Published an agent-readiness checklist that separates implemented LLM agent capabilities from partial RAG, observability, evaluation, and deeper incident-memory work.
