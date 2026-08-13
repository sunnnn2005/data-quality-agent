# API Contract

This generated artifact is built from the FastAPI OpenAPI schema. It verifies that the public API surface includes the business-data, agent, trace, memory, and incident-report endpoints used by the demo and resume evidence.

| Contract metric | Value |
| --- | ---: |
| OpenAPI version | `3.1.0` |
| API title | `Data Quality Agent` |
| Paths | 14 |
| Required integration endpoints | 6 |

## Required Endpoints

| Endpoint | Operation ID |
| --- | --- |
| `POST /business-data/quality-report` | `create_business_quality_report_business_data_quality_report_post` |
| `POST /business-data/agent-report` | `create_business_agent_report_business_data_agent_report_post` |
| `POST /postgres/support-tickets/agent-report` | `create_postgres_support_ticket_agent_report_postgres_support_tickets_agent_report_post` |
| `GET /datasets/{dataset_id}/memory` | `get_dataset_memory_datasets__dataset_id__memory_get` |
| `GET /runs/{trace_id}` | `get_run_trace_runs__trace_id__get` |
| `POST /datasets/{dataset_id}/incident-report.md` | `create_incident_report_markdown_datasets__dataset_id__incident_report_md_post` |
