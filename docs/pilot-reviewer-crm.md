# Pilot Reviewer CRM

This generated CRM turns the outcome-evidence goal into concrete reviewer leads and weekly execution.

## Purpose

Turn outcome evidence collection into an executable reviewer CRM without fabricating reviewer names, private replies, users, feedback, or GitHub stars.

## Target Counts

| Metric | Lead Count |
| --- | ---: |
| ai_engineer_review_items | 1 |
| business_case_feedback_items | 2 |
| confirmed_external_users | 1 |
| external_feedback_items | 3 |
| reproducible_feedback_items | 1 |

## Reviewer Leads

| Lead | Reviewer Segment | Target Metric | Priority | Status | Weekly Goal |
| --- | --- | --- | ---: | --- | --- |
| pilot_review_slot_07 | AI engineer, mentor, or ML systems reviewer | `ai_engineer_review_items` | 1 | `not_sent` | Get one technical reviewer to inspect the LLM agent loop and submit an AI Engineer review issue. |
| pilot_review_slot_04 | reviewer who tried demo or local repo | `confirmed_external_users` | 2 | `not_sent` | Get one non-owner reviewer to open the demo or run the repo and confirm the path publicly. |
| pilot_review_slot_03 | engineer comfortable with Docker or local setup | `reproducible_feedback_items` | 3 | `not_sent` | Get one reviewer to run the Docker/local path and paste command or URL evidence. |
| pilot_review_slot_05 | data analyst or analytics student | `business_case_feedback_items` | 4 | `not_sent` | Get one data or operations reviewer to map the demo to a real anonymized workflow. |
| pilot_review_slot_06 | small-business operator or operations teammate | `business_case_feedback_items` | 4 | `not_sent` | Get one data or operations reviewer to map the demo to a real anonymized workflow. |
| pilot_review_slot_01 | UC Davis data science peer | `external_feedback_items` | 5 | `not_sent` | Collect concrete product feedback from a peer reviewer without counting private replies. |
| pilot_review_slot_02 | student software engineer peer | `external_feedback_items` | 5 | `not_sent` | Collect concrete product feedback from a peer reviewer without counting private replies. |
| pilot_review_slot_08 | open-source maintainer or GitHub contributor | `external_feedback_items` | 5 | `not_sent` | Collect concrete product feedback from a peer reviewer without counting private replies. |

## Three-Week Sprint

| Week | Goal | Lead IDs | Success Metric |
| --- | --- | --- | --- |
| Week 1 | Send the top AI Engineer review ask and one confirmed-user ask. | pilot_review_slot_07, pilot_review_slot_04 | 2 real sends recorded, 0 resume outcomes upgraded until public evidence exists. |
| Week 2 | Follow up on week 1 and send reproducible-run plus business-case asks. | pilot_review_slot_03, pilot_review_slot_05, pilot_review_slot_06 | At least 1 public issue submitted or clear rejection reason recorded. |
| Week 3 | Collect remaining peer feedback and route public submissions through the evidence gate. | pilot_review_slot_01, pilot_review_slot_02, pilot_review_slot_08 | Accepted evidence rollup remains the source of truth for any resume upgrade. |

## First Commands To Record Real Sends

- `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<real reviewer>" --channel-used LinkedIn, email, or mentor message`
- `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_04 --status sent --reviewer-contact "<real reviewer>" --channel-used LinkedIn, email, or mentor message`
- `python scripts/record_reviewer_outreach_event.py --slot-id review_slot_03 --status sent --reviewer-contact "<real reviewer>" --channel-used LinkedIn, email, or mentor message`

## Operating Rules

- Do not enter private names into public files unless the reviewer explicitly wants public credit.
- Do not count sent messages, private replies, or self-authored issues as outcome evidence.
- Do not buy, trade, or pressure for GitHub stars.
- Every upgraded resume claim must point to accepted public evidence.
- Keep raw business rows, customer names, emails, phone numbers, tokens, and addresses out of public issues.

## Not Claimed

- No reviewer has been contacted until a real event is recorded.
- No external user, feedback, business validation, AI review, or star-growth outcome is claimed.
- No enterprise deployment is claimed.

## Resume-Safe Summary

Published a pilot reviewer CRM with 8 reviewer leads, 5 target outcome metrics, a 3-week evidence collection plan, 0 recorded sends, and 0 accepted public evidence items.
