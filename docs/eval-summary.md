# Evaluation Summary

This generated artifact summarizes the local agent evaluation harness. It is intentionally conservative: default CI runs without paid model credentials, so tool-agent results only claim disabled fallback behavior.

## Scenario Coverage

| Metric | Value |
| --- | ---: |
| Eval scenarios | 14 |
| Deterministic status accuracy | 1.0 |
| Deterministic finding recall | 1.0 |
| Deterministic evidence support rate | 1.0 |
| Tool-agent disabled fallback success | 1.0 |
| Tool-agent required report-tool rate without model key | 0.0 |
| Available agent tools | 9 |
| Required tools present | True |
| Strategy recommendation recall | 1.0 |

## Tool Planning Coverage

Allowed tools: `get_dataset_contract`, `profile_dataset`, `select_quality_strategy`, `retrieve_dataset_memory`, `inspect_primary_key_integrity`, `analyze_numeric_distribution`, `run_quality_checks`, `retrieve_business_rules`, `build_quality_report`

## Resume-Safe Summary

Built a 14-scenario eval harness measuring status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, latency, and 9-tool planning coverage.

## Not Claimed

- paid model benchmark results
- production traffic evaluation
- external human-labeled evaluation set
