import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.data import DATASETS, load_dataset
from app.evals import load_scenarios, run_all_evals
from app.tool_agent import DataQualityToolbox

OUTPUT_JSON_PATH = ROOT / "docs" / "eval-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "eval-summary.md"
REQUIRED_AGENT_TOOLS = [
    "get_dataset_contract",
    "profile_dataset",
    "select_quality_strategy",
    "retrieve_dataset_memory",
    "inspect_primary_key_integrity",
    "analyze_numeric_distribution",
    "run_quality_checks",
    "retrieve_business_rules",
    "build_quality_report",
]


def build_tool_planning_coverage() -> dict[str, Any]:
    toolbox = DataQualityToolbox(DATASETS["orders_daily"], load_dataset("orders_daily"))
    tool_names = [schema["function"]["name"] for schema in toolbox.schemas()]
    scenario_rows = []

    for scenario in load_scenarios():
        scenario_toolbox = DataQualityToolbox(DATASETS[scenario.dataset_id], load_dataset(scenario.dataset_id))
        strategy = scenario_toolbox.dispatch("select_quality_strategy", {})
        recommended_checks = set(strategy.get("recommended_checks", []))
        expected_findings = set(scenario.expected_findings)
        matched = sorted(recommended_checks & expected_findings)
        scenario_rows.append(
            {
                "scenario_id": scenario.id,
                "dataset_id": scenario.dataset_id,
                "expected_findings": sorted(expected_findings),
                "recommended_checks": sorted(recommended_checks),
                "matched_expected_findings": matched,
                "recommendation_recall": round(len(matched) / len(expected_findings), 3)
                if expected_findings
                else 1.0,
            }
        )

    return {
        "available_tool_count": len(tool_names),
        "tool_names": tool_names,
        "required_tools_present": all(tool in tool_names for tool in REQUIRED_AGENT_TOOLS),
        "required_tools": REQUIRED_AGENT_TOOLS,
        "scenario_strategy_recommendation_recall": round(
            sum(row["recommendation_recall"] for row in scenario_rows) / len(scenario_rows),
            3,
        ),
        "scenario_strategy_rows": scenario_rows,
    }


def build_eval_summary_payload() -> dict[str, Any]:
    results = run_all_evals()
    by_name = {item["name"]: item for item in results["results"]}
    deterministic = by_name["deterministic"]
    tool_agent = by_name["tool_agent"]
    tool_planning = build_tool_planning_coverage()
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
        "tool_planning_coverage": tool_planning,
        "resume_safe_summary": (
            f"Built a {results['scenario_count']}-scenario eval harness measuring status accuracy, finding recall, "
            "evidence support, fallback behavior, report-tool usage, report attachment, latency, and "
            f"{tool_planning['available_tool_count']}-tool planning coverage."
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
    tool_planning = payload["tool_planning_coverage"]
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    tools = ", ".join(f"`{tool}`" for tool in tool_planning["tool_names"])
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
| Available agent tools | {tool_planning["available_tool_count"]} |
| Required tools present | {tool_planning["required_tools_present"]} |
| Strategy recommendation recall | {tool_planning["scenario_strategy_recommendation_recall"]} |

## Tool Planning Coverage

Allowed tools: {tools}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_eval_summary(payload: dict[str, Any]) -> dict[str, Any]:
    deterministic = payload["deterministic_baseline"]
    tool_agent = payload["tool_agent_disabled_fallback"]
    tool_planning = payload["tool_planning_coverage"]
    expected = {
        "scenario_count": 14,
        "deterministic_finding_recall": 1.0,
        "deterministic_evidence_support_rate": 1.0,
        "tool_agent_fallback_success_rate": 1.0,
        "available_tool_count": 9,
        "strategy_recommendation_recall_floor": 0.75,
    }
    if payload["scenario_count"] != expected["scenario_count"]:
        raise AssertionError(
            f"scenario_count expected {expected['scenario_count']}, got {payload['scenario_count']!r}"
        )
    if deterministic["finding_recall"] != expected["deterministic_finding_recall"]:
        raise AssertionError("deterministic finding recall must stay at 1.0 for the known eval set")
    if deterministic["evidence_support_rate"] != expected["deterministic_evidence_support_rate"]:
        raise AssertionError("deterministic evidence support must stay at 1.0 for the known eval set")
    if tool_agent["fallback_success_rate"] != expected["tool_agent_fallback_success_rate"]:
        raise AssertionError("tool-agent disabled fallback must remain successful without a model key")
    if tool_planning["available_tool_count"] != expected["available_tool_count"]:
        raise AssertionError("eval summary must cover all allowed agent tools")
    if tool_planning["required_tools_present"] is not True:
        raise AssertionError("eval summary must verify required agent tools are present")
    for tool in (
        "retrieve_dataset_memory",
        "inspect_primary_key_integrity",
        "analyze_numeric_distribution",
        "retrieve_business_rules",
        "build_quality_report",
    ):
        if tool not in tool_planning["tool_names"]:
            raise AssertionError(f"eval summary missing required tool: {tool}")
    if (
        tool_planning["scenario_strategy_recommendation_recall"]
        < expected["strategy_recommendation_recall_floor"]
    ):
        raise AssertionError("strategy recommendation recall must stay above the eval threshold")
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
