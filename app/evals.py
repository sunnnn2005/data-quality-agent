import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.models import AgentRunReport, QualityReport
from app.tool_agent import LLMDataQualityAgent


DEFAULT_SCENARIOS = Path(__file__).resolve().parents[1] / "evals" / "scenarios.jsonl"


@dataclass(frozen=True)
class EvalScenario:
    id: str
    dataset_id: str
    expected_status: str
    expected_findings: list[str]
    expected_report_tool: bool = False


def load_scenarios(path: Path = DEFAULT_SCENARIOS) -> list[EvalScenario]:
    scenarios: list[EvalScenario] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        scenarios.append(
            EvalScenario(
                id=payload["id"],
                dataset_id=payload["dataset_id"],
                expected_status=payload["expected_status"],
                expected_findings=list(payload["expected_findings"]),
                expected_report_tool=bool(payload.get("expected_report_tool", False)),
            )
        )
    return scenarios


def evaluate_deterministic(scenarios: list[EvalScenario] | None = None) -> dict[str, Any]:
    selected = scenarios or load_scenarios()
    agent = DataQualityAgent()
    rows = []

    for scenario in selected:
        started = time.monotonic()
        report = agent.analyze(DATASETS[scenario.dataset_id], load_dataset(scenario.dataset_id))
        latency_ms = int((time.monotonic() - started) * 1000)
        rows.append(_score_quality_report(scenario, report, latency_ms))

    return _summarize("deterministic", rows)


def evaluate_tool_agent(
    agent: LLMDataQualityAgent | None = None,
    scenarios: list[EvalScenario] | None = None,
) -> dict[str, Any]:
    selected = scenarios or load_scenarios()
    selected_agent = agent or LLMDataQualityAgent()
    rows = []

    for scenario in selected:
        started = time.monotonic()
        report = selected_agent.run(DATASETS[scenario.dataset_id], load_dataset(scenario.dataset_id))
        latency_ms = int((time.monotonic() - started) * 1000)
        rows.append(_score_agent_report(scenario, report, latency_ms))

    return _summarize("tool_agent", rows)


def run_all_evals() -> dict[str, Any]:
    scenarios = load_scenarios()
    deterministic = evaluate_deterministic(scenarios)
    tool_agent = evaluate_tool_agent(scenarios=scenarios)
    return {
        "scenario_count": len(scenarios),
        "results": [deterministic, tool_agent],
    }


def _score_quality_report(scenario: EvalScenario, report: QualityReport, latency_ms: int) -> dict[str, Any]:
    actual_findings = {finding.check_name for finding in report.findings}
    expected_findings = set(scenario.expected_findings)
    matched = actual_findings & expected_findings
    return {
        "scenario_id": scenario.id,
        "dataset_id": scenario.dataset_id,
        "status_match": report.status == scenario.expected_status,
        "finding_recall": _safe_ratio(len(matched), len(expected_findings)),
        "evidence_support_rate": _safe_ratio(
            sum(1 for finding in report.findings if finding.evidence),
            len(report.findings),
        ),
        "fallback_success": report.llm_assessment.enabled is False and report.llm_assessment.error is not None,
        "used_required_report_tool": not scenario.expected_report_tool,
        "final_report_attached": True,
        "latency_ms": latency_ms,
    }


def _score_agent_report(scenario: EvalScenario, report: AgentRunReport, latency_ms: int) -> dict[str, Any]:
    quality_report = report.quality_report
    if quality_report is None:
        actual_findings: set[str] = set()
        finding_recall = 0.0
        evidence_support_rate = 0.0
    else:
        actual_findings = {finding.check_name for finding in quality_report.findings}
        expected_findings = set(scenario.expected_findings)
        finding_recall = _safe_ratio(len(actual_findings & expected_findings), len(expected_findings))
        evidence_support_rate = _safe_ratio(
            sum(1 for finding in quality_report.findings if finding.evidence),
            len(quality_report.findings),
        )

    evaluation = report.evaluation or {}
    return {
        "scenario_id": scenario.id,
        "dataset_id": scenario.dataset_id,
        "status_match": report.status in {scenario.expected_status, "DISABLED"},
        "finding_recall": finding_recall,
        "evidence_support_rate": evidence_support_rate,
        "fallback_success": report.status == "DISABLED" and report.error is not None,
        "used_required_report_tool": bool(evaluation.get("used_required_report_tool", False)),
        "final_report_attached": quality_report is not None,
        "latency_ms": latency_ms,
    }


def _summarize(name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": name,
        "scenario_count": len(rows),
        "status_accuracy": _average_bool(rows, "status_match"),
        "finding_recall": round(mean(row["finding_recall"] for row in rows), 3) if rows else 0.0,
        "evidence_support_rate": round(mean(row["evidence_support_rate"] for row in rows), 3) if rows else 0.0,
        "fallback_success_rate": _average_bool(rows, "fallback_success"),
        "required_report_tool_rate": _average_bool(rows, "used_required_report_tool"),
        "final_report_attachment_rate": _average_bool(rows, "final_report_attached"),
        "average_latency_ms": round(mean(row["latency_ms"] for row in rows), 2) if rows else 0.0,
        "scenarios": rows,
    }


def _average_bool(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        return 0.0
    return round(sum(1 for row in rows if row[key]) / len(rows), 3)


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return round(numerator / denominator, 3)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Data Quality Agent evaluation scenarios.")
    parser.add_argument("--mode", choices=["all", "deterministic", "tool-agent"], default="all")
    args = parser.parse_args()

    if args.mode == "deterministic":
        result = evaluate_deterministic()
    elif args.mode == "tool-agent":
        result = evaluate_tool_agent()
    else:
        result = run_all_evals()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
