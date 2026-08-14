# Reviewer Send Queue

This generated queue turns planned outreach into the next concrete sends.

## Purpose

Convert the reviewer outreach backlog into the next five concrete sends needed to unlock real, public, resume-countable evidence without claiming sent outreach or external outcomes prematurely.

## Status

| Metric | Count |
| --- | ---: |
| Prioritized sends | 5 |
| Not sent | 5 |
| Sent | 0 |
| Accepted evidence | 0 |
| Scoreboard remaining evidence items | 7 |

One-click evidence page: [https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html](https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html)

## Target Metrics

- `ai_engineer_review_items`
- `business_case_feedback_items`
- `confirmed_external_users`
- `external_feedback_items`
- `reproducible_feedback_items`

## Manual Execution Rule

Only change an item from not_sent to sent after the maintainer sends it to a real person; only count an outcome after a non-owner public GitHub issue passes the evidence gate.

## Next Sends

### 1. slot_07_ai_engineer_review

- Target metric: `ai_engineer_review_items`
- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Recommended channel: LinkedIn DM or mentor email
- Who to choose: Choose one AI/ML engineer, professor, mentor, or advanced student who can inspect agent architecture.
- Status: `not_sent`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

Follow-up:

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/26. A short observed-result note is enough, and private data should not be included.
```

Completion fields:
- reviewer_contact
- sent_at
- channel_used
- public_issue_or_response_url
- permission_sentence_present
- no_private_data_confirmed

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 2. slot_04_confirmed_use

- Target metric: `confirmed_external_users`
- Reviewer profile: reviewer who opened the demo or ran the repo
- Recommended channel: class Discord, friend DM, or club Slack
- Who to choose: Choose one person who can simply open the demo and confirm what they tried.
- Status: `not_sent`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/23](https://github.com/sunnnn2005/data-quality-agent/issues/23)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Follow-up:

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/23. A short observed-result note is enough, and private data should not be included.
```

Completion fields:
- reviewer_contact
- sent_at
- channel_used
- public_issue_or_response_url
- permission_sentence_present
- no_private_data_confirmed

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 3. slot_03_local_replay

- Target metric: `reproducible_feedback_items`
- Reviewer profile: engineer comfortable with Docker or local setup
- Recommended channel: GitHub issue comment, Discord, or DM to a developer comfortable with Docker
- Who to choose: Choose one developer who can run a command or inspect the local replay instructions.
- Status: `not_sent`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/22](https://github.com/sunnnn2005/data-quality-agent/issues/22)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Follow-up:

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/22. A short observed-result note is enough, and private data should not be included.
```

Completion fields:
- reviewer_contact
- sent_at
- channel_used
- public_issue_or_response_url
- permission_sentence_present
- no_private_data_confirmed

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 4. slot_05_data_analyst_case

- Target metric: `business_case_feedback_items`
- Reviewer profile: data analyst or analytics student
- Recommended channel: email or in-person ask to someone who has handled messy operational data
- Who to choose: Choose one person who has seen messy spreadsheets, support tickets, sales data, or operations data.
- Status: `not_sent`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/24](https://github.com/sunnnn2005/data-quality-agent/issues/24)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Follow-up:

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/24. A short observed-result note is enough, and private data should not be included.
```

Completion fields:
- reviewer_contact
- sent_at
- channel_used
- public_issue_or_response_url
- permission_sentence_present
- no_private_data_confirmed

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 5. slot_01_ds_peer_demo

- Target metric: `external_feedback_items`
- Reviewer profile: UC Davis data science peer
- Recommended channel: LinkedIn DM, class Discord, or project channel
- Who to choose: Choose one peer who can leave specific product or README feedback.
- Status: `not_sent`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/20](https://github.com/sunnnn2005/data-quality-agent/issues/20)
- Entry URL: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Follow-up:

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/20. A short observed-result note is enough, and private data should not be included.
```

Completion fields:
- reviewer_contact
- sent_at
- channel_used
- public_issue_or_response_url
- permission_sentence_present
- no_private_data_confirmed

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

## Resume-Safe Summary

Published a reviewer send queue with 5 prioritized next sends across 5 target metrics while preserving zero sent outreach, zero accepted evidence, and zero upgraded resume outcome claims.
