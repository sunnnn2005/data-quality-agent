# First Outcome Evidence Request

Create one public, sendable request for the first resume-countable external outcome: an AI Engineer review submitted by a non-owner reviewer through a public GitHub issue.

Public page: [https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html](https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html)

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `ai_engineer_review_items` |
| Current count | 0 |
| Required count | 1 |
| Remaining to unlock | 1 |
| Accepted external evidence | 0 |
| Resume status | `first_external_outcome_request_ready_not_claimable` |

## Who To Ask

- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Recommended channel: LinkedIn DM or mentor email
- Who to choose: Choose one AI/ML engineer, professor, mentor, or advanced student who can inspect agent architecture.
- Time requested: 12 minutes

## Reviewer Links

- Start page: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission form: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Public tracking issue: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)

## Copy-Ready Message

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

## Follow-Up

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/26. A short observed-result note is enough, and private data should not be included.
```

## Inspection Targets

- `app/tool_agent.py`: shows LLM-driven tool choice, loop state, and tool-result feedback
- `app/llm.py`: shows structured model calls, fallback handling, and output validation boundaries
- `app/models.py`: shows structured request and response schemas used by the API and agent
- `app/postgres_adapter.py`: shows read-only PostgreSQL access for realistic tabular business data
- `app/verifier.py`: shows deterministic checks that keep LLM conclusions tied to evidence
- `evals/scenarios.jsonl`: shows the project is evaluated against repeatable agent behavior cases

## Review Prompts

- Does the model choose tools from evidence, or does the code force a fixed workflow?
- Are tool outputs fed back into the agent before the final report is produced?
- Are findings, hypotheses, recommendations, evidence, confidence, and limitations separated?
- Where would prompt injection, sensitive data, or unsupported claims be blocked?
- What one change would make this more credible for an AI Engineer Intern resume?

## Required Public Evidence Fields

- implementation paths inspected
- strongest AI-agent signal
- least credible gap
- permission sentence if the reviewer allows the evidence to count

## Record After Sending

Run only after sending this to a real reviewer:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

## Acceptance Gate

A non-owner public review issue lists inspected paths and grants permission to count.

Manual rule: Do not increase any outcome metric until a non-owner public GitHub issue includes permission, contains no private data, and passes the external reviewer evidence gate.

## Future Resume Line

Locked until evidence passes:

```text
Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail.
```

## Counting Boundary

This request page is not evidence by itself. The outcome becomes resume-countable only after a non-owner public GitHub issue includes permission to count, no private data, inspected paths, and passes the external reviewer evidence gate.

## Not Claimed

- No AI Engineer review has been accepted yet.
- No reviewer message is recorded as sent yet.
- No external user, customer feedback, business impact, production deployment, or GitHub star is claimed.
- The future resume line is locked until the public evidence gate passes.

## Resume-Safe Summary

Published a first outcome evidence request for one AI Engineer reviewer, with 6 inspection targets, 5 review prompts, public submission links, required evidence fields, and a locked future resume line while preserving 0 accepted external evidence.
