import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AVAILABILITY_PATH = ROOT / "docs" / "public-availability-snapshot.json"
PUBLIC_STATS_PATH = ROOT / "docs" / "github-public-stats-snapshot.json"
OUTCOME_BADGES_PATH = ROOT / "docs" / "outcome-badges.json"
AI_REVIEWER_CARD_PATH = ROOT / "docs" / "ai-engineer-reviewer-card.json"
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "launch-evidence-snapshot.json"
OUTPUT_MD_PATH = ROOT / "docs" / "launch-evidence-snapshot.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_launch_evidence_snapshot() -> dict[str, Any]:
    availability = load_json(AVAILABILITY_PATH)
    public_stats = load_json(PUBLIC_STATS_PATH)
    badges = load_json(OUTCOME_BADGES_PATH)
    reviewer_card = load_json(AI_REVIEWER_CARD_PATH)
    application_pack = load_json(APPLICATION_PACK_PATH)
    badge_by_id = {badge["id"]: badge for badge in badges["badges"]}
    stats = public_stats["public_stats"]

    launch_surfaces = [
        {
            "id": "public_demo",
            "label": "Public demo",
            "url": "https://sunnnn2005.github.io/data-quality-agent/",
            "evidence": "GitHub Pages endpoint is reachable in the availability snapshot.",
        },
        {
            "id": "source_repo",
            "label": "Open-source repository",
            "url": "https://github.com/sunnnn2005/data-quality-agent",
            "evidence": "Repository is public and exposes source, tests, docs, issues, release, and package links.",
        },
        {
            "id": "container_image",
            "label": "Container image",
            "url": "https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
            "evidence": "Container publish workflow is successful in the availability snapshot.",
        },
        {
            "id": "reviewer_card",
            "label": "AI Engineer reviewer card",
            "url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-reviewer-card.md",
            "evidence": "Reviewer card gives technical reviewers exact files, commands, prompts, and submission link.",
        },
        {
            "id": "application_pack",
            "label": "Recruiter evidence pack",
            "url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md",
            "evidence": "Application pack summarizes verified proof, honest baselines, and recruiter-safe bullets.",
        },
    ]

    workflow_status = (
        f"{availability['successful_workflow_count']}/{availability['workflow_count']} main-branch workflows successful "
        "at snapshot time"
    )
    claimable_now = [
        f"{availability['available_endpoint_count']}/{availability['endpoint_count']} public launch surfaces reachable",
        workflow_status,
        f"{badge_by_id['ci-tests']['message']} CI test status",
        f"{stats['forks']} public fork and {stats['stars']} public stars as the current GitHub baseline",
        f"{reviewer_card['inspection_target_count']} AI-agent inspection targets available for external review",
    ]
    blocked_claims = [
        "Do not claim active users while confirmed users are 0.",
        "Do not claim external feedback while accepted feedback is 0.",
        "Do not claim AI Engineer review while accepted AI reviews are 0.",
        "Do not claim production business adoption from public demo reachability.",
        "Do not claim GitHub star growth beyond the live public star count.",
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_launch_evidence_snapshot.py",
        "purpose": "Summarize public launch readiness, reachability, review paths, and honest traction baselines in one recruiter-readable artifact.",
        "launch_surface_count": len(launch_surfaces),
        "launch_surfaces": launch_surfaces,
        "public_availability": {
            "available_endpoint_count": availability["available_endpoint_count"],
            "endpoint_count": availability["endpoint_count"],
            "successful_workflow_count": availability["successful_workflow_count"],
            "workflow_count": availability["workflow_count"],
            "max_latency_ms": availability["max_latency_ms"],
        },
        "public_github_stats": {
            "stars": stats["stars"],
            "forks": stats["forks"],
            "watchers": stats["watchers"],
            "subscribers": stats["subscribers"],
            "open_issues": stats["open_issues"],
        },
        "review_path": {
            "target_metric": reviewer_card["target_metric"],
            "current_count": reviewer_card["current_count"],
            "submit_review_url": reviewer_card["submit_review_url"],
            "public_slot_url": reviewer_card["public_slot_url"],
            "inspection_target_count": reviewer_card["inspection_target_count"],
        },
        "application_pack": {
            "verified_resume_claims": application_pack["verified_outcome_numbers"]["verified_resume_claims"],
            "passing_tests": application_pack["verified_outcome_numbers"]["passing_tests"],
            "target_roles": application_pack["target_roles"],
        },
        "claimable_now_count": len(claimable_now),
        "claimable_now": claimable_now,
        "blocked_claim_count": len(blocked_claims),
        "blocked_claims": blocked_claims,
        "resume_safe_summary": (
            "Published a recruiter-readable launch evidence snapshot covering 5 public project surfaces, "
            f"{availability['available_endpoint_count']}/{availability['endpoint_count']} reachable endpoints, "
            f"{availability['successful_workflow_count']}/{availability['workflow_count']} successful workflows, "
            f"{badge_by_id['ci-tests']['message']} tests, and honest GitHub/reviewer baselines."
        ),
        "resume_policy": (
            "Use this as public launch and review-readiness evidence only. It does not prove users, customer feedback, "
            "business adoption, or external AI Engineer review until the corresponding public counts are above zero."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    surfaces = "\n".join(
        f"| {item['label']} | [open]({item['url']}) | {item['evidence']} |"
        for item in payload["launch_surfaces"]
    )
    availability = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_availability"].items())
    github = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_github_stats"].items())
    review_path = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["review_path"].items())
    claimable = "\n".join(f"- {item}" for item in payload["claimable_now"])
    blocked = "\n".join(f"- {item}" for item in payload["blocked_claims"])
    roles = ", ".join(payload["application_pack"]["target_roles"])
    return f"""# Launch Evidence Snapshot

This generated artifact gives recruiters and technical reviewers one place to verify public launch readiness without inflating traction.

## Public Launch Surfaces

| Surface | Link | Evidence |
| --- | --- | --- |
{surfaces}

## Availability

| Metric | Value |
| --- | --- |
{availability}

## GitHub Public Stats

| Metric | Value |
| --- | ---: |
{github}

## AI Engineer Review Path

| Metric | Value |
| --- | --- |
{review_path}

## Application Pack

| Metric | Value |
| --- | --- |
| Verified resume claims | {payload["application_pack"]["verified_resume_claims"]} |
| Passing tests | {payload["application_pack"]["passing_tests"]} |
| Target roles | {roles} |

## Claimable Now

{claimable}

## Blocked Claims

{blocked}

## Resume Policy

{payload["resume_policy"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_launch_evidence_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["launch_surface_count"] != 5:
        raise AssertionError("launch evidence snapshot must expose 5 launch surfaces")
    if payload["public_availability"]["available_endpoint_count"] != 4:
        raise AssertionError("launch evidence snapshot must reflect 4 reachable endpoints")
    if payload["public_availability"]["successful_workflow_count"] > payload["public_availability"]["workflow_count"]:
        raise AssertionError("successful workflow count cannot exceed workflow count")
    if payload["public_availability"]["workflow_count"] != 3:
        raise AssertionError("launch evidence snapshot must reflect the three tracked workflows")
    if payload["application_pack"]["passing_tests"] != 192:
        raise AssertionError("launch evidence snapshot must reflect the current passing test count")
    if payload["public_github_stats"]["stars"] != 0:
        raise AssertionError("launch evidence snapshot must preserve the current zero-star baseline")
    if payload["public_github_stats"]["forks"] != 1:
        raise AssertionError("launch evidence snapshot must preserve the current public fork baseline")
    if payload["review_path"]["current_count"] != 0:
        raise AssertionError("launch evidence snapshot must preserve zero accepted AI Engineer reviews")
    if payload["claimable_now_count"] != 5:
        raise AssertionError("launch evidence snapshot must include 5 current claimable launch signals")
    if payload["blocked_claim_count"] != 5:
        raise AssertionError("launch evidence snapshot must include 5 blocked overclaiming rules")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("public demo", "container image", "ai engineer reviewer card", "active users", "business adoption"):
        if required not in joined:
            raise AssertionError(f"launch evidence snapshot missing required concept: {required}")
    return {
        "launch_evidence_snapshot_verified": True,
        "launch_surface_count": payload["launch_surface_count"],
        "claimable_now_count": payload["claimable_now_count"],
        "blocked_claim_count": payload["blocked_claim_count"],
    }


def main() -> None:
    payload = build_launch_evidence_snapshot()
    verify_launch_evidence_snapshot(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
