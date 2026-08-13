# Pilot Review Tracker

This generated tracker turns the pilot plan into an auditable review pipeline.

## Purpose

Track planned pilot review requests, public evidence links, and resume-safe status without counting private messages or unverified compliments as users or feedback.

## Planned Reviews

| ID | Segment | Status | Primary Review Path | Counts Toward Resume | Next Step |
| --- | --- | --- | --- | --- | --- |
| student-review-1 | student_reviewers | not_contacted | [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/) | False | Send a short demo-review request to one UC Davis classmate or club member. |
| developer-review-1 | developer_reviewers | not_contacted | [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent) | False | Ask one student developer to run the repo locally or inspect the API contract. |
| career-review-1 | career_reviewers | not_contacted | [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md) | False | Ask one mentor, recruiter, or hiring manager to review the evidence pack. |

## Status Counts

| Status | Count |
| --- | ---: |
| Not Contacted | 3 |
| Contacted | 0 |
| Feedback Received | 0 |

## Public Counts

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |

## Resume Upgrade Rules

| Signal | Current Value | Minimum Before Claim | Required Evidence | Status |
| --- | ---: | ---: | --- | --- |
| public pilot feedback | 0 | 3 | public GitHub issue labeled feedback | `not_claimable_yet` |
| external reviewer tried the project | 0 | 1 | public issue or note labeled confirmed-user | `not_claimable_yet` |
| real-world business case feedback | 0 | 1 | public issue using the business-case template | `not_claimable_yet` |

## Tracking Rules

- Only count feedback that is linked from a public GitHub issue or reproducible external note.
- Only count a user after they explicitly confirm they tried the demo or ran the project.
- Do not count private compliments, application submissions, or self-testing as external users.
- Keep stars, users, and feedback as zero until public metrics prove otherwise.

## Resume-Safe Summary

Published a CI-verified pilot review tracker with 3 planned reviewer segments, public evidence links, status counts, and resume-upgrade rules while preserving zero verified feedback and user claims.

## Not Claimed

- external users
- customer feedback
- enterprise production usage
- GitHub stars beyond the current public count
