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
| Ai Engineer Review Items | 0 |

## Public Review Request

Issue #17: [https://github.com/sunnnn2005/data-quality-agent/issues/17](https://github.com/sunnnn2005/data-quality-agent/issues/17)

Single public issue for sharing review paths and collecting the first external feedback item.

## One-Click Reviewer Share Card

**Review Data Quality Agent in 8-12 minutes**

- Primary: [https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html](https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html)
- Backup: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- One-click links: 4
- Target metrics: 4
- Accepted issue count: 0
- Claimable resume metric count: 0
- Record after sending: `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<name-or-private-label>" --channel-used "<LinkedIn|email|Discord|Slack|GitHub>" --note "Sent 8-12 minute one-click reviewer share card; no public evidence yet."`

Copy message:

> Could you spend 8-12 minutes reviewing my Data Quality Agent project? This one-click page lets you choose AI Engineer review, confirmed external use, product feedback, or an anonymized business-case note: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. Please submit only public, non-private evidence if you are comfortable.

Counting boundary: Opening a one-click issue link is not evidence by itself. A metric counts only after a non-owner submits the public issue, includes permission, includes no private data, and passes the evidence gate.

## Invitations

### classmate_quick_demo -> UC Davis classmate or student developer

- Minutes: 8
- Funnel stage: `visit_public_demo`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Could you spend 8 minutes trying my public Data Quality Agent demo and leave one GitHub issue with anything confusing, useful, or broken? The shortest route is the one-click evidence page: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I am tracking feedback publicly instead of claiming users without proof.

### technical_friend_local_replay -> student developer comfortable with local setup

- Minutes: 15
- Funnel stage: `run_local_replay`
- Counts toward: `reproducible_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)

Could you clone my Data Quality Agent repo, run the local replay path, and submit whether the result was reproducible? Please avoid raw private data; a short redacted run summary is enough.

### mentor_ai_engineer_review -> mentor, engineer, or AI/data practitioner

- Minutes: 12
- Funnel stage: `ai_engineer_review`
- Counts toward: `ai_engineer_review_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

I am improving this project for AI Engineer internship applications. Could you review whether the LLM tool-calling loop, business-data connector, structured output, guardrails, and evidence trail look credible enough for an intern interview? If yes, please use the one-click evidence page or leave a public AI Engineer review issue with the path you inspected: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

### confirmed_use_note -> reviewer who tried the demo or local repo

- Minutes: 5
- Funnel stage: `confirm_external_use`
- Counts toward: `confirmed_external_users`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

If you already tried the Data Quality Agent demo or ran the repo locally, could you leave a short public note saying what path you used and whether the result was understandable? The one-click evidence page has the confirmed-use form: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I only count confirmed external use when it is public and specific.

### data_practitioner_business_case -> data analyst, operations teammate, or small-business operator

- Minutes: 12
- Funnel stage: `submit_business_case`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)

Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness. The one-click evidence page is here: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

### club_or_discord_batch -> data science club, Discord, or Slack group

- Minutes: 10
- Funnel stage: `visit_public_demo`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

I am collecting public review evidence for a data-quality LLM agent project. If anyone can try the demo, please leave one GitHub issue with what worked, what broke, or what would make it more useful for real data workflows. Fastest path: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

## Success Thresholds

| Threshold | Value |
| --- | ---: |
| First Feedback | 1 |
| Resume Feedback Signal | 3 |
| Confirmed External User Signal | 1 |
| Business Case Signal | 1 |
| Ai Engineer Review Signal | 1 |

## Counting Rules

- Count only public GitHub issues or reproducible public notes.
- Count confirmed users only when the reviewer states they tried the demo or ran the repo.
- Do not count private messages, self-tests, application submissions, or unverifiable compliments.
- Do not collect raw customer data, secrets, addresses, emails, or production rows.
- Count AI Engineer reviews only when the reviewer names an inspected path or command and grants public permission.

## Resume-Safe Summary

Published 6 copy-ready reviewer invitations plus a short one-click reviewer share card tied to 5 public evidence paths, including AI Engineer review evidence, with explicit zero-feedback baselines.

## Not Claimed

- external users
- customer feedback
- validated business impact
- production adoption
- GitHub stars beyond the current public count
