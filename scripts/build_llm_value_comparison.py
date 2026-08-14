import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.data import DATASETS, load_dataset
from app.evals import load_scenarios
from app.tool_agent import DataQualityToolbox


OUTPUT_JSON_PATH = ROOT / "docs" / "llm-value-comparison.json"
OUTPUT_MD_PATH = ROOT / "docs" / "llm-value-comparison.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "llm-value-comparison.html"

FIXED_GENERIC_CHECKS = [
    "schema_required_columns",
    "missing_values",
    "volume_anomaly",
]


def _recall(recommended: set[str], expected: set[str]) -> float:
    if not expected:
        return 1.0
    return round(len(recommended & expected) / len(expected), 3)


def build_llm_value_comparison() -> dict[str, Any]:
    rows = []
    fixed_total = 0.0
    adaptive_total = 0.0

    for scenario in load_scenarios():
        dataset = DATASETS[scenario.dataset_id]
        frame = load_dataset(scenario.dataset_id)
        strategy = DataQualityToolbox(dataset, frame).dispatch("select_quality_strategy", {})
        expected = set(scenario.expected_findings)
        fixed = set(FIXED_GENERIC_CHECKS)
        adaptive = set(strategy["recommended_checks"])
        fixed_recall = _recall(fixed, expected)
        adaptive_recall = _recall(adaptive, expected)
        fixed_total += fixed_recall
        adaptive_total += adaptive_recall
        rows.append(
            {
                "scenario_id": scenario.id,
                "dataset_id": scenario.dataset_id,
                "expected_findings": sorted(expected),
                "fixed_generic_checks": FIXED_GENERIC_CHECKS,
                "adaptive_strategy_checks": sorted(adaptive),
                "fixed_generic_recall": fixed_recall,
                "adaptive_strategy_recall": adaptive_recall,
                "incremental_recall": round(adaptive_recall - fixed_recall, 3),
                "strategy_reason": strategy["strategy"],
            }
        )

    scenario_count = len(rows)
    fixed_average = round(fixed_total / scenario_count, 3)
    adaptive_average = round(adaptive_total / scenario_count, 3)
    improved_rows = [row for row in rows if row["incremental_recall"] > 0]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_llm_value_comparison.py",
        "purpose": (
            "Compare a fixed generic quality workflow against the agent's adaptive strategy-selection tool "
            "on the same public eval scenarios."
        ),
        "scenario_count": scenario_count,
        "fixed_generic_check_count": len(FIXED_GENERIC_CHECKS),
        "adaptive_tool_name": "select_quality_strategy",
        "fixed_generic_average_recall": fixed_average,
        "adaptive_strategy_average_recall": adaptive_average,
        "absolute_recall_lift": round(adaptive_average - fixed_average, 3),
        "relative_recall_lift_percent": round(((adaptive_average - fixed_average) / fixed_average) * 100, 1)
        if fixed_average
        else None,
        "improved_scenario_count": len(improved_rows),
        "unchanged_scenario_count": scenario_count - len(improved_rows),
        "comparison_rows": rows,
        "resume_safe_summary": (
            f"Published a {scenario_count}-scenario comparison showing adaptive data-quality strategy selection "
            f"improved finding recall from {fixed_average} to {adaptive_average} versus a fixed generic checklist, "
            "without claiming paid-model benchmark results or external adoption."
        ),
        "not_claimed": [
            "paid model benchmark results",
            "production traffic evaluation",
            "external human-labeled evaluation set",
            "enterprise customer impact",
        ],
    }


def verify_llm_value_comparison(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["scenario_count"] != 14:
        raise AssertionError("comparison must cover the public 14-scenario eval set")
    if payload["fixed_generic_check_count"] != 3:
        raise AssertionError("fixed baseline must remain a small generic checklist")
    if payload["adaptive_tool_name"] != "select_quality_strategy":
        raise AssertionError("comparison must identify the adaptive agent tool")
    if payload["adaptive_strategy_average_recall"] <= payload["fixed_generic_average_recall"]:
        raise AssertionError("adaptive strategy must outperform the fixed generic checklist")
    if payload["absolute_recall_lift"] < 0.3:
        raise AssertionError("comparison lift is too small to be a strong resume signal")
    if payload["improved_scenario_count"] < 8:
        raise AssertionError("adaptive strategy must improve a majority of scenarios")
    if any(row["adaptive_strategy_recall"] < row["fixed_generic_recall"] for row in payload["comparison_rows"]):
        raise AssertionError("adaptive strategy should not reduce recall on any scenario")
    for forbidden in ("users", "customers", "production traffic"):
        if forbidden in payload["resume_safe_summary"].lower():
            raise AssertionError(f"comparison summary must not claim {forbidden}")
    return {
        "llm_value_comparison_verified": True,
        "scenario_count": payload["scenario_count"],
        "absolute_recall_lift": payload["absolute_recall_lift"],
        "improved_scenario_count": payload["improved_scenario_count"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {scenario_id} | {dataset_id} | {fixed_generic_recall} | {adaptive_strategy_recall} | {incremental_recall} |".format(
            **row
        )
        for row in payload["comparison_rows"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# LLM Value Comparison

This generated artifact compares a fixed generic data-quality workflow against the agent's adaptive strategy-selection tool on the same public eval set.

## Summary

| Metric | Value |
| --- | ---: |
| Eval scenarios | {payload["scenario_count"]} |
| Fixed generic checks | {payload["fixed_generic_check_count"]} |
| Adaptive agent tool | `{payload["adaptive_tool_name"]}` |
| Fixed generic average recall | {payload["fixed_generic_average_recall"]} |
| Adaptive strategy average recall | {payload["adaptive_strategy_average_recall"]} |
| Absolute recall lift | {payload["absolute_recall_lift"]} |
| Relative recall lift | {payload["relative_recall_lift_percent"]}% |
| Improved scenarios | {payload["improved_scenario_count"]} |

## Scenario Rows

| Scenario | Dataset | Fixed Recall | Adaptive Recall | Lift |
| --- | --- | ---: | ---: | ---: |
{rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    row_cards = "\n".join(
        f"""<article>
        <h3>{row["scenario_id"]}</h3>
        <p>{row["dataset_id"]}</p>
        <strong>{row["fixed_generic_recall"]} -> {row["adaptive_strategy_recall"]}</strong>
        <span>lift {row["incremental_recall"]}</span>
      </article>"""
        for row in payload["comparison_rows"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Value Comparison</title>
  <style>
    :root {{ color-scheme: dark; --bg: #0b0f14; --panel: #151b25; --text: #f7fafc; --muted: #a7b3c5; --line: #293244; --accent: #5eead4; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 56px 0; }}
    h1 {{ font-size: clamp(42px, 7vw, 84px); line-height: .95; letter-spacing: 0; margin: 0 0 16px; }}
    p {{ color: var(--muted); font-size: 18px; max-width: 820px; }}
    .stats, .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 28px 0; }}
    .stat, article {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .stat strong {{ display: block; color: var(--accent); font-size: 34px; }}
    article h3 {{ font-size: 16px; margin: 0 0 6px; }}
    article p {{ font-size: 14px; margin: 0 0 10px; }}
    article strong {{ display: block; font-size: 22px; }}
    article span {{ color: var(--accent); }}
  </style>
</head>
<body>
  <main>
    <h1>LLM Value Comparison</h1>
    <p>Fixed generic checklist vs adaptive strategy selection on the same public eval scenarios. This is a resume-safe agent-value artifact: it does not claim paid-model benchmark results, external adoption, or customer impact.</p>
    <section class="stats">
      <div class="stat"><strong>{payload["scenario_count"]}</strong><span>eval scenarios</span></div>
      <div class="stat"><strong>{payload["fixed_generic_average_recall"]}</strong><span>fixed average recall</span></div>
      <div class="stat"><strong>{payload["adaptive_strategy_average_recall"]}</strong><span>adaptive average recall</span></div>
      <div class="stat"><strong>{payload["relative_recall_lift_percent"]}%</strong><span>relative recall lift</span></div>
    </section>
    <p>{payload["resume_safe_summary"]}</p>
    <section class="grid">
      {row_cards}
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    payload = build_llm_value_comparison()
    verify_llm_value_comparison(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
