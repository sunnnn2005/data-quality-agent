# First Reviewer Handoff

This generated handoff picks the single next reviewer ask most likely to unlock an honest AI Engineer resume signal.

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `ai_engineer_review_items` |
| Current count | 0 |
| Required count | 1 |
| Status | `not_sent` |
| Resume status | `not_claimable_until_public_issue_is_accepted` |

## Who To Ask

- Reviewer profile: AI engineer, mentor, or ML systems reviewer
- Recommended channel: LinkedIn DM or mentor email
- Who to choose: Choose one AI/ML engineer, professor, mentor, or advanced student who can inspect agent architecture.

## Links

- Public slot: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Reviewer entry page: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission form: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

## Copy-Ready Message

```text
Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes submitting this review form: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. The public tracking slot is https://github.com/sunnnn2005/data-quality-agent/issues/26. The ask is: Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility. Please create/submit your own public review issue, share only public, non-private details, and include the permission sentence in the issue if you are comfortable letting me count it. Shortest path if you do not want to read every doc: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.
```

## Follow-Up

```text
Quick follow-up on the Data Quality Agent review request. The public slot is still here: https://github.com/sunnnn2005/data-quality-agent/issues/26. A short observed-result note is enough, and private data should not be included.
```

## Required Public Evidence

- implementation paths inspected
- strongest AI-agent signal
- least credible gap
- permission sentence if the reviewer allows the evidence to count

## Completion Fields

- `reviewer_contact`
- `sent_at`
- `channel_used`
- `public_issue_or_response_url`
- `permission_sentence_present`
- `no_private_data_confirmed`

## After You Send

Run this only after the message is sent to a real reviewer:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

Expected pipeline change after recording one real send:

| Metric | Before | After recording one real send |
| --- | ---: | ---: |
| Sent reviewer messages | 0 | 1 |
| Claimable resume metrics | 0 | 0 |

Recording a sent outreach event proves distribution execution only. It does not count as an external user, accepted feedback, AI Engineer review, business validation, or GitHub star.

## Acceptance Gate

A non-owner public review issue lists inspected paths and grants permission to count.

Manual rule: Do not increase any outcome metric until a non-owner public GitHub issue includes permission, contains no private data, and passes the external reviewer evidence gate.

## Future Resume Line

This line is locked until the public evidence gate passes:

```text
Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail.
```

## Not Claimed

- message sent
- reviewer replied
- accepted AI Engineer review
- external user
- resume outcome upgrade

## Resume-Safe Summary

Prepared a first-reviewer handoff for the highest-priority AI Engineer review path, including copy-ready outreach, required public evidence fields, acceptance gate, and future resume wording while preserving zero sent outreach and zero accepted reviews.
