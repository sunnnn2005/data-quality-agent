# Evidence Acceptance Checklist

This generated checklist defines what evidence is required before stronger resume outcome claims can be made.

## Purpose

Turn every blocked resume outcome into a concrete acceptance checklist, so stronger claims are added only after public, non-owner, permissioned, redacted evidence exists.

## Current Gate Status

| Metric | Value |
| --- | ---: |
| Accepted public reviewer issues | 0 |
| Rejected/planning issues | 14 |
| Acceptance checklist items | 6 |

No accepted external reviewer issue exists yet.

## Blocked Outcome Checklist

| Metric | Current | Required | Remaining | Status |
| --- | ---: | ---: | ---: | --- |
| `ai_engineer_review_items` | 0 | 1 | 1 | `blocked_until_public_evidence` |
| `confirmed_external_users` | 0 | 1 | 1 | `blocked_until_public_evidence` |
| `reproducible_feedback_items` | 0 | 1 | 1 | `blocked_until_public_evidence` |
| `business_case_feedback_items` | 0 | 1 | 1 | `blocked_until_public_evidence` |
| `external_feedback_items` | 0 | 3 | 3 | `blocked_until_public_evidence` |
| `github_stars` | 0 | 5 | 5 | `blocked_until_public_evidence` |

## Acceptance Details

### `ai_engineer_review_items`

- Reviewer situation: I can review the agent architecture
- Review path: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Evidence gate: A non-owner public review issue lists inspected paths and grants permission to count.
- Future resume line: Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail.

Required fields:
- implementation paths inspected
- strongest AI-agent signal
- least credible gap
- permission sentence if the reviewer allows the evidence to count

### `confirmed_external_users`

- Reviewer situation: I can confirm I tried it
- Review path: [https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html](https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md)
- Evidence gate: A non-owner public GitHub issue confirms the path tried and includes permission to count.
- Future resume line: Validated the data-quality LLM agent with 1 external reviewer who ran the public demo or local repo.

Required fields:
- command or URL used
- observed result
- environment
- permission sentence if the reviewer allows the evidence to count

### `reproducible_feedback_items`

- Reviewer situation: I can run the project
- Review path: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Evidence gate: A public issue includes command or URL evidence, expected result, actual result, and environment.
- Future resume line: Converted 1 reproducible external run report into an evidence-backed fix backlog.

Required fields:
- endpoint or command used
- dataset shape without raw rows
- report status and finding count
- selected tools shown in the trace

### `business_case_feedback_items`

- Reviewer situation: I can describe a real messy-data problem
- Review path: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Evidence gate: A public business-case issue includes anonymized schema, quality failure, impact, and reviewer role.
- Future resume line: Reviewed the agent against 1 anonymized real-world data-quality workflow and mapped the resulting risks.

Required fields:
- anonymized workflow
- data-quality problem
- business impact
- permission sentence if the reviewer allows the evidence to count

### `external_feedback_items`

- Reviewer situation: I only have 5 minutes
- Review path: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Evidence gate: Public feedback issues include role, path tried, outcome, improvement request, and permission.
- Future resume line: Collected 3 public reviewer feedback items and converted them into prioritized product fixes.

Required fields:
- exact demo path opened
- one useful or confusing workflow detail
- permission sentence if the reviewer allows the evidence to count

### `github_stars`

- Reviewer situation: Someone genuinely finds the repo useful enough to star it
- Review path: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/stargazers](https://github.com/sunnnn2005/data-quality-agent/stargazers)
- Evidence gate: GitHub public star count and docs/adoption-metrics.json both show at least 5 stars.
- Future resume line: Reached 5 organic GitHub stars after publishing a reproducible LLM agent demo and evidence pack.

Required fields:
- public GitHub star count reaches threshold
- docs/adoption-metrics.json records the same public count
- no paid, traded, or fake engagement

## Current Public Counts

| Metric | Count |
| --- | ---: |
| `ai_engineer_review_items` | 0 |
| `business_case_feedback_items` | 0 |
| `confirmed_external_users` | 0 |
| `external_feedback_items` | 0 |
| `github_forks` | 1 |
| `github_stars` | 0 |
| `reproducible_feedback_items` | 0 |

## Manual Counting Rule

Do not increase any outcome metric until a non-owner public GitHub issue includes permission, contains no private data, and passes the external reviewer evidence gate.

## Resume-Safe Summary

Published an evidence acceptance checklist mapping 6 blocked resume outcome metrics to required public fields, submission URLs, evidence gates, and future resume lines while preserving zero accepted external evidence.

## Not Claimed

- external users
- external feedback
- real business validation
- external AI Engineer review
- GitHub stars
