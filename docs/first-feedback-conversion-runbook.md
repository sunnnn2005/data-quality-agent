# First Feedback Conversion Runbook

Convert the first real reviewer contact into a public evidence item that can unlock stronger resume outcome wording only after the evidence gate accepts it.

## Shareable Review Card

[https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html](https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html)

## First Send

- Slot: `slot_07_ai_engineer_review`
- Target metric: `ai_engineer_review_items`
- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Channel: LinkedIn DM or mentor email

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

## Five-Step Conversion Workflow

### 1. Send the first AI Engineer review ask

- Action: Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
- Counts as resume outcome: `False`
- Why: Sending a message creates outreach trace only; it does not prove feedback, use, or review quality.
- Record command: `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<private-label>" --channel-used "<LinkedIn|email|Discord>" --note "Sent first external review card; no public evidence yet."`


### 2. Ask the reviewer to choose one public path

- Action: https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html
- Counts as resume outcome: `False`
- Why: Opening the card is not enough; the reviewer must submit public, permissioned evidence.


### 3. Collect the first public GitHub issue

- Action: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md
- Counts as resume outcome: `False`
- Why: A submitted issue still needs to pass the evidence gate before it upgrades a metric.


### 4. Run the evidence gate and refresh outcome artifacts

- Action: python scripts/build_external_reviewer_evidence_gate.py && python scripts/build_accepted_evidence_rollup.py && python scripts/build_resume_outcome_metrics.py && python scripts/build_resume_claim_materializer.py
- Counts as resume outcome: `False`
- Why: Deterministic scripts decide whether the public issue is countable; the owner does not manually inflate metrics.


### 5. Use only materialized resume wording

- Action: docs/resume-claim-materializer.md
- Counts as resume outcome: `True`
- Why: The final resume line is allowed only after the materializer sees accepted public evidence.


## First Unlock Options

| Metric | Current | Required | Submission | Future Resume Line |
| --- | ---: | ---: | --- | --- |
| ai_engineer_review_items | 0 | 1 | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) | Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail. |
| confirmed_external_users | 0 | 1 | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md) | Validated the data-quality LLM agent with 1 external reviewer who ran the public demo or local repo. |
| external_feedback_items | 0 | 3 | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) | Collected 3 public reviewer feedback items and converted them into prioritized product fixes. |

## Current Counts

| Metric | Current Count |
| --- | ---: |
| `ai_engineer_review_items` | 0 |
| `confirmed_external_users` | 0 |
| `external_feedback_items` | 0 |

## Resume-Safe Summary

Published a first-feedback conversion runbook that turns one reviewer message into a 5-step evidence workflow, 3 possible public metric unlocks, and zero resume upgrades until a non-owner issue passes the gate.

## Not Claimed

- message sent
- accepted review
- confirmed external user
- external feedback
- GitHub stars
- production adoption
