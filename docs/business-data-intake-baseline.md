# Business Data Intake Baseline

This generated artifact verifies that the project can accept realistic business-data inputs through bounded,
reviewable paths without claiming external production usage.

## Supported Inputs

bounded CSV upload, optional read-only PostgreSQL adapter

## Verified Endpoints

| Input path | Route | Verified |
| --- | --- | --- |
| csv_quality_report | `/business-data/quality-report` | True |
| csv_agent_report | `/business-data/agent-report` | True |
| postgres_quality_report | `/postgres/support-tickets/quality-report` | True |
| postgres_agent_report | `/postgres/support-tickets/agent-report` | True |

## Safety Limits

| Limit | Value |
| --- | ---: |
| max_upload_bytes | 2000000 |
| max_rows | 10000 |
| max_columns | 80 |
| csv_only | True |
| primary_key_required | True |
| empty_file_rejected | True |

## API Tests

| Test coverage | Verified |
| --- | --- |
| csv_upload_acceptance | True |
| csv_agent_disabled_fallback | True |
| missing_primary_key_rejection | True |
| support_ticket_case_study | True |
| postgres_read_only_adapter | True |
| postgres_agent_disabled_fallback | True |

## Documentation Checks

| Documentation coverage | Verified |
| --- | --- |
| csv_limits_documented | True |
| no_uploaded_file_persistence_documented | True |
| read_only_postgres_documented | True |
| business_data_curl_documented | True |

## Resume-Safe Signal

CI-verified business-data intake baseline covering bounded CSV uploads, read-only PostgreSQL context, 4 integration endpoints, 3 upload limits, and 6 API tests without claiming external production usage.

## Not Claimed

- external production datasets
- persistent storage of uploaded CSV rows
- enterprise production usage
- external users
- customer feedback
