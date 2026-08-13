# Reviewer Invitation Kit

This generated kit gives copy-ready messages for collecting public review evidence.

## Purpose

Provide copy-ready invitations that route real reviewers into public GitHub evidence, so feedback and usage claims can be upgraded only after public proof exists.

## Current Baseline

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |

## Public Review Request

Issue #17: [https://github.com/sunnnn2005/data-quality-agent/issues/17](https://github.com/sunnnn2005/data-quality-agent/issues/17)

Single public issue for sharing review paths and collecting the first external feedback item.

## Invitations

### classmate_quick_demo -> UC Davis classmate or student developer

- Minutes: 8
- Funnel stage: `visit_public_demo`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Could you spend 8 minutes trying my public Data Quality Agent demo and leave one GitHub issue with anything confusing, useful, or broken? I am tracking feedback publicly instead of claiming users without proof.

### technical_friend_local_replay -> student developer comfortable with local setup

- Minutes: 15
- Funnel stage: `run_local_replay`
- Counts toward: `reproducible_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)

Could you clone my Data Quality Agent repo, run the local replay path, and submit whether the result was reproducible? Please avoid raw private data; a short redacted run summary is enough.

### mentor_ai_engineer_review -> mentor, engineer, or AI/data practitioner

- Minutes: 12
- Funnel stage: `confirm_external_use`
- Counts toward: `confirmed_external_users`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

I am improving this project for AI Engineer internship applications. Could you review whether the tool-calling agent, safety boundaries, and evidence trail look credible, then leave a public note if you tried the demo or repo?

### data_practitioner_business_case -> data analyst, operations teammate, or small-business operator

- Minutes: 12
- Funnel stage: `submit_business_case`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)

Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness.

### club_or_discord_batch -> data science club, Discord, or Slack group

- Minutes: 10
- Funnel stage: `visit_public_demo`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

I am collecting public review evidence for a data-quality LLM agent project. If anyone can try the demo, please leave one GitHub issue with what worked, what broke, or what would make it more useful for real data workflows.

## Success Thresholds

| Threshold | Value |
| --- | ---: |
| First Feedback | 1 |
| Resume Feedback Signal | 3 |
| Confirmed External User Signal | 1 |
| Business Case Signal | 1 |

## Counting Rules

- Count only public GitHub issues or reproducible public notes.
- Count confirmed users only when the reviewer states they tried the demo or ran the repo.
- Do not count private messages, self-tests, application submissions, or unverifiable compliments.
- Do not collect raw customer data, secrets, addresses, emails, or production rows.

## Resume-Safe Summary

Published 5 copy-ready reviewer invitations tied to 4 public evidence paths and explicit zero-feedback baselines.

## Not Claimed

- external users
- customer feedback
- validated business impact
- production adoption
- GitHub stars beyond the current public count
