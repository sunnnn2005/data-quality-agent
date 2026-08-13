# Support Ticket Export Case Study

This case study is a reproducible demo of Data Quality Agent on a realistic business CSV export. It is intentionally small so reviewers can inspect every row and verify the report by running the API locally.

## Business Scenario

A support-operations team exports ticket data used by an internal dashboard. The dashboard expects one row per ticket, complete routing fields, and non-negative customer-impact amounts.

Input file:

```text
examples/support_tickets.csv
```

Dataset context:

- Owner: `support-ops`
- Primary key: `ticket_id`
- Expected columns: `ticket_id,team,priority,status,amount,created_at`

## Reproduce

Start the API:

```bash
uvicorn app.main:app --reload
```

Run the deterministic report:

```bash
curl -X POST http://127.0.0.1:8000/business-data/quality-report \
  -F "file=@examples/support_tickets.csv" \
  -F "dataset_name=Support Tickets" \
  -F "owner=support-ops" \
  -F "primary_key=ticket_id" \
  -F "expected_columns=ticket_id,team,priority,status,amount,created_at" \
  -F "description=Support ticket export used by operations dashboards."
```

Run the LLM tool-calling route when an OpenAI-compatible key is configured:

```bash
curl -X POST http://127.0.0.1:8000/business-data/agent-report \
  -F "file=@examples/support_tickets.csv" \
  -F "dataset_name=Support Tickets" \
  -F "owner=support-ops" \
  -F "primary_key=ticket_id" \
  -F "expected_columns=ticket_id,team,priority,status,amount,created_at" \
  -F "description=Support ticket export used by operations dashboards."
```

Without `OPENAI_API_KEY`, the route returns a safe disabled response instead of calling an external model.

## Verified Findings

The deterministic report identifies the following findings. These results are also checked by `scripts/verify_support_ticket_demo.py`, which writes the machine-readable artifact at [`docs/verified-support-ticket-result.json`](verified-support-ticket-result.json) and fails CI if the status, score, checks, or business-rule references drift unexpectedly.

- Duplicate primary key: `ticket_id` contains 1 duplicate record.
- Missing values: `priority` and `team` each have a 12.5% missing rate.
- Negative business value: `amount` contains 1 negative value.
- Numeric outlier: `amount` contains 1 value outside the IQR band.

The report also retrieves source-cited business rules:

- `support_tickets:R1`: ticket identity must be unique.
- `support_tickets:R2`: routing fields are required before publication.
- `support_tickets:R3`: customer-impact amounts cannot be negative.
- `support_tickets:R4`: extreme amounts require review.

These findings map to practical remediation steps:

- Deduplicate support-ticket events by the latest `created_at` timestamp.
- Add required-field validation before dashboard publication.
- Separate refunds or credits from positive ticket impact amounts.
- Review outlier ticket `1005` before it reaches downstream analytics.

## Why This Matters

This demo represents a common business-data failure mode: a dashboard can look operational while silently mixing duplicate facts, incomplete routing metadata, refund-like amounts, and extreme values. The project turns those issues into structured, evidence-backed findings that can be attached to a data incident or pipeline ticket.
