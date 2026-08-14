import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-live-proof-snapshot.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-live-proof-snapshot.md"

PUBLIC_AVAILABILITY_PATH = ROOT / "docs" / "public-availability-snapshot.json"
PUBLIC_STATS_PATH = ROOT / "docs" / "github-public-stats-snapshot.json"
PUBLIC_HEALTH_PATH = ROOT / "docs" / "public-evidence-health.json"
LIVE_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
BUSINESS_PILOT_PATH = ROOT / "docs" / "business-pilot-offer.json"
OUTCOME_EVIDENCE_PATH = ROOT / "docs" / "outcome-evidence.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_live_proof_snapshot_payload() -> dict[str, Any]:
    availability = load_json(PUBLIC_AVAILABILITY_PATH)
    stats = load_json(PUBLIC_STATS_PATH)
    health = load_json(PUBLIC_HEALTH_PATH)
    scorecard = load_json(LIVE_SCORECARD_PATH)
    pilot = load_json(BUSINESS_PILOT_PATH)

    headline = scorecard["headline_metrics"]
    public_stats = stats["public_stats"]
    public_health_summary = f"{health['passed_count']}/{health['check_count']} public evidence checks passing"
    availability_summary = (
        f"{availability['available_endpoint_count']}/{availability['endpoint_count']} public endpoints reachable; "
        f"{availability['successful_workflow_count']}/{availability['workflow_count']} main-branch workflows passing"
    )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_live_proof_snapshot.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Give recruiters a concise, resume-safe snapshot of public proof without inflating adoption.",
        "evidence_links": {
            "public_demo": scorecard["public_demo"],
            "github_repo": scorecard["repo"],
            "container_image": "https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
            "live_scorecard": f"{scorecard['repo']}/blob/main/docs/live-project-scorecard.md",
            "public_availability": f"{scorecard['repo']}/blob/main/docs/public-availability-snapshot.md",
            "public_github_stats": f"{scorecard['repo']}/blob/main/docs/github-public-stats-snapshot.md",
            "public_evidence_health": f"{scorecard['repo']}/blob/main/docs/public-evidence-health.json",
            "business_pilot_offer": "https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html",
            "business_pilot_issue": pilot["public_pilot_issue"],
        },
        "verified_now": {
            "public_release": scorecard["release"],
            "container_image_published": True,
            "passing_test_baseline": headline["passing_tests"],
            "verified_resume_claims": headline["verified_resume_claims"],
            "implemented_agent_capabilities": headline["implemented_agent_capabilities"],
            "agent_tools_allowed": headline["agent_tools_allowed"],
            "rejected_unsafe_postgres_queries": headline["unsafe_postgres_queries_rejected"],
            "public_evidence_health": public_health_summary,
            "public_availability": availability_summary,
            "github_stars": public_stats["stars"],
            "github_forks": public_stats["forks"],
            "github_open_issues_or_prs": public_stats["open_issues"],
            "public_pilot_issue_status": pilot["public_issue_status"],
        },
        "resume_safe_bullets": [
            (
                "Built and released a public, containerized LLM data-quality agent with a GitHub Pages demo, "
                "OpenAPI contract, GHCR image, and CI-verified evidence artifacts."
            ),
            (
                f"Implemented {headline['implemented_agent_capabilities']} agent-readiness capabilities including "
                "tool selection, read-only data checks, guardrails, structured reports, observability artifacts, "
                "and deterministic fallback paths."
            ),
            (
                f"Maintained a resume-safe proof system with {headline['passing_tests']} passing test baseline, "
                f"{headline['verified_resume_claims']} verified claim entries, and {public_health_summary}."
            ),
            (
                "Published a redacted business-data pilot offer and public GitHub issue to collect external "
                "business replay evidence without claiming completed pilots or enterprise adoption."
            ),
        ],
        "blocked_until_external_evidence": [
            "confirmed external users",
            "external customer feedback",
            "completed business pilot",
            "enterprise production usage",
            "measured business impact from a real company",
            "GitHub stars beyond the live public count",
        ],
        "next_resume_unlocks": [
            "1 non-owner public GitHub issue confirming a reproducible run",
            "1 non-owner AI/ML reviewer issue validating the agent design",
            "1 redacted business-data replay issue with permission to count evidence",
            "1 organic public star or fork from someone who found the repo useful",
        ],
        "resume_policy": (
            "Use only the bullets in resume_safe_bullets until public, non-owner evidence unlocks the blocked claims. "
            "Self-authored issues, traffic, planning documents, and outreach attempts do not count as users, feedback, "
            "stars, or business impact."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    links = "\n".join(f"- {key.replace('_', ' ').title()}: [{url}]({url})" for key, url in payload["evidence_links"].items())
    verified = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["verified_now"].items())
    bullets = "\n".join(f"- {item}" for item in payload["resume_safe_bullets"])
    blocked = "\n".join(f"- {item}" for item in payload["blocked_until_external_evidence"])
    unlocks = "\n".join(f"- {item}" for item in payload["next_resume_unlocks"])
    return f"""# Resume Live Proof Snapshot

{payload["purpose"]}

## Evidence Links

{links}

## Verified Now

| Signal | Evidence-backed value |
| --- | --- |
{verified}

## Resume-Safe Bullets

{bullets}

## Blocked Until External Evidence

{blocked}

## Next Resume Unlocks

{unlocks}

## Resume Policy

{payload["resume_policy"]}
"""


def verify_resume_live_proof_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    verified = payload["verified_now"]
    links = payload["evidence_links"]
    evidence = load_json(OUTCOME_EVIDENCE_PATH)
    if len(payload["resume_safe_bullets"]) != 4:
        raise AssertionError("resume live proof snapshot must provide four resume-safe bullets")
    if verified["passing_test_baseline"] != 233:
        raise AssertionError("snapshot must preserve the verified 233-test baseline")
    if verified["verified_resume_claims"] != len(evidence["claims"]):
        raise AssertionError("snapshot must preserve the current verified resume claim count")
    if verified["implemented_agent_capabilities"] != 16:
        raise AssertionError("snapshot must preserve 16 implemented agent capabilities")
    if verified["github_stars"] < 0 or verified["github_forks"] < 0:
        raise AssertionError("public GitHub stats cannot be negative")
    health_count = verified["public_evidence_health"].split(" ", maxsplit=1)[0]
    passed_count, check_count = (int(value) for value in health_count.split("/", maxsplit=1))
    if passed_count != check_count or check_count < 102:
        raise AssertionError("snapshot must include all public evidence checks passing")
    if links["business_pilot_issue"] != "https://github.com/sunnnn2005/data-quality-agent/issues/31":
        raise AssertionError("snapshot must link the public business pilot issue")
    verified_claims = json.dumps(verified, sort_keys=True).lower()
    for forbidden in ("completed pilots", "enterprise adoption", "real company users"):
        if forbidden in verified_claims:
            raise AssertionError(f"verified signals must not claim {forbidden}")
    if "without claiming completed pilots or enterprise adoption" not in payload["resume_safe_bullets"][3]:
        raise AssertionError("pilot bullet must explicitly deny completed pilots and enterprise adoption")
    for blocked in (
        "confirmed external users",
        "external customer feedback",
        "completed business pilot",
        "enterprise production usage",
    ):
        if blocked not in payload["blocked_until_external_evidence"]:
            raise AssertionError(f"snapshot must block {blocked}")
    return {
        "resume_live_proof_snapshot_verified": True,
        "resume_safe_bullet_count": len(payload["resume_safe_bullets"]),
        "github_stars": verified["github_stars"],
        "github_forks": verified["github_forks"],
    }


def main() -> None:
    payload = build_resume_live_proof_snapshot_payload()
    verify_resume_live_proof_snapshot(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
