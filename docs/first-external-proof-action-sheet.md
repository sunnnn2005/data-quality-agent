# First External Proof Action Sheet

Turn the first resume-outcome goal into a single action sheet for getting one real, public, non-owner evidence item without inflating users, feedback, stars, or business impact.

Public page: [https://sunnnn2005.github.io/data-quality-agent/first-external-proof-action-sheet.html](https://sunnnn2005.github.io/data-quality-agent/first-external-proof-action-sheet.html)

## Current Status

| Metric | Value |
| --- | ---: |
| Accepted external evidence | 0 |
| GitHub stars | 0 |
| Confirmed external users | 0 |
| Reviewer targets | 3 |
| Required success fields | 6 |

## Today Execution Order

1. Send rank 1 AI Engineer review request to one real reviewer.
2. Record only the sent outreach event after sending it.
3. If no response after two days, send the follow-up from first-outcome-evidence-request.md.
4. Do not update resume outcome metrics until the public issue passes the evidence gate.

## Reviewer Targets

| Rank | Reviewer | Target Metric | Start | Submit |
| ---: | --- | --- | --- | --- |
| 1 | AI/ML engineer, mentor, or advanced CS/data science peer | `ai_engineer_review_items` | [Start](https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| 2 | Classmate or student developer who can open the public demo | `external_feedback_items` | [Start](https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) |
| 3 | Developer comfortable with Docker or local API testing | `reproducible_feedback_items` | [Start](https://github.com/sunnnn2005/data-quality-agent) | [Submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md) |

## Copy-Ready Messages

### Rank 1: ai_engineer_review_items

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

### Rank 2: external_feedback_items

```text
Could you spend 2 minutes reviewing my Data Quality Agent demo? Open this card, inspect one result, and leave one concrete public note if you are comfortable: https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_01 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "class Discord, LinkedIn DM, or text" --note "Sent two-minute demo feedback request"
```

### Rank 3: reproducible_feedback_items

```text
Could you try a reproducible run of my Data Quality Agent and leave public redacted evidence only if it works for you? Start here: https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_03 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "GitHub, Discord, or LinkedIn DM" --note "Sent reproducible local replay request"
```

## Required Success Fields

- reviewer is not the repository owner
- public GitHub issue URL exists
- issue includes explicit permission to count
- issue confirms no private data was posted
- issue has one concrete observed result
- external reviewer evidence gate accepts it

## Resume Unlock After Acceptance

Locked until evidence passes:

```text
Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail.
```

## Counting Boundary

This action sheet and any sent message are distribution evidence only. Resume outcome metrics stay at zero until a non-owner public GitHub issue passes the external reviewer evidence gate.

## Not Claimed

- No external feedback is claimed by this action sheet.
- No confirmed user is claimed by this action sheet.
- No business impact is claimed by this action sheet.
- No GitHub star growth is claimed by this action sheet.
- No AI Engineer review is claimed until a non-owner issue passes the gate.

## Resume-Safe Summary

Published a first external proof action sheet with 3 prioritized reviewer targets, 3 copy-ready asks, 6 required success fields, recorder commands, and zero upgraded resume outcomes.
