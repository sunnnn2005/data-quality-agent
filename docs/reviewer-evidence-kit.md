# Reviewer Evidence Kit

This generated kit gives reviewers copy-ready instructions for producing public, countable evidence.

## Purpose

Give real reviewers a copy-ready, privacy-safe path for submitting public evidence that can upgrade resume outcome claims only after the evidence gate accepts it.

## Public Evidence Forms

| Evidence Type | Metric | Template | Minimum Required | Link |
| --- | --- | --- | ---: | --- |
| external_run | `confirmed_external_users` | `external_run_review.md` | 1 | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md) |
| demo_feedback | `external_feedback_items` | `demo_feedback.md` | 3 | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) |
| business_case | `business_case_feedback_items` | `business_case_review.md` | 1 | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) |
| ai_engineer_review | `ai_engineer_review_items` | `ai_engineer_review.md` | 1 | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| reproducible_bug | `reproducible_feedback_items` | `bug_report.md` | 1 | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md) |

## Copy-Ready Reviewer Prompts

### external_run

I ran the public demo/container/PostgreSQL replay, used this command or URL, observed this result, and I grant permission to count this as public external run evidence.

### demo_feedback

I tried the demo or docs, this part was useful, this part was confusing, and this feedback can be counted publicly without private data.

### business_case

Here is an anonymized workflow, data-quality problem, business impact, fields involved, and evidence mapping. I grant permission to count it as anonymized public business-case feedback.

### ai_engineer_review

I inspected the tool-calling, structured output, guardrails, trace, evaluation, and data connector evidence, and I grant permission to count this as AI Engineer project feedback.

### reproducible_bug

I found a reproducible issue, included expected result, actual result, environment, and reproduction steps, without private business data.

## Reviewer Script

1. Open the public demo or run the container/PostgreSQL replay.
2. Copy the matching prompt into the linked GitHub issue template.
3. Include only redacted schema, aggregate stats, command output, or screenshots with private data removed.
4. Check the explicit permission box only if the issue can be counted publicly.
5. Wait for the evidence gate to accept or reject the issue before any resume wording is upgraded.

## Current Counts

| Metric | Current value |
| --- | ---: |
| Confirmed External Users | 0 |
| External Feedback Items | 0 |
| Business Case Feedback Items | 0 |
| Ai Engineer Review Items | 0 |
| Reproducible Feedback Items | 0 |
| Accepted Business Impact Signals | 0 |

## Missing Evidence

| Stage | Current | Minimum | Remaining |
| --- | ---: | ---: | ---: |
| confirmed_external_feedback | 0 | 3 | 3 |
| confirmed_external_users | 0 | 1 | 1 |
| business_case_validated | 0 | 1 | 1 |
| reproducible_replay_confirmed | 0 | 2 | 2 |

## Resume-Safe Summary

Published a CI-verified reviewer evidence kit with 5 public issue templates, 5 copy-ready reviewer prompts, 5 privacy/permission steps, and zero current external outcome counts.

## Not Claimed

- external users
- customer feedback
- validated business impact
- production adoption
- GitHub stars beyond the current public count
