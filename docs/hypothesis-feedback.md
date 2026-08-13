# Hypothesis Feedback

This generated artifact records human-review labels for the support-ticket root-cause hypotheses. It is a local project feedback loop for agent evaluation, not evidence of external product feedback.

| Hypothesis | Label | Confidence | Supporting checks |
| --- | --- | ---: | --- |
| Business-rule validation is not separating exceptional transactions from standard facts. | `accepted` | 0.71 | negative_amount, numeric_outliers |
| The ingestion pipeline may be replaying events without idempotent merge logic. | `accepted` | 0.65 | duplicate_primary_key |
| Source API or transform logic is producing incomplete fields for required analytics columns. | `needs_review` | 0.63 | missing_values |

## Summary

Added a human-review feedback artifact that labels 3 root-cause hypotheses with 2 accepted and 1 needing review.

## Not Claimed

- external product feedback
- production incident confirmation
- paid human-labeling dataset
