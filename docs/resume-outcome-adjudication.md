# Resume Outcome Adjudication

Translate public reviewer evidence-gate results into clear resume decisions: what can be claimed now, what remains blocked, and what public evidence would unlock each stronger outcome claim.

## Current Decision

| Metric | Value |
| --- | ---: |
| Evaluated public issues | 4 |
| Accepted public issues | 0 |
| Rejected public issues | 4 |
| Outcome categories | 5 |
| Claimable external categories | 0 |
| Blocked external categories | 5 |

## Claim Categories

| Claim Category | Metric | Current Count | Claimable | Unlock Condition | Safe Current Wording |
| --- | --- | ---: | --- | --- | --- |
| external users | `confirmed_external_users` | 0 | False | one accepted non-owner external-run issue with runnable-path evidence and permission to count | No verified external users yet; project is public and runnable. |
| customer feedback | `external_feedback_items` | 0 | False | three accepted non-owner feedback issues with concrete observations and permission to count | Feedback intake is public; no accepted external feedback has arrived yet. |
| reproducible external run | `reproducible_feedback_items` | 0 | False | one accepted reviewer issue containing command or URL evidence and observed result | CI and local tests verify reproducibility; no non-owner external run is counted yet. |
| business validation | `business_case_feedback_items` | 0 | False | one accepted anonymized business-case issue with workflow, impact, fields, and permission to count | Business-case intake is ready; no accepted external business case exists yet. |
| AI Engineer review | `ai_engineer_review_items` | 0 | False | one accepted AI Engineer review issue with inspected implementation paths and permission to count | AI Engineer review intake is public; no accepted external AI review is counted yet. |

## Rejected Public Issues

| Issue | Failure Reasons | Top Reasons |
| --- | ---: | --- |
| #16 | 7 | self-authored issue, missing no-private-data checkbox, missing public external run permission |
| #17 | 8 | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox |
| #18 | 8 | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox |
| #19 | 8 | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox |

## Launch Control Room Linkage

| Signal | Count |
| --- | ---: |
| Public issue threads | 4 |
| Target outcome metrics | 4 |
| Reviewer-send paths | 3 |

## Resume-Safe Summary

Published a CI-verified resume outcome adjudication report covering 5 outcome categories, 0 claimable external outcome categories, 5 blocked categories, and the exact public evidence required to unlock user, feedback, reproducible-run, business-validation, and AI-review resume claims.

## Not Claimed

- external users
- customer feedback
- reproducible external usage
- business validation
- external AI Engineer review feedback
