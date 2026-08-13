# Outcome Summary

This page converts the machine-generated business-impact artifact into a resume-safe outcome summary. It is generated from `docs/business-impact.json`; do not edit the metrics by hand.

## Business Problem

Support operations dashboard data can silently mix duplicate ticket facts, missing routing metadata, refund-like negative amounts, and extreme outliers before publication.

## Verified Outcomes

| Metric | Value |
| --- | ---: |
| Dataset | `support_tickets` |
| Rows analyzed | 8 |
| Quality score | 24 / 100 |
| Report status | `FAIL` |
| Issue categories | 4 |
| Findings | 5 |
| Affected columns | 4 |
| Recommended actions | 5 |
| Ranked root-cause hypotheses | 3 |
| Business-rule references | 4 |
| Business risk areas | 4 |
| High-priority actions | 3 |
| Owner handoffs | 4 |

## Issue Categories

- **Duplicate ticket identity**: 1 duplicate primary-key case found. Dashboards can double-count a support case or attach remediation to the wrong row.
- **Missing routing metadata**: 2 required routing fields missing across priority/team checks. Support operations cannot reliably route or prioritize every ticket.
- **Negative customer-impact amount**: 1 negative amount found. Refund-like events are mixed into positive customer-impact facts.
- **Extreme amount outlier**: 1 amount outlier found. Extreme values can skew reporting and need review before publication.

## Ranked Root-Cause Hypotheses

1. **Business-rule validation is not separating exceptional transactions from standard facts.** (confidence: 0.71; checks: negative_amount, numeric_outliers)
2. **The ingestion pipeline may be replaying events without idempotent merge logic.** (confidence: 0.65; checks: duplicate_primary_key)
3. **Source API or transform logic is producing incomplete fields for required analytics columns.** (confidence: 0.63; checks: missing_values)

## Remediation Scorecard

The agent converts raw quality findings into a prioritized remediation handoff for support-operations analytics owners.

| Business Risk Area | Priority | Owner | Evidence |
| --- | --- | --- | --- |
| Dashboard accuracy | HIGH | Data Engineering | 1 duplicate ticket_id case can double-count support volume. |
| Support routing | HIGH | Support Operations | 2 required routing fields are missing across priority and team. |
| Customer-impact reporting | HIGH | Analytics Engineering | 1 negative amount is mixed into positive customer-impact facts. |
| Executive metric review | MEDIUM | Data Analytics | 1 amount outlier can skew aggregate customer-impact reporting. |

## SLA-Style Checks

- one ticket_id per support event
- priority and team must be present for routing
- customer-impact amount must be non-negative
- extreme amounts require review before dashboard publication

## Resume-Safe Summary

Quantified 4 support-ticket data quality issue categories across 8 rows, including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers.

Produced a verified remediation scorecard mapping 5 data quality findings to 4 business risk areas, 3 high-priority actions, and 4 owner handoffs.

## Not Claimed

- No verified external users yet.
- No customer production deployment is claimed.
- This artifact measures a reproducible business-data case study, not enterprise adoption.
