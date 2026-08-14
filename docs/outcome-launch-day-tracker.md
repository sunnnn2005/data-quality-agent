# Outcome Launch Day Tracker

Turn the public outcome evidence system into a day-of-execution tracker for collecting the first real resume-countable external result without inflating outreach into user, feedback, or star claims.

## Launch Day Goal

Send the first five reviewer requests, record only messages that were actually sent, and wait for public non-owner GitHub issues before upgrading any resume outcome.

## Current Baseline

| Metric | Value |
| --- | ---: |
| Planned sends | 5 |
| Recorded outreach events | 0 |
| Sent count | 0 |
| Accepted external evidence | 0 |
| Resume outcome claimable now | False |

## First Resume Unlock

- Target metric: `ai_engineer_review_items`
- Current count: 0
- Required count: 1
- Remaining to unlock: 1
- Request page: [https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html](https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html)
- Locked future line: Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail.

## Send These Today

### 1. slot_07_ai_engineer_review

- Target metric: `ai_engineer_review_items`
- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Who to choose: Choose one AI/ML engineer, professor, mentor, or advanced student who can inspect agent architecture.
- Channel: LinkedIn DM or mentor email
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- After send counts as: `outreach_execution_only`
- Resume countable now: `False`

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent ai_engineer_review_items request"
```

### 2. slot_04_confirmed_use

- Target metric: `confirmed_external_users`
- Reviewer profile: reviewer who opened the demo or ran the repo
- Who to choose: Choose one person who can simply open the demo and confirm what they tried.
- Channel: class Discord, friend DM, or club Slack
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/23](https://github.com/sunnnn2005/data-quality-agent/issues/23)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- After send counts as: `outreach_execution_only`
- Resume countable now: `False`

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_04 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "class Discord, friend DM, or club Slack" --note "Sent confirmed_external_users request"
```

### 3. slot_03_local_replay

- Target metric: `reproducible_feedback_items`
- Reviewer profile: engineer comfortable with Docker or local setup
- Who to choose: Choose one developer who can run a command or inspect the local replay instructions.
- Channel: GitHub issue comment, Discord, or DM to a developer comfortable with Docker
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/22](https://github.com/sunnnn2005/data-quality-agent/issues/22)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- After send counts as: `outreach_execution_only`
- Resume countable now: `False`

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_03 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "GitHub issue comment, Discord, or DM to a developer comfortable with Docker" --note "Sent reproducible_feedback_items request"
```

### 4. slot_05_data_analyst_case

- Target metric: `business_case_feedback_items`
- Reviewer profile: data analyst or analytics student
- Who to choose: Choose one person who has seen messy spreadsheets, support tickets, sales data, or operations data.
- Channel: email or in-person ask to someone who has handled messy operational data
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/24](https://github.com/sunnnn2005/data-quality-agent/issues/24)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- After send counts as: `outreach_execution_only`
- Resume countable now: `False`

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_05 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "email or in-person ask to someone who has handled messy operational data" --note "Sent business_case_feedback_items request"
```

### 5. slot_01_ds_peer_demo

- Target metric: `external_feedback_items`
- Reviewer profile: UC Davis data science peer
- Who to choose: Choose one peer who can leave specific product or README feedback.
- Channel: LinkedIn DM, class Discord, or project channel
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/20](https://github.com/sunnnn2005/data-quality-agent/issues/20)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- After send counts as: `outreach_execution_only`
- Resume countable now: `False`

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after sending:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_01 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM, class Discord, or project channel" --note "Sent external_feedback_items request"
```

## Post-Send Rules

- Record a sent event only after a real message is sent to a real reviewer.
- A sent event is distribution evidence, not usage, feedback, business impact, or a star.
- Ask reviewers to submit public redacted GitHub issues through the linked templates.
- Count a resume outcome only after a non-owner public issue passes the evidence gate.
- Do not include private data, customer rows, secrets, private emails, addresses, or API keys.

## Resume-Safe Summary

Published a launch-day outcome tracker with 5 concrete reviewer sends, 0 recorded outreach events, 0 accepted external evidence items, and explicit rules preventing outreach from being counted as users or feedback.

## Not Claimed

- No outreach is claimed as sent unless it is recorded in reviewer-outreach-events.json.
- No external users, feedback, business impact, production deployment, or GitHub stars are claimed.
- No resume line is unlocked until accepted evidence count for its metric reaches the threshold.
