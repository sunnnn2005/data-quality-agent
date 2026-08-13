# Support Tickets Business Rules

These rules describe how the support-operations dashboard expects ticket export data to behave. They are intentionally small and source-citable so the agent can attach business context to generic data-quality findings.

## Ticket identity must be unique
id: support_tickets:R1
checks: duplicate_primary_key
keywords: ticket_id, duplicate_primary_key
text: Each `ticket_id` must identify exactly one support ticket event in the analytics export. Duplicate ticket IDs can double-count support volume and distort SLA reporting.

## Routing fields are required before publication
id: support_tickets:R2
checks: missing_values
keywords: team, priority, missing_values
text: The `team` and `priority` fields are required for routing dashboards. Missing routing values should block dashboard publication until the upstream source or transform is corrected.

## Customer-impact amounts cannot be negative
id: support_tickets:R3
checks: negative_amount
keywords: amount, negative_amount
text: `amount` represents positive customer-impact value for support analytics. Refunds, credits, or reversals must be modeled as separate event types rather than negative values in this export.

## Extreme amounts require review
id: support_tickets:R4
checks: numeric_outliers
keywords: amount, numeric_outliers
text: Extreme `amount` values should be reviewed before publication because they can dominate customer-impact reporting and hide normal support-ticket patterns.

## Raw customer identifiers must not be added to rule docs
id: support_tickets:R5
checks:
keywords: privacy, sensitive
text: Business-rule documentation must describe field-level constraints only. It must not contain raw customer identifiers, emails, phone numbers, ticket descriptions, or uploaded CSV row data.
