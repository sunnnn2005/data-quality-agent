import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
SUPPORT_TICKET_ARTIFACT_PATH = ROOT / "docs" / "verified-support-ticket-result.json"
IMPACT_REVIEW_PACKET_PATH = ROOT / "docs" / "impact-review-packet.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-problem-casebook.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-problem-casebook.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_problem_casebook_payload() -> dict[str, Any]:
    impact = load_json(BUSINESS_IMPACT_PATH)
    support_ticket = load_json(SUPPORT_TICKET_ARTIFACT_PATH)
    impact_packet = load_json(IMPACT_REVIEW_PACKET_PATH)
    repo = impact_packet["evidence_links"]["github_repo"]
    risk_areas = impact["remediation_scorecard"]["business_risk_areas"]
    root_causes = impact["top_root_cause_hypotheses"]

    case = {
        "case_id": "support-operations-dashboard-quality",
        "business_workflow": "Support operations dashboard refresh",
        "business_problem": (
            "Internal support dashboards can silently mislead operators when ticket exports contain duplicate "
            "ticket ids, missing routing fields, negative customer-impact amounts, and amount outliers."
        ),
        "input_context": {
            "dataset_id": impact["dataset_id"],
            "scenario": impact["business_scenario"],
            "rows_analyzed": support_ticket["row_count"],
            "primary_key": "ticket_id",
            "owner": "support-ops",
        },
        "detected_risks": [
            {
                "risk": "Dashboard double counting",
                "evidence": "1 duplicate ticket_id was detected.",
                "tool_check": "duplicate_primary_key",
                "affected_field": "ticket_id",
                "owner_handoff": "Data Engineering",
            },
            {
                "risk": "Unreliable ticket routing",
                "evidence": "2 required routing fields were missing across priority and team.",
                "tool_check": "missing_values",
                "affected_field": "priority, team",
                "owner_handoff": "Support Operations",
            },
            {
                "risk": "Incorrect customer-impact reporting",
                "evidence": "1 negative amount was mixed into positive customer-impact facts.",
                "tool_check": "negative_amount",
                "affected_field": "amount",
                "owner_handoff": "Analytics Engineering",
            },
            {
                "risk": "Skewed executive metrics",
                "evidence": "1 amount outlier can distort aggregate reporting.",
                "tool_check": "numeric_outliers",
                "affected_field": "amount",
                "owner_handoff": "Data Analytics",
            },
        ],
        "agent_outputs": {
            "quality_score": support_ticket["quality_score"],
            "status": support_ticket["status"],
            "finding_count": support_ticket["finding_count"],
            "business_rule_reference_count": len(support_ticket["business_rule_references"]),
            "root_cause_hypothesis_count": len(root_causes),
            "recommended_action_count": len(support_ticket["recommended_next_steps"]),
            "owner_handoff_count": len(risk_areas),
        },
        "resume_safe_result": (
            "Converted a support-operations CSV export into a verified data-quality casebook with 4 business risks, "
            "5 evidence-backed findings, 3 ranked root-cause hypotheses, and 4 remediation owner handoffs."
        ),
        "interview_answer": (
            "The project models a common internal analytics failure: a dashboard may keep refreshing even when the "
            "underlying export has duplicate identities, missing routing metadata, and invalid amount values. The "
            "agent turns those raw checks into evidence-backed root-cause hypotheses and owner-specific remediation steps."
        ),
        "evidence_links": {
            "casebook": f"{repo}/blob/main/docs/business-problem-casebook.md",
            "business_impact": f"{repo}/blob/main/docs/business-impact.json",
            "support_ticket_case_study": f"{repo}/blob/main/docs/support-ticket-case-study.md",
            "verified_result": f"{repo}/blob/main/docs/verified-support-ticket-result.json",
            "impact_review_packet": f"{repo}/blob/main/docs/impact-review-packet.md",
        },
        "not_claimed": [
            "real customer dataset",
            "external users",
            "customer feedback",
            "production deployment",
            "production financial impact avoided",
        ],
    }

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_problem_casebook.py",
        "case_count": 1,
        "business_case_count": 1,
        "detected_risk_count": len(case["detected_risks"]),
        "owner_handoff_count": case["agent_outputs"]["owner_handoff_count"],
        "evidence_link_count": len(case["evidence_links"]),
        "casebook": [case],
        "resume_safe_summary": case["resume_safe_result"],
        "not_claimed": case["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    case = payload["casebook"][0]
    risks = "\n".join(
        "| {risk} | {tool_check} | {evidence} | {owner_handoff} |".format(**item)
        for item in case["detected_risks"]
    )
    outputs = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in case["agent_outputs"].items()
    )
    links = "\n".join(
        f"- {key.replace('_', ' ').title()}: [{value}]({value})" for key, value in case["evidence_links"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Problem Casebook

This generated casebook explains what business problem the project solves, using only CI-verified evidence.

## Case: {case["business_workflow"]}

{case["business_problem"]}

## Input Context

| Field | Value |
| --- | --- |
| Dataset | `{case["input_context"]["dataset_id"]}` |
| Scenario | {case["input_context"]["scenario"]} |
| Rows analyzed | {case["input_context"]["rows_analyzed"]} |
| Primary key | `{case["input_context"]["primary_key"]}` |
| Owner | `{case["input_context"]["owner"]}` |

## Detected Business Risks

| Risk | Tool check | Evidence | Owner handoff |
| --- | --- | --- | --- |
{risks}

## Agent Outputs

| Output | Value |
| --- | ---: |
{outputs}

## Interview Answer

{case["interview_answer"]}

## Resume-Safe Result

{case["resume_safe_result"]}

## Evidence Links

{links}

## Not Claimed

{not_claimed}
"""


def verify_business_problem_casebook(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["business_case_count"] != 1:
        raise AssertionError("business problem casebook must include one verified business case")
    if payload["detected_risk_count"] != 4:
        raise AssertionError("business problem casebook must include 4 detected business risks")
    if payload["owner_handoff_count"] != 4:
        raise AssertionError("business problem casebook must include 4 owner handoffs")
    if payload["evidence_link_count"] != 5:
        raise AssertionError("business problem casebook must include 5 evidence links")

    case = payload["casebook"][0]
    outputs = case["agent_outputs"]
    expected_outputs = {
        "quality_score": 24,
        "status": "FAIL",
        "finding_count": 5,
        "business_rule_reference_count": 4,
        "root_cause_hypothesis_count": 3,
        "recommended_action_count": 5,
        "owner_handoff_count": 4,
    }
    for key, expected in expected_outputs.items():
        if outputs.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {outputs.get(key)!r}")

    required_checks = {"duplicate_primary_key", "missing_values", "negative_amount", "numeric_outliers"}
    observed_checks = {risk["tool_check"] for risk in case["detected_risks"]}
    if observed_checks != required_checks:
        raise AssertionError(f"detected risk checks mismatch: {observed_checks}")

    if "verified data-quality casebook" not in payload["resume_safe_summary"]:
        raise AssertionError("casebook must expose resume-safe result wording")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("used by customers", "production users", "saved revenue", "reduced cost"):
        if forbidden in joined:
            raise AssertionError(f"casebook must not claim {forbidden}")
    for required in (
        "real customer dataset",
        "external users",
        "customer feedback",
        "production deployment",
        "production financial impact avoided",
    ):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"casebook must not claim {required}")

    return {
        "business_problem_casebook_verified": True,
        "business_case_count": payload["business_case_count"],
        "detected_risk_count": payload["detected_risk_count"],
        "owner_handoff_count": payload["owner_handoff_count"],
        "evidence_link_count": payload["evidence_link_count"],
    }


def main() -> None:
    payload = build_business_problem_casebook_payload()
    verify_business_problem_casebook(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
