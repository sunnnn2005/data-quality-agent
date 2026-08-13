import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
COMMUNITY_GROWTH_PATH = ROOT / "docs" / "community-growth-baseline.json"
PUBLIC_TRACTION_PATH = ROOT / "docs" / "public-traction-dashboard.json"
GITHUB_TRAFFIC_PATH = ROOT / "docs" / "github-traffic-snapshot.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "star-growth-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "star-growth-kit.md"


REQUIRED_TOPICS = {
    "ai-agent",
    "data-engineering",
    "data-quality",
    "fastapi",
    "github-actions",
    "python",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_star_growth_kit_payload() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    community = load_json(COMMUNITY_GROWTH_PATH)
    traction = load_json(PUBLIC_TRACTION_PATH)
    traffic = load_json(GITHUB_TRAFFIC_PATH)
    repo_topics = _load_repo_topics()
    missing_topics = sorted(REQUIRED_TOPICS - set(repo_topics))
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_star_growth_kit.py",
        "repo": adoption["repo"],
        "public_demo": adoption["public_demo"],
        "current_public_counts": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "watchers": adoption["watchers"],
            "issues_total": adoption["issues_total"],
            "external_feedback_items": adoption["external_feedback_items"],
            "confirmed_external_users": adoption["confirmed_external_users"],
            "github_views_14d": traffic["traffic_metrics"]["view_count"],
            "github_unique_visitors_14d": traffic["traffic_metrics"]["unique_visitors"],
            "github_clones_14d": traffic["traffic_metrics"]["clone_count"],
            "github_unique_cloners_14d": traffic["traffic_metrics"]["unique_cloners"],
        },
        "traffic_snapshot": {
            "source": traffic["traffic_window"],
            "traffic_available": traffic["traffic_available"],
            "snapshot_url": f"{adoption['repo']}/blob/main/docs/github-traffic-snapshot.md",
            "resume_policy": traffic["resume_policy"],
        },
        "topic_readiness": {
            "required_topics": sorted(REQUIRED_TOPICS),
            "current_topics": repo_topics,
            "missing_topics": missing_topics,
            "ready": not missing_topics,
        },
        "growth_assets": {
            "readme_badges": True,
            "public_demo": adoption["public_demo"],
            "release": adoption["release"]["url"],
            "container_image": adoption["container_image"]["package_url"],
            "contributing_guide": f"{adoption['repo']}/blob/main/CONTRIBUTING.md",
            "good_first_issues": "https://github.com/sunnnn2005/data-quality-agent/labels/good%20first%20issue",
            "pilot_feedback_tracker": "https://github.com/sunnnn2005/data-quality-agent/issues/16",
            "public_traction_dashboard": f"{adoption['repo']}/blob/main/docs/public-traction-dashboard.md",
        },
        "ethical_growth_actions": [
            {
                "channel": "classmates_or_club",
                "action": "Ask reviewers to try the demo, leave feedback, and star only if they genuinely want to follow the project.",
            },
            {
                "channel": "github_readme",
                "action": "Keep the first screen clear: demo, release, tests, container, evidence links, and contribution entrypoints.",
            },
            {
                "channel": "good_first_issues",
                "action": "Maintain beginner-friendly issues so contributors have a low-friction first task.",
            },
            {
                "channel": "linkedin_or_email",
                "action": "Share the public demo and evidence pack as a technical project, not as a request for fake engagement.",
            },
        ],
        "resume_upgrade_rules": [
            {
                "signal": "github stars",
                "current_value": adoption["stars"],
                "minimum_before_claim": 5,
                "evidence_required": "GitHub stargazer count from the public repository",
                "resume_status": "not_claimable_yet",
            },
            {
                "signal": "external contributors",
                "current_value": 0,
                "minimum_before_claim": 1,
                "evidence_required": "merged pull request or public issue from a non-owner contributor",
                "resume_status": "not_claimable_yet",
            },
            {
                "signal": "public pilot feedback",
                "current_value": adoption["external_feedback_items"],
                "minimum_before_claim": 3,
                "evidence_required": "public feedback issues linked from the pilot tracker",
                "resume_status": "not_claimable_yet",
            },
            {
                "signal": "repository interest",
                "current_value": traffic["traffic_metrics"]["unique_visitors"],
                "minimum_before_claim": 25,
                "evidence_required": "GitHub traffic snapshot showing unique visitors in the rolling 14-day window",
                "resume_status": "not_claimable_yet",
            },
        ],
        "current_growth_channels": traction["growth_channel_count"],
        "community_growth_channels": len(community["public_growth_channels"]),
        "not_claimed": [
            "GitHub star growth beyond the current public count",
            "external contributors",
            "community adoption",
            "paid promotion",
            "fake or incentivized stars",
            "confirmed users from traffic alone",
        ],
        "resume_safe_summary": (
            "Published a CI-verified star growth kit with repository topic readiness, ethical growth actions, "
            "GitHub traffic context, growth assets, and resume-upgrade rules while keeping current stars at the verified public count."
        ),
    }


def _load_repo_topics() -> list[str]:
    try:
        import subprocess

        completed = subprocess.run(
            [
                "gh",
                "repo",
                "view",
                "sunnnn2005/data-quality-agent",
                "--json",
                "repositoryTopics",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(REQUIRED_TOPICS)
    payload = json.loads(completed.stdout)
    return sorted(topic["name"] for topic in payload.get("repositoryTopics", []))


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    topics = payload["topic_readiness"]
    topic_rows = "\n".join(
        f"| {topic} | {'yes' if topic in topics['current_topics'] else 'no'} |" for topic in topics["required_topics"]
    )
    assets = "\n".join(f"- {key.replace('_', ' ').title()}: [{value}]({value})" for key, value in payload["growth_assets"].items() if isinstance(value, str))
    actions = "\n".join(f"- {item['channel']}: {item['action']}" for item in payload["ethical_growth_actions"])
    traffic = payload["traffic_snapshot"]
    rules = "\n".join(
        f"| {item['signal']} | {item['current_value']} | {item['minimum_before_claim']} | {item['evidence_required']} | `{item['resume_status']}` |"
        for item in payload["resume_upgrade_rules"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Star Growth Kit

This generated kit documents ethical ways to improve public GitHub traction without buying, trading, or inflating stars.

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Topic Readiness

| Topic | Present |
| --- | --- |
{topic_rows}

Topic readiness: `{topics["ready"]}`

## Growth Assets

{assets}

## Ethical Growth Actions

{actions}

## Traffic Snapshot

- Source: {traffic["source"]}
- Traffic available: `{traffic["traffic_available"]}`
- Snapshot: [{traffic["snapshot_url"]}]({traffic["snapshot_url"]})
- Policy: {traffic["resume_policy"]}

## Resume Upgrade Rules

| Signal | Current value | Minimum before claim | Evidence required | Status |
| --- | ---: | ---: | --- | --- |
{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_star_growth_kit(payload: dict[str, Any]) -> dict[str, Any]:
    counts = payload["current_public_counts"]
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "watchers": 0,
        "issues_total": 14,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"star growth kit {key} expected {expected!r}, got {counts.get(key)!r}")
    if payload["topic_readiness"]["ready"] is not True:
        raise AssertionError("star growth kit must verify required repository topics")
    if len(payload["ethical_growth_actions"]) != 4:
        raise AssertionError("star growth kit must include four ethical growth actions")
    if len(payload["resume_upgrade_rules"]) != 4:
        raise AssertionError("star growth kit must include four resume upgrade rules")
    traffic_snapshot = payload["traffic_snapshot"]
    if traffic_snapshot["source"] != "GitHub traffic API rolling 14-day window":
        raise AssertionError("star growth kit must link the GitHub traffic snapshot source")
    if "confirmed users" not in traffic_snapshot["resume_policy"]:
        raise AssertionError("star growth kit must separate traffic from confirmed users")
    if not all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"]):
        raise AssertionError("star growth kit must keep zero-traction signals not claimable")
    forbidden_text = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("buy stars", "paid stars", "star exchange"):
        if forbidden in forbidden_text:
            raise AssertionError(f"star growth kit must not recommend {forbidden}")
    for required in ("fake or incentivized stars", "external contributors", "community adoption", "confirmed users from traffic alone"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"star growth kit must not claim {required}")
    return {
        "star_growth_kit_verified": True,
        "ethical_growth_action_count": len(payload["ethical_growth_actions"]),
        "resume_upgrade_rule_count": len(payload["resume_upgrade_rules"]),
        "required_topic_count": len(payload["topic_readiness"]["required_topics"]),
    }


def main() -> None:
    payload = build_star_growth_kit_payload()
    verify_star_growth_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
