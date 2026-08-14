import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
BUSINESS_REPLAY_DEMO_PATH = ROOT / "docs" / "business-replay-demo.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-resolution-brief.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-resolution-brief.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_resolution_brief() -> dict[str, Any]:
    impact = load_json(BUSINESS_IMPACT_PATH)
    replay = load_json(BUSINESS_REPLAY_DEMO_PATH)
    scorecard = impact["remediation_scorecard"]
    high_priority = [item for item in scorecard["business_risk_areas"] if item["priority"] == "HIGH"]
    owners = sorted({item["owner"] for item in scorecard["business_risk_areas"]})
    detected_checks = impact["impact_summary"]["check_coverage"]["observed_checks"]

    resolution_steps = [
        {
            "step": "Block duplicate identities before dashboard publication",
            "owner": "Data Engineering",
            "evidence": "1 duplicate ticket_id can double-count support volume.",
            "recommended_action": "Deduplicate by latest event timestamp and add an idempotent merge check.",
        },
        {
            "step": "Require routing fields before support operations consume the export",
            "owner": "Support Operations",
            "evidence": "priority and team each have missing values.",
            "recommended_action": "Trace null generation and reject rows missing required routing fields.",
        },
        {
            "step": "Separate refund-like records from positive customer-impact facts",
            "owner": "Analytics Engineering",
            "evidence": "1 negative amount is mixed into the support-ticket export.",
            "recommended_action": "Validate amount sign rules and split credits/refunds into an explicit event type.",
        },
        {
            "step": "Review extreme values before executive metrics refresh",
            "owner": "Data Analytics",
            "evidence": "1 amount outlier can skew aggregate reporting.",
            "recommended_action": "Inspect outlier ticket records before publishing dashboard aggregates.",
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_resolution_brief.py",
        "source_artifacts": [
            "docs/business-impact.json",
            "docs/business-replay-demo.json",
            "docs/support-ticket-case-study.md",
        ],
        "business_problem": "Support dashboards can continue refreshing while duplicate ticket ids, missing routing fields, negative amounts, and outliers silently corrupt operational decisions.",
        "dataset_context": {
            "scenario": impact["business_scenario"],
            "dataset_id": impact["dataset_id"],
            "row_count": impact["row_count"],
            "quality_score": impact["quality_score"],
            "status": impact["status"],
            "contains_real_company_data": replay["dataset"]["contains_real_company_data"],
            "contains_pii": replay["dataset"]["contains_pii"],
        },
        "detected_signal_counts": {
            "issue_categories": impact["issue_category_count"],
            "findings": impact["finding_count"],
            "affected_columns": impact["affected_column_count"],
            "business_risk_areas": impact["business_risk_area_count"],
            "high_priority_actions": impact["high_priority_action_count"],
            "owner_handoffs": impact["owner_handoff_count"],
            "root_cause_hypotheses": impact["root_cause_hypothesis_count"],
            "business_rule_references": impact["business_rule_reference_count"],
        },
        "detected_checks": detected_checks,
        "owners": owners,
        "resolution_steps": resolution_steps,
        "interview_story": (
            "I modeled a realistic support-operations dashboard failure, ran the agent on an anonymized CSV export, "
            "and converted raw quality checks into prioritized remediation handoffs for data engineering, support operations, "
            "analytics engineering, and data analytics owners."
        ),
        "resume_safe_result": (
            "Produced a verified business-resolution brief for an anonymized support-operations export, mapping "
            f"{impact['finding_count']} findings across {impact['business_risk_area_count']} business risks to "
            f"{impact['high_priority_action_count']} high-priority actions and {impact['owner_handoff_count']} owner handoffs."
        ),
        "claim_boundaries": [
            "anonymized replay, not a real customer dataset",
            "no external user validated this brief yet",
            "no customer production deployment is claimed",
            "no revenue, SLA, or time-saved number is claimed without external evidence",
        ],
        "next_evidence_to_unlock_stronger_claim": {
            "target": "validated business-impact scenario",
            "required_evidence": "accepted non-owner public business-case review issue with anonymized workflow, impact field, project evidence mapping, and permission to count",
            "current_value": impact["business_impact_ledger_accepted_signals"] if "business_impact_ledger_accepted_signals" in impact else 0,
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["detected_signal_counts"].items()
    )
    steps = "\n".join(
        f"| {item['step']} | {item['owner']} | {item['evidence']} | {item['recommended_action']} |"
        for item in payload["resolution_steps"]
    )
    boundaries = "\n".join(f"- {item}" for item in payload["claim_boundaries"])
    context = payload["dataset_context"]
    unlock = payload["next_evidence_to_unlock_stronger_claim"]
    return f"""# Business Resolution Brief

This generated artifact turns the support-ticket replay into a resume-safe business problem resolution story. It is intentionally conservative: it proves a reproducible anonymized business-data scenario, not customer adoption.

## Business Problem

{payload["business_problem"]}

## Dataset Context

| Field | Value |
| --- | --- |
| Scenario | {context["scenario"]} |
| Dataset | `{context["dataset_id"]}` |
| Rows | {context["row_count"]} |
| Status | `{context["status"]}` |
| Quality score | {context["quality_score"]} |
| Contains real company data | `{context["contains_real_company_data"]}` |
| Contains PII | `{context["contains_pii"]}` |

## Detected Signals

| Signal | Count |
| --- | ---: |
{counts}

## Resolution Steps

| Step | Owner | Evidence | Recommended action |
| --- | --- | --- | --- |
{steps}

## Interview Story

{payload["interview_story"]}

## Resume-Safe Result

{payload["resume_safe_result"]}

## Claim Boundaries

{boundaries}

## Next Evidence To Unlock Stronger Claim

| Target | Required evidence | Current value |
| --- | --- | ---: |
| {unlock["target"]} | {unlock["required_evidence"]} | {unlock["current_value"]} |
"""


def verify_business_resolution_brief(payload: dict[str, Any]) -> dict[str, Any]:
    counts = payload["detected_signal_counts"]
    expected_counts = {
        "issue_categories": 4,
        "findings": 5,
        "affected_columns": 4,
        "business_risk_areas": 4,
        "high_priority_actions": 3,
        "owner_handoffs": 4,
        "root_cause_hypotheses": 3,
        "business_rule_references": 4,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"business resolution brief {key} expected {expected!r}")
    context = payload["dataset_context"]
    if context["status"] != "FAIL" or context["quality_score"] != 24:
        raise AssertionError("business resolution brief must preserve the verified failing quality result")
    if context["contains_real_company_data"] is not False or context["contains_pii"] is not False:
        raise AssertionError("business resolution brief must keep anonymized-data boundaries")
    if len(payload["resolution_steps"]) != 4:
        raise AssertionError("business resolution brief must map four owner handoff steps")
    for owner in ("Data Engineering", "Support Operations", "Analytics Engineering", "Data Analytics"):
        if owner not in payload["owners"]:
            raise AssertionError(f"business resolution brief missing owner {owner}")
    boundaries = " ".join(payload["claim_boundaries"]).lower()
    for forbidden_claim in ("real customer dataset", "external user", "production deployment", "revenue"):
        if forbidden_claim not in boundaries:
            raise AssertionError(f"business resolution brief must block {forbidden_claim}")
    return {"business_resolution_brief_verified": True, **expected_counts}


def main() -> None:
    payload = build_business_resolution_brief()
    verify_business_resolution_brief(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
