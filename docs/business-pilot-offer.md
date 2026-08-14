# Business Pilot Offer

Turn the project from a portfolio demo into a safe pilot-ready offer for people who can bring anonymized business-shaped data or a real data-quality workflow problem.

Public page: [https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html](https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html)

Public pilot issue: [https://github.com/sunnnn2005/data-quality-agent/issues/31](https://github.com/sunnnn2005/data-quality-agent/issues/31)

Evidence checklist: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-pilot-evidence-checklist.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-pilot-evidence-checklist.md)

## Pilot Scope

| Step | Name | Owner | Output |
| ---: | --- | --- | --- |
| 1 | Scope a safe dataset | reviewer_or_pilot_contact | Dataset shape, non-sensitive field names, business rule candidates, and permission boundary. |
| 2 | Run a bounded replay | project_owner_or_reviewer | CSV upload or read-only PostgreSQL run with row/column limits and no stored raw data. |
| 3 | Review evidence-backed findings | reviewer_or_domain_contact | Useful finding, missed rule, confusing recommendation, or accepted root-cause hypothesis. |
| 4 | Publish redacted evidence | reviewer | GitHub issue with permission to count, no private data, and a concrete observed result. |

## Eligible Data Sources

- anonymized order, ticket, transaction, inventory, or signup CSV
- read-only PostgreSQL table with non-sensitive columns
- synthetic-but-business-shaped export that mirrors a real workflow
- written business case when data cannot be shared

## Not Allowed

- customer names, emails, addresses, phone numbers, tokens, secrets, or raw production rows
- write access to production databases
- unbounded warehouse queries
- private evidence that cannot be audited publicly

## Evidence Gates

- non-owner reviewer or pilot contact
- public GitHub issue or public review link
- explicit permission to count the redacted result
- dataset shape and path tried
- one concrete useful, confusing, missing, or reproducible finding
- confirmation that no private data was posted

## Current Public Counts

| Metric | Count |
| --- | ---: |
| `confirmed_external_users` | 0 |
| `external_feedback_items` | 0 |
| `business_case_feedback_items` | 0 |
| `reproducible_feedback_items` | 0 |

## Submission Paths

- `business_data_replay`: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md
- `business_case_review`: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md
- `demo_feedback`: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md

## Resume Upgrade Rules

| Future metric | Current value | Minimum before claim | Future resume line |
| --- | ---: | ---: | --- |
| confirmed_external_users | 0 | 1 | Validated the agent with an external reviewer on an anonymized business-shaped dataset. |
| business_case_feedback_items | 0 | 1 | Collected public business-case feedback mapping agent findings to a real workflow risk. |
| reproducible_feedback_items | 0 | 1 | Converted external replay feedback into a reproducible quality-rule improvement. |

## Resume-Safe Summary

Published a pilot-ready business data offer with 4 pilot steps, 4 eligible data-source types, 6 evidence gates, a public pilot issue, and zero current external pilot claims.

## Not Claimed

- completed pilot
- real enterprise customer
- production deployment
- external business-data replay
- measured company impact
