---
name: Real model run review
about: Submit redacted evidence from a real OpenAI-compatible LLM agent run
title: "Real model run: "
labels: real-model-run,ai-engineer-review,evidence-candidate
assignees: ""
---

## Run path

- [ ] Built-in dataset: `python scripts/capture_real_model_run.py --dataset-id orders_daily --write`
- [ ] Business CSV replay: `python scripts/capture_real_model_run.py --csv-path sample.csv --dataset-name "Replay Dataset" --owner reviewer --primary-key id --expected-columns "id,status,amount" --description "Anonymized business replay dataset" --write`
- [ ] Read-only PostgreSQL route inspected before capture
- [ ] I reviewed the runbook but did not execute a model call

## Environment

- Model provider:
- Model name:
- API route used:
- Dataset id or anonymized dataset name:
- Operating system:
- Python version:

## Redacted telemetry

Paste only safe values from `docs/real-model-evidence-capture.json`.

- Trace id:
- Prompt version:
- Model call count:
- Tool call count:
- Distinct tool count:
- Used strategy tool:
- Used required report tool:
- Final report attached:
- Verification passed:
- Total tokens:
- Estimated cost USD:
- Latency ms:

## Tool evidence

Which tools did the model select before the final report?

- [ ] `get_dataset_contract`
- [ ] `profile_dataset`
- [ ] `select_quality_strategy`
- [ ] `retrieve_dataset_memory`
- [ ] `inspect_primary_key_integrity`
- [ ] `analyze_numeric_distribution`
- [ ] `run_quality_checks`
- [ ] `retrieve_business_rules`
- [ ] `build_quality_report`

## Outcome

- [ ] The model selected more than one whitelisted tool.
- [ ] Tool results changed or informed the final report.
- [ ] The final answer attached a verified structured quality report.
- [ ] Token, cost, and latency telemetry were captured.
- [ ] The run is useful evidence for AI Engineer Intern readiness.

## Permission and privacy

- [ ] This issue contains no provider credentials, raw prompts, customer names, emails, addresses, secrets, tokens, or raw production rows.
- [ ] You may count this public issue as accepted real-model run evidence if it passes the repository evidence gate.
- [ ] Do not count this issue publicly.

## Notes

What was convincing, confusing, or missing from the real LLM agent run?
