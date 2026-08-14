import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "feedback-metrics.json"
EXTERNAL_REVIEWER_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
REPO = "sunnnn2005/data-quality-agent"
PUBLIC_ISSUES_API = f"https://api.github.com/repos/{REPO}/issues"
OWNER_LOGINS = {"sunnnn2005"}
PLANNING_LABELS = {"pilot", "roadmap"}
EXTERNAL_EVIDENCE_METRICS = {
    "external_feedback_items",
    "confirmed_external_users",
    "reproducible_feedback_items",
    "business_case_feedback_items",
    "ai_engineer_review_items",
}
FEEDBACK_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md"
BUSINESS_CASE_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md"
AI_ENGINEER_REVIEW_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md"
TRACKING_LABELS = {
    "external_feedback_items": "feedback",
    "confirmed_external_users": "confirmed-user",
    "reproducible_feedback_items": "reproducible",
    "bug_feedback_items": "bug",
    "feature_feedback_items": "enhancement",
    "business_case_feedback_items": "business-case",
    "ai_engineer_review_items": "ai-engineer-review",
}


def collect_feedback_metrics() -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "feedback_issue_template": FEEDBACK_ISSUE_URL,
        "external_feedback_items": _read_count(
            "FEEDBACK_ITEMS",
            TRACKING_LABELS["external_feedback_items"],
            metric_name="external_feedback_items",
        ),
        "confirmed_external_users": _read_count(
            "CONFIRMED_EXTERNAL_USERS",
            TRACKING_LABELS["confirmed_external_users"],
            metric_name="confirmed_external_users",
        ),
        "reproducible_feedback_items": _read_count(
            "REPRODUCIBLE_FEEDBACK_ITEMS",
            TRACKING_LABELS["reproducible_feedback_items"],
            metric_name="reproducible_feedback_items",
        ),
        "bug_feedback_items": _read_count("BUG_FEEDBACK_ITEMS", TRACKING_LABELS["bug_feedback_items"]),
        "feature_feedback_items": _read_count("FEATURE_FEEDBACK_ITEMS", TRACKING_LABELS["feature_feedback_items"]),
        "business_case_feedback_items": _read_count(
            "BUSINESS_CASE_FEEDBACK_ITEMS",
            TRACKING_LABELS["business_case_feedback_items"],
            metric_name="business_case_feedback_items",
        ),
        "ai_engineer_review_items": _read_count(
            "AI_ENGINEER_REVIEW_ITEMS",
            TRACKING_LABELS["ai_engineer_review_items"],
            metric_name="ai_engineer_review_items",
        ),
        "tracking_labels": TRACKING_LABELS,
        "feedback_channels": [
            {
                "name": "Demo feedback",
                "url": FEEDBACK_ISSUE_URL,
                "counts_toward": "external_feedback_items",
            },
            {
                "name": "Bug report",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md",
                "counts_toward": "bug_feedback_items",
            },
            {
                "name": "Feature request",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=feature_request.md",
                "counts_toward": "feature_feedback_items",
            },
            {
                "name": "Business case review",
                "url": BUSINESS_CASE_ISSUE_URL,
                "counts_toward": "business_case_feedback_items",
            },
            {
                "name": "AI Engineer review",
                "url": AI_ENGINEER_REVIEW_ISSUE_URL,
                "counts_toward": "ai_engineer_review_items",
            },
        ],
        "status": "TRACKING",
        "self_authored_planning_excluded": True,
        "resume_policy": "Do not claim users, customer feedback, or production adoption until these metrics are greater than zero and backed by public issues.",
    }


def _read_count(env_name: str, label: str, metric_name: str | None = None) -> int:
    if env_name in os.environ:
        return int(os.environ[env_name])
    if metric_name in EXTERNAL_EVIDENCE_METRICS:
        gate_count = _read_external_gate_count(metric_name)
        if gate_count is not None:
            return gate_count
    count = _count_issues_by_label(label, exclude_self_authored_planning=metric_name in EXTERNAL_EVIDENCE_METRICS)
    return 0 if count is None else count


def _read_external_gate_count(metric_name: str | None) -> int | None:
    if not metric_name or not EXTERNAL_REVIEWER_GATE_PATH.exists():
        return None
    payload = json.loads(EXTERNAL_REVIEWER_GATE_PATH.read_text())
    accepted_counts = payload.get("accepted_counts", {})
    if metric_name in accepted_counts:
        return int(accepted_counts[metric_name])
    return None


def _count_issues_by_label(label: str, *, exclude_self_authored_planning: bool = False) -> int | None:
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
                "number,labels,author",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        payload = _collect_public_issues_by_label(label)
        if payload is None:
            return None
    else:
        payload = json.loads(completed.stdout)
    if exclude_self_authored_planning:
        payload = [
            issue
            for issue in payload
            if not (
                issue.get("author", {}).get("login") in OWNER_LOGINS
                and PLANNING_LABELS.intersection({label["name"] for label in issue.get("labels", [])})
            )
        ]
    return len(payload)


def _collect_public_issues_by_label(label: str) -> list[dict[str, Any]] | None:
    query = urlencode({"state": "all", "labels": label, "per_page": "100"})
    request = Request(
        f"{PUBLIC_ISSUES_API}?{query}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "data-quality-agent-feedback-metrics",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError):
        return None
    return [_normalize_public_api_issue(issue) for issue in payload if "pull_request" not in issue]


def _normalize_public_api_issue(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": issue.get("number"),
        "author": {"login": (issue.get("user") or {}).get("login", "")},
        "labels": [{"name": label.get("name", "")} for label in issue.get("labels", [])],
    }


def write_feedback_metrics() -> dict[str, Any]:
    metrics = collect_feedback_metrics()
    OUTPUT_PATH.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    return metrics


def main() -> None:
    print(json.dumps(write_feedback_metrics(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
