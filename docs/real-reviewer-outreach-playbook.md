# Real Reviewer Outreach Playbook

Turn the zero-outcome baseline into a concrete manual outreach plan for getting real, non-owner, permissioned public evidence that can eventually unlock stronger resume claims.

## Current Baseline

| Metric | Count |
| --- | ---: |
| Accepted public evidence | 0 |
| External feedback items | 0 |
| Confirmed external users | 0 |
| AI Engineer review items | 0 |
| GitHub stars claimable | 0 |

## First Action

- Metric: `ai_engineer_review_items`
- Slot: `review_slot_07`
- Reviewer profile: AI engineer, mentor, or ML systems reviewer

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

## Today Completion Definition

- Choose one real person from the first contact pool.
- Send the copy-ready message outside the repo.
- Record only the sent event with scripts/record_reviewer_outreach_event.py.
- Do not change user, feedback, star, or business-impact counts until public evidence is accepted.

## Outreach Steps

### 1. UC Davis technical mentor

- Target metric: `ai_engineer_review_items`
- Who to find: TA, professor office-hour contact, AI/ML club officer, or advanced CS/data science student
- Suggested channel: LinkedIn, email, Discord, or in-person follow-up
- Status-board slot: `review_slot_07`
- Why it matters: This is the strongest first evidence for an AI Engineer Intern resume because the reviewer can inspect architecture, tool calling, and guardrails.
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

Record after a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<private label or public handle>" --channel-used "LinkedIn, email, Discord, or in-person follow-up" --note "Sent ai_engineer_review_items reviewer ask from real outreach playbook"
```

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 2. Student developer peer

- Target metric: `confirmed_external_users`
- Who to find: classmate or hackathon peer who can open the public demo and submit a short public run issue
- Suggested channel: class Discord, club Slack, or direct message
- Status-board slot: `review_slot_04`
- Why it matters: One confirmed non-owner run turns the project from only self-published into externally tried.
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/23](https://github.com/sunnnn2005/data-quality-agent/issues/23)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_04 --status sent --reviewer-contact "<private label or public handle>" --channel-used "class Discord, club Slack, or direct message" --note "Sent confirmed_external_users reviewer ask from real outreach playbook"
```

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 3. Developer comfortable with Docker

- Target metric: `reproducible_feedback_items`
- Who to find: peer who can run docker compose or inspect the local PostgreSQL replay path
- Suggested channel: GitHub, Discord, or direct message
- Status-board slot: `review_slot_03`
- Why it matters: Reproducible run evidence is stronger than a casual demo view and supports engineering credibility.
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/22](https://github.com/sunnnn2005/data-quality-agent/issues/22)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_03 --status sent --reviewer-contact "<private label or public handle>" --channel-used "GitHub, Discord, or direct message" --note "Sent reproducible_feedback_items reviewer ask from real outreach playbook"
```

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 4. Operations or spreadsheet-heavy user

- Target metric: `business_case_feedback_items`
- Who to find: student org treasurer, tutoring coordinator, small-business operator, or anyone who has cleaned messy CSVs
- Suggested channel: email, LinkedIn, or in-person ask
- Status-board slot: `review_slot_05`
- Why it matters: Business-case feedback is the closest honest substitute for enterprise impact before a real company pilot exists.
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/24](https://github.com/sunnnn2005/data-quality-agent/issues/24)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_05 --status sent --reviewer-contact "<private label or public handle>" --channel-used "email, LinkedIn, or in-person ask" --note "Sent business_case_feedback_items reviewer ask from real outreach playbook"
```

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### 5. General product reviewer

- Target metric: `external_feedback_items`
- Who to find: friend, classmate, or club member who can say what was useful, confusing, or broken
- Suggested channel: direct message or class group
- Status-board slot: `review_slot_01`
- Why it matters: Specific product feedback creates a real iteration loop without pretending there are users yet.
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/20](https://github.com/sunnnn2005/data-quality-agent/issues/20)
- Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Record after a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_01 --status sent --reviewer-contact "<private label or public handle>" --channel-used "direct message or class group" --note "Sent external_feedback_items reviewer ask from real outreach playbook"
```

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

## Counting Policy

A sent message is only distribution evidence. Resume outcomes increase only when a non-owner public GitHub issue includes permission to count, contains no private data, and passes the evidence gate.

## Resume-Safe Summary

Added a real reviewer outreach playbook with 5 contact pools, 5 evidence targets, copy-ready asks, recording commands, and strict counting boundaries for converting future external reviews into resume-safe outcome claims.

## Not Claimed

- message sent
- external user
- external feedback
- AI Engineer review
- business pilot
- GitHub star growth
