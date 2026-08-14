# Public Metrics Provenance

This generated artifact explains where public outcome metrics come from and whether each metric is safe for resume wording.

## Summary

| Metric | Value |
| --- | ---: |
| Tracked metrics | 8 |
| Claimable metrics | 2 |
| Blocked or baseline metrics | 5 |

## Metric Sources

| Metric | Value | Evidence Source | Resume Status | Rule |
| --- | ---: | --- | --- | --- |
| github_stars | 0 | GitHub public repository count via update_adoption_metrics.py | `baseline_only` | May claim the exact public star count only; never imply growth beyond GitHub's public number. |
| github_forks | 1 | GitHub public repository count via update_adoption_metrics.py | `claimable` | May claim the exact public fork baseline because it is visible on GitHub. |
| passing_tests | 193 | pytest collection and CI evidence via update_adoption_metrics.py | `claimable` | May claim passing test count after local and CI verification. |
| confirmed_external_users | 0 | docs/external-reviewer-evidence-gate.json accepted_counts | `blocked_until_accepted_evidence` | Counts only accepted public reviewer issues with explicit permission and non-owner authorship. |
| external_feedback_items | 0 | docs/external-reviewer-evidence-gate.json accepted_counts | `blocked_until_accepted_evidence` | Counts only accepted public reviewer issues that pass the evidence gate. |
| business_case_feedback_items | 0 | docs/external-reviewer-evidence-gate.json accepted_counts | `blocked_until_accepted_evidence` | Counts only accepted anonymized business-case reviews. |
| ai_engineer_review_items | 0 | docs/external-reviewer-evidence-gate.json accepted_counts | `blocked_until_accepted_evidence` | Counts only accepted AI Engineer review issues with inspected paths and concrete feedback. |
| feature_feedback_items | 8 | GitHub issue labels via update_feedback_metrics.py | `tracking_only` | Feature-request labels are product backlog signal, not user adoption or customer feedback. |

## Source Controls

- GitHub public metrics use update_adoption_metrics.py with gh CLI first and GitHub public API fallback.
- External users, external feedback, business-case feedback, and AI Engineer reviews are counted only from accepted evidence-gate counts.
- Self-authored planning issues and unaccepted labeled issues do not unlock resume outcome claims.
- Feature-request labels are tracked separately from user/customer outcome metrics.

## Resume-Safe Summary

Published a public metrics provenance record for 8 outcome metrics, showing 2 currently claimable metrics and evidence-gated zero counts for users, feedback, business-case validation, and AI Engineer review.

## Not Claimed

- No external users are claimed while confirmed_external_users is zero.
- No external feedback is claimed while external_feedback_items is zero.
- No business-case validation is claimed while business_case_feedback_items is zero.
- No AI Engineer review is claimed while ai_engineer_review_items is zero.
- No GitHub star growth is claimed while github_stars is zero.
