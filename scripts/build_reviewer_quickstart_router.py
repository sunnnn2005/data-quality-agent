import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-quickstart-router.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-quickstart-router.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_quickstart_router() -> dict[str, Any]:
    hub = load_json(SUBMISSION_HUB_PATH)
    queue = load_json(SEND_QUEUE_PATH)
    path_by_id = {path["id"]: path for path in hub["submission_paths"]}
    queue_by_metric = {item["target_metric"]: item for item in queue["next_sends"]}

    routes = [
        {
            "id": "five_minute_demo_feedback",
            "label": "I only have 5 minutes",
            "best_for": "A peer, recruiter, or classmate who can open the public demo and leave one specific note.",
            "submission_path_id": "try_public_demo",
            "target_metric": "external_feedback_items",
            "review_path": path_by_id["try_public_demo"]["review_path"],
            "submission_url": path_by_id["try_public_demo"]["submission_url"],
            "evidence_to_collect": [
                "exact demo path opened",
                "one useful or confusing workflow detail",
                "permission sentence if the reviewer allows the evidence to count",
            ],
            "resume_claim_unlocked_after_acceptance": "after acceptance: external feedback from a non-owner reviewer",
        },
        {
            "id": "eight_minute_confirmed_use",
            "label": "I can confirm I tried it",
            "best_for": "Someone who can open the demo or quickstart and confirm the observed result.",
            "submission_path_id": "confirm_external_run",
            "target_metric": "confirmed_external_users",
            "review_path": path_by_id["confirm_external_run"]["review_path"],
            "submission_url": path_by_id["confirm_external_run"]["submission_url"],
            "evidence_to_collect": [
                "command or URL used",
                "observed result",
                "environment",
                "permission sentence if the reviewer allows the evidence to count",
            ],
            "resume_claim_unlocked_after_acceptance": "after acceptance: confirmed external user or reviewer run",
        },
        {
            "id": "ten_minute_replay",
            "label": "I can run the project",
            "best_for": "A developer who can run Docker, the API, or a sanitized replay path.",
            "submission_path_id": "submit_reproducible_issue",
            "target_metric": "reproducible_feedback_items",
            "review_path": path_by_id["submit_reproducible_issue"]["review_path"],
            "submission_url": path_by_id["submit_reproducible_issue"]["submission_url"],
            "evidence_to_collect": [
                "endpoint or command used",
                "dataset shape without raw rows",
                "report status and finding count",
                "selected tools shown in the trace",
            ],
            "resume_claim_unlocked_after_acceptance": "after acceptance: reproducible external run evidence",
        },
        {
            "id": "ai_engineer_review",
            "label": "I can review the agent architecture",
            "best_for": "An AI/ML engineer, mentor, or advanced student who can inspect the tool-calling loop.",
            "submission_path_id": "submit_ai_engineer_review",
            "target_metric": "ai_engineer_review_items",
            "review_path": path_by_id["submit_ai_engineer_review"]["review_path"],
            "submission_url": path_by_id["submit_ai_engineer_review"]["submission_url"],
            "evidence_to_collect": [
                "implementation paths inspected",
                "strongest AI-agent signal",
                "least credible gap",
                "permission sentence if the reviewer allows the evidence to count",
            ],
            "resume_claim_unlocked_after_acceptance": "after acceptance: external AI Engineer project review",
        },
        {
            "id": "business_case_review",
            "label": "I can describe a real messy-data problem",
            "best_for": "A data analyst, operator, or student who has seen messy spreadsheet, ticket, sales, or ops data.",
            "submission_path_id": "submit_business_case",
            "target_metric": "business_case_feedback_items",
            "review_path": path_by_id["submit_business_case"]["review_path"],
            "submission_url": path_by_id["submit_business_case"]["submission_url"],
            "evidence_to_collect": [
                "anonymized workflow",
                "data-quality problem",
                "business impact",
                "permission sentence if the reviewer allows the evidence to count",
            ],
            "resume_claim_unlocked_after_acceptance": "after acceptance: business-case feedback tied to a real workflow",
        },
    ]

    prioritized_next_send = queue["next_sends"][0]
    zero_counts = {
        metric: status["current_count"]
        for metric, status in hub["tracked_outcome_status"].items()
        if metric in {route["target_metric"] for route in routes}
    }

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_quickstart_router.py",
        "purpose": (
            "Route external reviewers to the shortest evidence path for their available time and background, "
            "so public feedback can become resume-countable only after the evidence gate accepts it."
        ),
        "route_count": len(routes),
        "routes": routes,
        "prioritized_next_send": {
            "slot_id": prioritized_next_send["slot_id"],
            "target_metric": prioritized_next_send["target_metric"],
            "reviewer_profile": prioritized_next_send["reviewer_profile"],
            "public_issue": prioritized_next_send["public_issue_url"],
            "submission_url": prioritized_next_send["submission_url"],
        },
        "current_zero_counts": zero_counts,
        "manual_counting_rule": (
            "Do not increase any outcome metric until a non-owner public GitHub issue includes permission, "
            "contains no private data, and passes the external reviewer evidence gate."
        ),
        "resume_safe_summary": (
            "Published a reviewer quickstart router with 5 evidence paths mapped to feedback, confirmed-use, "
            "reproducible-run, AI-review, and business-case outcome metrics while preserving zero current claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    route_rows = "\n".join(
        "| {label} | `{target_metric}` | {best_for} | [Review]({review_path}) | [Submit]({submission_url}) |".format(
            **route
        )
        for route in payload["routes"]
    )
    evidence_sections = "\n\n".join(
        "### {label}\n\n".format(**route)
        + "\n".join(f"- {item}" for item in route["evidence_to_collect"])
        + f"\n\nUnlocks after acceptance: {route['resume_claim_unlocked_after_acceptance']}."
        for route in payload["routes"]
    )
    zero_rows = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in sorted(payload["current_zero_counts"].items())
    )
    next_send = payload["prioritized_next_send"]
    return f"""# Reviewer Quickstart Router

This generated router helps a reviewer choose the shortest public evidence path.

## Purpose

{payload["purpose"]}

## Choose a Path

| Reviewer Situation | Target Metric | Best For | Review | Submit Evidence |
| --- | --- | --- | --- | --- |
{route_rows}

## Evidence to Collect

{evidence_sections}

## First Manual Send

- Slot: `{next_send["slot_id"]}`
- Target metric: `{next_send["target_metric"]}`
- Reviewer profile: {next_send["reviewer_profile"]}
- Public issue: [{next_send["public_issue"]}]({next_send["public_issue"]})
- Submission URL: [{next_send["submission_url"]}]({next_send["submission_url"]})

## Current Zero Counts

| Metric | Current Count |
| --- | ---: |
{zero_rows}

## Manual Counting Rule

{payload["manual_counting_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_reviewer_quickstart_router(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["route_count"] != 5:
        raise AssertionError("reviewer quickstart router must expose five route choices")
    required_metrics = {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "ai_engineer_review_items",
        "business_case_feedback_items",
    }
    actual_metrics = {route["target_metric"] for route in payload["routes"]}
    if actual_metrics != required_metrics:
        raise AssertionError("reviewer quickstart router must cover the five human-review outcome metrics")
    for route in payload["routes"]:
        if not route["review_path"].startswith("https://"):
            raise AssertionError("review routes must be public URLs")
        if not route["submission_url"].startswith("https://github.com/"):
            raise AssertionError("submission URLs must use public GitHub evidence surfaces")
        if len(route["evidence_to_collect"]) < 3:
            raise AssertionError("each route must define at least three evidence fields")
        if "after acceptance" not in route["resume_claim_unlocked_after_acceptance"]:
            raise AssertionError("each route must avoid immediate resume outcome claims")
    if any(count != 0 for count in payload["current_zero_counts"].values()):
        raise AssertionError("quickstart router must preserve zero outcome counts until external evidence exists")
    if payload["prioritized_next_send"]["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first manual send should prioritize AI Engineer review evidence")
    if "non-owner public GitHub issue" not in payload["manual_counting_rule"]:
        raise AssertionError("manual counting rule must require non-owner public evidence")
    return {
        "reviewer_quickstart_router_verified": True,
        "route_count": payload["route_count"],
        "zero_metric_count": len(payload["current_zero_counts"]),
        "prioritized_next_metric": payload["prioritized_next_send"]["target_metric"],
    }


def main() -> None:
    payload = build_reviewer_quickstart_router()
    verify_reviewer_quickstart_router(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
