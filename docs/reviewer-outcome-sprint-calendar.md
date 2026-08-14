# Reviewer Outcome Sprint Calendar

This generated calendar converts planned outreach into a one-week push for real, public outcome evidence.

## Summary

| Metric | Value |
| --- | ---: |
| Sprint days | 7 |
| Send days | 5 |
| Follow-up days | 2 |
| Target metrics | 5 |
| Completion criteria | 25 |
| Current sent messages | 0 |
| Current accepted evidence | 0 |
| Resume claim allowed now | False |

## Send Calendar

| Day | Target Metric | Reviewer Profile | Tracking Slot | Submission | Remaining Needed |
| --- | --- | --- | --- | --- | ---: |
| Day 1 | `ai_engineer_review_items` | AI engineer, mentor, or ML systems reviewer | [slot_07_ai_engineer_review](https://github.com/sunnnn2005/data-quality-agent/issues/26) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) | 1 |
| Day 2 | `confirmed_external_users` | reviewer who opened the demo or ran the repo | [slot_04_confirmed_use](https://github.com/sunnnn2005/data-quality-agent/issues/23) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) | 1 |
| Day 3 | `reproducible_feedback_items` | engineer comfortable with Docker or local setup | [slot_03_local_replay](https://github.com/sunnnn2005/data-quality-agent/issues/22) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md) | 1 |
| Day 4 | `business_case_feedback_items` | data analyst or analytics student | [slot_05_data_analyst_case](https://github.com/sunnnn2005/data-quality-agent/issues/24) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) | 1 |
| Day 5 | `external_feedback_items` | UC Davis data science peer | [slot_01_ds_peer_demo](https://github.com/sunnnn2005/data-quality-agent/issues/20) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) | 1 |

## Daily Details

### Day 1: ai_engineer_review_items

- Slot: `slot_07_ai_engineer_review`
- Sprint action: Ask one AI/ML systems reviewer to inspect the agent loop, guardrails, traces, and AI Engineer readiness evidence.
- Resume unlock after accepted evidence: first public AI Engineer review of tool calling, structured output, guardrails, and evidence quality
- Recommended channel: LinkedIn DM or mentor email

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

Completion criteria:
- Message sent through LinkedIn DM or mentor email.
- Reviewer submits their own public GitHub issue or response URL.
- Issue contains no private data, secrets, raw production rows, or customer identifiers.
- Issue includes explicit permission to count the evidence publicly.
- External reviewer evidence gate marks the issue accepted before any resume metric changes.

### Day 2: confirmed_external_users

- Slot: `slot_04_confirmed_use`
- Sprint action: Ask one peer to open the public demo or local quickstart and submit observed-result evidence.
- Resume unlock after accepted evidence: first confirmed non-owner external run of the public demo or repo
- Recommended channel: class Discord, friend DM, or club Slack

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Completion criteria:
- Message sent through class Discord, friend DM, or club Slack.
- Reviewer submits their own public GitHub issue or response URL.
- Issue contains no private data, secrets, raw production rows, or customer identifiers.
- Issue includes explicit permission to count the evidence publicly.
- External reviewer evidence gate marks the issue accepted before any resume metric changes.

### Day 3: reproducible_feedback_items

- Slot: `slot_03_local_replay`
- Sprint action: Ask one developer to run the Docker/local replay path and report whether the result is reproducible.
- Resume unlock after accepted evidence: first reproducible local replay from a non-owner reviewer
- Recommended channel: GitHub issue comment, Discord, or DM to a developer comfortable with Docker

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Completion criteria:
- Message sent through GitHub issue comment, Discord, or DM to a developer comfortable with Docker.
- Reviewer submits their own public GitHub issue or response URL.
- Issue contains no private data, secrets, raw production rows, or customer identifiers.
- Issue includes explicit permission to count the evidence publicly.
- External reviewer evidence gate marks the issue accepted before any resume metric changes.

### Day 4: business_case_feedback_items

- Slot: `slot_05_data_analyst_case`
- Sprint action: Ask one data/ops reviewer for an anonymized real data-quality scenario and business impact mapping.
- Resume unlock after accepted evidence: first anonymized business-case validation tied to a real workflow
- Recommended channel: email or in-person ask to someone who has handled messy operational data

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Completion criteria:
- Message sent through email or in-person ask to someone who has handled messy operational data.
- Reviewer submits their own public GitHub issue or response URL.
- Issue contains no private data, secrets, raw production rows, or customer identifiers.
- Issue includes explicit permission to count the evidence publicly.
- External reviewer evidence gate marks the issue accepted before any resume metric changes.

### Day 5: external_feedback_items

- Slot: `slot_01_ds_peer_demo`
- Sprint action: Ask one peer to leave product or README feedback after trying the demo.
- Resume unlock after accepted evidence: first specific external product feedback item
- Recommended channel: LinkedIn DM, class Discord, or project channel

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Completion criteria:
- Message sent through LinkedIn DM, class Discord, or project channel.
- Reviewer submits their own public GitHub issue or response URL.
- Issue contains no private data, secrets, raw production rows, or customer identifiers.
- Issue includes explicit permission to count the evidence publicly.
- External reviewer evidence gate marks the issue accepted before any resume metric changes.


## Follow-Up Days

- Day 6: Follow up with any reviewer who was contacted but has not submitted a public issue. Success condition: At least one reviewer submits a public issue URL; still not claimable until the gate accepts it.
- Day 7: Run the external reviewer evidence gate and update resume outcome metrics only for accepted public issues. Success condition: Accepted evidence count is greater than zero; otherwise keep all user/feedback/business-impact claims blocked.

## Execution Commands

- `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact '<name-or-handle>' --channel-used '<LinkedIn|email|Discord>'`
- `python scripts/build_external_reviewer_evidence_gate.py`
- `python scripts/verify_outcome_evidence.py`

## Resume-Safe Summary

Published a seven-day reviewer outcome sprint calendar with 5 prioritized sends, 5 target metrics, 25 completion criteria, 0 sent messages, 0 accepted evidence, and no upgraded resume claims.

## Not Claimed

- The calendar itself does not count as users, feedback, business impact, stars, or accepted model runs.
- Sent outreach and private replies are tracked but not resume-countable.
- Only non-owner public GitHub issues accepted by the evidence gate can unlock outcome wording.
