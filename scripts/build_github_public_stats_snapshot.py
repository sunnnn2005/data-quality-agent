import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "github-public-stats-snapshot.json"
OUTPUT_MD_PATH = ROOT / "docs" / "github-public-stats-snapshot.md"
REPO = "sunnnn2005/data-quality-agent"


def fetch_repo_payload() -> dict[str, Any]:
    try:
        completed = subprocess.run(
            ["gh", "api", f"repos/{REPO}"],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        return {"error": exc.__class__.__name__}
    return json.loads(completed.stdout)


def build_github_public_stats_snapshot(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    repo = fetch_repo_payload() if payload is None else payload
    available = "stargazers_count" in repo
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_github_public_stats_snapshot.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "source": f"https://api.github.com/repos/{REPO}",
        "source_available": available,
        "public_stats": {
            "stars": _int(repo.get("stargazers_count")),
            "forks": _int(repo.get("forks_count")),
            "watchers": _int(repo.get("watchers_count")),
            "subscribers": _int(repo.get("subscribers_count")),
            "open_issues": _int(repo.get("open_issues_count")),
        },
        "repo_metadata": {
            "default_branch": repo.get("default_branch"),
            "pushed_at": repo.get("pushed_at"),
            "html_url": repo.get("html_url") or f"https://github.com/{REPO}",
            "visibility": repo.get("visibility"),
        },
        "resume_policy": (
            "Public GitHub stats are external visibility signals. Stars may be claimed only as the current public "
            "star count. Forks, watchers, subscribers, and issues must not be described as confirmed users, "
            "customer feedback, production adoption, or business impact."
        ),
        "metric_notes": {
            "open_issues": "GitHub REST API open_issues_count includes open issues and pull requests.",
        },
        "resume_safe_summary": (
            "Captured the repository's public GitHub API stats so future stars/forks can be reported from a "
            "verifiable source without inflating them into users or feedback."
        ),
        "not_claimed": [
            "confirmed users",
            "customer feedback",
            "production deployment",
            "business impact",
            "stars above the live public count",
        ],
    }


def _int(value: Any) -> int:
    return int(value) if isinstance(value, int) else 0


def render_markdown(payload: dict[str, Any]) -> str:
    stats = payload["public_stats"]
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# GitHub Public Stats Snapshot

This generated artifact records live public repository stats from the GitHub API.

## Summary

| Metric | Value |
| --- | ---: |
| Source available | {payload["source_available"]} |
| Stars | {stats["stars"]} |
| Forks | {stats["forks"]} |
| Watchers | {stats["watchers"]} |
| Subscribers | {stats["subscribers"]} |
| Open issues / PRs | {stats["open_issues"]} |

Source: {payload["source"]}

Repository: {payload["repo_metadata"]["html_url"]}

Last pushed: {payload["repo_metadata"]["pushed_at"]}

Metric note: {payload["metric_notes"]["open_issues"]}

## Resume Policy

{payload["resume_policy"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_github_public_stats_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    stats = payload["public_stats"]
    for key, value in stats.items():
        if not isinstance(value, int) or value < 0:
            raise AssertionError(f"{key} must be a non-negative integer")
    if payload["repo"] != "https://github.com/sunnnn2005/data-quality-agent":
        raise AssertionError("public stats snapshot must point to the Data Quality Agent repo")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("confirmed users", "customer feedback", "production adoption", "business impact"):
        if forbidden not in joined:
            raise AssertionError(f"public stats policy must avoid claiming {forbidden}")
    return {
        "github_public_stats_snapshot_verified": True,
        "stars": stats["stars"],
        "forks": stats["forks"],
        "watchers": stats["watchers"],
        "open_issues": stats["open_issues"],
    }


def main() -> None:
    payload = build_github_public_stats_snapshot()
    verify_github_public_stats_snapshot(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
