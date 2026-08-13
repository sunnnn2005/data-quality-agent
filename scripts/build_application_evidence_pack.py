import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
PUBLIC_METRICS_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_MD_PATH = ROOT / "docs" / "application-evidence-pack.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_application_evidence_pack_payload() -> dict[str, Any]:
    scorecard = load_json(SCORECARD_PATH)
    recruiter_pitch = load_json(RECRUITER_PITCH_PATH)
    public_metrics = load_json(PUBLIC_METRICS_PATH)
    headline = scorecard["headline_metrics"]
    footprint = scorecard["live_footprint"]
    outcomes = public_metrics["verified_project_outcomes"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_application_evidence_pack.py",
        "audience": ["recruiters", "hiring managers", "technical interviewers"],
        "target_roles": recruiter_pitch["target_roles"],
        "one_line_project_proof": (
            "Public, containerized LLM data-quality agent with CI-verified evidence artifacts, "
            f"{headline['passing_tests']} tests, {headline['verified_resume_claims']} verified resume claims, "
            "and honest adoption baselines."
        ),
        "application_links": {
            "demo": scorecard["public_demo"],
            "github_repo": scorecard["repo"],
            "container_image": f"https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
            "recruiter_pitch": f"{scorecard['repo']}/blob/main/docs/recruiter-pitch.md",
            "live_scorecard": f"{scorecard['repo']}/blob/main/docs/live-project-scorecard.md",
            "resume_evidence": f"{scorecard['repo']}/blob/main/docs/resume-evidence.md",
            "api_contract": f"{scorecard['repo']}/blob/main/docs/api-contract.md",
            "public_metrics": f"{scorecard['repo']}/blob/main/docs/public-metrics-summary.md",
        },
        "verified_outcome_numbers": {
            "passing_tests": headline["passing_tests"],
            "verified_resume_claims": headline["verified_resume_claims"],
            "implemented_agent_capabilities": headline["implemented_agent_capabilities"],
            "agent_tools_allowed": headline["agent_tools_allowed"],
            "openapi_required_endpoints": headline["openapi_required_endpoints"],
            "support_ticket_issue_categories": headline["support_ticket_issue_categories"],
            "rejected_unsafe_postgres_queries": headline["unsafe_postgres_queries_rejected"],
            "recruiter_safe_resume_bullets": outcomes["recruiter_pitch_resume_bullets"],
            "target_roles": outcomes["recruiter_pitch_target_roles"],
        },
        "resume_bullets": recruiter_pitch["resume_bullets"],
        "email_attachment_note": (
            "I included the project link because the repository has a public demo, runnable container, "
            "OpenAPI contract, CI-verified evidence page, and a generated scorecard that keeps adoption claims honest."
        ),
        "interview_opening": recruiter_pitch["thirty_second_pitch"],
        "evidence_review_order": [
            "Open the public demo to see the product-style result.",
            "Open the live scorecard for the current tests, claims, release, container, and adoption baseline.",
            "Open the recruiter pitch for resume bullets and interview framing.",
            "Open the OpenAPI contract and safety boundaries for implementation depth.",
            "Open public metrics to verify stars, forks, feedback, and not-claimed signals.",
        ],
        "honest_baseline": {
            "stars": footprint["stars"],
            "forks": footprint["forks"],
            "confirmed_external_users": footprint["confirmed_external_users"],
            "external_feedback_items": footprint["external_feedback_items"],
        },
        "not_claimed": scorecard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    links = "\n".join(f"- {label.replace('_', ' ').title()}: [{url}]({url})" for label, url in payload["application_links"].items())
    numbers = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["verified_outcome_numbers"].items())
    bullets = "\n".join(f"- {item}" for item in payload["resume_bullets"])
    review_order = "\n".join(f"{index}. {item}" for index, item in enumerate(payload["evidence_review_order"], start=1))
    baseline = "\n".join(f"- `{key}`: {value}" for key, value in payload["honest_baseline"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    roles = ", ".join(payload["target_roles"])
    return f"""# Application Evidence Pack

This generated pack gives recruiters and interviewers a compact review path for {roles}.

## One-Line Project Proof

{payload["one_line_project_proof"]}

## Application Links

{links}

## Verified Outcome Numbers

| Metric | Value |
| --- | ---: |
{numbers}

## Resume Bullets

{bullets}

## Email Attachment Note

{payload["email_attachment_note"]}

## Interview Opening

{payload["interview_opening"]}

## Evidence Review Order

{review_order}

## Honest Baseline

{baseline}

## Not Claimed

{not_claimed}
"""


def verify_application_evidence_pack(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "application_link_count": 8,
        "resume_bullet_count": 3,
        "target_role_count": 4,
        "passing_tests": 80,
        "verified_resume_claims": 39,
    }
    if len(payload["application_links"]) != expected["application_link_count"]:
        raise AssertionError("application evidence pack must include 8 application links")
    if len(payload["resume_bullets"]) != expected["resume_bullet_count"]:
        raise AssertionError("application evidence pack must include 3 resume bullets")
    if len(payload["target_roles"]) != expected["target_role_count"]:
        raise AssertionError("application evidence pack must include 4 target roles")
    numbers = payload["verified_outcome_numbers"]
    for key in ("passing_tests", "verified_resume_claims"):
        if numbers.get(key) != expected[key]:
            raise AssertionError(f"{key} expected {expected[key]!r}, got {numbers.get(key)!r}")
    if payload["honest_baseline"]["stars"] != 0:
        raise AssertionError("application evidence pack must preserve current star baseline")
    if payload["honest_baseline"]["confirmed_external_users"] != 0:
        raise AssertionError("application evidence pack must preserve current user baseline")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("production users", "customer traction", "earned github stars"):
        if forbidden in joined:
            raise AssertionError(f"application evidence pack must not claim {forbidden}")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"application evidence pack must not claim {required}")
    return {"application_evidence_pack_verified": True, **expected}


def main() -> None:
    payload = build_application_evidence_pack_payload()
    verify_application_evidence_pack(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
