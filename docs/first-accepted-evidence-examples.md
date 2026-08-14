# First Accepted Evidence Examples

This generated artifact gives external reviewers concrete examples of evidence that passes or fails the public evidence gate.

## Summary

| Metric | Value |
| --- | ---: |
| Examples | 4 |
| Accepted examples | 2 |
| Rejected examples | 2 |
| Real public issue required | True |
| Resume claim allowed now | False |

## Gate-Tested Examples

| Example | Evidence Type | Accepted | Counts Toward | Failure Reasons |
| --- | --- | --- | --- | --- |
| accepted_business_case | business_case_review | True | business_case_feedback_items | - |
| accepted_real_model_run | real_model_run_review | True | accepted_real_model_runs | - |
| rejected_self_authored_business_case | business_case_review | False | - | self-authored issue |
| rejected_docs_only_replay | business_data_replay | False | - | docs-only review is not a confirmed business-data replay, missing business-data replay path tried |

## Resume-Safe Summary

Published gate-tested examples for the first acceptable business-case and real-model-run evidence, plus rejected self-authored and docs-only examples, while keeping real outcome counts unchanged.

## Not Claimed

- Synthetic examples are not counted as users, feedback, stars, pilots, or accepted real-model runs.
- Resume outcome metrics change only after a real non-owner public GitHub issue passes the evidence gate.
- Owner-authored evidence and docs-only reviews remain blocked from outcome claims.
