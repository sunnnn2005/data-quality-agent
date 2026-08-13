import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "adoption-metrics.json"
HISTORY_PATH = ROOT / "docs" / "adoption-history.jsonl"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REPO = "sunnnn2005/data-quality-agent"
CURRENT_RELEASE_TAG = "v0.3.0"


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
    feedback_metrics = _load_feedback_metrics()
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
            CURRENT_RELEASE_TAG,
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
        "external_feedback_items": feedback_metrics.get("external_feedback_items", 0),
        "confirmed_external_users": feedback_metrics.get("confirmed_external_users", 0),
        "reproducible_feedback_items": feedback_metrics.get("reproducible_feedback_items", 0),
        "issues_total": _read_nested_int(repo_payload, ["issues", "totalCount"], "ADOPTION_ISSUES_TOTAL"),
        "public_demo": "https://sunnnn2005.github.io/data-quality-agent/",
        "release": release_payload
        or {
            "tagName": CURRENT_RELEASE_TAG,
            "url": f"https://github.com/sunnnn2005/data-quality-agent/releases/tag/{CURRENT_RELEASE_TAG}",
            "publishedAt": None,
            "isDraft": False,
            "isPrerelease": False,
        },
        "container_image": {
            "image": "ghcr.io/sunnnn2005/data-quality-agent:latest",
            "package_url": "https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
        },
        "verified_demo_artifact": "docs/verified-support-ticket-result.json",
        "test_count": _collect_test_count(),
        "commit": _current_commit(),
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


def _load_feedback_metrics() -> dict[str, Any]:
    if FEEDBACK_METRICS_PATH.exists():
        return json.loads(FEEDBACK_METRICS_PATH.read_text())
    return {
        "external_feedback_items": int(os.environ.get("FEEDBACK_ITEMS", "0")),
        "confirmed_external_users": int(os.environ.get("CONFIRMED_EXTERNAL_USERS", "0")),
        "reproducible_feedback_items": int(os.environ.get("REPRODUCIBLE_FEEDBACK_ITEMS", "0")),
    }


def _collect_test_count() -> int:
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return int(os.environ.get("ADOPTION_TEST_COUNT", "0"))

    match = re.search(r"(\d+)\s+tests?\s+collected", completed.stdout)
    if match:
        return int(match.group(1))
    existing = _load_existing_metrics()
    if "test_count" in existing:
        return int(existing["test_count"])
    return int(os.environ.get("ADOPTION_TEST_COUNT", "0"))


def _load_existing_metrics() -> dict[str, Any]:
    if OUTPUT_PATH.exists():
        return json.loads(OUTPUT_PATH.read_text())
    return {}


def main() -> None:
    metrics = collect_metrics()
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    append_history(metrics)
    print(json.dumps(metrics, indent=2, sort_keys=True))


def append_history(metrics: dict[str, Any]) -> None:
    point = {
        "date": metrics["generated_at"][:10],
        "commit": metrics.get("commit"),
        "stars": metrics["stars"],
        "forks": metrics["forks"],
        "watchers": metrics["watchers"],
        "issues_total": metrics["issues_total"],
        "external_feedback_items": metrics["external_feedback_items"],
        "confirmed_external_users": metrics["confirmed_external_users"],
        "test_count": metrics["test_count"],
        "release": metrics["release"]["tagName"],
    }
    existing = []
    if HISTORY_PATH.exists():
        existing = [json.loads(line) for line in HISTORY_PATH.read_text().splitlines() if line.strip()]

    deduped = [
        item
        for item in existing
        if not (item.get("date") == point["date"] and item.get("commit") == point["commit"])
    ]
    deduped.append(point)
    HISTORY_PATH.write_text("\n".join(json.dumps(item, sort_keys=True) for item in deduped) + "\n")


def _current_commit() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


if __name__ == "__main__":
    main()
