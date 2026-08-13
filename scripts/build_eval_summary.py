import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.evals import run_all_evals

OUTPUT_JSON_PATH = ROOT / "docs" / "eval-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "eval-summary.md"


def build_eval_summary_payload() -> dict[str, Any]:
    results = run_all_evals()
    by_name = {item["name"]: item for item in results["results"]}
    deterministic = by_name["deterministic"]
    tool_agent = by_name["tool_agent"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_eval_summary.py",
        "scenario_count": results["scenario_count"],
        "deterministic_baseline": {
            "status_accuracy": deterministic["status_accuracy"],
            "finding_recall": deterministic["finding_recall"],
            "evidence_support_rate": deterministic["evidence_support_rate"],
            "average_latency_ms": deterministic["average_latency_ms"],
        },
        "tool_agent_disabled_fallback": {
            "status_accuracy": tool_agent["status_accuracy"],
            "fallback_success_rate": tool_agent["fallback_success_rate"],
            "required_report_tool_rate": tool_agent["required_report_tool_rate"],
            "final_report_attachment_rate": tool_agent["final_report_attachment_rate"],
            "average_latency_ms": tool_agent["average_latency_ms"],
        },
        "resume_safe_summary": (
            f"Built a {results['scenario_count']}-scenario eval harness measuring status accuracy, finding recall, "
            "evidence support, fallback behavior, report-tool usage, report attachment, and latency."
        ),
        "not_claimed": [
            "paid model benchmark results",
            "production traffic evaluation",
            "external human-labeled evaluation set",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    deterministic = payload["deterministic_baseline"]
    tool_agent = payload["tool_agent_disabled_fallback"]
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Evaluation Summary

This generated artifact summarizes the local agent evaluation harness. It is intentionally conservative: default CI runs without paid model credentials, so tool-agent results only claim disabled fallback behavior.

## Scenario Coverage

| Metric | Value |
| --- | ---: |
| Eval scenarios | {payload["scenario_count"]} |
| Deterministic status accuracy | {deterministic["status_accuracy"]} |
| Deterministic finding recall | {deterministic["finding_recall"]} |
| Deterministic evidence support rate | {deterministic["evidence_support_rate"]} |
| Tool-agent disabled fallback success | {tool_agent["fallback_success_rate"]} |
| Tool-agent required report-tool rate without model key | {tool_agent["required_report_tool_rate"]} |

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_eval_summary(payload: dict[str, Any]) -> dict[str, Any]:
    deterministic = payload["deterministic_baseline"]
    tool_agent = payload["tool_agent_disabled_fallback"]
    expected = {
        "scenario_count": 3,
        "deterministic_finding_recall": 1.0,
        "deterministic_evidence_support_rate": 1.0,
        "tool_agent_fallback_success_rate": 1.0,
    }
    if payload["scenario_count"] != expected["scenario_count"]:
        raise AssertionError(f"scenario_count expected 3, got {payload['scenario_count']!r}")
    if deterministic["finding_recall"] != expected["deterministic_finding_recall"]:
        raise AssertionError("deterministic finding recall must stay at 1.0 for the known eval set")
    if deterministic["evidence_support_rate"] != expected["deterministic_evidence_support_rate"]:
        raise AssertionError("deterministic evidence support must stay at 1.0 for the known eval set")
    if tool_agent["fallback_success_rate"] != expected["tool_agent_fallback_success_rate"]:
        raise AssertionError("tool-agent disabled fallback must remain successful without a model key")
    for forbidden in ("users", "customers", "production traffic"):
        if forbidden in payload["resume_safe_summary"].lower():
            raise AssertionError(f"eval summary must not claim {forbidden}")
    return {"eval_summary_verified": True, **expected}


def main() -> None:
    payload = build_eval_summary_payload()
    verify_eval_summary(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
