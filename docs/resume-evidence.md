# Resume Evidence

This page maps resume-ready claims for Data Quality Agent to public evidence. It is intentionally conservative: verified signals are separated from metrics that are not available yet.

## Verified Signals

| Claim ID | Resume signal | Evidence | What it proves |
| --- | --- | --- | --- |
| `public-demo` | Launched public demo | [GitHub Pages demo](https://sunnnn2005.github.io/data-quality-agent/) | The project is publicly viewable and has a product-style demo page. |
| `public-release` | Published release | [v0.2.0 release](https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.2.0) | The project has a tagged public release. |
| `container-image` | Published runnable container | [GHCR package](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent) | The FastAPI service is packaged as a container image. |
| `ci-tests` | 68 passing CI tests | [GitHub Actions CI](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml) | Tests, support-ticket demo verification, business-impact verification, evaluation summary verification, incident-pattern memory verification, agent observability verification, agent safety-boundary verification, live project scorecard verification, recruiter pitch verification, OpenAPI contract verification, hypothesis feedback verification, feedback metrics verification, adoption metrics verification, and outcome evidence verification run in CI. |
| `support-ticket-artifact` | CI-verified support-ticket artifact | [Verified JSON artifact](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/verified-support-ticket-result.json) | The business-data case study result is machine-generated and checked for expected findings. |
| `postgres-agent-route` | Read-only PostgreSQL agent route | [API source](https://github.com/sunnnn2005/data-quality-agent/blob/main/app/main.py) | The project exposes a PostgreSQL support-ticket agent endpoint that reuses the read-only database adapter and safely falls back when no model key is configured. |
| `business-impact-artifact` | Quantified business-impact artifact | [Business impact JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json) | The support-ticket case study quantifies 4 issue categories, 4 affected columns, and 5 recommended actions without claiming external adoption. |
| `outcome-summary` | Resume-safe business outcome summary | [Outcome summary](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/outcome-summary.md) | The business-impact artifact is translated into a public business problem, issue category, risk, and remediation summary. |
| `report-guardrails` | Report verification guardrails | [Verifier tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_verifier.py) | Reports are checked for evidence support, valid field references, sensitive evidence values, unsupported LLM evidence, actions, and score bounds. |
| `persistent-trace-audit` | Persistent SQLite trace audit trail | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | Sanitized run traces can be persisted with `TRACE_DB_PATH` and recovered by trace id after process restart. |
| `dataset-memory-retrieval` | Dataset-level agent memory retrieval | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | The API retrieves recent sanitized traces, recurring checks, and recurring root-cause titles for a dataset. |
| `incident-pattern-memory` | CI-verified incident-pattern memory | [Incident pattern memory](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/incident-pattern-memory.json) | The project retrieves 3 recurring incident patterns from 2 sanitized support-ticket traces without claiming external production incidents. |
| `agent-observability` | CI-verified agent observability artifact | [Agent observability](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-observability.json) | The project summarizes 2 observed run traces with fallback status, verification status, dataset memory, and tool-call preview coverage without claiming production monitoring. |
| `agent-safety-boundaries` | CI-verified agent safety boundaries | [Agent safety boundaries](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-safety-boundaries.json) | The project verifies 5 allowed agent tools, 3 rejected unsafe PostgreSQL queries, sensitive-field redaction, disabled fallback, and 6 report verifier rules without claiming a formal security audit. |
| `live-project-scorecard` | CI-verified live project scorecard | [Live project scorecard](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/live-project-scorecard.json) | The project gives reviewers one generated artifact for the demo, release, container image, CI tests, verified resume claims, agent capabilities, reviewer paths, and honest zero-adoption baselines. |
| `recruiter-pitch` | CI-verified recruiter pitch artifact | [Recruiter pitch](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/recruiter-pitch.json) | The project turns verified evidence into 3 resume bullets, a LinkedIn project description, a 30-second pitch, interview talking points, and evidence links without claiming unverified users or production usage. |
| `root-cause-ranking` | Evidence-ranked root-cause hypotheses | [Agent tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_agent.py) | Reports rank likely causes by confidence and include supporting checks, evidence, and recommended actions. |
| `eval-summary` | CI-verified agent evaluation harness | [Eval summary](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json) | The project publishes a 3-scenario evaluation summary for status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency. |
| `hypothesis-feedback` | Human-reviewed root-cause feedback labels | [Hypothesis feedback](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/hypothesis-feedback.json) | The project publishes accepted / needs-review labels for 3 root-cause hypotheses without claiming external product feedback. |
| `openapi-contract` | CI-verified OpenAPI contract | [OpenAPI JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/openapi.json) | The FastAPI app publishes a generated API contract covering 6 core integration endpoints for business data, agent reports, trace lookup, dataset memory, and incident export. |
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
| Automated tests | 68 |
| Support-ticket issue categories | 4 |
| Affected support-ticket columns | 4 |
| Recommended support-ticket actions | 5 |
| Ranked support-ticket root-cause hypotheses | 3 |
| Agent evaluation scenarios | 3 |
| Root-cause feedback labels | 3 |
| Recurring incident patterns | 3 |
| Observed run traces | 2 |
| Fallback events captured | 2 |
| Allowed agent tools | 5 |
| Rejected unsafe PostgreSQL queries | 3 |
| Report verifier rules | 6 |
| Live project scorecard | 1 |
| Scorecard reviewer paths | 5 |
| OpenAPI required integration endpoints | 6 |
| OpenAPI paths | 14 |
| Recruiter-safe resume bullets | 3 |
| Recruiter pitch target roles | 4 |
| Public evidence health checks | 16 |
| Public release | v0.2.0 |
| Public metrics summary | 1 |
| External feedback items | 0 |
| Confirmed external users | 0 |
| Reproducible feedback items | 0 |
| Adoption history entries | 3 |
| Implemented agent-readiness capabilities | 14 |

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
- Added CI-verified incident-pattern memory that retrieves 3 recurring support-ticket incident patterns from sanitized traces.
- Added CI-verified agent observability that tracks 2 run traces, fallback events, verification status, dataset memory, and tool-call preview coverage.
- Added CI-verified safety boundaries covering 5 allowed agent tools, read-only PostgreSQL query limits, sensitive-field redaction, disabled fallback, and 6 report verifier rules.
- Added a CI-verified live project scorecard with 5 reviewer paths for the demo, resume evidence, OpenAPI contract, safety boundaries, and public metrics.
- Added a CI-verified recruiter pitch artifact with 3 resume bullets, LinkedIn project description, 30-second pitch, interview talking points, and 5 evidence links.
- Added evidence-ranked root-cause hypotheses with confidence, supporting checks, and recommended actions.
- Added a CI-verified 3-scenario agent evaluation summary measuring status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency.
- Added 3 human-reviewed root-cause feedback labels for accepted / needs-review hypotheses without claiming external product feedback.
- Published a CI-verified OpenAPI contract covering 6 integration endpoints for business-data uploads, LLM agent reports, PostgreSQL reports, trace lookup, dataset memory, and incident export.
- Quantified 4 support-ticket data quality issue categories across 8 rows, including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers.
- Added a scheduled public evidence health check for the live demo, release page, business-impact artifact, outcome evidence, and adoption metrics.
- Added machine-readable feedback metrics that track public feedback and reproducible reports from an honest zero baseline.
- Added deterministic report verification guardrails and 68 passing CI tests.
- Published an agent-readiness checklist that separates implemented tool-calling, business-data, OpenAPI contract, dataset memory, incident-pattern memory, observability artifacts, safety boundaries, persistent trace, root-cause ranking, hypothesis feedback, guardrail, and fallback capabilities from planned RAG, observability, evaluation, and deeper incident-memory work.

Avoid wording that is not true yet:

- Do not say the project has users.
- Do not say it has customer feedback.
- Do not say it is used by a company in production.
- Do not imply GitHub stars have been earned beyond the current public count.
