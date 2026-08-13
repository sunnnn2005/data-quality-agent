import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-summary.md"


def load_business_impact() -> dict[str, Any]:
    return json.loads(BUSINESS_IMPACT_PATH.read_text())


def build_outcome_summary_payload() -> dict[str, Any]:
    impact = load_business_impact()
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_summary.py",
        "source_artifact": "docs/business-impact.json",
        "business_problem": (
            "Support operations dashboard data can silently mix duplicate ticket facts, missing routing metadata, "
            "refund-like negative amounts, and extreme outliers before publication."
        ),
        "verified_outcomes": {
            "dataset": impact["dataset_id"],
            "row_count": impact["row_count"],
            "quality_score": impact["quality_score"],
            "status": impact["status"],
            "issue_category_count": impact["issue_category_count"],
            "finding_count": impact["finding_count"],
            "affected_column_count": impact["affected_column_count"],
            "recommended_action_count": impact["recommended_action_count"],
            "root_cause_hypothesis_count": impact["root_cause_hypothesis_count"],
            "business_rule_reference_count": impact["business_rule_reference_count"],
            "business_risk_area_count": impact["business_risk_area_count"],
            "high_priority_action_count": impact["high_priority_action_count"],
            "owner_handoff_count": impact["owner_handoff_count"],
        },
        "issue_categories": [
            {
                "name": "Duplicate ticket identity",
                "evidence": f"{impact['duplicate_primary_key_count']} duplicate primary-key case found.",
                "risk": impact["impact_summary"]["duplicate_primary_keys"]["business_risk"],
            },
            {
                "name": "Missing routing metadata",
                "evidence": (
                    f"{impact['missing_routing_field_count']} required routing fields missing across "
                    "priority/team checks."
                ),
                "risk": impact["impact_summary"]["missing_routing_fields"]["business_risk"],
            },
            {
                "name": "Negative customer-impact amount",
                "evidence": f"{impact['negative_amount_count']} negative amount found.",
                "risk": impact["impact_summary"]["negative_amounts"]["business_risk"],
            },
            {
                "name": "Extreme amount outlier",
                "evidence": f"{impact['amount_outlier_count']} amount outlier found.",
                "risk": impact["impact_summary"]["amount_outliers"]["business_risk"],
            },
        ],
        "resume_safe_summary": impact["resume_safe_summary"],
        "remediation_scorecard": impact["remediation_scorecard"],
        "top_root_cause_hypotheses": impact["top_root_cause_hypotheses"],
        "not_claimed": impact["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    outcomes = payload["verified_outcomes"]
    categories = "\n".join(
        f"- **{item['name']}**: {item['evidence']} {item['risk']}" for item in payload["issue_categories"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    hypotheses = "\n".join(
        (
            f"{index}. **{item['title']}** "
            f"(confidence: {item['confidence']}; checks: {', '.join(item['supporting_checks'])})"
        )
        for index, item in enumerate(payload["top_root_cause_hypotheses"], start=1)
    )
    remediation_rows = "\n".join(
        (
            f"| {item['area']} | {item['priority']} | {item['owner']} | "
            f"{item['evidence']} |"
        )
        for item in payload["remediation_scorecard"]["business_risk_areas"]
    )
    sla_checks = "\n".join(f"- {item}" for item in payload["remediation_scorecard"]["sla_style_checks"])
    return f"""# Outcome Summary

This page converts the machine-generated business-impact artifact into a resume-safe outcome summary. It is generated from `docs/business-impact.json`; do not edit the metrics by hand.

## Business Problem

{payload["business_problem"]}

## Verified Outcomes

| Metric | Value |
| --- | ---: |
| Dataset | `{outcomes["dataset"]}` |
| Rows analyzed | {outcomes["row_count"]} |
| Quality score | {outcomes["quality_score"]} / 100 |
| Report status | `{outcomes["status"]}` |
| Issue categories | {outcomes["issue_category_count"]} |
| Findings | {outcomes["finding_count"]} |
| Affected columns | {outcomes["affected_column_count"]} |
| Recommended actions | {outcomes["recommended_action_count"]} |
| Ranked root-cause hypotheses | {outcomes["root_cause_hypothesis_count"]} |
| Business-rule references | {outcomes["business_rule_reference_count"]} |
| Business risk areas | {outcomes["business_risk_area_count"]} |
| High-priority actions | {outcomes["high_priority_action_count"]} |
| Owner handoffs | {outcomes["owner_handoff_count"]} |

## Issue Categories

{categories}

## Ranked Root-Cause Hypotheses

{hypotheses}

## Remediation Scorecard

{payload["remediation_scorecard"]["summary"]}

| Business Risk Area | Priority | Owner | Evidence |
| --- | --- | --- | --- |
{remediation_rows}

## SLA-Style Checks

{sla_checks}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

{payload["remediation_scorecard"]["resume_safe_outcome"]}

## Not Claimed

{not_claimed}
"""


def verify_outcome_summary(payload: dict[str, Any]) -> dict[str, Any]:
    outcomes = payload["verified_outcomes"]
    expected = {
        "row_count": 8,
        "quality_score": 24,
        "status": "FAIL",
        "issue_category_count": 4,
        "finding_count": 5,
        "affected_column_count": 4,
        "recommended_action_count": 5,
        "root_cause_hypothesis_count": 3,
        "business_rule_reference_count": 4,
        "business_risk_area_count": 4,
        "high_priority_action_count": 3,
        "owner_handoff_count": 4,
    }
    for key, value in expected.items():
        if outcomes.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {outcomes.get(key)!r}")
    if len(payload["issue_categories"]) != 4:
        raise AssertionError("outcome summary must include four issue categories")
    if len(payload["remediation_scorecard"]["business_risk_areas"]) != 4:
        raise AssertionError("outcome summary must include four remediation scorecard risk areas")
    if "owner handoffs" not in payload["remediation_scorecard"]["resume_safe_outcome"]:
        raise AssertionError("outcome summary must include owner-handoff evidence")
    if "external users" not in " ".join(payload["not_claimed"]).lower():
        raise AssertionError("outcome summary must avoid external-user claims")
    return {"outcome_summary_verified": True, **expected}


def main() -> None:
    payload = build_outcome_summary_payload()
    verify_outcome_summary(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
