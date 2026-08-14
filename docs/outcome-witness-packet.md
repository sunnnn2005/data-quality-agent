# Outcome Witness Packet

This generated packet turns outreach into short, public reviewer tasks with explicit evidence gates.

## Purpose

Give one external reviewer a short, public, permissioned task card that can become resume-countable only after the evidence gate accepts the submitted GitHub issue.

## Current Public Counts

| Metric | Count |
| --- | ---: |
| `confirmed_external_users` | 0 |
| `external_feedback_items` | 0 |
| `reproducible_feedback_items` | 0 |
| `business_case_feedback_items` | 0 |
| `ai_engineer_review_items` | 0 |

## Witness Cards

### ai_engineer_review_items

Prompt: Inspect the public AI Engineer evidence and tell me whether this looks like a real LLM agent project.

- Time: 12 minutes
- Review: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submit: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Permission sentence: `I give permission for this public issue to be counted as project review evidence.`
- No-private-data sentence: `I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.`
- First unlock requirement: One non-owner `ai-engineer-review` issue with inspected paths, no-private-data checkbox, and permission to count.
- Resume upgrade after acceptance: AI Engineer review bullet can materialize after one accepted non-owner public issue.

Required evidence:

- inspected implementation paths
- strongest AI-agent signal
- weakest AI-agent gap
- permission to count public AI Engineer feedback

### confirmed_external_users

Prompt: Open the public demo or run path and submit what you actually observed.

- Time: 8 minutes
- Review: [https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html](https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html)
- Submit: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md)
- Permission sentence: `I give permission for this public issue to be counted as project review evidence.`
- No-private-data sentence: `I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.`
- First unlock requirement: One non-owner external run issue with a runnable path, observed result, command or URL evidence, and permission to count.
- Resume upgrade after acceptance: External-user validation bullet can materialize after one accepted public run issue.

Required evidence:

- command or URL used
- observed result
- environment
- permission to count public run evidence

### external_feedback_items

Prompt: Try one visible workflow and submit one useful improvement or confusing moment.

- Time: 5 minutes
- Review: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submit: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Permission sentence: `I give permission for this public issue to be counted as project review evidence.`
- No-private-data sentence: `I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.`
- First unlock requirement: Counts only after a non-owner public issue grants permission and passes the evidence gate.
- Resume upgrade after acceptance: Feedback bullet can materialize after one accepted non-owner public feedback issue.

Required evidence:

- path tried
- what was useful
- what was confusing
- permission to count publicly

### business_case_feedback_items

Prompt: Share one anonymized data-quality workflow where a wrong result would affect a business decision.

- Time: 12 minutes
- Review: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-case-intake.md)
- Submit: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Permission sentence: `I give permission for this public issue to be counted as project review evidence.`
- No-private-data sentence: `I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.`
- First unlock requirement: One anonymized business-case review issue with workflow context, impact, fields, project evidence mapping, and permission to count.
- Resume upgrade after acceptance: Business-case bullet can materialize after one accepted anonymized business-case issue.

Required evidence:

- anonymized workflow
- data-quality problem
- business impact
- project evidence mapping
- permission to count anonymized case

### reproducible_feedback_items

Prompt: Run or replay one workflow and report the command, result, and what the agent caught or missed.

- Time: 10 minutes
- Review: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submit: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Permission sentence: `I give permission for this public issue to be counted as project review evidence.`
- No-private-data sentence: `I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.`
- First unlock requirement: Counts only when a non-owner submits a sanitized business-data replay issue with run evidence, agent trace summary, and permission to count publicly.
- Resume upgrade after acceptance: Reproducible-run bullet can materialize after one accepted replay issue with trace evidence.

Required evidence:

- command or endpoint used
- dataset shape
- report status and finding count
- selected tools shown in the agent trace
- what the agent caught or missed


## Not Claimed

- Witness cards are invitations, not users or feedback.
- No resume outcome is upgraded until a non-owner public GitHub issue passes the evidence gate.
- Private messages, private names, and private notes are not counted as public evidence.
- GitHub stars must come from public GitHub data and must never be bought, traded, or pressured.

## Resume-Safe Summary

Published an outcome witness packet with 5 reviewer task cards, 5 target outcome metrics, 22 required evidence fields, and zero resume outcome upgrades.
