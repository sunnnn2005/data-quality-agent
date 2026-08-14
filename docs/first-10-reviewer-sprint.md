# First 10 Reviewer Sprint

This generated sprint converts the project traction goal into 10 concrete external-review slots.

## Purpose

Turn the zero-user and zero-feedback baseline into a 10-slot reviewer sprint that can produce resume-safe public evidence without inflating current outcomes.

## Current Counts

| Metric | Current Count |
| --- | ---: |
| confirmed_external_users | 0 |
| external_feedback_items | 0 |
| reproducible_feedback_items | 0 |
| business_case_feedback_items | 0 |
| ai_engineer_review_items | 0 |
| github_stars | 0 |

## Target Slot Mix

| Metric | Slots |
| --- | ---: |
| ai_engineer_review_items | 1 |
| business_case_feedback_items | 2 |
| confirmed_external_users | 1 |
| external_feedback_items | 3 |
| github_stars | 1 |
| reproducible_feedback_items | 2 |

## Reviewer Slots

### slot_01_ds_peer_demo

- Reviewer profile: UC Davis data science peer
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Source task: `review_uc_davis_ds_peer_demo`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Ask: Try the public demo and report one confusing or useful workflow detail.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- demo path tried
- specific feedback
- permission to count publicly

### slot_02_swe_peer_demo

- Reviewer profile: student software engineer peer
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Source task: `review_student_swe_peer_demo`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Ask: Review setup clarity, README flow, and whether the project looks runnable.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- reviewed URL
- engineering feedback
- permission to count publicly

### slot_03_local_replay

- Reviewer profile: engineer comfortable with Docker or local setup
- Status: `not_sent`
- Target metric: `reproducible_feedback_items`
- Source task: `review_local_replay_engineer`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Ask: Run the local replay path and confirm whether the report is reproducible.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- command or URL used
- observed result
- environment summary

### slot_04_confirmed_use

- Reviewer profile: reviewer who opened the demo or ran the repo
- Status: `not_sent`
- Target metric: `confirmed_external_users`
- Source task: `review_confirmed_external_use`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Ask: Confirm the exact path used and whether the result was understandable.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- path used
- observed result
- permission to count as external use

### slot_05_data_analyst_case

- Reviewer profile: data analyst or analytics student
- Status: `not_sent`
- Target metric: `business_case_feedback_items`
- Source task: `review_data_analyst_business_case`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Ask: Submit one anonymized data-quality problem this agent should handle.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- anonymized workflow
- data-quality problem
- business impact

### slot_06_operator_case

- Reviewer profile: small-business operator or operations teammate
- Status: `not_sent`
- Target metric: `business_case_feedback_items`
- Source task: `review_operator_business_case`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Ask: Describe one workflow where bad data would cause a wrong operational decision.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- workflow affected
- decision risk
- permission to count anonymized case

### slot_07_ai_engineer_review

- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Status: `not_sent`
- Target metric: `ai_engineer_review_items`
- Source task: `review_ai_engineer_agent_readiness`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Ask: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- inspected implementation path
- AI-agent signal feedback
- permission to count publicly

### slot_08_open_source_review

- Reviewer profile: open-source maintainer or GitHub contributor
- Status: `not_sent`
- Target metric: `external_feedback_items`
- Source task: `review_open_source_maintainer`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Ask: Review whether a first-time contributor can understand and run the project.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- contributor-readiness feedback
- suggested improvement
- permission to count publicly

### slot_09_public_star_if_useful

- Reviewer profile: reviewer who finds the repo useful enough to save
- Status: `not_sent`
- Target metric: `github_stars`
- Source task: `star_or_fork_if_useful`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/stargazers](https://github.com/sunnnn2005/data-quality-agent/stargazers)
- Ask: Star or fork only if the project is genuinely useful; no traded or fake engagement.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- public GitHub star count above zero
- no paid or traded engagement

### slot_10_second_replay

- Reviewer profile: second technical reviewer for independent reproducibility
- Status: `not_sent`
- Target metric: `reproducible_feedback_items`
- Source task: `confirm_external_run`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/external-run-quickstart.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/external-run-quickstart.md)
- Submit evidence: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md)
- Ask: Run either the public demo or local replay and submit an independent observed result.
- Counts only after: A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission to count the evidence, and contains no private data.

Acceptance evidence:
- independent run path
- observed result
- permission to count public run evidence

## Success Thresholds

- 1 accepted confirmed external user issue
- 3 accepted external feedback issues
- 1 accepted reproducible run issue
- 1 accepted anonymized business case
- 1 accepted AI Engineer review issue
- 1 organic public GitHub star or fork

## Resume-Safe Summary

Published a CI-verified first-10 reviewer sprint with 10 public evidence slots, 6 target metrics, zero sent outreach, and zero upgraded outcome claims.

## Still Blocked

- users
- customer feedback
- business impact
- AI Engineer external review
- GitHub star growth
