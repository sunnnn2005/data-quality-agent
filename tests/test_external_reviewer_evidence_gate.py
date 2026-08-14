from scripts.build_external_reviewer_evidence_gate import (
    build_external_reviewer_evidence_gate,
    collect_public_reviewer_issues,
    evaluate_issue,
    render_markdown,
    verify_external_reviewer_evidence_gate,
)
import scripts.build_external_reviewer_evidence_gate as evidence_gate


VALID_EXTERNAL_RUN_BODY = """## Reviewer role

- Role or background: student developer
- Relationship to the project owner, if any: none

## Path tried

- [x] Public demo review
- [ ] GHCR container smoke run
- [ ] Docker Compose PostgreSQL replay
- [ ] I reviewed the docs but did not run it

## Environment

- OS: macOS
- Browser: Chrome
- Docker version, if used:
- Python version, if used:

## Commands or URLs used

```bash
https://sunnnn2005.github.io/data-quality-agent/
```

## Observed result

- Health endpoint result: ok
- Report or page opened: support-ticket case study
- Agent/report status: FAIL
- Finding or output inspected: duplicate ticket IDs

## Usefulness score

- [x] 4 - useful with small changes

## Main feedback

The support-ticket example makes the data-quality workflow clear.

## Permission to count publicly

- [x] This issue contains no private business data, secrets, customer names, emails, addresses, or raw production rows.
- [x] This can be counted as public external run evidence.
- [x] This can be counted as external feedback.
- [x] This can be counted as a reproducible local replay, if I ran the container or Docker Compose path.
- [ ] Do not quote my name, organization, or private context.
"""


def issue(body: str, author: str = "external-reviewer", labels: list[str] | None = None):
    return {
        "number": 31,
        "title": "External run: public demo",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/31",
        "author": {"login": author},
        "labels": [{"name": name} for name in (labels or ["feedback", "pilot", "reproducible"])],
        "body": body,
    }


VALID_AI_ENGINEER_REVIEW_BODY = """## Reviewer context

AI engineer with data tooling experience.

## What did you inspect?

- [x] README and AI Engineer readiness docs
- [x] LLM value comparison: `docs/llm-value-comparison.md`
- [x] app/tool_agent.py
- [x] app/postgres_adapter.py

## Strongest AI Engineer signals

The project shows tool calling, adaptive strategy selection, evidence-backed reports, read-only data access, and telemetry.

## Missing or weak AI Engineer signals

It still needs one captured real-model run and a larger labeled eval set.

## Permission to count publicly

- [x] This issue contains no private business data, secrets, customer names, emails, addresses, or raw production rows.
- [x] You may count this public issue as external AI Engineer project feedback.
- [ ] Do not count this issue publicly.
"""


VALID_BUSINESS_CASE_BODY = """## Business context

- Industry or team: support operations
- Workflow affected: weekly SLA dashboard
- Data source type: support ticket export

## Data-quality problem

Duplicate ticket IDs and missing routing fields made the dashboard undercount escalations.

## Business impact

- Who would be affected if this issue reached production? support managers and customer success leads
- What decision, dashboard, SLA, customer workflow, or revenue process could be affected? SLA escalation dashboard
- Approximate time spent investigating manually: 2 hours
- Approximate rows, records, or entities affected, if known: 1,200 tickets

## Fields involved

ticket_id, routing_team, amount

## Evidence from this project

- Which finding matched the real problem? duplicate ticket IDs
- Which root-cause hypothesis looked plausible? upstream export merge introduced duplicate keys
- Which recommendation or owner handoff was useful? assign data engineering owner to dedupe key logic
- What evidence was missing or wrong? none for this sample

## Tried path

- [x] Public demo page
- [ ] CSV upload endpoint
- [ ] PostgreSQL Docker Compose demo
- [ ] LLM tool-calling route
- [ ] I only reviewed the repository/docs

## Outcome

- [x] The agent found a relevant issue.
- [x] The deterministic checks found a relevant issue.
- [ ] The report missed an important business rule.
- [x] The suggested owner handoff/action was useful.
- [ ] I would need another integration before using this pattern.
- [x] This could reduce manual investigation time.
- [x] This could prevent a bad dashboard, report, or operational decision.
- [x] This is close enough for a small pilot with anonymized data.

## Permission

- [x] This can be counted as anonymized public business-case feedback.
- [x] This can be counted as an anonymized business-impact signal.
- [x] Do not quote my organization, name, or raw data.
"""


VALID_BUSINESS_DATA_REPLAY_BODY = """## Replay path

- [x] Sanitized CSV upload: `POST /business-data/agent-report`
- [ ] Read-only PostgreSQL table: `POST /postgres/support-tickets/agent-report`
- [ ] Local Docker Compose support-ticket replay
- [ ] Repository/docs review before trying my own data

## Data source type

- [x] Anonymized business CSV export
- [ ] Synthetic-but-business-shaped CSV
- [ ] Read-only PostgreSQL table
- [ ] Local seeded PostgreSQL demo table
- [ ] Other:

## Dataset shape

- Row count or table size: 1,240
- Column count: 8
- Primary key used: ticket_id
- Non-sensitive field names involved: ticket_id, status, priority, routing_team

## Agent run summary

- Command or endpoint used: POST /business-data/agent-report
- Report status: FAIL
- Finding count: 4
- Selected tools shown in the agent trace: select_quality_strategy, run_quality_checks, build_quality_report
- Did the agent call `build_quality_report`? yes

## Usefulness rating

- [x] 4 - useful with small changes

## What did it catch or miss?

It caught duplicate ticket IDs and missing routing fields that matched an anonymized support-operations export.

## Permission boundary

- [x] This issue contains no customer names, emails, addresses, tokens, secrets, or raw production rows.
- [x] This can be counted as a confirmed anonymized replay.
- [x] This can be counted as external feedback.
- [ ] Do not quote my organization, name, or raw data.

## Optional redacted output summary

Status FAIL, quality score 61, checks duplicate_primary_key and missing_values.
"""


VALID_REAL_MODEL_RUN_BODY = """## Run path

- [x] Built-in dataset: `python scripts/capture_real_model_run.py --dataset-id orders_daily --write`
- [ ] Business CSV replay: `python scripts/capture_real_model_run.py --csv-path sample.csv --dataset-name "Replay Dataset" --owner reviewer --primary-key id --expected-columns "id,status,amount" --description "Anonymized business replay dataset" --write`
- [ ] Read-only PostgreSQL route inspected before capture
- [ ] I reviewed the runbook but did not execute a model call

## Environment

- Model provider: OpenAI-compatible
- Model name: gpt-4o-mini
- API route used: /datasets/orders_daily/agent-report
- Dataset id or anonymized dataset name: orders_daily
- Operating system: macOS
- Python version: 3.12

## Redacted telemetry

Paste only safe values from `docs/real-model-evidence-capture.json`.

- Trace id: run_abc123
- Prompt version: tool-agent-v3
- Model call count: 3
- Tool call count: 5
- Distinct tool count: 4
- Used strategy tool: true
- Used required report tool: true
- Final report attached: true
- Verification passed: true
- Total tokens: 1842
- Estimated cost USD: 0.0011
- Latency ms: 2410

## Tool evidence

Which tools did the model select before the final report?

- [ ] `get_dataset_contract`
- [x] `profile_dataset`
- [x] `select_quality_strategy`
- [ ] `retrieve_dataset_memory`
- [ ] `inspect_primary_key_integrity`
- [ ] `analyze_numeric_distribution`
- [x] `run_quality_checks`
- [ ] `retrieve_business_rules`
- [x] `build_quality_report`

## Outcome

- [x] The model selected more than one whitelisted tool.
- [x] Tool results changed or informed the final report.
- [x] The final answer attached a verified structured quality report.
- [x] Token, cost, and latency telemetry were captured.
- [x] The run is useful evidence for AI Engineer Intern readiness.

## Permission and privacy

- [x] This issue contains no provider credentials, raw prompts, customer names, emails, addresses, secrets, tokens, or raw production rows.
- [x] You may count this public issue as accepted real-model run evidence if it passes the repository evidence gate.
- [ ] Do not count this issue publicly.

## Notes

The trace showed the model selecting strategy, profiling data, running checks, and attaching the verified final report.
"""


def test_external_reviewer_evidence_gate_starts_from_zero_without_fake_claims():
    payload = build_external_reviewer_evidence_gate()
    verification = verify_external_reviewer_evidence_gate(payload)
    markdown = render_markdown(payload)

    assert verification["external_reviewer_evidence_gate_verified"] is True
    assert payload["issue_collection"]["source"] in {"github_issues", "github_public_api", "provided_issues"}
    assert payload["issue_collection"]["collected_issue_count"] == payload["evaluated_issue_count"]
    assert payload["accepted_issue_count"] == 0
    assert payload["accepted_counts"]["external_feedback_items"] == 0
    assert payload["accepted_counts"]["confirmed_external_users"] == 0
    assert payload["accepted_counts"]["ai_engineer_review_items"] == 0
    assert payload["accepted_counts"]["accepted_real_model_runs"] == 0
    assert payload["linked_outreach_queue_count"] == 3
    assert "No accepted external reviewer issue exists yet." in payload["not_claimed"]
    assert "No accepted real-model run count is increased by runbook-only or self-authored issues." in payload["not_claimed"]
    assert "External Reviewer Evidence Gate" in markdown


def test_external_reviewer_evidence_gate_accepts_complete_public_run_issue():
    payload = build_external_reviewer_evidence_gate(issues=[issue(VALID_EXTERNAL_RUN_BODY)])
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["failure_reasons"] == []
    assert evaluation["counts_toward"] == [
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    ]
    assert payload["accepted_issue_count"] == 1
    assert payload["accepted_counts"]["confirmed_external_users"] == 1
    assert payload["accepted_counts"]["external_feedback_items"] == 1
    assert payload["accepted_counts"]["reproducible_feedback_items"] == 1


def test_external_reviewer_evidence_gate_accepts_ai_engineer_review_issue():
    payload = build_external_reviewer_evidence_gate(
        issues=[issue(VALID_AI_ENGINEER_REVIEW_BODY, labels=["ai-engineer-review"])]
    )
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["evidence_type"] == "ai_engineer_review"
    assert evaluation["counts_toward"] == ["ai_engineer_review_items"]
    assert payload["accepted_counts"]["ai_engineer_review_items"] == 1


def test_external_reviewer_evidence_gate_accepts_business_case_with_impact_summary():
    payload = build_external_reviewer_evidence_gate(
        issues=[issue(VALID_BUSINESS_CASE_BODY, labels=["business-case"])]
    )
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["evidence_type"] == "business_case_review"
    assert evaluation["counts_toward"] == ["business_case_feedback_items"]
    assert payload["accepted_counts"]["business_case_feedback_items"] == 1
    assert "weekly SLA dashboard" in evaluation["extracted_business_impact"]["business_context"]
    assert "2 hours" in evaluation["extracted_business_impact"]["business_impact"]
    assert "duplicate ticket IDs" in evaluation["extracted_business_impact"]["project_evidence_mapping"]


def test_external_reviewer_evidence_gate_accepts_business_data_replay_issue():
    payload = build_external_reviewer_evidence_gate(
        issues=[issue(VALID_BUSINESS_DATA_REPLAY_BODY, labels=["feedback", "confirmed-user", "business-data-replay"])]
    )
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["evidence_type"] == "business_data_replay"
    assert evaluation["counts_toward"] == ["confirmed_external_users", "external_feedback_items"]
    assert payload["accepted_counts"]["confirmed_external_users"] == 1
    assert payload["accepted_counts"]["external_feedback_items"] == 1


def test_external_reviewer_evidence_gate_accepts_real_model_run_issue():
    payload = build_external_reviewer_evidence_gate(
        issues=[issue(VALID_REAL_MODEL_RUN_BODY, labels=["real-model-run", "ai-engineer-review"])]
    )
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["evidence_type"] == "real_model_run_review"
    assert evaluation["counts_toward"] == ["accepted_real_model_runs"]
    assert payload["accepted_counts"]["accepted_real_model_runs"] == 1


def test_external_reviewer_evidence_gate_rejects_self_authored_missing_permission_or_sensitive_issue():
    missing_permission_body = VALID_EXTERNAL_RUN_BODY.replace(
        "- [x] This can be counted as public external run evidence.",
        "- [ ] This can be counted as public external run evidence.",
    )
    self_authored = evaluate_issue(issue(VALID_EXTERNAL_RUN_BODY, author="sunnnn2005"))
    missing_permission = evaluate_issue(issue(missing_permission_body))
    sensitive = evaluate_issue(issue(VALID_EXTERNAL_RUN_BODY + "\npassword: example"))
    opted_out = evaluate_issue(
        issue(
            VALID_AI_ENGINEER_REVIEW_BODY.replace("- [ ] Do not count this issue publicly.", "- [x] Do not count this issue publicly."),
            labels=["ai-engineer-review"],
        )
    )
    missing_value_comparison = evaluate_issue(
        issue(
            VALID_AI_ENGINEER_REVIEW_BODY.replace(
                "- [x] LLM value comparison: `docs/llm-value-comparison.md`\n",
                "",
            ),
            labels=["ai-engineer-review"],
        )
    )
    business_case_missing_impact_permission = evaluate_issue(
        issue(
            VALID_BUSINESS_CASE_BODY.replace(
                "- [x] This can be counted as an anonymized business-impact signal.",
                "- [ ] This can be counted as an anonymized business-impact signal.",
            ),
            labels=["business-case"],
        )
    )
    docs_only_replay = evaluate_issue(
        issue(
            VALID_BUSINESS_DATA_REPLAY_BODY.replace(
                "- [ ] Repository/docs review before trying my own data",
                "- [x] Repository/docs review before trying my own data",
            ),
            labels=["feedback", "confirmed-user", "business-data-replay"],
        )
    )
    replay_missing_permission = evaluate_issue(
        issue(
            VALID_BUSINESS_DATA_REPLAY_BODY.replace(
                "- [x] This can be counted as a confirmed anonymized replay.",
                "- [ ] This can be counted as a confirmed anonymized replay.",
            ),
            labels=["feedback", "confirmed-user", "business-data-replay"],
        )
    )
    real_model_missing_telemetry = evaluate_issue(
        issue(
            VALID_REAL_MODEL_RUN_BODY.replace("- Total tokens: 1842\n", ""),
            labels=["real-model-run", "ai-engineer-review"],
        )
    )
    real_model_docs_only = evaluate_issue(
        issue(
            VALID_REAL_MODEL_RUN_BODY.replace(
                "- [ ] I reviewed the runbook but did not execute a model call",
                "- [x] I reviewed the runbook but did not execute a model call",
            ),
            labels=["real-model-run", "ai-engineer-review"],
        )
    )
    real_model_missing_tool_evidence = evaluate_issue(
        issue(
            VALID_REAL_MODEL_RUN_BODY.replace("- [x] `run_quality_checks`", "- [ ] `run_quality_checks`")
            .replace("- [x] `build_quality_report`", "- [ ] `build_quality_report`")
            .replace("- [x] `profile_dataset`", "- [ ] `profile_dataset`"),
            labels=["real-model-run", "ai-engineer-review"],
        )
    )

    assert self_authored["accepted"] is False
    assert "self-authored issue" in self_authored["failure_reasons"]
    assert missing_permission["accepted"] is False
    assert "missing public external run permission" in missing_permission["failure_reasons"]
    assert sensitive["accepted"] is False
    assert "contains sensitive-data risk terms" in sensitive["failure_reasons"]
    assert opted_out["accepted"] is False
    assert "reviewer opted out of public counting" in opted_out["failure_reasons"]
    assert missing_value_comparison["accepted"] is False
    assert "missing LLM value comparison inspection" in missing_value_comparison["failure_reasons"]
    assert business_case_missing_impact_permission["accepted"] is False
    assert "missing business-impact counting permission" in business_case_missing_impact_permission["failure_reasons"]
    assert docs_only_replay["accepted"] is False
    assert "docs-only review is not a confirmed business-data replay" in docs_only_replay["failure_reasons"]
    assert replay_missing_permission["accepted"] is False
    assert "missing confirmed anonymized replay permission" in replay_missing_permission["failure_reasons"]
    assert real_model_missing_telemetry["accepted"] is False
    assert "missing real-model telemetry field: Total tokens:" in real_model_missing_telemetry["failure_reasons"]
    assert real_model_docs_only["accepted"] is False
    assert "runbook-only review is not a real model run" in real_model_docs_only["failure_reasons"]
    assert real_model_missing_tool_evidence["accepted"] is False
    assert "real-model run must show at least two selected whitelisted tools" in real_model_missing_tool_evidence["failure_reasons"]


def test_external_reviewer_evidence_gate_falls_back_to_public_api_when_gh_auth_fails(monkeypatch):
    def fake_run(*args, **kwargs):
        raise evidence_gate.subprocess.CalledProcessError(returncode=1, cmd=args[0])

    def fake_public_api(label):
        if label != "feedback":
            return []
        return [issue(VALID_EXTERNAL_RUN_BODY)]

    monkeypatch.setattr(evidence_gate.subprocess, "run", fake_run)
    monkeypatch.setattr(evidence_gate, "_collect_public_issues_by_label", fake_public_api)

    issues, collection = collect_public_reviewer_issues()

    assert collection["source"] == "github_public_api"
    assert collection["error_count"] == 0
    assert collection["collected_issue_count"] == 1
    assert issues[0]["number"] == 31
