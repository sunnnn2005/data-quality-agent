import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "feedback-metrics.json"
REPO = "sunnnn2005/data-quality-agent"
FEEDBACK_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md"


def collect_feedback_metrics() -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "feedback_issue_template": FEEDBACK_ISSUE_URL,
        "external_feedback_items": _read_count("FEEDBACK_ITEMS", "feedback"),
        "confirmed_external_users": _read_count("CONFIRMED_EXTERNAL_USERS", "confirmed-user"),
        "reproducible_feedback_items": _read_count("REPRODUCIBLE_FEEDBACK_ITEMS", "reproducible"),
        "bug_feedback_items": _read_count("BUG_FEEDBACK_ITEMS", "bug"),
        "feature_feedback_items": _read_count("FEATURE_FEEDBACK_ITEMS", "enhancement"),
        "status": "TRACKING",
        "resume_policy": "Do not claim users, customer feedback, or production adoption until these metrics are greater than zero and backed by public issues.",
    }


def _read_count(env_name: str, label: str) -> int:
    if env_name in os.environ:
        return int(os.environ[env_name])
    count = _count_issues_by_label(label)
    return 0 if count is None else count


def _count_issues_by_label(label: str) -> int | None:
    try:
        completed = subprocess.run(
            [
                "gh",
                "issue",
                "list",
                "--repo",
                REPO,
                "--label",
                label,
                "--state",
                "all",
                "--limit",
                "1000",
                "--json",
                "number",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    payload = json.loads(completed.stdout)
    return len(payload)


def write_feedback_metrics() -> dict[str, Any]:
    metrics = collect_feedback_metrics()
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    return metrics


def main() -> None:
    print(json.dumps(write_feedback_metrics(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
