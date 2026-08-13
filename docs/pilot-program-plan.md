# Pilot Program Plan

This generated plan defines how the project can collect real feedback before making adoption claims.

## Objective

Run a small public pilot to turn the current zero-feedback baseline into verified public feedback, while keeping resume claims tied to GitHub issues and metrics artifacts.

## Pilot Window

3 weeks

## Participant Segments

| Segment | Target Count | Source | Requested Action |
| --- | ---: | --- | --- |
| student_reviewers | 5 | UC Davis classmates or data/AI club members | Try the public demo and leave one feedback issue. |
| developer_reviewers | 3 | student developers or open-source reviewers | Run the repo locally or inspect the API contract and leave a bug or feature issue. |
| career_reviewers | 2 | recruiters, mentors, or hiring managers | Review the evidence pack and comment on project clarity for AI Engineer Intern roles. |

## Weekly Plan

| Week | Focus | Deliverable |
| ---: | --- | --- |
| 1 | Send outreach and collect first impressions. | At least one public feedback issue or a documented zero-response checkpoint. |
| 2 | Ask reviewers to reproduce one demo path or local run path. | Bug, feature, or reproducibility feedback labeled in GitHub issues. |
| 3 | Triage feedback, implement one small improvement, and update metrics. | A public changelog entry linking feedback to a resolved issue or documented decision. |

## Feedback Evidence Rules

- Only count feedback that is linked from a public GitHub issue or reproducible external note.
- Only count a user after they explicitly confirm they tried the demo or ran the project.
- Do not count private compliments, application submissions, or self-testing as external users.
- Keep stars, users, and feedback as zero until public metrics prove otherwise.

## Success Thresholds

| Metric | Current / Threshold |
| --- | ---: |
| Current External Feedback Items | 0 |
| Current Confirmed External Users | 0 |
| Minimum Feedback Items Before Resume Claim | 3 |
| Minimum Confirmed Users Before User Claim | 1 |
| Minimum Reproducible Items Before Case Study Claim | 1 |

## Issue Labels To Count

| Metric | GitHub Label |
| --- | --- |
| Bug Feedback Items | `bug` |
| Business Case Feedback Items | `business-case` |
| Confirmed External Users | `confirmed-user` |
| External Feedback Items | `feedback` |
| Feature Feedback Items | `enhancement` |
| Reproducible Feedback Items | `reproducible` |

## Review Paths

- Application Evidence Pack: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md)
- Bug Report: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md)
- Business Case Review: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Feature Request: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=feature_request.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=feature_request.md)
- Feedback Issue: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Github Repo: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Live Scorecard: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/live-project-scorecard.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/live-project-scorecard.md)
- Pilot Feedback Tracker: [https://github.com/sunnnn2005/data-quality-agent/issues/16](https://github.com/sunnnn2005/data-quality-agent/issues/16)
- Quick Demo: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)

## Resume Upgrade Rules

- If external_feedback_items reaches 3, resume may say the project collected public pilot feedback.
- If confirmed_external_users reaches 1, resume may say it was tried by an external reviewer.
- If reproducible_feedback_items reaches 1 and an improvement is merged, resume may say it used feedback to improve the product.
- Do not claim production usage, customers, or traction unless public evidence exists.

## Not Claimed

- external users
- customer feedback
- enterprise production usage
- GitHub stars beyond the current public count
