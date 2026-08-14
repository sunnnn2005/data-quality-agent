import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_external_reviewer_evidence_gate import evaluate_issue

OUTPUT_JSON_PATH = ROOT / "docs" / "first-accepted-evidence-examples.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-accepted-evidence-examples.md"


def _issue(number: int, title: str, author: str, labels: list[str], body: str) -> dict[str, Any]:
    return {
        "number": number,
        "title": title,
        "url": f"https://github.com/sunnnn2005/data-quality-agent/issues/{number}",
        "author": {"login": author},
        "labels": [{"name": label} for label in labels],
        "body": body,
    }


ACCEPTED_BUSINESS_CASE_BODY = """## Business context

Support operations team reviewing a weekly SLA dashboard built from a ticket export.

## Data-quality problem

Duplicate ticket IDs and missing routing teams made escalation counts unreliable.

## Business impact

Support managers could undercount urgent tickets, spend about 2 hours manually reconciling the dashboard, and route follow-up work to the wrong owner.

## Fields involved

ticket_id, routing_team, priority, status

## Evidence from this project

The demo report's duplicate primary-key finding, missing-values finding, and data-engineering owner handoff match this workflow.

## Permission

- [x] This can be counted as anonymized public business-case feedback.
- [x] This can be counted as an anonymized business-impact signal.
"""


ACCEPTED_REAL_MODEL_RUN_BODY = """## Run path

- [x] Built-in dataset: `python scripts/capture_real_model_run.py --dataset-id orders_daily --write`
- [ ] Business CSV replay: `python scripts/capture_real_model_run.py --csv-path sample.csv --dataset-name "Replay Dataset" --owner reviewer --primary-key id --expected-columns "id,status,amount" --description "Anonymized business replay dataset" --write`
- [ ] I reviewed the runbook but did not execute a model call

## Environment

- Model provider: OpenAI-compatible
- Model name: gpt-4o-mini
- API route used: /datasets/orders_daily/agent-report
- Dataset id or anonymized dataset name: orders_daily

## Redacted telemetry

- Trace id: run_example_001
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
- Latency ms: 2430

## Tool evidence

- [x] `profile_dataset`
- [x] `select_quality_strategy`
- [x] `run_quality_checks`
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

## Notes

The model selected strategy, profiling, checks, and report-building tools before returning the verified final report.
"""


REJECTED_SELF_AUTHORED_BODY = ACCEPTED_BUSINESS_CASE_BODY


REJECTED_DOCS_ONLY_BODY = """## Replay path

- [ ] Sanitized CSV upload: `POST /business-data/agent-report`
- [ ] Read-only PostgreSQL table: `POST /postgres/support-tickets/agent-report`
- [ ] Local Docker Compose support-ticket replay
- [x] Repository/docs review before trying my own data

## Data source type

Anonymized business CSV export.

## Dataset shape

Row count: 1,240; columns: 8; primary key: ticket_id.

## Agent run summary

- Command or endpoint used: docs only
- Report status: not run
- Finding count: unknown
- Selected tools shown in the agent trace: none

## What did it catch or miss?

I did not run the agent, so this should not count as confirmed replay evidence.

## Permission boundary

- [x] This issue contains no customer names, emails, addresses, tokens, secrets, or raw production rows.
- [x] This can be counted as a confirmed anonymized replay.
- [x] This can be counted as external feedback.
"""


def build_first_accepted_evidence_examples() -> dict[str, Any]:
    examples = [
        {
            "id": "accepted_business_case",
            "purpose": "Unlocks one anonymized business-case feedback item after a non-owner reviewer maps a real workflow problem to project evidence.",
            "issue": _issue(901, "Business case: support SLA dashboard", "external-reviewer", ["business-case"], ACCEPTED_BUSINESS_CASE_BODY),
        },
        {
            "id": "accepted_real_model_run",
            "purpose": "Unlocks one accepted real-model run after a non-owner reviewer captures redacted model, tool, token, cost, latency, and verification evidence.",
            "issue": _issue(902, "Real model run: orders_daily", "external-reviewer", ["real-model-run"], ACCEPTED_REAL_MODEL_RUN_BODY),
        },
        {
            "id": "rejected_self_authored_business_case",
            "purpose": "Shows why owner-authored evidence cannot count as external feedback or business impact.",
            "issue": _issue(903, "Business case: owner example", "sunnnn2005", ["business-case"], REJECTED_SELF_AUTHORED_BODY),
        },
        {
            "id": "rejected_docs_only_replay",
            "purpose": "Shows why reading docs is useful feedback but not enough for confirmed business-data replay evidence.",
            "issue": _issue(904, "Business replay: docs only", "external-reviewer", ["business-data-replay", "confirmed-user"], REJECTED_DOCS_ONLY_BODY),
        },
    ]
    evaluated_examples = []
    for example in examples:
        evaluation = evaluate_issue(example["issue"])
        evaluated_examples.append(
            {
                "id": example["id"],
                "purpose": example["purpose"],
                "accepted": evaluation["accepted"],
                "evidence_type": evaluation["evidence_type"],
                "counts_toward": evaluation["counts_toward"],
                "failure_reasons": evaluation["failure_reasons"],
                "author": evaluation["author"],
                "labels": evaluation["labels"],
            }
        )

    accepted = [example for example in evaluated_examples if example["accepted"]]
    rejected = [example for example in evaluated_examples if not example["accepted"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_accepted_evidence_examples.py",
        "purpose": (
            "Show reviewers exactly what the first acceptable public evidence issue looks like, and what the gate rejects, "
            "without increasing real resume outcome counts."
        ),
        "example_count": len(evaluated_examples),
        "accepted_example_count": len(accepted),
        "rejected_example_count": len(rejected),
        "examples": evaluated_examples,
        "real_public_issue_required": True,
        "resume_claim_allowed_now": False,
        "resume_safe_summary": (
            "Published gate-tested examples for the first acceptable business-case and real-model-run evidence, plus "
            "rejected self-authored and docs-only examples, while keeping real outcome counts unchanged."
        ),
        "not_claimed": [
            "Synthetic examples are not counted as users, feedback, stars, pilots, or accepted real-model runs.",
            "Resume outcome metrics change only after a real non-owner public GitHub issue passes the evidence gate.",
            "Owner-authored evidence and docs-only reviews remain blocked from outcome claims.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {id} | {evidence_type} | {accepted} | {metrics} | {reasons} |".format(
            id=example["id"],
            evidence_type=example["evidence_type"],
            accepted=example["accepted"],
            metrics=", ".join(example["counts_toward"]) or "-",
            reasons=", ".join(example["failure_reasons"]) or "-",
        )
        for example in payload["examples"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First Accepted Evidence Examples

This generated artifact gives external reviewers concrete examples of evidence that passes or fails the public evidence gate.

## Summary

| Metric | Value |
| --- | ---: |
| Examples | {payload["example_count"]} |
| Accepted examples | {payload["accepted_example_count"]} |
| Rejected examples | {payload["rejected_example_count"]} |
| Real public issue required | {payload["real_public_issue_required"]} |
| Resume claim allowed now | {payload["resume_claim_allowed_now"]} |

## Gate-Tested Examples

| Example | Evidence Type | Accepted | Counts Toward | Failure Reasons |
| --- | --- | --- | --- | --- |
{rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_first_accepted_evidence_examples(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["example_count"] != 4:
        raise AssertionError("first accepted evidence examples must include four examples")
    if payload["accepted_example_count"] != 2:
        raise AssertionError("first accepted evidence examples must include two passing examples")
    if payload["rejected_example_count"] != 2:
        raise AssertionError("first accepted evidence examples must include two rejected examples")
    if payload["resume_claim_allowed_now"] is not False:
        raise AssertionError("examples must not unlock resume claims by themselves")
    expected = {
        "accepted_business_case": ["business_case_feedback_items"],
        "accepted_real_model_run": ["accepted_real_model_runs"],
    }
    examples = {example["id"]: example for example in payload["examples"]}
    for example_id, counts_toward in expected.items():
        if examples[example_id]["counts_toward"] != counts_toward:
            raise AssertionError(f"{example_id} must count toward {counts_toward}")
    if "self-authored issue" not in examples["rejected_self_authored_business_case"]["failure_reasons"]:
        raise AssertionError("self-authored example must be rejected")
    if "docs-only review is not a confirmed business-data replay" not in examples["rejected_docs_only_replay"]["failure_reasons"]:
        raise AssertionError("docs-only replay example must be rejected")
    return {"first_accepted_evidence_examples_verified": True}


def main() -> None:
    payload = build_first_accepted_evidence_examples()
    verify_first_accepted_evidence_examples(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
