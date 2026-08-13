# Evaluation Summary

This generated artifact summarizes the local agent evaluation harness. It is intentionally conservative: default CI runs without paid model credentials, so tool-agent results only claim disabled fallback behavior.

## Scenario Coverage

| Metric | Value |
| --- | ---: |
| Eval scenarios | 3 |
| Deterministic status accuracy | 1.0 |
| Deterministic finding recall | 1.0 |
| Deterministic evidence support rate | 1.0 |
| Tool-agent disabled fallback success | 1.0 |
| Tool-agent required report-tool rate without model key | 0.0 |

## Resume-Safe Summary

Built a 3-scenario eval harness measuring status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, report attachment, and latency.

## Not Claimed

- paid model benchmark results
- production traffic evaluation
- external human-labeled evaluation set
