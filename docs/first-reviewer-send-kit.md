# First Reviewer Send Kit

This generated kit gives the first concrete reviewer send needed to move from public launch to real outreach.

## First Send

| Field | Value |
| --- | --- |
| Selected metric | `ai_engineer_review_items` |
| Reviewer profile | AI engineer, mentor, or ML systems reviewer |
| Recommended channel | LinkedIn DM or mentor email |
| Status-board slot ID | `review_slot_07` |
| Current status | `not_sent` |
| Public issue | [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26) |
| Submission URL | [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| Entry URL | [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md) |

## Copy-Ready Message

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it.
```

## Follow-Up

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/26. A short observed-result note is enough, and private data should not be included.
```

## Record After Sending

Run this only after the message is actually sent to a real person:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

## Expected Pipeline Change

| Metric | Before | After Recording One Real Send |
| --- | ---: | ---: |
| Sent reviewer messages | 0 | 1 |
| Claimable resume metrics | 0 | 0 |

## Counting Boundary

Recording a sent outreach event proves distribution execution only. It does not count as an external user, accepted feedback, AI Engineer review, business validation, or GitHub star.

## Resume-Safe Summary

Prepared one first AI Engineer reviewer send with a copy-ready message, public issue URL, and state-aware recording guidance while preserving zero claimable resume outcomes.
