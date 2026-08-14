# Reviewer Quickstart Router

This generated router helps a reviewer choose the shortest public evidence path.

## Purpose

Route external reviewers to the shortest evidence path for their available time and background, so public feedback can become resume-countable only after the evidence gate accepts it.

## Choose a Path

| Reviewer Situation | Target Metric | Best For | Review | Submit Evidence |
| --- | --- | --- | --- | --- |
| I only have 5 minutes | `external_feedback_items` | A peer, recruiter, or classmate who can open the public demo and leave one specific note. | [Review](https://sunnnn2005.github.io/data-quality-agent/) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) |
| I can confirm I tried it | `confirmed_external_users` | Someone who can open the demo or quickstart and confirm the observed result. | [Review](https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md) |
| I can run the project | `reproducible_feedback_items` | A developer who can run Docker, the API, or a sanitized replay path. | [Review](https://github.com/sunnnn2005/data-quality-agent) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md) |
| I can review the agent architecture | `ai_engineer_review_items` | An AI/ML engineer, mentor, or advanced student who can inspect the tool-calling loop. | [Review](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| I can describe a real messy-data problem | `business_case_feedback_items` | A data analyst, operator, or student who has seen messy spreadsheet, ticket, sales, or ops data. | [Review](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) |

## Evidence to Collect

### I only have 5 minutes

- exact demo path opened
- one useful or confusing workflow detail
- permission sentence if the reviewer allows the evidence to count

Unlocks after acceptance: after acceptance: external feedback from a non-owner reviewer.

### I can confirm I tried it

- command or URL used
- observed result
- environment
- permission sentence if the reviewer allows the evidence to count

Unlocks after acceptance: after acceptance: confirmed external user or reviewer run.

### I can run the project

- endpoint or command used
- dataset shape without raw rows
- report status and finding count
- selected tools shown in the trace

Unlocks after acceptance: after acceptance: reproducible external run evidence.

### I can review the agent architecture

- implementation paths inspected
- strongest AI-agent signal
- least credible gap
- permission sentence if the reviewer allows the evidence to count

Unlocks after acceptance: after acceptance: external AI Engineer project review.

### I can describe a real messy-data problem

- anonymized workflow
- data-quality problem
- business impact
- permission sentence if the reviewer allows the evidence to count

Unlocks after acceptance: after acceptance: business-case feedback tied to a real workflow.

## First Manual Send

- Slot: `slot_07_ai_engineer_review`
- Target metric: `ai_engineer_review_items`
- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

## Current Zero Counts

| Metric | Current Count |
| --- | ---: |
| `ai_engineer_review_items` | 0 |
| `business_case_feedback_items` | 0 |
| `confirmed_external_users` | 0 |
| `external_feedback_items` | 0 |
| `reproducible_feedback_items` | 0 |

## Manual Counting Rule

Do not increase any outcome metric until a non-owner public GitHub issue includes permission, contains no private data, and passes the external reviewer evidence gate.

## Resume-Safe Summary

Published a reviewer quickstart router with 5 evidence paths mapped to feedback, confirmed-use, reproducible-run, AI-review, and business-case outcome metrics while preserving zero current claims.
