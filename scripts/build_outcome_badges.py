import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
ACCEPTED_EVIDENCE_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
GITHUB_PUBLIC_STATS_PATH = ROOT / "docs" / "github-public-stats-snapshot.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-badges.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-badges.md"
BADGE_DIR = ROOT / "docs" / "badges"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _badge(
    *,
    badge_id: str,
    label: str,
    message: str,
    color: str,
    source: str,
    resume_claimable: bool,
    policy: str,
) -> dict[str, Any]:
    return {
        "id": badge_id,
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
        "source": source,
        "resume_claimable": resume_claimable,
        "policy": policy,
    }


def build_outcome_badges() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    accepted = load_json(ACCEPTED_EVIDENCE_PATH)
    public_stats = load_json(GITHUB_PUBLIC_STATS_PATH)
    accepted_counts = accepted["accepted_counts"]
    github_stats = public_stats["public_stats"]

    badges = [
        _badge(
            badge_id="ci-tests",
            label="tests",
            message=f"{adoption['test_count']} passing",
            color="brightgreen",
            source="docs/adoption-metrics.json",
            resume_claimable=True,
            policy="Engineering-quality signal backed by local and GitHub Actions test output.",
        ),
        _badge(
            badge_id="github-stars",
            label="stars",
            message=f"{github_stats['stars']} public",
            color="blue" if github_stats["stars"] > 0 else "lightgrey",
            source="docs/github-public-stats-snapshot.json",
            resume_claimable=github_stats["stars"] >= 5,
            policy="Claim only the current public GitHub star count; never imply users or adoption from stars.",
        ),
        _badge(
            badge_id="github-forks",
            label="forks",
            message=f"{github_stats['forks']} public",
            color="blue" if github_stats["forks"] > 0 else "lightgrey",
            source="docs/github-public-stats-snapshot.json",
            resume_claimable=github_stats["forks"] > 0,
            policy="Forks are public repository-interest signals, not confirmed users or customer feedback.",
        ),
        _badge(
            badge_id="confirmed-users",
            label="confirmed users",
            message=f"{accepted_counts['confirmed_external_users']} accepted",
            color="success" if accepted_counts["confirmed_external_users"] > 0 else "lightgrey",
            source="docs/accepted-evidence-rollup.json",
            resume_claimable=accepted_counts["confirmed_external_users"] > 0,
            policy="Count only non-owner public evidence that passed the external reviewer evidence gate.",
        ),
        _badge(
            badge_id="external-feedback",
            label="feedback",
            message=f"{accepted_counts['external_feedback_items']} accepted",
            color="success" if accepted_counts["external_feedback_items"] > 0 else "lightgrey",
            source="docs/accepted-evidence-rollup.json",
            resume_claimable=accepted_counts["external_feedback_items"] > 0,
            policy="Count only public, permissioned, redacted feedback issues accepted by the evidence gate.",
        ),
        _badge(
            badge_id="ai-review",
            label="AI review",
            message=f"{accepted_counts['ai_engineer_review_items']} accepted",
            color="success" if accepted_counts["ai_engineer_review_items"] > 0 else "lightgrey",
            source="docs/accepted-evidence-rollup.json",
            resume_claimable=accepted_counts["ai_engineer_review_items"] > 0,
            policy="Count only external AI Engineer review issues that name inspected implementation evidence.",
        ),
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_badges.py",
        "badge_count": len(badges),
        "claimable_badge_count": sum(1 for badge in badges if badge["resume_claimable"]),
        "blocked_badge_ids": [badge["id"] for badge in badges if not badge["resume_claimable"]],
        "badges": badges,
        "resume_policy": (
            "These badges are display helpers over verified evidence artifacts. They must not turn views, forks, "
            "stars, or prepared outreach into confirmed users, feedback, production usage, or business impact."
        ),
        "resume_safe_summary": (
            "Generated evidence-backed outcome badges for tests, GitHub stats, confirmed users, feedback, and AI "
            "review while keeping blocked outcome claims visibly grey until accepted public evidence exists."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| `{id}` | {label} | {message} | {color} | {resume_claimable} | `{source}` |".format(**badge)
        for badge in payload["badges"]
    )
    blocked = "\n".join(f"- `{badge_id}`" for badge_id in payload["blocked_badge_ids"])
    return f"""# Outcome Badges

This generated artifact provides embeddable, evidence-backed badge metadata for README, portfolio, and resume project pages.

## Summary

| Metric | Value |
| --- | ---: |
| Badge count | {payload["badge_count"]} |
| Claimable badges | {payload["claimable_badge_count"]} |

## Badges

| ID | Label | Message | Color | Resume claimable | Source |
| --- | --- | --- | --- | --- | --- |
{rows}

## Blocked Badges

{blocked}

## Resume Policy

{payload["resume_policy"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_outcome_badges(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["badge_count"] != 6:
        raise AssertionError("outcome badges must expose six display badges")
    badges = {badge["id"]: badge for badge in payload["badges"]}
    for required in ("ci-tests", "github-stars", "github-forks", "confirmed-users", "external-feedback", "ai-review"):
        if required not in badges:
            raise AssertionError(f"missing outcome badge: {required}")
    if not badges["ci-tests"]["resume_claimable"]:
        raise AssertionError("CI tests badge should be claimable as an engineering-quality signal")
    for blocked in ("github-stars", "confirmed-users", "external-feedback", "ai-review"):
        if badges[blocked]["resume_claimable"]:
            raise AssertionError(f"{blocked} should stay blocked until external evidence exists")
        if badges[blocked]["color"] != "lightgrey":
            raise AssertionError(f"{blocked} should render as grey while blocked")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("confirmed users", "feedback", "production usage", "business impact"):
        if phrase not in joined:
            raise AssertionError(f"outcome badge policy missing {phrase}")
    return {
        "outcome_badges_verified": True,
        "badge_count": payload["badge_count"],
        "claimable_badge_count": payload["claimable_badge_count"],
    }


def write_shields_badges(payload: dict[str, Any]) -> None:
    BADGE_DIR.mkdir(parents=True, exist_ok=True)
    for badge in payload["badges"]:
        shield_payload = {
            "schemaVersion": badge["schemaVersion"],
            "label": badge["label"],
            "message": badge["message"],
            "color": badge["color"],
        }
        (BADGE_DIR / f"{badge['id']}.json").write_text(json.dumps(shield_payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    payload = build_outcome_badges()
    verify_outcome_badges(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    write_shields_badges(payload)
    print(json.dumps({"status": "ok", "badge_count": payload["badge_count"]}))


if __name__ == "__main__":
    main()
