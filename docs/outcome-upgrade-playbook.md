# Outcome Upgrade Playbook

This generated playbook defines when the project is allowed to upgrade resume wording from engineering evidence to real outcome claims.

## Purpose

Define exactly when public adoption, feedback, business-case review, and repository-interest metrics can upgrade resume wording from baseline engineering evidence to real outcome claims.

## Current Public Counts

| Metric | Current value |
| --- | ---: |
| Stars | 0 |
| Forks | 1 |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |

## Upgrade Rules

| Rule | Metric | Current | Threshold | Status | Remaining |
| --- | --- | ---: | ---: | --- | ---: |
| first_confirmed_external_run | `confirmed_external_users` | 0 | 1 | `not_claimable_yet` | 1 |
| pilot_feedback_signal | `external_feedback_items` | 0 | 3 | `not_claimable_yet` | 3 |
| reproducible_bug_signal | `reproducible_feedback_items` | 0 | 1 | `not_claimable_yet` | 1 |
| business_case_signal | `business_case_feedback_items` | 0 | 1 | `not_claimable_yet` | 1 |
| github_interest_signal | `stars` | 0 | 5 | `not_claimable_yet` | 5 |

## Claimable Now

- Public GitHub Pages demo
- v0.3.0 release
- GHCR container image
- 190 passing CI tests
- 16 implemented LLM agent-readiness capabilities
- Read-only PostgreSQL and bounded CSV business-data intake

## Baseline Resume Wording

Built a public, containerized LLM data-quality agent with tool-calling, memory-informed planning, read-only PostgreSQL analysis, structured report guardrails, and CI-verified outcome evidence.

## Resume-Safe Summary

Published a CI-verified outcome upgrade playbook with 5 threshold-based rules that keep adoption, feedback, business-case, and repository-interest claims blocked until public evidence exists.

## Forbidden Until Proven

- external users
- customer feedback
- enterprise production usage
- business impact avoided
- revenue saved
- GitHub stars beyond the current public count

## Evidence Sources

- `adoption_metrics`: `docs/adoption-metrics.json`
- `feedback_metrics`: `docs/feedback-metrics.json`
- `pilot_review_tracker`: `docs/pilot-review-tracker.json`
- `external_review_evidence_ledger`: `docs/external-review-evidence-ledger.json`
