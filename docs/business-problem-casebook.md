# Business Problem Casebook

This generated casebook explains what business problem the project solves, using only CI-verified evidence.

## Case: Support operations dashboard refresh

Internal support dashboards can silently mislead operators when ticket exports contain duplicate ticket ids, missing routing fields, negative customer-impact amounts, and amount outliers.

## Input Context

| Field | Value |
| --- | --- |
| Dataset | `support_tickets` |
| Scenario | Support-operations ticket export used by internal dashboards. |
| Rows analyzed | 8 |
| Primary key | `ticket_id` |
| Owner | `support-ops` |

## Detected Business Risks

| Risk | Tool check | Evidence | Owner handoff |
| --- | --- | --- | --- |
| Dashboard double counting | duplicate_primary_key | 1 duplicate ticket_id was detected. | Data Engineering |
| Unreliable ticket routing | missing_values | 2 required routing fields were missing across priority and team. | Support Operations |
| Incorrect customer-impact reporting | negative_amount | 1 negative amount was mixed into positive customer-impact facts. | Analytics Engineering |
| Skewed executive metrics | numeric_outliers | 1 amount outlier can distort aggregate reporting. | Data Analytics |

## Agent Outputs

| Output | Value |
| --- | ---: |
| Quality Score | 24 |
| Status | FAIL |
| Finding Count | 5 |
| Business Rule Reference Count | 4 |
| Root Cause Hypothesis Count | 3 |
| Recommended Action Count | 5 |
| Owner Handoff Count | 4 |

## Interview Answer

The project models a common internal analytics failure: a dashboard may keep refreshing even when the underlying export has duplicate identities, missing routing metadata, and invalid amount values. The agent turns those raw checks into evidence-backed root-cause hypotheses and owner-specific remediation steps.

## Resume-Safe Result

Converted a support-operations CSV export into a verified data-quality casebook with 4 business risks, 5 evidence-backed findings, 3 ranked root-cause hypotheses, and 4 remediation owner handoffs.

## Evidence Links

- Casebook: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Business Impact: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-impact.json](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-impact.json)
- Support Ticket Case Study: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/support-ticket-case-study.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/support-ticket-case-study.md)
- Verified Result: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/verified-support-ticket-result.json](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/verified-support-ticket-result.json)
- Impact Review Packet: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/impact-review-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/impact-review-packet.md)

## Not Claimed

- real customer dataset
- external users
- customer feedback
- production deployment
- production financial impact avoided
