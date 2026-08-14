import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
DEMO_USAGE_BASELINE_PATH = ROOT / "docs" / "demo-usage-baseline.json"
COMMUNITY_GROWTH_BASELINE_PATH = ROOT / "docs" / "community-growth-baseline.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-traction-dashboard.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-traction-dashboard.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_traction_dashboard_payload() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    demo_usage = load_json(DEMO_USAGE_BASELINE_PATH)
    community = load_json(COMMUNITY_GROWTH_BASELINE_PATH)
    pilot_outreach = load_json(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_json(PILOT_PROGRAM_PLAN_PATH)
    public_counts = {
        "stars": adoption["stars"],
        "forks": adoption["forks"],
        "watchers": adoption["watchers"],
        "issues_total": adoption["issues_total"],
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
    }
    traction_surfaces = [
        {
            "name": "public_demo",
            "url": adoption["public_demo"],
            "resume_signal": "publicly launched demo",
            "status": "live",
        },
        {
            "name": "github_release",
            "url": adoption["release"]["url"],
            "resume_signal": "public release",
            "status": adoption["release"]["tagName"],
        },
        {
            "name": "container_image",
            "url": adoption["container_image"]["package_url"],
            "resume_signal": "runnable deployment artifact",
            "status": "published",
        },
        {
            "name": "feedback_issue_template",
            "url": feedback["feedback_issue_template"],
            "resume_signal": "public feedback channel",
            "status": "tracking",
        },
    ]
    pilot_review_channels = [
        {
            "name": key,
            "url": value,
            "purpose": "pilot review path",
        }
        for key, value in pilot_outreach["review_paths"].items()
    ]
    growth_channels = community["public_growth_channels"] + pilot_review_channels
    resume_upgrade_rules = [
        {
            "signal": "external users",
            "current_value": public_counts["confirmed_external_users"],
            "minimum_before_claim": 3,
            "evidence_required": "public issue or testimonial with confirmed-user label",
            "resume_status": "not_claimable_yet",
        },
        {
            "signal": "customer feedback",
            "current_value": public_counts["external_feedback_items"],
            "minimum_before_claim": pilot_plan["success_thresholds"]["minimum_feedback_items_before_resume_claim"],
            "evidence_required": "public feedback issues with feedback/reproducible labels",
            "resume_status": "not_claimable_yet",
        },
        {
            "signal": "github stars",
            "current_value": public_counts["stars"],
            "minimum_before_claim": 5,
            "evidence_required": "GitHub repository stargazer count",
            "resume_status": "not_claimable_yet",
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_traction_dashboard.py",
        "public_counts": public_counts,
        "traction_surface_count": len(traction_surfaces),
        "traction_surfaces": traction_surfaces,
        "growth_channel_count": len(growth_channels),
        "growth_channels": growth_channels,
        "tracked_funnel_steps": len(demo_usage["tracked_usage_funnel"]),
        "demo_entrypoints_verified": sum(1 for value in demo_usage["demo_entrypoints_verified"].values() if value),
        "resume_upgrade_rules": resume_upgrade_rules,
        "resume_safe_summary": (
            f"Published a public traction dashboard covering {len(traction_surfaces)} live project surfaces, "
            f"{len(growth_channels)} growth or review channels, {len(demo_usage['tracked_usage_funnel'])} tracked "
            "demo funnel steps, and explicit resume-upgrade rules for users, feedback, and stars."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "production adoption",
            "GitHub star growth beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    surfaces = "\n".join(
        f"| {item['name']} | [{item['url']}]({item['url']}) | {item['resume_signal']} | `{item['status']}` |"
        for item in payload["traction_surfaces"]
    )
    channels = "\n".join(
        f"- [{item['name']}]({item['url']}) -> {item.get('purpose', item.get('counts_toward', 'review path'))}"
        for item in payload["growth_channels"]
    )
    rules = "\n".join(
        f"| {item['signal']} | {item['current_value']} | {item['minimum_before_claim']} | {item['evidence_required']} | `{item['resume_status']}` |"
        for item in payload["resume_upgrade_rules"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Traction Dashboard

This generated dashboard separates what is live and trackable from what is not yet safe to claim on a resume.

## Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Traction Surfaces

| Surface | URL | Resume signal | Status |
| --- | --- | --- | --- |
{surfaces}

## Growth And Review Channels

{channels}

## Resume Upgrade Rules

| Signal | Current value | Minimum before claim | Evidence required | Status |
| --- | ---: | ---: | --- | --- |
{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_public_traction_dashboard(payload: dict[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "watchers": 0,
        "issues_total": 25,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    for key, expected in expected_counts.items():
        if payload["public_counts"].get(key) != expected:
            raise AssertionError(f"public traction {key} expected {expected!r}")
    if payload["traction_surface_count"] != 4:
        raise AssertionError("public traction dashboard must include 4 traction surfaces")
    if payload["growth_channel_count"] != 19:
        raise AssertionError("public traction dashboard must include 19 growth or review channels")
    if payload["tracked_funnel_steps"] != 5:
        raise AssertionError("public traction dashboard must include 5 tracked funnel steps")
    if payload["demo_entrypoints_verified"] != 6:
        raise AssertionError("public traction dashboard must verify 6 demo entrypoints")
    if len(payload["resume_upgrade_rules"]) != 3:
        raise AssertionError("public traction dashboard must include 3 resume upgrade rules")
    if not all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"]):
        raise AssertionError("public traction dashboard must preserve not-claimable status for zero traction")
    for required in ("external users", "customer feedback", "production adoption"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"public traction dashboard must not claim {required}")
    return {
        "public_traction_dashboard_verified": True,
        "traction_surface_count": payload["traction_surface_count"],
        "growth_channel_count": payload["growth_channel_count"],
        "resume_upgrade_rule_count": len(payload["resume_upgrade_rules"]),
    }


def main() -> None:
    payload = build_public_traction_dashboard_payload()
    verify_public_traction_dashboard(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
