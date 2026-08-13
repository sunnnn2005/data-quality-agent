# External Reviewer Evidence Gate

This generated gate validates public reviewer issues before they can become resume-safe outcome metrics.

## Summary

| Metric | Value |
| --- | ---: |
| Evaluated issues | 4 |
| Accepted issues | 0 |
| Rejected issues | 4 |
| Collected public issues | 4 |
| Collection errors | 0 |
| Linked outreach queue | 3 |

## Accepted Counts

| Metric | Accepted count |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |
| Ai Engineer Review Items | 0 |

## Evaluations

| Issue | Title | Author | Evidence Type | Accepted | Counts Toward | Failure Reasons |
| --- | --- | --- | --- | --- | --- | --- |
| #16 | [Pilot feedback tracker: collect external reviewer evidence](https://github.com/sunnnn2005/data-quality-agent/issues/16) | sunnnn2005 | external_run_review | False |  | self-authored issue, missing no-private-data checkbox, missing public external run permission, missing runnable path tried, missing command or URL evidence, missing observed result evidence, missing main feedback |
| #17 | [Review request: collect first public external feedback](https://github.com/sunnnn2005/data-quality-agent/issues/17) | sunnnn2005 | external_run_review | False |  | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox, missing public external run permission, missing runnable path tried, missing command or URL evidence, missing observed result evidence, missing main feedback |
| #18 | [External run evidence: reviewer run collection point](https://github.com/sunnnn2005/data-quality-agent/issues/18) | sunnnn2005 | external_run_review | False |  | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox, missing public external run permission, missing runnable path tried, missing command or URL evidence, missing observed result evidence, missing main feedback |
| #19 | [Public reviewer call: collect external review and pilot evidence](https://github.com/sunnnn2005/data-quality-agent/issues/19) | sunnnn2005 | external_run_review | False |  | self-authored issue, contains sensitive-data risk terms, missing no-private-data checkbox, missing public external run permission, missing runnable path tried, missing command or URL evidence, missing observed result evidence, missing main feedback |

## Gate Rules

- Self-authored issues do not count as external evidence.
- Reviewer must grant explicit permission before a run or feedback is counted.
- A docs-only review does not count as a confirmed run.
- Commands or URLs used, observed result, and main feedback must be non-placeholder text.
- AI Engineer review issues require explicit permission plus inspected paths and concrete signal feedback.
- Issues containing sensitive-data risk terms are rejected until redacted.
- The default artifact collects tracked public GitHub issues before applying the evidence gate.

## Resume-Safe Summary

Published a CI-verified external reviewer evidence gate that validates issue body fields, explicit permission, non-owner authorship, runnable-path evidence, and sensitive-data guardrails before any reviewer issue can increase resume-safe usage, feedback, or AI Engineer review metrics.

## Not Claimed

- No accepted external reviewer issue exists yet.
- No user, feedback, reproducible-run, business-case, or AI Engineer review count is increased by planning issues.
- No private business data is accepted as evidence.
