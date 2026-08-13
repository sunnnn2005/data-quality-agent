import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "github-traffic-snapshot.json"
OUTPUT_MD_PATH = ROOT / "docs" / "github-traffic-snapshot.md"
REPO = "sunnnn2005/data-quality-agent"


def fetch_traffic_payloads() -> dict[str, Any]:
    endpoints = {
        "views": f"repos/{REPO}/traffic/views",
        "clones": f"repos/{REPO}/traffic/clones",
        "referrers": f"repos/{REPO}/traffic/popular/referrers",
        "paths": f"repos/{REPO}/traffic/popular/paths",
    }
    payloads: dict[str, Any] = {}
    for key, endpoint in endpoints.items():
        try:
            completed = subprocess.run(
                ["gh", "api", endpoint],
                check=True,
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            payloads[key] = {"error": exc.__class__.__name__}
            continue
        payloads[key] = json.loads(completed.stdout)
    return payloads


def build_github_traffic_snapshot(payloads: dict[str, Any] | None = None) -> dict[str, Any]:
    traffic = fetch_traffic_payloads() if payloads is None else payloads
    views = traffic.get("views", {})
    clones = traffic.get("clones", {})
    traffic_available = "count" in views and "count" in clones
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_github_traffic_snapshot.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "traffic_window": "GitHub traffic API rolling 14-day window",
        "traffic_available": traffic_available,
        "views": {
            "count": int(views.get("count", 0)) if isinstance(views, dict) else 0,
            "uniques": int(views.get("uniques", 0)) if isinstance(views, dict) else 0,
            "daily": views.get("views", []) if isinstance(views, dict) else [],
        },
        "clones": {
            "count": int(clones.get("count", 0)) if isinstance(clones, dict) else 0,
            "uniques": int(clones.get("uniques", 0)) if isinstance(clones, dict) else 0,
            "daily": clones.get("clones", []) if isinstance(clones, dict) else [],
        },
        "top_referrers": traffic.get("referrers", []) if isinstance(traffic.get("referrers"), list) else [],
        "top_paths": traffic.get("paths", []) if isinstance(traffic.get("paths"), list) else [],
        "resume_policy": (
            "Traffic, views, and clones are repository-interest signals only. Do not claim these as confirmed users, "
            "customer feedback, production adoption, or successful business outcomes."
        ),
        "resume_safe_summary": (
            "Captured a GitHub traffic snapshot as an early public-interest signal while explicitly separating "
            "views and clones from confirmed users or feedback."
        ),
        "not_claimed": [
            "confirmed users from traffic alone",
            "customer feedback from traffic alone",
            "production adoption",
            "GitHub stars beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    referrers = "\n".join(
        f"| {item.get('referrer', '-')} | {item.get('count', 0)} | {item.get('uniques', 0)} |"
        for item in payload["top_referrers"][:10]
    )
    if not referrers:
        referrers = "| - | 0 | 0 |"
    paths = "\n".join(
        f"| {item.get('path', '-')} | {item.get('title', '-')} | {item.get('count', 0)} | {item.get('uniques', 0)} |"
        for item in payload["top_paths"][:10]
    )
    if not paths:
        paths = "| - | - | 0 | 0 |"
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# GitHub Traffic Snapshot

This generated artifact captures GitHub's rolling traffic window as a public-interest signal.

## Summary

| Metric | Value |
| --- | ---: |
| Traffic available | {payload["traffic_available"]} |
| View count | {payload["views"]["count"]} |
| Unique visitors | {payload["views"]["uniques"]} |
| Clone count | {payload["clones"]["count"]} |
| Unique cloners | {payload["clones"]["uniques"]} |

Traffic window: {payload["traffic_window"]}

## Top Referrers

| Referrer | Count | Unique visitors |
| --- | ---: | ---: |
{referrers}

## Top Paths

| Path | Title | Count | Unique visitors |
| --- | --- | ---: | ---: |
{paths}

## Resume Policy

{payload["resume_policy"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_github_traffic_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["traffic_window"] != "GitHub traffic API rolling 14-day window":
        raise AssertionError("traffic snapshot must document the GitHub rolling window")
    for section in ("views", "clones"):
        if payload[section]["count"] < 0 or payload[section]["uniques"] < 0:
            raise AssertionError(f"{section} counts must be non-negative")
        if payload[section]["uniques"] > payload[section]["count"]:
            raise AssertionError(f"{section} unique count cannot exceed total count")
    for forbidden in ("confirmed users", "customer feedback", "production adoption"):
        if forbidden not in payload["resume_policy"]:
            raise AssertionError(f"traffic policy must not claim {forbidden}")
    return {
        "github_traffic_snapshot_verified": True,
        "traffic_available": payload["traffic_available"],
        "view_count": payload["views"]["count"],
        "unique_visitors": payload["views"]["uniques"],
        "clone_count": payload["clones"]["count"],
        "unique_cloners": payload["clones"]["uniques"],
    }


def main() -> None:
    payload = build_github_traffic_snapshot()
    verify_github_traffic_snapshot(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
