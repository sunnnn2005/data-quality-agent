import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
OUTCOME_SUMMARY_PATH = ROOT / "docs" / "outcome-summary.json"
SUPPORT_TICKET_ARTIFACT_PATH = ROOT / "docs" / "verified-support-ticket-result.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "impact-review-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "impact-review-packet.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_impact_review_packet_payload() -> dict[str, Any]:
    impact = load_json(BUSINESS_IMPACT_PATH)
    outcome = load_json(OUTCOME_SUMMARY_PATH)
    support_ticket = load_json(SUPPORT_TICKET_ARTIFACT_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    verified = outcome["verified_outcomes"]
    repo = adoption["repo"]
    business_metrics = {
        "rows_analyzed": support_ticket["row_count"],
        "quality_score": support_ticket["quality_score"],
        "status": support_ticket["status"],
        "issue_categories": impact["issue_category_count"],
        "findings": verified["finding_count"],
        "affected_columns": impact["affected_column_count"],
        "recommended_actions": verified["recommended_action_count"],
        "root_cause_hypotheses": verified["root_cause_hypothesis_count"],
        "business_rule_references": verified["business_rule_reference_count"],
        "business_risk_areas": verified["business_risk_area_count"],
        "high_priority_actions": verified["high_priority_action_count"],
        "owner_handoffs": verified["owner_handoff_count"],
    }
    evidence_links = {
        "public_demo": adoption["public_demo"],
        "github_repo": repo,
        "business_impact_json": f"{repo}/blob/main/docs/business-impact.json",
        "verified_support_ticket_result": f"{repo}/blob/main/docs/verified-support-ticket-result.json",
        "outcome_summary": f"{repo}/blob/main/docs/outcome-summary.md",
        "resume_evidence": f"{repo}/blob/main/docs/resume-evidence.md",
        "public_metrics": f"{repo}/blob/main/docs/public-metrics-summary.md",
        "application_evidence_pack": f"{repo}/blob/main/docs/application-evidence-pack.md",
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_impact_review_packet.py",
        "business_problem": (
            "Support operations dashboard data can be distorted by duplicate ticket ids, missing routing fields, "
            "negative customer-impact amounts, and amount outliers."
        ),
        "expected_reviewer_question": (
            "Can the project show a real business problem, quantified evidence, and honest adoption limits?"
        ),
        "business_metrics": business_metrics,
        "business_metric_count": len(business_metrics),
        "evidence_links": evidence_links,
        "evidence_link_count": len(evidence_links),
        "reviewer_takeaway": (
            "The project demonstrates a reviewable internal-data workflow: ingest bounded business data, detect "
            "quality risks, rank evidence-backed root causes, map risks to remediation owners, and publish the "
            "evidence without claiming external adoption."
        ),
        "resume_safe_summary": (
            f"Published a CI-verified impact review packet for a support-operations data-quality case study with "
            f"{len(business_metrics)} verified business metrics, {len(evidence_links)} evidence links, "
            f"{business_metrics['recommended_actions']} remediation actions, and "
            f"{business_metrics['owner_handoffs']} owner handoffs."
        ),
        "current_public_counts": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "issues_total": adoption["issues_total"],
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "not_claimed": [
            "external users",
            "customer feedback",
            "production deployment",
            "production financial impact avoided",
            "company adoption",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    metrics = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["business_metrics"].items()
    )
    links = "\n".join(
        f"- {key.replace('_', ' ').title()}: [{value}]({value})" for key, value in payload["evidence_links"].items()
    )
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Impact Review Packet

This generated packet gives recruiters and technical interviewers one place to review the project's business-impact evidence without overstating adoption.

## Business Problem

{payload["business_problem"]}

## Reviewer Question

{payload["expected_reviewer_question"]}

## Verified Business Metrics

| Metric | Value |
| --- | ---: |
{metrics}

## Evidence Links

{links}

## Reviewer Takeaway

{payload["reviewer_takeaway"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Current Public Counts

| Metric | Value |
| --- | ---: |
{counts}

## Not Claimed

{not_claimed}
"""


def verify_impact_review_packet(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = payload["business_metrics"]
    expected_metrics = {
        "rows_analyzed": 8,
        "quality_score": 24,
        "status": "FAIL",
        "issue_categories": 4,
        "findings": 5,
        "affected_columns": 4,
        "recommended_actions": 5,
        "root_cause_hypotheses": 3,
        "business_rule_references": 4,
        "business_risk_areas": 4,
        "high_priority_actions": 3,
        "owner_handoffs": 4,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {metrics.get(key)!r}")
    if payload["business_metric_count"] != len(expected_metrics):
        raise AssertionError("impact review packet must expose 12 business metrics")
    if payload["evidence_link_count"] != 8:
        raise AssertionError("impact review packet must expose 8 evidence links")
    if "Support operations dashboard data" not in payload["business_problem"]:
        raise AssertionError("impact review packet must describe the support operations business problem")
    if "support-operations data-quality case study" not in payload["resume_safe_summary"]:
        raise AssertionError("impact review packet must include resume-safe summary wording")
    counts = payload["current_public_counts"]
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "issues_total": 14,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"current public count {key} expected {expected!r}, got {counts.get(key)!r}")
    for required in (
        "external users",
        "customer feedback",
        "production deployment",
        "production financial impact avoided",
        "company adoption",
    ):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"impact review packet must not claim {required}")
    return {
        "impact_review_packet_verified": True,
        "business_metric_count": payload["business_metric_count"],
        "evidence_link_count": payload["evidence_link_count"],
    }


def main() -> None:
    payload = build_impact_review_packet_payload()
    verify_impact_review_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
