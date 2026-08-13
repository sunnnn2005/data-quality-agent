# Agent Safety Boundaries

This generated artifact summarizes the local safety boundaries around the LLM agent. It is not a formal security audit.

## Verified Boundaries

| Boundary | Value |
| --- | ---: |
| Tool allowlist count | 5 |
| Rejected unsafe PostgreSQL queries | 3 |
| Default PostgreSQL row limit | 1000 |
| Verifier rule count | 6 |
| Sensitive redaction verified | True |
| Disabled-agent fallback verified | True |

## Tool Allowlist

- `get_dataset_contract`
- `profile_dataset`
- `select_quality_strategy`
- `run_quality_checks`
- `build_quality_report`

## Verifier Rules

- `finding_evidence_required`
- `known_column_references`
- `sensitive_value_redaction`
- `llm_evidence_must_match_findings`
- `recommended_actions_required`
- `quality_score_bounds`

## Resume-Safe Summary

Generated a safety-boundary artifact covering tool allowlists, read-only PostgreSQL query limits, sensitive-field redaction, disabled-agent fallback, and deterministic report verification rules.

## Not Claimed

- formal security audit
- penetration test
- SOC 2 compliance
