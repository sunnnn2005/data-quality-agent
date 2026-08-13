import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "adoption-metrics.json"
REPO = "sunnnn2005/data-quality-agent"


def _run_gh(args: list[str]) -> dict[str, Any] | None:
    try:
        completed = subprocess.run(
            ["gh", *args],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return json.loads(completed.stdout)


def collect_metrics() -> dict[str, Any]:
    repo_payload = _run_gh(
        [
            "repo",
            "view",
            REPO,
            "--json",
            "stargazerCount,forkCount,watchers,issues,url",
        ]
    )
    release_payload = _run_gh(
        [
            "release",
            "view",
            "v0.1.0",
            "--repo",
            REPO,
            "--json",
            "tagName,url,publishedAt,isDraft,isPrerelease",
        ]
    )

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "stars": _read_int_env("ADOPTION_STARS", repo_payload, "stargazerCount"),
        "forks": _read_int_env("ADOPTION_FORKS", repo_payload, "forkCount"),
        "watchers": _read_nested_int(repo_payload, ["watchers", "totalCount"], "ADOPTION_WATCHERS"),
        "open_feedback_loop": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
        "issues_total": _read_nested_int(repo_payload, ["issues", "totalCount"], "ADOPTION_ISSUES_TOTAL"),
        "public_demo": "https://sunnnn2005.github.io/data-quality-agent/",
        "release": release_payload
        or {
            "tagName": "v0.1.0",
            "url": "https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.1.0",
            "publishedAt": None,
            "isDraft": False,
            "isPrerelease": False,
        },
        "container_image": {
            "image": "ghcr.io/sunnnn2005/data-quality-agent:latest",
            "package_url": "https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
        },
        "verified_demo_artifact": "docs/verified-support-ticket-result.json",
        "test_count": 42,
    }
    return metrics


def _read_int_env(name: str, payload: dict[str, Any] | None, key: str) -> int:
    if name in os.environ:
        return int(os.environ[name])
    if payload is None:
        return 0
    return int(payload.get(key, 0))


def _read_nested_int(payload: dict[str, Any] | None, keys: list[str], env_name: str) -> int:
    if env_name in os.environ:
        return int(os.environ[env_name])
    value: Any = payload or {}
    for key in keys:
        value = value.get(key, {}) if isinstance(value, dict) else {}
    return int(value or 0)


def main() -> None:
    metrics = collect_metrics()
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
