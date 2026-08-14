import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "public-launch-broadcast.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-launch-broadcast.md"


def build_public_launch_broadcast() -> dict[str, Any]:
    broadcasts = [
        {
            "id": "github_issue_19_launch_update",
            "channel": "GitHub issue comment",
            "public_url": "https://github.com/sunnnn2005/data-quality-agent/issues/19#issuecomment-5289908319",
            "published": True,
            "audience": "non-owner reviewers, AI Engineer reviewers, data peers, and open-source contributors",
            "purpose": "Route real reviewers to the public demo, external run quickstart, AI Engineer review slot, reviewer submission hub, and evidence acceptance checklist.",
            "counts_as_outcome": False,
            "why_not_outcome": "Owner-authored launch comments are distribution evidence only; they are not external users, feedback, accepted reviews, or stars.",
            "privacy_boundary": "The broadcast asks reviewers not to include private data, secrets, customer rows, emails, addresses, API keys, or proprietary screenshots.",
        }
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_launch_broadcast.py",
        "purpose": "Record public distribution actions that make external review possible without converting owner-authored launch posts into resume outcomes.",
        "broadcast_count": len(broadcasts),
        "published_broadcast_count": sum(1 for item in broadcasts if item["published"]),
        "public_broadcasts": broadcasts,
        "current_outcome_counts": {
            "confirmed_external_users": 0,
            "external_feedback_items": 0,
            "ai_engineer_review_items": 0,
            "github_stars": 0,
        },
        "resume_status": "public_launch_published_not_outcome_evidence",
        "not_claimed": [
            "external users",
            "external feedback",
            "accepted AI Engineer reviews",
            "GitHub stars",
        ],
        "resume_safe_summary": (
            "Published 1 public GitHub launch update routing reviewers to the demo, quickstart, AI Engineer "
            "review slot, and evidence gates while preserving zero external outcome counts."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {item['id']} | {item['channel']} | [link]({item['public_url']}) | {item['counts_as_outcome']} |"
        for item in payload["public_broadcasts"]
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_outcome_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Launch Broadcast

This generated artifact records public distribution actions without treating owner-authored launch posts as external outcomes.

## Broadcasts

| ID | Channel | Public URL | Counts As Outcome |
| --- | --- | --- | --- |
{rows}

## Current Outcome Counts

| Metric | Count |
| --- | ---: |
{counts}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_public_launch_broadcast(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["broadcast_count"] != 1:
        raise AssertionError("public launch broadcast must record one current public launch update")
    if payload["published_broadcast_count"] != 1:
        raise AssertionError("public launch broadcast must confirm the GitHub issue comment was published")
    broadcast = payload["public_broadcasts"][0]
    if "issuecomment-" not in broadcast["public_url"]:
        raise AssertionError("public launch broadcast must include the concrete GitHub issue comment URL")
    if broadcast["counts_as_outcome"] is not False:
        raise AssertionError("owner-authored launch broadcast must not count as outcome evidence")
    if any(value != 0 for value in payload["current_outcome_counts"].values()):
        raise AssertionError("public launch broadcast must preserve zero external outcome counts")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "owner-authored",
        "not external users",
        "privacy",
        "evidence acceptance checklist",
        "zero external outcome counts",
    ):
        if phrase not in joined:
            raise AssertionError(f"public launch broadcast missing phrase: {phrase}")
    return {
        "public_launch_broadcast_verified": True,
        "broadcast_count": payload["broadcast_count"],
        "published_broadcast_count": payload["published_broadcast_count"],
    }


def main() -> None:
    payload = build_public_launch_broadcast()
    verify_public_launch_broadcast(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "broadcast_count": payload["broadcast_count"]}))


if __name__ == "__main__":
    main()
