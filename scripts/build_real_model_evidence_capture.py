import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REAL_MODEL_RUNBOOK_PATH = ROOT / "docs" / "real-model-runbook.json"
AGENT_OBSERVABILITY_PATH = ROOT / "docs" / "agent-observability.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
OUTPUT_MD_PATH = ROOT / "docs" / "real-model-evidence-capture.md"

CAPTURE_REQUIRED_FIELDS = [
    "trace_id",
    "provider",
    "model",
    "prompt_version",
    "dataset_id",
    "model_call_count",
    "tool_call_count",
    "distinct_tool_count",
    "used_strategy_tool",
    "used_required_report_tool",
    "final_report_attached",
    "total_tokens",
    "estimated_cost_usd",
    "latency_ms",
    "verification_passed",
    "redaction_status",
    "raw_prompt_logged",
]

CLAIMABLE_METRIC_DEFINITIONS = {
    "real_model_runs": "At least one accepted real OpenAI-compatible model run is captured.",
    "real_model_tool_calling_runs": "The accepted real model run used multiple whitelisted tools.",
    "real_model_verified_reports": "The accepted real model run produced a verified report with attached evidence.",
    "real_model_cost_tracked_runs": "The accepted real model run recorded token, cost, and latency telemetry.",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and value > 0


def _is_non_negative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and value >= 0


def evaluate_real_model_run(run: dict[str, Any], prompt_version: str) -> dict[str, Any]:
    failures = []
    for field in CAPTURE_REQUIRED_FIELDS:
        if field not in run:
            failures.append(f"missing:{field}")

    if run.get("provider") in ("", None, "disabled"):
        failures.append("provider must identify a real OpenAI-compatible provider")
    if run.get("model") in ("", None, "fake-model"):
        failures.append("model must identify the real model used")
    if run.get("prompt_version") != prompt_version:
        failures.append("prompt_version must match the current agent prompt version")
    if run.get("dataset_id") in ("", None):
        failures.append("dataset_id is required")
    if not isinstance(run.get("trace_id"), str) or not run.get("trace_id"):
        failures.append("trace_id is required")
    if not _is_positive_int(run.get("model_call_count")) or run.get("model_call_count", 0) < 2:
        failures.append("model_call_count must be at least 2")
    if not _is_positive_int(run.get("tool_call_count")) or run.get("tool_call_count", 0) < 3:
        failures.append("tool_call_count must be at least 3")
    if not _is_positive_int(run.get("distinct_tool_count")) or run.get("distinct_tool_count", 0) < 3:
        failures.append("distinct_tool_count must be at least 3")
    if run.get("used_strategy_tool") is not True:
        failures.append("used_strategy_tool must be true")
    if run.get("used_required_report_tool") is not True:
        failures.append("used_required_report_tool must be true")
    if run.get("final_report_attached") is not True:
        failures.append("final_report_attached must be true")
    if not _is_positive_int(run.get("total_tokens")):
        failures.append("total_tokens must be positive")
    if not _is_non_negative_number(run.get("estimated_cost_usd")):
        failures.append("estimated_cost_usd must be non-negative")
    if not _is_non_negative_number(run.get("latency_ms")):
        failures.append("latency_ms must be non-negative")
    if run.get("verification_passed") is not True:
        failures.append("verification_passed must be true")
    if run.get("redaction_status") not in {"redacted", "passed"}:
        failures.append("redaction_status must be redacted or passed")
    if run.get("raw_prompt_logged") is not False:
        failures.append("raw_prompt_logged must be false")

    public_summary = {
        "trace_id": run.get("trace_id"),
        "provider": run.get("provider"),
        "model": run.get("model"),
        "prompt_version": run.get("prompt_version"),
        "dataset_id": run.get("dataset_id"),
        "model_call_count": run.get("model_call_count"),
        "tool_call_count": run.get("tool_call_count"),
        "distinct_tool_count": run.get("distinct_tool_count"),
        "total_tokens": run.get("total_tokens"),
        "estimated_cost_usd": run.get("estimated_cost_usd"),
        "latency_ms": run.get("latency_ms"),
        "verification_passed": run.get("verification_passed"),
        "redaction_status": run.get("redaction_status"),
        "raw_prompt_logged": run.get("raw_prompt_logged"),
    }
    return {
        "accepted": not failures,
        "failures": failures,
        "public_summary": public_summary,
    }


def build_real_model_evidence_capture_payload(real_runs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    runbook = load_json(REAL_MODEL_RUNBOOK_PATH)
    observability = load_json(AGENT_OBSERVABILITY_PATH)
    runs = real_runs or []
    evaluations = [
        evaluate_real_model_run(run, prompt_version=runbook["prompt_version"])
        for run in runs
    ]
    accepted_runs = [
        evaluation["public_summary"]
        for evaluation in evaluations
        if evaluation["accepted"]
    ]
    rejected_runs = [
        {
            "trace_id": evaluation["public_summary"].get("trace_id"),
            "failures": evaluation["failures"],
        }
        for evaluation in evaluations
        if not evaluation["accepted"]
    ]
    accepted_count = len(accepted_runs)
    claimable_metrics = {
        "real_model_runs": {
            "claimable": accepted_count >= 1,
            "current_value": accepted_count,
            "minimum_before_claim": 1,
            "evidence": CLAIMABLE_METRIC_DEFINITIONS["real_model_runs"],
        },
        "real_model_tool_calling_runs": {
            "claimable": any(run["tool_call_count"] >= 3 and run["distinct_tool_count"] >= 3 for run in accepted_runs),
            "current_value": accepted_count,
            "minimum_before_claim": 1,
            "evidence": CLAIMABLE_METRIC_DEFINITIONS["real_model_tool_calling_runs"],
        },
        "real_model_verified_reports": {
            "claimable": any(run["verification_passed"] is True for run in accepted_runs),
            "current_value": accepted_count,
            "minimum_before_claim": 1,
            "evidence": CLAIMABLE_METRIC_DEFINITIONS["real_model_verified_reports"],
        },
        "real_model_cost_tracked_runs": {
            "claimable": any(
                run["total_tokens"] > 0
                and run["estimated_cost_usd"] >= 0
                and run["latency_ms"] >= 0
                for run in accepted_runs
            ),
            "current_value": accepted_count,
            "minimum_before_claim": 1,
            "evidence": CLAIMABLE_METRIC_DEFINITIONS["real_model_cost_tracked_runs"],
        },
    }
    blocked_claims = [
        metric
        for metric, details in claimable_metrics.items()
        if not details["claimable"]
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_real_model_evidence_capture.py",
        "purpose": (
            "Capture public-safe evidence from real OpenAI-compatible Data Quality Agent runs before any "
            "resume claim is upgraded from ready to completed."
        ),
        "current_real_model_runs": accepted_count,
        "mock_model_calls_available": observability["model_telemetry"]["model_call_count"],
        "runbook_evidence_field_count": runbook["evidence_field_count"],
        "capture_required_field_count": len(CAPTURE_REQUIRED_FIELDS),
        "capture_required_fields": CAPTURE_REQUIRED_FIELDS,
        "evaluated_run_count": len(runs),
        "accepted_real_model_run_count": accepted_count,
        "rejected_real_model_run_count": len(rejected_runs),
        "accepted_runs": accepted_runs,
        "rejected_runs": rejected_runs,
        "claimable_metric_count": len(claimable_metrics),
        "claimable_metrics": claimable_metrics,
        "blocked_outcome_claim_count": len(blocked_claims),
        "blocked_outcome_claims": blocked_claims,
        "resume_status": "real_model_evidence_gate_ready",
        "resume_safe_summary": (
            "Published a CI-verified real-model evidence capture gate requiring redacted trace, provider, model, "
            "prompt version, tool calls, token usage, estimated cost, latency, and report verification before "
            "claiming a real LLM agent run."
        ),
        "not_claimed": [
            "real OpenAI model run completed",
            "paid model benchmark results",
            "real model accuracy improvement",
            "production model traffic",
            "raw prompts published",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    fields = "\n".join(f"- `{field}`" for field in payload["capture_required_fields"])
    metrics = "\n".join(
        "| {metric} | {claimable} | {current_value} | {minimum_before_claim} | {evidence} |".format(
            metric=metric,
            claimable=details["claimable"],
            current_value=details["current_value"],
            minimum_before_claim=details["minimum_before_claim"],
            evidence=details["evidence"],
        )
        for metric, details in payload["claimable_metrics"].items()
    )
    accepted = "\n".join(
        f"- `{run['trace_id']}`: {run['model']} on `{run['dataset_id']}` with {run['tool_call_count']} tool calls"
        for run in payload["accepted_runs"]
    ) or "- None yet."
    rejected = "\n".join(
        f"- `{run['trace_id']}`: {', '.join(run['failures'])}"
        for run in payload["rejected_runs"]
    ) or "- None."
    blocked = "\n".join(f"- `{claim}`" for claim in payload["blocked_outcome_claims"]) or "- None."
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Real Model Evidence Capture

This generated artifact defines and verifies the public-safe capture format for real LLM agent runs. It keeps the current baseline honest until a redacted real run is available.

## Current Status

| Metric | Value |
| --- | ---: |
| Evaluated runs | {payload["evaluated_run_count"]} |
| Accepted real model runs | {payload["accepted_real_model_run_count"]} |
| Rejected real model runs | {payload["rejected_real_model_run_count"]} |
| Runbook evidence fields | {payload["runbook_evidence_field_count"]} |
| Capture required fields | {payload["capture_required_field_count"]} |
| Blocked outcome claims | {payload["blocked_outcome_claim_count"]} |

## Required Capture Fields

{fields}

## Claimable Metrics

| Metric | Claimable | Current value | Minimum before claim | Evidence rule |
| --- | --- | ---: | ---: | --- |
{metrics}

## Accepted Runs

{accepted}

## Rejected Runs

{rejected}

## Blocked Outcome Claims

{blocked}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_real_model_evidence_capture(
    payload: dict[str, Any],
    *,
    expected_current_real_model_runs: int = 0,
) -> dict[str, Any]:
    expected = {
        "current_real_model_runs": expected_current_real_model_runs,
        "runbook_evidence_field_count": 15,
        "capture_required_field_count": 17,
        "claimable_metric_count": 4,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if len(payload["capture_required_fields"]) != len(set(payload["capture_required_fields"])):
        raise AssertionError("capture required fields must be unique")
    for required in ("trace_id", "provider", "model", "tool_call_count", "total_tokens", "raw_prompt_logged"):
        if required not in payload["capture_required_fields"]:
            raise AssertionError(f"real model evidence capture missing {required}")
    if payload["accepted_real_model_run_count"] != expected_current_real_model_runs:
        raise AssertionError("accepted run count must match expected current real model runs")
    if payload["accepted_real_model_run_count"] == 0 and payload["blocked_outcome_claim_count"] != 4:
        raise AssertionError("zero-run baseline must block all real-model outcome claims")
    if payload["accepted_real_model_run_count"] > 0 and payload["blocked_outcome_claim_count"] != 0:
        raise AssertionError("accepted real run should unblock all real-model outcome claims")
    for run in payload["accepted_runs"]:
        if run["raw_prompt_logged"] is not False:
            raise AssertionError("accepted run must not expose raw prompts")
        if run["redaction_status"] not in {"redacted", "passed"}:
            raise AssertionError("accepted run must be redacted")
    not_claimed = {item.lower() for item in payload["not_claimed"]}
    for forbidden in ("real openai model run completed", "paid model benchmark results", "production model traffic"):
        if forbidden not in not_claimed:
            raise AssertionError(f"real model evidence capture must explicitly not claim {forbidden}")
    return {"real_model_evidence_capture_verified": True, **expected}


def main() -> None:
    payload = build_real_model_evidence_capture_payload()
    verify_real_model_evidence_capture(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
