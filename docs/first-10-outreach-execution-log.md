# First 10 Outreach Execution Log

This generated log turns the public reviewer issues into concrete manual outreach steps.

## Purpose

Turn the ten public reviewer issue entrypoints into a manual outreach execution log with copy-ready messages, follow-up timing, evidence fields, and conservative resume-counting boundaries.

## Current Counts

| Metric | Current Count |
| --- | ---: |
| ai_engineer_review_items | 0 |
| business_case_feedback_items | 0 |
| confirmed_external_users | 0 |
| external_feedback_items | 0 |
| github_stars | 0 |
| reproducible_feedback_items | 0 |

## Target Mix

| Metric | Target Slots |
| --- | ---: |
| ai_engineer_review_items | 1 |
| business_case_feedback_items | 2 |
| confirmed_external_users | 1 |
| external_feedback_items | 3 |
| github_stars | 1 |
| reproducible_feedback_items | 2 |

## Execution Baseline

| Metric | Count |
| --- | ---: |
| Public issue entrypoints | 10 |
| Copy-ready outreach messages | 10 |
| Sent outreach | 0 |
| Replies | 0 |
| Accepted evidence | 0 |

## Manual Update Rules

- Fill reviewer_contact only after choosing a real person to contact.
- Move status to sent only after the message is actually sent.
- Private replies are notes, not resume-countable evidence.
- Move accepted_evidence_url only after a non-owner public GitHub issue passes the evidence gate.
- Do not count paid, traded, or requested-only GitHub stars as project traction.

## Entries

### slot_01_ds_peer_demo

- Reviewer profile: UC Davis data science peer
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/20](https://github.com/sunnnn2005/data-quality-agent/issues/20)
- Entry URL: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- demo path tried
- specific feedback
- permission to count publicly

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_02_swe_peer_demo

- Reviewer profile: student software engineer peer
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/21](https://github.com/sunnnn2005/data-quality-agent/issues/21)
- Entry URL: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/21. The ask is: Review setup clarity, README flow, and whether the project looks runnable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- reviewed URL
- engineering feedback
- permission to count publicly

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_03_local_replay

- Reviewer profile: engineer comfortable with Docker or local setup
- Status: `not_sent`
- Target metric: `reproducible_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/22](https://github.com/sunnnn2005/data-quality-agent/issues/22)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- command or URL used
- observed result
- environment summary

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_04_confirmed_use

- Reviewer profile: reviewer who opened the demo or ran the repo
- Status: `not_sent`
- Target metric: `confirmed_external_users`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/23](https://github.com/sunnnn2005/data-quality-agent/issues/23)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- path used
- observed result
- permission to count as external use

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_05_data_analyst_case

- Reviewer profile: data analyst or analytics student
- Status: `not_sent`
- Target metric: `business_case_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/24](https://github.com/sunnnn2005/data-quality-agent/issues/24)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- anonymized workflow
- data-quality problem
- business impact

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_06_operator_case

- Reviewer profile: small-business operator or operations teammate
- Status: `not_sent`
- Target metric: `business_case_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/25](https://github.com/sunnnn2005/data-quality-agent/issues/25)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/25. The ask is: Describe one workflow where bad data would cause a wrong operational decision. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- workflow affected
- decision risk
- permission to count anonymized case

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_07_ai_engineer_review

- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Status: `not_sent`
- Target metric: `ai_engineer_review_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- inspected implementation path
- AI-agent signal feedback
- permission to count publicly

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_08_open_source_review

- Reviewer profile: open-source maintainer or GitHub contributor
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/27](https://github.com/sunnnn2005/data-quality-agent/issues/27)
- Entry URL: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/27. The ask is: Review whether a first-time contributor can understand and run the project. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- contributor-readiness feedback
- suggested improvement
- permission to count publicly

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_09_public_star_if_useful

- Reviewer profile: reviewer who finds the repo useful enough to save
- Status: `not_sent`
- Target metric: `github_stars`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/28](https://github.com/sunnnn2005/data-quality-agent/issues/28)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/stargazers. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/28. The ask is: Star or fork only if the project is genuinely useful; no traded or fake engagement. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- public GitHub star count above zero
- no paid or traded engagement

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

### slot_10_second_replay

- Reviewer profile: second technical reviewer for independent reproducibility
- Status: `not_sent`
- Target metric: `reproducible_feedback_items`
- Public issue: [https://github.com/sunnnn2005/data-quality-agent/issues/29](https://github.com/sunnnn2005/data-quality-agent/issues/29)
- Entry URL: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/external-run-quickstart.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/external-run-quickstart.md)
- Follow up after: 4 days

Copy-ready message:

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/29. The ask is: Run either the public demo or local replay and submit an independent observed result. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

Acceptance evidence:
- independent run path
- observed result
- permission to count public run evidence

Counting rule: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

## Resume-Safe Summary

Published a CI-verified first-10 outreach execution log with 10 copy-ready reviewer messages, 10 public issue entrypoints, zero sent outreach, and zero claimable external outcomes.
