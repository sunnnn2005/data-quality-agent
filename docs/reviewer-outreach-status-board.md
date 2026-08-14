# Reviewer Outreach Status Board

This generated board tracks reviewer outreach execution without claiming results that have not happened.

## Purpose

Track real reviewer outreach from planned to sent, replied, public issue, and accepted evidence without converting private outreach into resume claims.

## Status Stages

| Stage | Meaning | Resume Countable |
| --- | --- | --- |
| `not_sent` | The outreach slot exists, but no real reviewer has been contacted. | False |
| `sent` | A message was actually sent to a real reviewer. | False |
| `replied_private` | The reviewer replied privately; private replies are notes only and do not count as public evidence. | False |
| `public_issue_submitted` | A reviewer submitted a public, redacted GitHub issue with permission to count it. | False |
| `accepted_evidence` | A non-owner public GitHub issue passed the evidence gate and can update outcome metrics. | True |

## Outreach Slots

| Slot | Reviewer Segment | Counts Toward | Status |
| --- | --- | --- | --- |
| review_slot_01 | UC Davis data science peer | `external_feedback_items` | `not_sent` |
| review_slot_02 | student software engineer peer | `external_feedback_items` | `not_sent` |
| review_slot_03 | engineer comfortable with Docker or local setup | `reproducible_feedback_items` | `not_sent` |
| review_slot_04 | reviewer who tried demo or local repo | `confirmed_external_users` | `not_sent` |
| review_slot_05 | data analyst or analytics student | `business_case_feedback_items` | `not_sent` |
| review_slot_06 | small-business operator or operations teammate | `business_case_feedback_items` | `not_sent` |
| review_slot_07 | AI engineer, mentor, or ML systems reviewer | `ai_engineer_review_items` | `not_sent` |
| review_slot_08 | open-source maintainer or GitHub contributor | `external_feedback_items` | `not_sent` |

## Recorded Events

| Metric | Count |
| --- | ---: |
| Recorded outreach events | 0 |
| Sent messages | 0 |
| Replies or public submissions | 0 |
| Public issues submitted | 0 |
| Accepted evidence | 0 |

## Current Outcome Counts

| Metric | Count |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |
| Ai Engineer Review Items | 0 |

## Resume Upgrade Rules

- No resume outcome is upgraded until a public issue URL exists.
- Private replies are useful notes but never public evidence.
- Evidence must include permission to count the reviewer submission publicly.
- Self-authored issues and owner-authored planning issues are excluded.
- Accepted evidence updates resume-outcome-metrics only after the evidence gate passes.

## Resume-Safe Summary

Published a CI-verified outreach status board tracking 8 reviewer slots across 5 status stages, 5 evidence goals, 0 recorded outreach events, and zero accepted-evidence or resume-upgrade claims.
