# Evidence Gap Diagnostics

This generated artifact explains why current public reviewer issues are not yet resume-countable.

## Summary

| Metric | Value |
| --- | ---: |
| Evaluated issues | 15 |
| Accepted issues | 0 |
| Rejected issues | 15 |
| Self-authored rejections | 15 |
| Sensitive-risk rejections | 14 |
| Failure reason types | 33 |

## Top Failure Reasons

| Reason | Count |
| --- | ---: |
| self-authored issue | 15 |
| contains sensitive-data risk terms | 14 |
| missing no-private-data checkbox | 11 |
| missing public external run permission | 11 |
| missing runnable path tried | 11 |
| missing command or URL evidence | 11 |
| missing observed result evidence | 11 |
| missing main feedback | 11 |
| missing business-case counting permission | 2 |
| missing business-impact counting permission | 2 |

## Evidence Type Gaps

| Evidence Type | Evaluated | Accepted | Rejected | Next Reviewer Checklist |
| --- | ---: | ---: | ---: | --- |
| ai_engineer_review | 1 | 0 | 1 | Use a non-owner GitHub account.<br>Confirm no private business data, secrets, customer names, emails, addresses, or raw production rows.<br>Grant permission to count the issue as external AI Engineer project feedback.<br>Include inspected paths or commands.<br>Include strongest AI Engineer signals and missing or weak signals. |
| business_case_review | 2 | 0 | 2 | Use a non-owner GitHub account.<br>Grant anonymized business-case and business-impact counting permission.<br>Describe business context, data-quality problem, business impact, fields involved, and project evidence mapping.<br>Keep organization names, customer names, raw rows, and sensitive identifiers out of the issue. |
| business_data_replay | 1 | 0 | 1 | Use a non-owner GitHub account.<br>Confirm no customer names, emails, addresses, tokens, secrets, or raw production rows.<br>Grant permission to count the anonymized replay and external feedback.<br>Select CSV upload, read-only PostgreSQL, or Docker Compose replay path.<br>Include data source type, dataset shape, agent run summary, and catch-or-miss notes. |
| external_run_review | 11 | 0 | 11 | Use a non-owner GitHub account.<br>Check the no-private-data permission box.<br>Check the public external run permission box.<br>Select a runnable path such as public demo, GHCR container, or Docker Compose replay.<br>Include non-placeholder commands or URLs used.<br>Include observed result and main feedback. |

## Nearest Unlock Paths

| Target Metric | Current | First Unlock Requirement | Submission |
| --- | ---: | --- | --- |
| ai_engineer_review_items | 0 | One non-owner `ai-engineer-review` issue with inspected paths, no-private-data checkbox, and permission to count. | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md) |
| confirmed_external_users | 0 | One non-owner external run issue with a runnable path, observed result, command or URL evidence, and permission to count. | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md) |
| business_case_feedback_items | 0 | One anonymized business-case review issue with workflow context, impact, fields, project evidence mapping, and permission to count. | [submit](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md) |

## Not Claimed

- No rejected issue is counted as a user, feedback item, reproducible run, business case, or AI Engineer review.
- Self-authored planning issues remain excluded from outcome metrics.
- Sensitive or private data must be redacted before any public issue can count.

## Resume-Safe Summary

Published evidence-gap diagnostics for 15 evaluated public issues, 0 accepted issues, 15 rejected issues, 15 self-authored rejections, and 3 nearest unlock paths for future resume-safe outcome evidence.
