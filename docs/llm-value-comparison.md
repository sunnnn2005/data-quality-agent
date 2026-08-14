# LLM Value Comparison

This generated artifact compares a fixed generic data-quality workflow against the agent's adaptive strategy-selection tool on the same public eval set.

## Summary

| Metric | Value |
| --- | ---: |
| Eval scenarios | 14 |
| Fixed generic checks | 3 |
| Adaptive agent tool | `select_quality_strategy` |
| Fixed generic average recall | 0.417 |
| Adaptive strategy average recall | 1.0 |
| Absolute recall lift | 0.583 |
| Relative recall lift | 139.8% |
| Improved scenarios | 9 |

## Scenario Rows

| Scenario | Dataset | Fixed Recall | Adaptive Recall | Lift |
| --- | --- | ---: | ---: | ---: |
| orders_daily_core_failures | orders_daily | 0.333 | 1.0 | 0.667 |
| orders_daily_duplicate_key_guardrail | orders_daily | 0.0 | 1.0 | 1.0 |
| orders_daily_revenue_null_monitor | orders_daily | 1.0 | 1.0 | 0.0 |
| orders_daily_high_value_outlier_review | orders_daily | 0.0 | 1.0 | 1.0 |
| payments_events_freshness_negative_amount | payments_events | 0.0 | 1.0 | 1.0 |
| payments_events_missing_status_monitor | payments_events | 1.0 | 1.0 | 0.0 |
| payments_events_settlement_freshness_sla | payments_events | 0.0 | 1.0 | 1.0 |
| payments_events_refund_domain_guardrail | payments_events | 0.0 | 1.0 | 1.0 |
| payments_events_low_volume_ingestion_check | payments_events | 1.0 | 1.0 | 0.0 |
| customer_profiles_schema_missingness | customer_profiles | 0.5 | 1.0 | 0.5 |
| customer_profiles_unexpected_column_contract | customer_profiles | 0.0 | 1.0 | 1.0 |
| customer_profiles_contact_completeness | customer_profiles | 1.0 | 1.0 | 0.0 |
| customer_profiles_ltv_outlier_review | customer_profiles | 0.0 | 1.0 | 1.0 |
| customer_profiles_low_volume_ingestion_check | customer_profiles | 1.0 | 1.0 | 0.0 |

## Resume-Safe Summary

Published a 14-scenario comparison showing adaptive data-quality strategy selection improved finding recall from 0.417 to 1.0 versus a fixed generic checklist, without claiming paid-model benchmark results or external adoption.

## Not Claimed

- paid model benchmark results
- production traffic evaluation
- external human-labeled evaluation set
- enterprise customer impact
