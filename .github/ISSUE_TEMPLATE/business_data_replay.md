---
name: Business data replay
about: Share evidence after replaying the agent on anonymized CSV or read-only business-shaped data
title: "Business data replay: "
labels: feedback,confirmed-user,business-data-replay
assignees: ""
---

## Replay path

- [ ] Sanitized CSV upload: `POST /business-data/agent-report`
- [ ] Read-only PostgreSQL table: `POST /postgres/support-tickets/agent-report`
- [ ] Local Docker Compose support-ticket replay
- [ ] Repository/docs review before trying my own data

## Data source type

- [ ] Anonymized business CSV export
- [ ] Synthetic-but-business-shaped CSV
- [ ] Read-only PostgreSQL table
- [ ] Local seeded PostgreSQL demo table
- [ ] Other:

## Dataset shape

- Row count or table size:
- Column count:
- Primary key used:
- Non-sensitive field names involved:

## Agent run summary

- Command or endpoint used:
- Report status:
- Finding count:
- Selected tools shown in the agent trace:
- Did the agent call `build_quality_report`?

## Usefulness rating

- [ ] 5 - directly useful for a real data-quality workflow
- [ ] 4 - useful with small changes
- [ ] 3 - promising, but missing important context
- [ ] 2 - mostly a demo, not useful yet
- [ ] 1 - did not help

## What did it catch or miss?

Summarize the most useful finding, missed rule, confusing output, or root-cause hypothesis. Do not paste raw data.

## Permission boundary

- [ ] This issue contains no customer names, emails, addresses, tokens, secrets, or raw production rows.
- [ ] This can be counted as a confirmed anonymized replay.
- [ ] This can be counted as external feedback.
- [ ] Do not quote my organization, name, or raw data.

## Optional redacted output summary

Paste only a short redacted summary, such as report status, quality score, check names, and action titles.
