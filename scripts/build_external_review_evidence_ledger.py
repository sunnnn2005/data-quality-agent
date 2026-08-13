import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-review-evidence-ledger.md"
REPO = "sunnnn2005/data-quality-agent"
OWNER_LOGINS = {"sunnnn2005"}
TRACKED_LABELS = {
    "feedback": "external_feedback_items",
    "confirmed-user": "confirmed_external_users",
    "business-case": "business_case_feedback_items",
    "business-data-replay": "reproducible_feedback_items",
    "reproducible": "reproducible_feedback_items",
}
PLANNING_LABELS = {"pilot", "roadmap"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_review_evidence_ledger(issues: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    evidence_entries = collect_public_evidence_entries(fetch_issues() if issues is None else issues)
    evidence_requirements = [
        {
            "evidence_type": "demo_feedback",
            "required_public_source": "GitHub issue created from demo_feedback.md",
            "required_labels": ["feedback"],
            "counts_toward": "external_feedback_items",
            "resume_upgrade_after": 3,
        },
        {
            "evidence_type": "confirmed_run",
            "required_public_source": "GitHub issue or reproducible note confirming the reviewer tried the demo or ran the repo",
            "required_labels": ["confirmed-user"],
            "counts_toward": "confirmed_external_users",
            "resume_upgrade_after": 1,
        },
        {
            "evidence_type": "business_case_review",
            "required_public_source": "GitHub issue created from business_case_review.md",
            "required_labels": ["business-case"],
            "counts_toward": "business_case_feedback_items",
            "resume_upgrade_after": 1,
        },
        {
            "evidence_type": "reproducible_bug",
            "required_public_source": "GitHub issue with steps, environment, expected result, and actual result",
            "required_labels": ["bug", "reproducible"],
            "counts_toward": "reproducible_feedback_items",
            "resume_upgrade_after": 1,
        },
    ]
    public_counts = {
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
    }
    evidence_counts = count_evidence_entries(evidence_entries)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_review_evidence_ledger.py",
        "purpose": (
            "Define the public evidence required before pilot reviews, feedback, confirmed runs, or business-case "
            "reviews can be converted into resume outcome claims."
        ),
        "entry_count": len(evidence_entries),
        "entries": evidence_entries,
        "evidence_requirement_count": len(evidence_requirements),
        "evidence_requirements": evidence_requirements,
        "public_counts": public_counts,
        "evidence_counts": evidence_counts,
        "self_authored_planning_excluded": True,
        "ignored_planning_labels": sorted(PLANNING_LABELS),
        "linked_planned_reviews": tracker["planned_review_count"],
        "review_status_counts": tracker["status_counts"],
        "resume_upgrade_rules": tracker["resume_upgrade_rules"],
        "resume_status": "claimable_feedback_exists" if evidence_entries else "not_claimable_yet",
        "not_claimed": tracker["not_claimed"],
        "resume_safe_summary": (
            f"Published a CI-verified external review evidence ledger defining 4 public evidence types, "
            f"3 linked pilot review slots, {len(evidence_entries)} counted public evidence entries, and "
            "explicit rules that exclude self-authored planning issues from external feedback claims."
        ),
    }


def fetch_issues() -> list[dict[str, Any]]:
    try:
        completed = subprocess.run(
            [
                "gh",
                "issue",
                "list",
                "--repo",
                REPO,
                "--state",
                "all",
                "--limit",
                "1000",
                "--json",
                "number,title,url,labels,state,createdAt,author",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []
    return json.loads(completed.stdout)


def collect_public_evidence_entries(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for issue in issues:
        labels = sorted(label["name"] for label in issue.get("labels", []))
        tracked_metrics = sorted({TRACKED_LABELS[label] for label in labels if label in TRACKED_LABELS})
        if not tracked_metrics:
            continue
        author = issue.get("author", {}).get("login", "")
        if author in OWNER_LOGINS and PLANNING_LABELS.intersection(labels):
            continue
        entries.append(
            {
                "issue_number": issue["number"],
                "title": issue["title"],
                "url": issue["url"],
                "state": issue["state"],
                "created_at": issue["createdAt"],
                "author": author,
                "labels": labels,
                "counts_toward": tracked_metrics,
                "external_author": author not in OWNER_LOGINS,
            }
        )
    return sorted(entries, key=lambda item: item["issue_number"])


def count_evidence_entries(entries: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    for entry in entries:
        for metric in entry["counts_toward"]:
            counts[metric] += 1
    return counts


def render_markdown(payload: dict[str, Any]) -> str:
    requirements = "\n".join(
        "| {evidence_type} | {required_public_source} | {labels} | `{counts_toward}` | {resume_upgrade_after} |".format(
            labels=", ".join(item["required_labels"]),
            **item,
        )
        for item in payload["evidence_requirements"]
    )
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    evidence_counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["evidence_counts"].items()
    )
    entries = "\n".join(
        "| #{issue_number} | [{title}]({url}) | {author} | {labels} | {metrics} | `{state}` |".format(
            issue_number=entry["issue_number"],
            title=entry["title"],
            url=entry["url"],
            author=entry["author"],
            labels=", ".join(entry["labels"]),
            metrics=", ".join(entry["counts_toward"]),
            state=entry["state"],
        )
        for entry in payload["entries"]
    )
    if not entries:
        entries = "| - | - | - | - | - | - |"
    statuses = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["review_status_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# External Review Evidence Ledger

This generated ledger defines what public proof is required before any external review can become a resume outcome.

## Purpose

{payload["purpose"]}

## Current Ledger

| Metric | Current value |
| --- | ---: |
| Evidence entries | {payload["entry_count"]} |
| Linked planned reviews | {payload["linked_planned_reviews"]} |
| Evidence requirement types | {payload["evidence_requirement_count"]} |
| Resume status | `{payload["resume_status"]}` |
| Self-authored planning excluded | {payload["self_authored_planning_excluded"]} |

## Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Counted Public Evidence

| Metric | Counted entries |
| --- | ---: |
{evidence_counts}

| Issue | Title | Author | Labels | Counts Toward | State |
| --- | --- | --- | --- | --- | --- |
{entries}

## Pilot Review Status

| Status | Count |
| --- | ---: |
{statuses}

## Evidence Requirements

| Evidence Type | Required Public Source | Required Labels | Counts Toward | Resume Upgrade After |
| --- | --- | --- | --- | ---: |
{requirements}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_review_evidence_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "evidence_requirement_count": 4,
        "linked_planned_reviews": 3,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    if payload["evidence_requirement_count"] != expected["evidence_requirement_count"]:
        raise AssertionError("external review ledger must define four evidence requirement types")
    if payload["linked_planned_reviews"] != expected["linked_planned_reviews"]:
        raise AssertionError("external review ledger must link to three planned pilot reviews")
    if payload["resume_status"] not in {"not_claimable_yet", "claimable_feedback_exists"}:
        raise AssertionError("external review ledger has an invalid resume status")
    if not payload["self_authored_planning_excluded"]:
        raise AssertionError("external review ledger must exclude self-authored planning issues")
    required_types = {item["evidence_type"] for item in payload["evidence_requirements"]}
    for required in {"demo_feedback", "confirmed_run", "business_case_review", "reproducible_bug"}:
        if required not in required_types:
            raise AssertionError(f"external review ledger missing evidence type {required}")
    counts = payload["public_counts"]
    for key in (
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
    ):
        if counts[key] != expected[key]:
            raise AssertionError(f"external review ledger must preserve zero {key}")
    evidence_counts = payload["evidence_counts"]
    for key in (
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
    ):
        if evidence_counts[key] > counts[key]:
            raise AssertionError(f"evidence ledger cannot count more {key} entries than feedback metrics")
    if payload["review_status_counts"]["not_contacted"] != 3:
        raise AssertionError("external review ledger must preserve the three not-contacted pilot reviews")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"external review ledger must not claim {required}")
    return {"external_review_evidence_ledger_verified": True, "entry_count": payload["entry_count"], **expected}


def main() -> None:
    payload = build_external_review_evidence_ledger()
    verify_external_review_evidence_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
