# Resume Evidence

This page maps resume-ready claims for Data Quality Agent to public evidence. It is intentionally conservative: verified signals are separated from metrics that are not available yet.

## Verified Signals

| Claim ID | Resume signal | Evidence | What it proves |
| --- | --- | --- | --- |
| `public-demo` | Launched public demo | [GitHub Pages demo](https://sunnnn2005.github.io/data-quality-agent/) | The project is publicly viewable and has a product-style demo page. |
| `public-release` | Published release | [v0.1.0 release](https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.1.0) | The project has a tagged public release. |
| `container-image` | Published runnable container | [GHCR package](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent) | The FastAPI service is packaged as a container image. |
| `ci-tests` | 51 passing CI tests | [GitHub Actions CI](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml) | Tests, support-ticket demo verification, business-impact verification, feedback metrics verification, adoption metrics verification, and outcome evidence verification run in CI. |
| `support-ticket-artifact` | CI-verified support-ticket artifact | [Verified JSON artifact](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/verified-support-ticket-result.json) | The business-data case study result is machine-generated and checked for expected findings. |
| `postgres-agent-route` | Read-only PostgreSQL agent route | [API source](https://github.com/sunnnn2005/data-quality-agent/blob/main/app/main.py) | The project exposes a PostgreSQL support-ticket agent endpoint that reuses the read-only database adapter and safely falls back when no model key is configured. |
| `business-impact-artifact` | Quantified business-impact artifact | [Business impact JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json) | The support-ticket case study quantifies 4 issue categories, 4 affected columns, and 5 recommended actions without claiming external adoption. |
| `report-guardrails` | Report verification guardrails | [Verifier tests](https://github.com/sunnnn2005/data-quality-agent/blob/main/tests/test_verifier.py) | Reports are checked for evidence support, valid field references, sensitive evidence values, unsupported LLM evidence, actions, and score bounds. |
| `adoption-baseline` | Public adoption baseline | [Adoption metrics](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json) | Stars, forks, watchers, issue count, release, container image, and test count are tracked without inflation. |
| `adoption-history` | Public adoption history timeline | [Adoption history JSONL](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-history.jsonl) | Stars, forks, watchers, issues, release, commit, and test count can be audited over time. |
| `outcome-evidence` | Machine-readable evidence manifest | [Outcome evidence JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-evidence.json) | Resume claims are listed with public URLs and CI-verified by `scripts/verify_outcome_evidence.py`. |
| `resume-evidence-page` | Human-readable resume evidence page | [Resume evidence Markdown](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/resume-evidence.md) | Resume-safe claims, current metrics, and not-claimed outcomes are summarized for human review. |
| `feedback-log` | Public feedback tracking loop | [Feedback log](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/feedback-log.md) | Feedback collection exists, but starts from an honest zero-feedback baseline. |
| `feedback-metrics` | Machine-readable feedback metrics | [Feedback metrics JSON](https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-metrics.json) | Feedback and reproducible reports are tracked from public issue labels without inflating usage claims. |
| `public-evidence-health` | Scheduled public evidence health check | [Public Evidence Health workflow](https://github.com/sunnnn2005/data-quality-agent/actions/workflows/public-evidence-health.yml) | A scheduled workflow verifies the public demo, release page, business-impact artifact, outcome evidence, and adoption metrics remain reachable. |

## Current Public Metrics

These are the current verified public metrics from `docs/adoption-metrics.json`:

| Metric | Current value |
| --- | ---: |
| GitHub stars | 0 |
| Forks | 1 |
| Watchers | 0 |
| GitHub issues | 10 |
| Automated tests | 51 |
| Support-ticket issue categories | 4 |
| Affected support-ticket columns | 4 |
| Recommended support-ticket actions | 5 |
| Public evidence health checks | 6 |
| Public release | v0.1.0 |
| External feedback items | 0 |
| Confirmed external users | 0 |
| Reproducible feedback items | 0 |
| Adoption history entries | 3 |

## Not Claimed Yet

These signals should not be written on the resume until there is evidence:

| Metric ID | Signal | Current status |
| --- | --- | --- |
| `users` | External users | No verified external users yet. |
| `customer_feedback` | Customer feedback | No external feedback issue has been submitted yet. |
| `production_company_usage` | Enterprise production usage | The project demonstrates a realistic business workflow, not verified enterprise production adoption. |

## Resume-Safe Wording

Use wording that is true today:

- Launched a public GitHub Pages demo and v0.1.0 release for an LLM-powered data reliability agent.
- Published a GHCR container image and CI-verified support-ticket artifact for a reproducible business data-quality case study.
- Added a read-only PostgreSQL agent route that analyzes a seeded business support-ticket table with model-key fallback.
- Quantified 4 support-ticket data quality issue categories across 8 rows, including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers.
- Added a scheduled public evidence health check for the live demo, release page, business-impact artifact, outcome evidence, and adoption metrics.
- Added machine-readable feedback metrics that track public feedback and reproducible reports from an honest zero baseline.
- Added deterministic report verification guardrails and 51 passing CI tests.

Avoid wording that is not true yet:

- Do not say the project has users.
- Do not say it has customer feedback.
- Do not say it is used by a company in production.
- Do not imply GitHub stars have been earned beyond the current public count.
