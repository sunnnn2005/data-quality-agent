# Contributor Conversion Kit

Convert public repo visibility into real, resume-safe outcome evidence by routing reviewers through specific contribution, replay, review, and ethical star paths.

## Current Public Counts

| Metric | Value |
| --- | ---: |
| Stars | 0 |
| Forks | 1 |
| Confirmed External Users | 0 |
| External Feedback Items | 0 |
| Reproducible Feedback Items | 0 |
| Ai Engineer Review Items | 0 |
| Business Case Feedback Items | 0 |
| Feature Feedback Items Excluded From External Claims | 8 |

## Conversion Paths

| Path | Target Signal | Best Reviewer | Entrypoint | Evidence Gate |
| --- | --- | --- | --- | --- |
| demo_feedback_review | external_feedback_items | classmate, club member, or engineer who can try the public demo | [open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md) | public non-owner issue using demo_feedback.md and explicit permission to count |
| business_data_replay | reproducible_feedback_items | data analyst, data engineer, or operations teammate with an anonymized CSV workflow | [open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md) | public non-owner issue using business_data_replay.md with no raw private data |
| ai_engineer_review | ai_engineer_review_items | AI engineer, ML engineer, or senior CS student familiar with LLM agents | [open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) | public non-owner issue using ai_engineer_review.md with permission to count |
| business_case_review | business_case_feedback_items | someone who has worked with support, billing, ecommerce, or operations data | [open](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) | public non-owner issue using business_case_review.md and explicit business-case feedback |
| ethical_star_or_fork | github_stars | developer who inspected the repo, demo, tests, or Docker run and genuinely wants to follow it | [open](https://github.com/sunnnn2005/data-quality-agent) | public GitHub stargazer or fork count; no paid, traded, or fake engagement |

## Copy-Ready Asks

### demo_feedback_review

Counts only after: The accepted evidence gate increments external_feedback_items.

```text
I published a local-first LLM data-quality agent with a public demo and evidence-backed reports. Could you spend 8-10 minutes running the demo and leave feedback through this issue form? Please only grant permission to count the review publicly if you are comfortable with that.
```

### business_data_replay

Counts only after: The accepted evidence gate confirms a reproducible replay without sensitive data.

```text
I am validating whether this agent is useful on realistic business data. If you have a small anonymized CSV shape, could you run the replay path and submit what failed, what was useful, and whether the evidence-backed report matched the workflow?
```

### ai_engineer_review

Counts only after: The accepted evidence gate confirms an external AI-engineering review.

```text
I am trying to make this project strong enough for AI Engineer internship interviews. Could you review the LLM tool-calling loop, guardrails, structured output, and eval artifacts, then leave specific technical feedback through the AI Engineer review issue?
```

### business_case_review

Counts only after: The accepted evidence gate increments business_case_feedback_items.

```text
Could you review the support-operations case study and tell me whether the data-quality failures, root-cause hypotheses, and owner handoffs feel realistic for an actual business workflow?
```

### ethical_star_or_fork

Counts only after: The public GitHub count changes organically.

```text
If you inspect the repo or demo and genuinely find the project useful, a GitHub star would help signal public interest. No pressure, and please do not star it unless it is actually useful to you.
```

## Counting Rules

- public non-owner issue
- explicit permission to count publicly
- accepted evidence gate
- public GitHub star or fork count
- no private business data or secrets

## Resume-Safe Summary

Published a contributor conversion kit with 5 public contributor paths, 5 evidence gates, 0 contributor-claimable outcomes, and explicit rules for turning reviews, replays, AI-engineering feedback, and organic GitHub stars into future resume-safe metrics.

## Not Claimed

- external contributors
- external users
- customer feedback
- production adoption
- GitHub stars beyond the current public count
- business impact validated by a company
