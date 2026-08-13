# Resume Evidence

This page maps resume-ready claims for Data Quality Agent to public evidence. It is intentionally conservative: verified signals are separated from metrics that are not available yet.

## Verified Signals

| Claim ID | Resume signal | Evidence | What it proves |
| --- | --- | --- | --- |
| `public-demo` | Launched public demo | [GitHub Pages demo](https://sunnnn2005.github.io/data-quality-agent/) | The project is publicly viewable and has a product-style demo page. |
| `public-release` | Published release | [v0.3.0 release](https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.3.0) | The project has a tagged public release. |
| `container-image` | Published runnable container | [GHCR package](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent) | The FastAPI service is packaged as a container image. |
| `ci-tests` | 90 passing CI tests | [GitHub Actions CI](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml) | Tests, support-ticket demo verification, business-impact verification, evaluation summary verification, incident-pattern memory verification, agent observability verification, agent safety-boundary verification, local reviewer demo verification, API smoke report verification, performance baseline verification, demo usage baseline verification, business-data intake baseline verification, community growth baseline verification, impact review packet verification, business problem casebook verification, public traction dashboard verification, feedback intake quality verification, business case intake verification, star growth kit verification, live project scorecard verification, recruiter pitch verification, application evidence pack verification, pilot outreach kit verification, pilot program plan verification, OpenAPI contract verification, hypothesis feedback verification, feedback metrics verification, adoption metrics verification, and outcome evidence verification run in CI. |
| `support-ticket-artifact` | CI-verified support-ticket artifact | [Verified JSON artifact](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/verified-support-ticket-result.json) | The business-data case study result is machine-generated and checked for expected findings. |
| `postgres-agent-route` | Read-only PostgreSQL agent route | [API source](https://github.com/sunnnn2005/data-quality-agent/blob/main/app/main.py) | The project exposes a PostgreSQL support-ticket agent endpoint that reuses the read-only database adapter and safely falls back when no model key is configured. |
| `business-impact-artifact` | Quantified business-impact artifact | [Business impact JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json) | The support-ticket case study quantifies 4 issue categories, 4 affected columns, and 5 recommended actions without claiming external adoption. |
| `outcome-summary` | Resume-safe business outcome summary | [Outcome summary](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/outcome-summary.md) | The business-impact artifact is translated into a public business problem, issue category, risk, and remediation summary. |
| `business-remediation-scorecard` | CI-verified business remediation scorecard | [Business impact JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json) | The project maps support-ticket findings to 4 business risk areas, 3 high-priority actions, and 4 owner handoffs without claiming external adoption. |
| `report-guardrails` | Report verification guardrails | [Verifier tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_verifier.py) | Reports are checked for evidence support, valid field references, sensitive evidence values, unsupported LLM evidence, actions, and score bounds. |
| `persistent-trace-audit` | Persistent SQLite trace audit trail | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | Sanitized run traces can be persisted with `TRACE_DB_PATH` and recovered by trace id after process restart. |
| `dataset-memory-retrieval` | Dataset-level agent memory retrieval | [Trace tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_traces.py) | The API retrieves recent sanitized traces, recurring checks, and recurring root-cause titles for a dataset. |
| `incident-pattern-memory` | CI-verified incident-pattern memory | [Incident pattern memory](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/incident-pattern-memory.json) | The project retrieves 3 recurring incident patterns from 2 sanitized support-ticket traces without claiming external production incidents. |
| `memory-informed-planning` | Memory-informed LLM agent planning | [Agent tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_agent.py) | The LLM tool-calling agent can retrieve sanitized dataset memory inside the agent loop so recurring checks and incident patterns from prior runs can inform follow-up planning. |
| `source-cited-business-rule-tool` | Source-cited business-rule retrieval tool | [Agent tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_agent.py) | The LLM tool-calling agent can retrieve source-cited business rules after quality checks so remediation guidance can reference business constraints instead of only generic data statistics. |
| `agent-observability` | CI-verified agent observability artifact | [Agent observability](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-observability.json) | The project summarizes 2 observed run traces with fallback status, verification status, dataset memory, and tool-call preview coverage without claiming production monitoring. |
| `model-telemetry-artifact` | CI-verified model telemetry artifact | [Agent observability](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-observability.json) | The project verifies mocked LLM telemetry for 2 model calls, 360 tokens, prompt version, latency, retry budget, estimated cost, and raw-prompt logging status without claiming paid model benchmark results. |
| `agent-safety-boundaries` | CI-verified agent safety boundaries | [Agent safety boundaries](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-safety-boundaries.json) | The project verifies 7 allowed agent tools, 3 rejected unsafe PostgreSQL queries, sensitive-field redaction, disabled fallback, and 6 report verifier rules without claiming a formal security audit. |
| `agent-capability-matrix` | CI-verified LLM agent capability matrix | [Agent capability matrix](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-capability-matrix.json) | The project maps itself against a practical LLM-agent checklist with 13 implemented capabilities, 4 partial maturity areas, 7 allowed tools, and explicit not-claimed production adoption. |
| `local-reviewer-demo` | CI-verified local reviewer demo | [Local reviewer demo](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/local-reviewer-demo.json) | The project verifies a Docker Compose reviewer path with 8 seeded PostgreSQL rows, a read-only database user, and 3 local review routes without claiming external reviewer completion. |
| `api-smoke-report` | CI-verified API smoke report | [API smoke report](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/api-smoke-report.json) | The project verifies 6 FastAPI route checks for health, catalog, profiling, deterministic reports, disabled agent fallback, and incident Markdown export without claiming production uptime. |
| `performance-baseline` | CI-verified local performance baseline | [Performance baseline](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/performance-baseline.json) | The project verifies 2 local FastAPI route benchmarks and 24 measured endpoint calls without claiming production latency or hosted traffic. |
| `demo-usage-baseline` | Public demo usage baseline | [Demo usage baseline](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/demo-usage-baseline.json) | The project verifies public demo entrypoints and tracks feedback issues, GitHub stars, and forks without claiming visitor analytics or product adoption. |
| `business-data-intake-baseline` | CI-verified business-data intake baseline | [Business data intake baseline](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-data-intake-baseline.json) | The project verifies bounded CSV uploads, read-only PostgreSQL context, 4 integration endpoints, 3 upload limits, and 6 API tests without claiming production datasets or external users. |
| `community-growth-baseline` | CI-verified community growth baseline | [Community growth baseline](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/community-growth-baseline.json) | The project verifies 5 issue templates, 6 configured labels, contribution guidance, public feedback entrypoints, and current public counts without claiming community adoption. |
| `impact-review-packet` | CI-verified impact review packet | [Impact review packet](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/impact-review-packet.json) | The project maps a support-operations data-quality case study to 12 verified business metrics, 8 evidence links, 5 remediation actions, and 4 owner handoffs without claiming external adoption. |
| `business-problem-casebook` | CI-verified business problem casebook | [Business problem casebook](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-problem-casebook.json) | The project explains a support-operations dashboard failure mode with 4 detected business risks, 5 findings, 3 root-cause hypotheses, and 4 remediation owner handoffs without claiming real customer data. |
| `public-traction-dashboard` | CI-verified public traction dashboard | [Public traction dashboard](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-traction-dashboard.json) | The project tracks 4 live project surfaces, 13 growth or review channels, 5 demo funnel steps, and 3 resume-upgrade rules without inflating current traction. |
| `star-growth-kit` | CI-verified star growth kit | [Star growth kit](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/star-growth-kit.json) | The project verifies 6 repo topics, 4 ethical growth actions, 3 resume-upgrade rules, and the current 0-star baseline without inflating traction. |
| `business-case-intake` | CI-verified business-case intake path | [Business case intake](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-case-intake.json) | The project publishes a GitHub issue template and generated artifact for collecting anonymized real-world data-quality problems, business context, tried route, outcome signal, and permission boundaries without claiming submitted external cases yet. |
| `live-project-scorecard` | CI-verified live project scorecard | [Live project scorecard](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/live-project-scorecard.json) | The project gives reviewers one generated artifact for the demo, release, container image, CI tests, verified resume claims, agent capabilities, 11 reviewer paths, and honest zero-adoption baselines. |
| `recruiter-pitch` | CI-verified recruiter pitch artifact | [Recruiter pitch](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/recruiter-pitch.json) | The project turns verified evidence into 3 resume bullets, a LinkedIn project description, a 30-second pitch, interview talking points, and evidence links without claiming unverified users or production usage. |
| `application-evidence-pack` | CI-verified application evidence pack | [Application evidence pack](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/application-evidence-pack.json) | The project gives recruiters 13 application evidence links, verified outcome numbers, resume bullets, an email attachment note, an interview opening, review order, and honest adoption baselines. |
| `pilot-outreach-kit` | CI-verified pilot outreach kit | [Pilot outreach kit](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-outreach-kit.json) | The project publishes 3 outreach messages, 8 review paths, tracking rules, and target feedback metrics to collect real public feedback without inflating current adoption. |
| `pilot-program-plan` | CI-verified pilot program plan | [Pilot program plan](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-program-plan.json) | The project publishes 3 participant segments, a 3-week feedback plan, feedback evidence rules, success thresholds, issue labels, and resume upgrade rules before adoption claims are allowed. |
| `root-cause-ranking` | Evidence-ranked root-cause hypotheses | [Agent tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_agent.py) | Reports rank likely causes by confidence and include supporting checks, evidence, and recommended actions. |
| `eval-summary` | CI-verified agent evaluation harness | [Eval summary](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json) | The project publishes a 3-scenario evaluation summary for status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency. |
| `tool-planning-eval` | CI-verified tool-planning evaluation | [Eval summary](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json) | The project verifies 7 allowed LLM agent tools and 0.889 strategy recommendation recall across 3 dataset scenarios without claiming paid model benchmark results. |
| `hypothesis-feedback` | Human-reviewed root-cause feedback labels | [Hypothesis feedback](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/hypothesis-feedback.json) | The project publishes accepted / needs-review labels for 3 root-cause hypotheses without claiming external product feedback. |
| `openapi-contract` | CI-verified OpenAPI contract | [OpenAPI JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/openapi.json) | The FastAPI app publishes a generated API contract covering 6 core integration endpoints for business data, agent reports, trace lookup, dataset memory, and incident export. |
| `adoption-baseline` | Public adoption baseline | [Adoption metrics](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json) | Stars, forks, watchers, issue count, release, container image, and test count are tracked without inflation. |
| `adoption-history` | Public adoption history timeline | [Adoption history JSONL](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-history.jsonl) | Stars, forks, watchers, issues, release, commit, and test count can be audited over time. |
| `public-metrics-summary` | Unified public metrics summary | [Public metrics summary](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/public-metrics-summary.md) | Adoption, feedback, CI, release, outcome, and agent-readiness metrics are combined into one resume-safe public artifact. |
| `outcome-evidence` | Machine-readable evidence manifest | [Outcome evidence JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-evidence.json) | Resume claims are listed with public URLs and CI-verified by `scripts/verify_outcome_evidence.py`. |
| `resume-evidence-page` | Human-readable resume evidence page | [Resume evidence Markdown](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/resume-evidence.md) | Resume-safe claims, current metrics, and not-claimed outcomes are summarized for human review. |
| `feedback-log` | Public feedback tracking loop | [Feedback log](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/feedback-log.md) | Feedback collection exists, but starts from an honest zero-feedback baseline. |
| `feedback-metrics` | Machine-readable feedback metrics | [Feedback metrics JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-metrics.json) | Feedback and reproducible reports are tracked from public issue labels without inflating usage claims. |
| `feedback-intake-quality` | CI-verified feedback intake system | [Feedback intake quality](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-intake-quality.json) | The public demo feedback template captures reviewer path, environment, reproducibility outcome, bug or feature signals, and real-workflow usefulness while preserving honest adoption and feedback baselines. |
| `public-evidence-health` | Scheduled public evidence health check | [Public Evidence Health workflow](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/public-evidence-health.yml) | A scheduled workflow verifies the public demo, release page, business-impact artifact, outcome evidence, and adoption metrics remain reachable. |
| `agent-readiness` | Public LLM agent readiness checklist | [Agent readiness](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/agent-readiness.md) | Implemented LLM agent capabilities are separated from partial and planned work, including RAG, observability, evaluation, and deeper incident-memory gaps. |

## Current Public Metrics

These are the current verified public metrics from `docs/adoption-metrics.json`:

| Metric | Current value |
| --- | ---: |
| GitHub stars | 0 |
| Forks | 1 |
| Watchers | 0 |
| GitHub issues | 11 |
| Automated tests | 90 |
| Support-ticket issue categories | 4 |
| Affected support-ticket columns | 4 |
| Recommended support-ticket actions | 5 |
| Ranked support-ticket root-cause hypotheses | 3 |
| Business risk areas | 4 |
| High-priority remediation actions | 3 |
| Owner handoffs | 4 |
| Agent evaluation scenarios | 3 |
| Agent strategy recommendation recall | 0.889 |
| Root-cause feedback labels | 3 |
| Recurring incident patterns | 3 |
| Observed run traces | 2 |
| Fallback events captured | 2 |
| Mocked LLM model calls | 2 |
| Mocked LLM token count | 360 |
| Mocked LLM estimated cost USD | 0.000081 |
| Allowed agent tools | 7 |
| Rejected unsafe PostgreSQL queries | 3 |
| Report verifier rules | 6 |
| Agent capability matrix | 1 |
| Agent matrix implemented capabilities | 13 |
| Agent matrix partial maturity areas | 4 |
| Agent matrix not-claimed areas | 1 |
| Local reviewer seeded PostgreSQL rows | 8 |
| Local reviewer routes | 3 |
| API smoke checks | 6 |
| API smoke passed checks | 6 |
| Performance route benchmarks | 2 |
| Performance measured endpoint calls | 24 |
| Demo usage tracked funnel steps | 5 |
| Demo usage entrypoints verified | 4 |
| Business-data intake endpoints | 4 |
| Business-data intake API tests | 6 |
| Business-data intake max rows | 10,000 |
| Business-data intake max columns | 80 |
| Community issue templates | 5 |
| Community labels | 6 |
| Community public growth channels | 6 |
| Impact review packet | 1 |
| Impact review business metrics | 12 |
| Impact review evidence links | 8 |
| Business problem casebook | 1 |
| Business problem cases | 1 |
| Business problem detected risks | 4 |
| Business problem owner handoffs | 4 |
| Public traction dashboard | 1 |
| Public traction surfaces | 4 |
| Public traction growth channels | 13 |
| Public traction resume upgrade rules | 3 |
| Live project scorecard | 1 |
| Scorecard reviewer paths | 11 |
| OpenAPI required integration endpoints | 6 |
| OpenAPI paths | 14 |
| Recruiter-safe resume bullets | 3 |
| Recruiter pitch target roles | 4 |
| Application evidence pack | 1 |
| Application evidence links | 13 |
| Pilot outreach messages | 3 |
| Pilot review paths | 8 |
| Star growth kit | 1 |
| Star growth required topics | 6 |
| Star growth ethical actions | 4 |
| Star growth resume upgrade rules | 3 |
| Business-case intake | 1 |
| Business-case intake required sections | 6 |
| Business-case intake tried paths | 5 |
| Business-case intake outcome signals | 5 |
| Business-case intake captured evidence groups | 6 |
| Pilot program segments | 3 |
| Pilot program weeks | 3 |
| Feedback intake quality | 1 |
| Feedback intake required sections | 5 |
| Feedback intake demo paths | 5 |
| Feedback intake outcome signals | 4 |
| Feedback intake captured evidence groups | 5 |
| Public evidence health checks | 19 |
| Public release | v0.3.0 |
| Public metrics summary | 1 |
| External feedback items | 0 |
| Confirmed external users | 0 |
| Reproducible feedback items | 0 |
| Adoption history entries | 24 |
| Implemented agent-readiness capabilities | 16 |

## Not Claimed Yet

These signals should not be written on the resume until there is evidence:

| Metric ID | Signal | Current status |
| --- | --- | --- |
| `users` | External users | No verified external users yet. |
| `customer_feedback` | Customer feedback | No external feedback issue has been submitted yet. |
| `production_company_usage` | Enterprise production usage | The project demonstrates a realistic business workflow, not verified enterprise production adoption. |

## Resume-Safe Wording

Use wording that is true today:

- Launched a public GitHub Pages demo and v0.3.0 release for an LLM-powered data reliability agent.
- Published a GHCR container image and CI-verified support-ticket artifact for a reproducible business data-quality case study.
- Added a read-only PostgreSQL agent route that analyzes a seeded business support-ticket table with model-key fallback.
- Added optional SQLite persistence for sanitized agent run traces, enabling audit lookup after process restart.
- Added dataset-level memory retrieval over recent sanitized trace summaries, recurring checks, and recurring root-cause titles.
- Added CI-verified incident-pattern memory that retrieves 3 recurring support-ticket incident patterns from sanitized traces.
- Added memory-informed LLM agent planning that lets the model call `retrieve_dataset_memory` inside the tool loop before continuing investigation.
- Added source-cited business-rule retrieval that lets the model call `retrieve_business_rules` after quality checks and cite local rule documentation.
- Added CI-verified agent observability that tracks 2 run traces, fallback events, verification status, dataset memory, and tool-call preview coverage.
- Added CI-verified model telemetry for 2 mocked LLM calls, 360 tokens, prompt version, latency, retry budget, estimated cost, and raw-prompt logging status.
- Added CI-verified safety boundaries covering 7 allowed agent tools, read-only PostgreSQL query limits, sensitive-field redaction, disabled fallback, and 6 report verifier rules.
- Added a CI-verified local reviewer demo with 8 seeded PostgreSQL rows, a read-only database user, and 3 local review routes.
- Added a CI-verified API smoke report covering 6 FastAPI route checks for health, catalog, profiling, deterministic reports, disabled agent fallback, and incident Markdown export.
- Added a CI-verified local performance baseline covering 2 FastAPI route benchmarks and 24 measured endpoint calls without claiming production latency.
- Added a public demo usage baseline with 5 tracked funnel steps and 4 verified demo entrypoints, while preserving zero external-user and zero-feedback claims.
- Added a CI-verified business-data intake baseline covering bounded CSV uploads, read-only PostgreSQL context, 4 integration endpoints, 3 upload limits, and 6 API tests without claiming production datasets.
- Added a CI-verified community growth baseline with 5 issue templates, 6 configured labels, 6 public contribution or feedback channels, contribution guidance, and honest current public counts.
- Added a CI-verified impact review packet with 12 verified business metrics, 8 evidence links, 5 remediation actions, and 4 owner handoffs for a support-operations data-quality case study.
- Added a CI-verified public traction dashboard with 4 live project surfaces, 13 growth or review channels, 5 tracked demo funnel steps, and 3 resume-upgrade rules.
- Added a CI-verified business problem casebook with 1 support-operations dashboard case, 4 detected business risks, 5 evidence-backed findings, 3 root-cause hypotheses, and 4 owner handoffs.
- Added a CI-verified live project scorecard with 11 reviewer paths for the demo, resume evidence, impact packet, business problem casebook, traction dashboard, feedback intake quality, OpenAPI contract, safety boundaries, agent capability matrix, local reviewer demo, and public metrics.
- Added a CI-verified agent capability matrix with 13 implemented LLM-agent checklist items, 4 partial maturity areas, 7 allowed tools, and explicit not-claimed production adoption.
- Added a CI-verified recruiter pitch artifact with 3 resume bullets, LinkedIn project description, 30-second pitch, interview talking points, and 11 evidence links.
- Added a CI-verified application evidence pack with 13 recruiter review links, verified outcome numbers, resume bullets, an email note, and an interview opening.
- Added a CI-verified pilot outreach kit with 3 outreach messages, 8 review paths, feedback tracking rules, and target feedback metrics.
- Added a CI-verified pilot program plan with 3 participant segments, a 3-week feedback plan, success thresholds, issue labels, and resume upgrade rules.
- Added a CI-verified feedback intake system with 5 required sections, 5 demo paths, 4 outcome signals, and 5 captured evidence groups.
- Added a CI-verified business-case intake path with 6 required sections, 5 tried paths, 5 outcome signals, and 6 captured evidence groups for future anonymized real-world data-quality problem feedback.
- Added evidence-ranked root-cause hypotheses with confidence, supporting checks, and recommended actions.
- Added a CI-verified 3-scenario agent evaluation summary measuring status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency.
- Added CI-verified tool-planning evaluation covering 7 allowed LLM agent tools and 0.889 strategy recommendation recall across 3 dataset scenarios.
- Added 3 human-reviewed root-cause feedback labels for accepted / needs-review hypotheses without claiming external product feedback.
- Published a CI-verified OpenAPI contract covering 6 integration endpoints for business-data uploads, LLM agent reports, PostgreSQL reports, trace lookup, dataset memory, and incident export.
- Quantified 4 support-ticket data quality issue categories across 8 rows, including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers.
- Added a remediation scorecard mapping 5 support-ticket findings to 4 business risk areas, 3 high-priority actions, and 4 owner handoffs.
- Added a scheduled public evidence health check for the live demo, release page, business-impact artifact, outcome evidence, and adoption metrics.
- Added machine-readable feedback metrics that track public feedback and reproducible reports from an honest zero baseline.
- Added a CI-verified star growth kit with 6 verified repo topics, 4 ethical growth actions, 3 resume-upgrade rules, and the current 0-star baseline.
- Added deterministic report verification guardrails and 90 passing CI tests.
- Published an agent-readiness checklist that separates implemented tool-calling, business-data, OpenAPI contract, dataset memory, memory-informed planning, source-cited business-rule retrieval, incident-pattern memory, observability artifacts, safety boundaries, persistent trace, root-cause ranking, hypothesis feedback, guardrail, and fallback capabilities from planned embedding-backed RAG, observability, evaluation, and feedback-informed memory work.

Avoid wording that is not true yet:

- Do not say the project has users.
- Do not say it has customer feedback.
- Do not say it is used by a company in production.
- Do not imply GitHub stars have been earned beyond the current public count.
