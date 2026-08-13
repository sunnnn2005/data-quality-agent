# Business Data Replay Packet

This generated packet gives reviewers a safe way to replay the agent on business-shaped data and submit public evidence without inflating current outcome claims.

## Purpose

Give reviewers a safe, repeatable way to replay the agent against their own anonymized business-shaped CSV or read-only database data, then submit public evidence that can later upgrade resume outcomes.

## Replay Paths

| Path | Data Source | Endpoint | Counts Toward | Evidence Required |
| --- | --- | --- | --- | --- |
| sanitized_csv_upload | non-sensitive CSV export | `POST /business-data/agent-report` | `confirmed_external_users` | GitHub issue with dataset shape, command used, status, finding count, and redacted output summary |
| readonly_postgres_table | read-only PostgreSQL table or local compose table | `POST /postgres/support-tickets/agent-report` | `confirmed_external_users` | GitHub issue confirming read-only run, table row count, selected tools, and report status |
| business_case_replay | anonymized description of a real workflow problem | `docs/business-case-intake.md` | `business_case_feedback_items` | Public business-case issue with business-case label and no raw customer data |

## Commands

### sanitized_csv_upload

```bash
curl -X POST http://127.0.0.1:8000/business-data/agent-report -F file=@sample.csv -F dataset_name='Replay Dataset' -F owner='reviewer' -F primary_key='id' -F expected_columns='id,status,amount,created_at'
```

### readonly_postgres_table

```bash
docker compose up --build && curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report
```

### business_case_replay

```bash
Open the business-case issue template and submit only anonymized context, tried path, outcome, and permission boundary.
```

## Evidence Fields

- `path_tried`
- `data_source_type`
- `row_count_or_table_size`
- `selected_tools`
- `report_status`
- `finding_count`
- `usefulness_rating`
- `permission_boundary`

## Safety Requirements

- Use non-sensitive, anonymized, or synthetic-but-business-shaped data only.
- Do not upload customer names, emails, addresses, tokens, secrets, or raw production exports.
- Use read-only database credentials and bounded row limits.
- Submit public evidence summaries, not raw data.
- Mark whether the replay can be counted as feedback, confirmed run, reproducible issue, or business case.

## Current Public Counts

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Business Case Feedback Items | 0 |
| Reproducible Feedback Items | 0 |

## Replay Evidence Submission

- Template: [`.github/ISSUE_TEMPLATE/business_data_replay.md`](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Required sections: `8`
- Required labels: `feedback, confirmed-user, business-data-replay`

## Resume Upgrade Rules

| Metric | Current value | Minimum before claim | Claim when met |
| --- | ---: | ---: | --- |
| confirmed_external_users | 0 | 1 | at least one external reviewer replayed the agent on a business-shaped dataset |
| business_case_feedback_items | 0 | 1 | at least one anonymized real-world data-quality problem was reviewed publicly |
| reproducible_feedback_items | 0 | 1 | at least one reproducible issue or missed quality rule was submitted publicly |

## Resume-Safe Summary

Published a CI-verified business-data replay packet with 3 safe replay paths, 8 evidence fields, 5 safety requirements, and zero current external replay claims.

## Not Claimed

- external replay completed
- real company data analyzed
- customer feedback
- enterprise production usage
- raw production data stored
