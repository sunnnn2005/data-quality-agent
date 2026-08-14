# Business Pilot Evidence Checklist

Define the exact public evidence needed before business pilot usage, external users, feedback, or business-impact claims can be added to a resume.

Public pilot offer: [https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html](https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html)

Public pilot issue: [https://github.com/sunnnn2005/data-quality-agent/issues/31](https://github.com/sunnnn2005/data-quality-agent/issues/31)

## Outcome Tracks

| Metric | Current value | Minimum before claim | Accepted source | Future resume line |
| --- | ---: | ---: | --- | --- |
| confirmed_external_users | 0 | 1 | business_data_replay.md issue | Validated the agent with an external reviewer on an anonymized business-shaped dataset. |
| business_case_feedback_items | 0 | 1 | business_case_review.md issue | Collected public business-case feedback mapping agent findings to a real workflow risk. |
| reproducible_feedback_items | 0 | 1 | business_data_replay.md issue with reproducible run evidence | Converted external replay feedback into a reproducible quality-rule improvement. |
| external_feedback_items | 0 | 1 | demo_feedback.md or business_data_replay.md issue | Incorporated external reviewer feedback into the agent evidence workflow. |

## Required Public Evidence

### `confirmed_external_users`

- non-owner reviewer
- replay path tried
- dataset shape
- agent run summary
- usefulness rating
- permission to count confirmed anonymized replay
- no private data confirmation

### `business_case_feedback_items`

- business context
- data-quality problem
- business impact
- fields involved
- project evidence mapping
- business-case counting permission
- business-impact counting permission

### `reproducible_feedback_items`

- command or endpoint used
- observed report status
- finding count
- selected tools or agent trace summary
- catch-or-miss feedback
- redacted output summary

### `external_feedback_items`

- specific path tried
- observed result
- main feedback
- permission to count external feedback
- no private data confirmation

## Template Coverage Checks

| Check | Passed |
| --- | --- |
| business case collects impact | True |
| business case maps project evidence | True |
| replay collects agent trace | True |
| replay collects usefulness rating | True |
| replay blocks private data | True |

## Current Public Counts

| Metric | Count |
| --- | ---: |
| `confirmed_external_users` | 0 |
| `business_case_feedback_items` | 0 |
| `reproducible_feedback_items` | 0 |
| `external_feedback_items` | 0 |

## Blocked Until Public Evidence

- `confirmed_external_users`
- `business_case_feedback_items`
- `reproducible_feedback_items`
- `external_feedback_items`

## Resume-Safe Summary

Published a business pilot evidence checklist with 4 outcome tracks, explicit public evidence requirements, template coverage checks, and zero current business-pilot outcome claims.

## Not Claimed

- completed business pilot
- confirmed external user
- real enterprise customer
- measured company impact
