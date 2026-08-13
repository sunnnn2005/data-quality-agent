# Reviewer Submission Hub

This generated hub gives external reviewers one short path to submit public evidence.

## Purpose

Give reviewers one short public hub for submitting evidence that can turn zero-count resume outcomes into evidence-backed claims after the external evidence gate accepts them.

## Submission Paths

| Path | Target Metric | Minutes | Review Path | Submit Evidence | Counting Rule |
| --- | --- | ---: | --- | --- | --- |
| try_public_demo | `external_feedback_items` | 5 | [Review](https://sunnnn2005.github.io/data-quality-agent/) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) | Counts only after a non-owner public issue grants permission and passes the evidence gate. |
| confirm_external_run | `confirmed_external_users` | 8 | [Review](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/external-run-quickstart.md) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md) | Counts only when the reviewer ran or opened a runnable path and submitted observed-result evidence. |
| submit_reproducible_issue | `reproducible_feedback_items` | 10 | [Review](https://github.com/sunnnn2005/data-quality-agent) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md) | Counts only when reproduction steps are specific enough for the maintainer to retry. |
| submit_business_case | `business_case_feedback_items` | 12 | [Review](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) | Counts only when the business case is anonymized, permissioned, and contains no raw production data. |
| submit_ai_engineer_review | `ai_engineer_review_items` | 12 | [Review](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) | Counts only when an external reviewer inspects implementation evidence and grants permission. |
| star_or_fork_if_useful | `github_stars` | 1 | [Review](https://github.com/sunnnn2005/data-quality-agent) | [Submit](https://github.com/sunnnn2005/data-quality-agent/stargazers) | Counts only from GitHub public star data; never asks for fake engagement. |

## Required Evidence Fields

### try_public_demo

- path tried
- what was useful
- what was confusing
- permission to count publicly

### confirm_external_run

- command or URL used
- observed result
- environment
- permission to count public run evidence

### submit_reproducible_issue

- expected behavior
- actual behavior
- reproduction steps
- safe logs or screenshots

### submit_business_case

- anonymized workflow
- data-quality problem
- business impact
- project evidence mapping
- permission to count anonymized case

### submit_ai_engineer_review

- inspected implementation paths
- strongest AI-agent signal
- weakest AI-agent gap
- permission to count public AI Engineer feedback

### star_or_fork_if_useful

- public GitHub star count above zero
- no paid, traded, or fake engagement

## Current Outcome Status

| Metric | Current Count | Resume Status | Blocked Reason |
| --- | ---: | --- | --- |
| confirmed_external_users | 0 | `not_claimable_yet` | Needs a non-owner public reviewer issue that passes the external evidence gate. |
| external_feedback_items | 0 | `not_claimable_yet` | Needs accepted public feedback with permission to count and non-placeholder comments. |
| reproducible_feedback_items | 0 | `not_claimable_yet` | Needs reviewer-submitted command, URL, and observed-result evidence. |
| business_case_feedback_items | 0 | `not_claimable_yet` | Needs anonymized business-case issue evidence with explicit permission to count. |
| ai_engineer_review_items | 0 | `not_claimable_yet` | Needs a non-owner AI Engineer review issue with inspected paths and permission to count. |
| github_stars | 0 | `not_claimable_yet` | Needs public GitHub stars above zero; never buy, trade, or fake stars. |

## Resume-Safe Summary

Published a CI-verified reviewer submission hub with 6 public submission paths, 6 tracked outcome metrics, 23 required evidence fields, and zero current outcome claims upgraded.

## Not Claimed

- No external users are claimed while confirmed_external_users is zero.
- No customer feedback is claimed while external_feedback_items is zero.
- No real business impact is claimed while business_case_feedback_items is zero.
- No GitHub star growth is claimed while github_stars is zero.
- GitHub traffic is treated as repository interest, not as users.
