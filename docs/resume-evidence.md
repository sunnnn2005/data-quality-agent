# Resume Evidence

This page maps resume-ready claims for Data Quality Agent to public evidence. It is intentionally conservative: verified signals are separated from metrics that are not available yet.

## Verified Signals

| Claim ID | Resume signal | Evidence | What it proves |
| --- | --- | --- | --- |
| `public-demo` | Launched public demo | [GitHub Pages demo](https://sunnnn2005.github.io/data-quality-agent/) | The project is publicly viewable and has a product-style demo page. |
| `public-release` | Published release | [v0.2.0 release](https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.2.0) | The project has a tagged public release. |
| `container-image` | Published runnable container | [GHCR package](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent) | The FastAPI service is packaged as a container image. |
| `ci-tests` | 61 passing CI tests | [GitHub Actions CI](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml) | Tests, support-ticket demo verification, business-impact verification, evaluation summary verification, feedback metrics verification, adoption metrics verification, and outcome evidence verification run in CI. |
| `support-ticket-artifact` | CI-verified support-ticket artifact | [Verified JSON artifact](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/verified-support-ticket-result.json) | The business-data case study result is machine-generated and checked for expected findings. |
| `postgres-agent-route` | Read-only PostgreSQL agent route | [API source](https://github.com/sunnnn2005/data-quality-agent/blob/main/app/main.py) | The project exposes a PostgreSQL support-ticket agent endpoint that reuses the read-only database adapter and safely falls back when no model key is configured. |
| `business-impact-artifact` | Quantified business-impact artifact | [Business impact JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json) | The support-ticket case study quantifies 4 issue categories, 4 affected columns, and 5 recommended actions without claiming external adoption. |
| `outcome-summary` | Resume-safe business outcome summary | [Outcome summary](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/outcome-summary.md) | The business-impact artifact is translated into a public business problem, issue category, risk, and remediation summary. |
| `report-guardrails` | Report verification guardrails | [Verifier tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_verifier.py) | Reports are checked for evidence support, valid field references, sensitive evidence values, unsupported LLM evidence, actions, and score bounds. |
| `persistent-trace-audit` | Persistent SQLite trace audit trail | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | Sanitized run traces can be persisted with `TRACE_DB_PATH` and recovered by trace id after process restart. |
| `dataset-memory-retrieval` | Dataset-level agent memory retrieval | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | The API retrieves recent sanitized traces, recurring checks, and recurring root-cause titles for a dataset. |
| `root-cause-ranking` | Evidence-ranked root-cause hypotheses | [Agent tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_agent.py) | Reports rank likely causes by confidence and include supporting checks, evidence, and recommended actions. |
| `eval-summary` | CI-verified agent evaluation harness | [Eval summary](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json) | The project publishes a 3-scenario evaluation summary for status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency. |
| `adoption-baseline` | Public adoption baseline | [Adoption metrics](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json) | Stars, forks, watchers, issue count, release, container image, and test count are tracked without inflation. |
| `adoption-history` | Public adoption history timeline | [Adoption history JSONL](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-history.jsonl) | Stars, forks, watchers, issues, release, commit, and test count can be audited over time. |
| `public-metrics-summary` | Unified public metrics summary | [Public metrics summary](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/public-metrics-summary.md) | Adoption, feedback, CI, release, outcome, and agent-readiness metrics are combined into one resume-safe public artifact. |
| `outcome-evidence` | Machine-readable evidence manifest | [Outcome evidence JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-evidence.json) | Resume claims are listed with public URLs and CI-verified by `scripts/verify_outcome_evidence.py`. |
| `resume-evidence-page` | Human-readable resume evidence page | [Resume evidence Markdown](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/resume-evidence.md) | Resume-safe claims, current metrics, and not-claimed outcomes are summarized for human review. |
| `feedback-log` | Public feedback tracking loop | [Feedback log](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/feedback-log.md) | Feedback collection exists, but starts from an honest zero-feedback baseline. |
| `feedback-metrics` | Machine-readable feedback metrics | [Feedback metrics JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-metrics.json) | Feedback and reproducible reports are tracked from public issue labels without inflating usage claims. |
| `public-evidence-health` | Scheduled public evidence health check | [Public Evidence Health workflow](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/public-evidence-health.yml) | A scheduled workflow verifies the public demo, release page, business-impact artifact, outcome evidence, and adoption metrics remain reachable. |
| `agent-readiness` | Public LLM agent readiness checklist | [Agent readiness](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/agent-readiness.md) | Implemented LLM agent capabilities are separated from partial and planned work, including RAG, observability, evaluation, and deeper incident-memory gaps. |

## Current Public Metrics

These are the current verified public metrics from `docs/adoption-metrics.json`:

| Metric | Current value |
| --- | ---: |
| GitHub stars | 0 |
| Forks | 1 |
| Watchers | 0 |
| GitHub issues | 10 |
| Automated tests | 61 |
| Support-ticket issue categories | 4 |
| Affected support-ticket columns | 4 |
| Recommended support-ticket actions | 5 |
| Ranked support-ticket root-cause hypotheses | 3 |
| Agent evaluation scenarios | 3 |
| Public evidence health checks | 9 |
| Public release | v0.2.0 |
| Public metrics summary | 1 |
| External feedback items | 0 |
| Confirmed external users | 0 |
| Reproducible feedback items | 0 |
| Adoption history entries | 3 |
| Implemented agent-readiness capabilities | 9 |

## Not Claimed Yet

These signals should not be written on the resume until there is evidence:

| Metric ID | Signal | Current status |
| --- | --- | --- |
| `users` | External users | No verified external users yet. |
| `customer_feedback` | Customer feedback | No external feedback issue has been submitted yet. |
| `production_company_usage` | Enterprise production usage | The project demonstrates a realistic business workflow, not verified enterprise production adoption. |

## Resume-Safe Wording

Use wording that is true today:

- Launched a public GitHub Pages demo and v0.2.0 release for an LLM-powered data reliability agent.
- Published a GHCR container image and CI-verified support-ticket artifact for a reproducible business data-quality case study.
- Added a read-only PostgreSQL agent route that analyzes a seeded business support-ticket table with model-key fallback.
- Added optional SQLite persistence for sanitized agent run traces, enabling audit lookup after process restart.
- Added dataset-level memory retrieval over recent sanitized trace summaries, recurring checks, and recurring root-cause titles.
- Added evidence-ranked root-cause hypotheses with confidence, supporting checks, and recommended actions.
- Added a CI-verified 3-scenario agent evaluation summary measuring status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency.
- Quantified 4 support-ticket data quality issue categories across 8 rows, including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers.
- Added a scheduled public evidence health check for the live demo, release page, business-impact artifact, outcome evidence, and adoption metrics.
- Added machine-readable feedback metrics that track public feedback and reproducible reports from an honest zero baseline.
- Added deterministic report verification guardrails and 61 passing CI tests.
- Published an agent-readiness checklist that separates implemented tool-calling, business-data, dataset memory, persistent trace, root-cause ranking, guardrail, and fallback capabilities from planned RAG, observability, evaluation, and deeper incident-memory work.

Avoid wording that is not true yet:

- Do not say the project has users.
- Do not say it has customer feedback.
- Do not say it is used by a company in production.
- Do not imply GitHub stars have been earned beyond the current public count.
