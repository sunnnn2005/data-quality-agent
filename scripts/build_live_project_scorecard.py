import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_METRICS_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTCOME_EVIDENCE_PATH = ROOT / "docs" / "outcome-evidence.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "live-project-scorecard.json"
OUTPUT_MD_PATH = ROOT / "docs" / "live-project-scorecard.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_live_project_scorecard_payload() -> dict[str, Any]:
    metrics = load_json(PUBLIC_METRICS_PATH)
    evidence = load_json(OUTCOME_EVIDENCE_PATH)
    public = metrics["public_metrics"]
    outcomes = metrics["verified_project_outcomes"]
    claim_ids = [claim["id"] for claim in evidence["claims"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_live_project_scorecard.py",
        "public_demo": metrics["public_demo"],
        "repo": metrics["repo"],
        "release": metrics["release"],
        "container_image": metrics["container_image"],
        "headline_metrics": {
            "passing_tests": public["test_count"],
            "verified_resume_claims": len(evidence["claims"]),
            "implemented_agent_capabilities": outcomes["implemented_agent_capabilities"],
            "support_ticket_issue_categories": outcomes["support_ticket_issue_categories"],
            "openapi_required_endpoints": outcomes["openapi_required_endpoints"],
            "agent_tools_allowed": outcomes["tool_allowlist_count"],
            "agent_matrix_implemented_capabilities": outcomes["agent_matrix_implemented_capabilities"],
            "unsafe_postgres_queries_rejected": outcomes["postgres_rejected_write_query_count"],
        },
        "live_footprint": {
            "stars": public["stars"],
            "forks": public["forks"],
            "watchers": public["watchers"],
            "external_feedback_items": public["external_feedback_items"],
            "confirmed_external_users": public["confirmed_external_users"],
        },
        "reviewer_paths": [
            {"label": "Try the public demo", "url": metrics["public_demo"]},
            {"label": "Inspect resume evidence", "url": f"{metrics['repo']}/blob/main/docs/resume-evidence.md"},
            {"label": "Inspect impact review packet", "url": f"{metrics['repo']}/blob/main/docs/impact-review-packet.md"},
            {"label": "Inspect business problem casebook", "url": f"{metrics['repo']}/blob/main/docs/business-problem-casebook.md"},
            {"label": "Inspect public traction dashboard", "url": f"{metrics['repo']}/blob/main/docs/public-traction-dashboard.md"},
            {"label": "Inspect feedback intake quality", "url": f"{metrics['repo']}/blob/main/docs/feedback-intake-quality.md"},
            {"label": "Inspect OpenAPI contract", "url": f"{metrics['repo']}/blob/main/docs/api-contract.md"},
            {"label": "Inspect safety boundaries", "url": f"{metrics['repo']}/blob/main/docs/agent-safety-boundaries.md"},
            {"label": "Inspect agent capability matrix", "url": f"{metrics['repo']}/blob/main/docs/agent-capability-matrix.md"},
            {"label": "Run the local reviewer demo", "url": f"{metrics['repo']}/blob/main/docs/local-reviewer-demo.md"},
            {"label": "Inspect public metrics", "url": f"{metrics['repo']}/blob/main/docs/public-metrics-summary.md"},
        ],
        "claim_coverage": {
            "has_public_demo": "public-demo" in claim_ids,
            "has_release": "public-release" in claim_ids,
            "has_container": "container-image" in claim_ids,
            "has_openapi_contract": "openapi-contract" in claim_ids,
            "has_agent_safety": "agent-safety-boundaries" in claim_ids,
            "has_agent_capability_matrix": "agent-capability-matrix" in claim_ids,
            "has_local_reviewer_demo": "local-reviewer-demo" in claim_ids,
            "has_observability": "agent-observability" in claim_ids,
            "has_feedback_baseline": "feedback-metrics" in claim_ids,
            "has_impact_review_packet": "impact-review-packet" in claim_ids,
            "has_business_problem_casebook": "business-problem-casebook" in claim_ids,
            "has_public_traction_dashboard": "public-traction-dashboard" in claim_ids,
            "has_feedback_intake_quality": "feedback-intake-quality" in claim_ids,
            "has_business_case_intake": "business-case-intake" in claim_ids,
        },
        "resume_safe_summary": (
            f"Live project scorecard: public demo, {metrics['release']} release, container image, "
            f"{public['test_count']} passing CI tests, {len(evidence['claims'])} verified resume claims, "
            f"and {outcomes['implemented_agent_capabilities']} implemented LLM agent-readiness capabilities."
        ),
        "not_claimed": metrics["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    headline_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["headline_metrics"].items()
    )
    footprint_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["live_footprint"].items()
    )
    reviewer_paths = "\n".join(f"- [{item['label']}]({item['url']})" for item in payload["reviewer_paths"])
    coverage_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["claim_coverage"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Live Project Scorecard

This generated scorecard gives reviewers one place to inspect the project's public footprint, engineering evidence, and honest not-claimed signals.

## Headline Metrics

| Metric | Value |
| --- | ---: |
{headline_rows}

## Live Footprint

| Metric | Current value |
| --- | ---: |
{footprint_rows}

## Reviewer Paths

{reviewer_paths}

## Claim Coverage

| Signal | Verified |
| --- | --- |
{coverage_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_live_project_scorecard(payload: dict[str, Any]) -> dict[str, Any]:
    headline = payload["headline_metrics"]
    footprint = payload["live_footprint"]
    expected = {
        "passing_tests": 90,
        "verified_resume_claims": 49,
        "implemented_agent_capabilities": 16,
        "agent_tools_allowed": 7,
        "agent_matrix_implemented_capabilities": 13,
        "unsafe_postgres_queries_rejected": 3,
    }
    for key, value in expected.items():
        if headline.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {headline.get(key)!r}")
    if footprint["stars"] != 0 or footprint["confirmed_external_users"] != 0:
        raise AssertionError("scorecard must preserve honest zero adoption baselines")
    if not all(payload["claim_coverage"].values()):
        raise AssertionError("scorecard must cover core public evidence claims")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"scorecard must not claim {required}")
    return {"live_project_scorecard_verified": True, **expected}


def main() -> None:
    payload = build_live_project_scorecard_payload()
    verify_live_project_scorecard(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
