# Resume Outcome Conversion Plan

Turn blocked resume outcomes into a concrete conversion plan: one next action, one reviewer profile, one evidence gate, and one copy-ready message per future outcome claim.

## Summary

| Metric | Value |
| --- | ---: |
| Claimable now | 6 |
| Blocked outcomes | 6 |
| Conversion rows | 6 |

One-click evidence page: [https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html](https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html)

## Conversion Queue

| Metric | Current | Required | Remaining | Reviewer Profile | Channel | Submission |
| --- | ---: | ---: | ---: | --- | --- | --- |
| confirmed_external_users | 0 | 1 | 1 | reviewer who opened the demo or ran the repo | class Discord, friend DM, or club Slack | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) |
| external_feedback_items | 0 | 3 | 3 | UC Davis data science peer | LinkedIn DM, class Discord, or project channel | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) |
| reproducible_feedback_items | 0 | 1 | 1 | engineer comfortable with Docker or local setup | GitHub issue comment, Discord, or DM to a developer comfortable with Docker | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md) |
| business_case_feedback_items | 0 | 1 | 1 | data analyst or analytics student | email or in-person ask to someone who has handled messy operational data | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) |
| ai_engineer_review_items | 0 | 1 | 1 | AI engineer, mentor, or ML systems reviewer | LinkedIn DM or mentor email | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| github_stars | 0 | 5 | 5 | developer or data/AI peer who finds the project useful | GitHub README, public demo, class Discord, or LinkedIn project post | [submit](https://github.com/sunnnn2005/data-quality-agent) |

## Copy-Ready Asks

### confirmed_external_users

Evidence gate: A non-owner public GitHub issue confirms the path tried and includes permission to count.

Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/23. The ask is: Confirm the exact path used and whether the result was understandable. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

### external_feedback_items

Evidence gate: Public feedback issues include role, path tried, outcome, improvement request, and permission.

Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/20. The ask is: Try the public demo and report one confusing or useful workflow detail. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

### reproducible_feedback_items

Evidence gate: A public issue includes command or URL evidence, expected result, actual result, and environment.

Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/22. The ask is: Run the local replay path and confirm whether the report is reproducible. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

### business_case_feedback_items

Evidence gate: A public business-case issue includes anonymized schema, quality failure, impact, and reviewer role.

Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/24. The ask is: Submit one anonymized data-quality problem this agent should handle. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

### ai_engineer_review_items

Evidence gate: A non-owner public review issue lists inspected paths and grants permission to count.

Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

### github_stars

Evidence gate: GitHub public star count and docs/adoption-metrics.json both show at least 5 stars.

Counts only after: The public GitHub stargazer count reaches the threshold organically.

```text
I published a local-first LLM data-quality agent with a public demo, tests, tool-calling evidence, and conservative outcome tracking. If the project is genuinely useful after you inspect it, and only if the project is useful to you, a GitHub star would help signal public interest: https://github.com/sunnnn2005/data-quality-agent
```

## Execution Rule

Do not upgrade a resume line from blocked to claimable until the public evidence gate is satisfied by a non-owner issue, accepted public metric, or public GitHub count. Outreach attempts alone do not count.

## Resume-Safe Summary

Published a conversion plan for 6 blocked resume outcomes with one-click evidence routing, copy-ready reviewer asks, public issue gates, and zero upgraded outcome claims until evidence is accepted.

## Not Claimed

- external users
- external feedback
- real business validation
- external AI Engineer review
- GitHub stars
