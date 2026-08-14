# Business Impact Validation Plan

This generated plan defines how the project can earn real business-impact evidence from an external reviewer.

## Purpose

Define how a reviewer can turn the current anonymized business demo into externally validated, resume-safe business impact evidence without fabricating users, ROI, or production adoption.

## Current Demo Baseline

| Metric | Value |
| --- | ---: |
| Dataset Id | support_tickets |
| Quality Score | 24 |
| Status | FAIL |
| Findings | 5 |
| Business Risk Areas | 4 |
| Owner Handoffs | 4 |
| High Priority Actions | 3 |
| Casebook Cases | 1 |
| Resolution Steps | 4 |
| External Validated Business Cases | 0 |

## Validation Metrics

| Metric | Current Demo Value | First External Target | Evidence Required |
| --- | ---: | --- | --- |
| defects_found_per_dataset | 5 | >= 1 confirmed issue on an anonymized non-owner dataset | public business-case issue with anonymized row/field summary and permission to count |
| owner_handoffs_created | 4 | >= 1 reviewer-confirmed owner or workflow handoff | reviewer confirms at least one suggested owner/action maps to their workflow |
| manual_review_minutes_estimated | None | reviewer-provided before/after estimate | reviewer reports approximate manual check time and whether the report changed their triage path |
| dashboard_risk_prevented | 4 | >= 1 reviewer-confirmed dashboard, report, or workflow risk | reviewer states which business workflow, decision, or report would have been affected by the detected issue |
| false_positive_review | None | reviewer labels at least one finding as useful, noisy, or incorrect | public feedback issue separates useful findings from false positives |

## First Pilot Protocol

| Step | Action | Done When |
| ---: | --- | --- |
| 1 | Collect an anonymized CSV or table schema | The reviewer confirms there is no private data, secrets, or customer identifiers. |
| 2 | Run the deterministic checks and LLM-agent report | The run produces findings, evidence, recommendations, and limitations. |
| 3 | Ask the reviewer to label findings | The reviewer marks each key finding as useful, noisy, incorrect, or needs context. |
| 4 | Map findings to a workflow decision | At least one detected issue is tied to a dashboard, report, owner, or operational process. |
| 5 | Submit public redacted evidence | A non-owner public GitHub issue includes permission to count and no sensitive data. |

## Minimum Resume Upgrade Gate

| Rule | Value |
| --- | --- |
| Required Public Issues | 1 |
| Required Non Owner Author | True |
| Requires Permission To Count | True |
| Requires No Sensitive Data | True |
| Requires Business Workflow Mapping | True |
| Current Accepted Business Cases | 0 |
| Resume Claim Allowed | False |

## Resume-Safe Now

Built a CI-verified business-impact validation plan mapping 5 measurable pilot metrics to public evidence requirements, while preserving a zero external-business-case baseline.

## Future Resume Lines After Evidence

- Validated the agent on a non-owner data-quality case and surfaced confirmed defects before reporting consumption.
- Mapped data-quality findings to reviewer-confirmed operational handoffs.
- Collected reviewer-estimated manual review time for a real anonymized workflow.
- Linked confirmed data-quality findings to a concrete downstream decision risk.
- Used reviewer feedback to calibrate data-quality findings and reduce noisy recommendations.

## Not Claimed

- validated business impact
- production adoption
- external business users
- revenue saved
- manual time saved
- customer dataset
