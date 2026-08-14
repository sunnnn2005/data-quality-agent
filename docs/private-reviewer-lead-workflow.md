# Private Reviewer Lead Workflow

This generated workflow lets real reviewer outreach happen without publishing private contacts.

## Purpose

Give the project a privacy-safe workflow for tracking real reviewer leads locally while publishing only redacted, permissioned, non-owner evidence after a reviewer submits a public issue.

## Private File

- Local path: `private/reviewer-leads.csv`
- Legacy local path: `private-reviewer-leads.csv`
- Gitignored: `True`

## Required Columns

- `lead_id`
- `reviewer_segment`
- `private_contact_label`
- `channel`
- `target_metric`
- `status`
- `next_action_date`
- `public_evidence_url`
- `permission_to_count`
- `no_private_data_confirmed`
- `notes_private`

## Allowed Statuses

- `not_contacted`
- `sent`
- `replied_private`
- `public_issue_submitted`
- `accepted_evidence`
- `declined`

## Target Metrics

- `ai_engineer_review_items`
- `confirmed_external_users`
- `external_feedback_items`
- `reproducible_feedback_items`
- `business_case_feedback_items`
- `github_stars`

## Example CSV

```csv
lead_id,reviewer_segment,private_contact_label,channel,target_metric,status,next_action_date,public_evidence_url,permission_to_count,no_private_data_confirmed,notes_private
lead_001,AI engineer or ML systems mentor,keep-real-name-private,LinkedIn,ai_engineer_review_items,not_contacted,2026-08-15,,false,false,Store real contact details only in the local ignored file.
```

## Commands

Record a real send:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id <review_slot_id> --status sent --reviewer-contact "<private label or public handle>" --channel-used <channel>
```

Record a public evidence submission:

```bash
python scripts/record_reviewer_outreach_event.py --slot-id <review_slot_id> --status public_issue_submitted --reviewer-contact "<public handle>" --channel-used <channel> --public-evidence-url <github issue url> --permission-to-count --no-private-data-confirmed
```

## Conversion Rules

- Keep real names, emails, phone numbers, and private notes only in the ignored local CSV.
- Record a sent event only after a message is actually sent to a real reviewer.
- Do not count private replies as resume evidence.
- Ask the reviewer to submit a public redacted GitHub issue before any outcome metric can increase.
- Run the external reviewer evidence gate before upgrading any resume claim.
- Never ask for fake stars, traded stars, raw customer data, secrets, or private production rows.

## Not Claimed

- This workflow does not claim contacted reviewers until real events are recorded.
- This workflow does not claim users, feedback, business validation, AI reviews, or GitHub stars.
- Private lead rows are not public evidence.

## Resume-Safe Summary

Published a privacy-safe reviewer lead workflow with 11 required private CSV columns, 6 lead statuses, 6 target outcome metrics, gitignored private lead paths, and zero upgraded outcome claims.
