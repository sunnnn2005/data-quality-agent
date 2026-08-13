import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
REVIEWER_ACTION_QUEUE_PATH = ROOT / "docs" / "reviewer-action-queue.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-reviewer-call.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-reviewer-call.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_reviewer_call() -> dict[str, Any]:
    hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    queue = load_json(REVIEWER_ACTION_QUEUE_PATH)
    outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)
    repo = "https://github.com/sunnnn2005/data-quality-agent"
    call_issue = f"{repo}/issues/19"
    reviewer_segments = [
        {
            "id": "technical_reviewer",
            "who": "AI Engineer, SWE, or data engineer reviewer",
            "ask": "Run or inspect one technical path and leave implementation feedback.",
            "submit_to": next(path["submission_url"] for path in hub["submission_paths"] if path["id"] == "submit_ai_engineer_review"),
            "counts_toward": "ai_engineer_review_items",
        },
        {
            "id": "business_data_reviewer",
            "who": "Data analyst, operations teammate, or student with a messy CSV workflow",
            "ask": "Submit an anonymized data-quality problem and whether this agent would help triage it.",
            "submit_to": next(path["submission_url"] for path in hub["submission_paths"] if path["id"] == "submit_business_case"),
            "counts_toward": "business_case_feedback_items",
        },
        {
            "id": "quick_demo_reviewer",
            "who": "Student, recruiter, or open-source reviewer with 5 minutes",
            "ask": "Open the public demo or quickstart and leave one concrete useful/confusing/broken observation.",
            "submit_to": next(path["submission_url"] for path in hub["submission_paths"] if path["id"] == "try_public_demo"),
            "counts_toward": "external_feedback_items",
        },
    ]
    current_counts = {
        item["metric"]: item["current_count"]
        for item in outcome_metrics["tracked_outcomes"]
        if item["metric"]
        in {
            "confirmed_external_users",
            "external_feedback_items",
            "business_case_feedback_items",
            "ai_engineer_review_items",
            "github_stars",
        }
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_reviewer_call.py",
        "public_call_issue": call_issue,
        "purpose": (
            "Publish one public call for external reviewers and pilot users so future resume outcome claims "
            "can be backed by non-owner GitHub evidence instead of private messages or self-authored notes."
        ),
        "reviewer_segment_count": len(reviewer_segments),
        "reviewer_segments": reviewer_segments,
        "linked_submission_paths": hub["submission_path_count"],
        "linked_outreach_tasks": queue["queue_count"],
        "minimum_review_minutes": min(path["minimum_minutes"] for path in hub["submission_paths"]),
        "max_review_minutes": max(path["minimum_minutes"] for path in hub["submission_paths"]),
        "required_public_evidence_fields": hub["total_required_evidence_fields"],
        "current_counts": current_counts,
        "counting_rules": [
            "Counts only public, non-owner GitHub issues that pass the external evidence gate.",
            "Does not count private DMs, self-authored planning issues, or vague reactions.",
            "Does not ask for raw customer data, secrets, production rows, or fake GitHub engagement.",
            "Keeps all user, feedback, business-impact, AI-review, and star claims blocked while counts are zero.",
        ],
        "resume_status": "public_call_open_not_claimable",
        "resume_safe_summary": (
            "Published a public reviewer call linked to 3 reviewer segments, 6 submission paths, "
            "8 outreach tasks, and 23 evidence fields while keeping current outcome counts at zero."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    segment_rows = "\n".join(
        "| {who} | {ask} | `{counts_toward}` | [Submit evidence]({submit_to}) |".format(**segment)
        for segment in payload["reviewer_segments"]
    )
    counts = "\n".join(f"| {key} | {value} |" for key, value in payload["current_counts"].items())
    rules = "\n".join(f"- {rule}" for rule in payload["counting_rules"])
    return f"""# Public Reviewer Call

This generated call is the public entry point for collecting real reviewer and pilot evidence.

## Purpose

{payload["purpose"]}

## Public Call Issue

[{payload["public_call_issue"]}]({payload["public_call_issue"]})

## Reviewer Segments

| Reviewer | Ask | Counts Toward | Submission |
| --- | --- | --- | --- |
{segment_rows}

## Evidence Scope

| Metric | Value |
| --- | ---: |
| Reviewer segments | {payload["reviewer_segment_count"]} |
| Linked submission paths | {payload["linked_submission_paths"]} |
| Linked outreach tasks | {payload["linked_outreach_tasks"]} |
| Minimum review minutes | {payload["minimum_review_minutes"]} |
| Maximum review minutes | {payload["max_review_minutes"]} |
| Required public evidence fields | {payload["required_public_evidence_fields"]} |

## Current Counts

| Outcome | Current Count |
| --- | ---: |
{counts}

## Counting Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_public_reviewer_call(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["reviewer_segment_count"] != 3:
        raise AssertionError("public reviewer call must target three reviewer segments")
    if payload["linked_submission_paths"] != 6:
        raise AssertionError("public reviewer call must link the six submission paths")
    if payload["linked_outreach_tasks"] != 8:
        raise AssertionError("public reviewer call must link the eight outreach tasks")
    if payload["required_public_evidence_fields"] != 23:
        raise AssertionError("public reviewer call must preserve the 23 evidence fields")
    if payload["resume_status"] != "public_call_open_not_claimable":
        raise AssertionError("public reviewer call must not be claimable as usage evidence")
    if not payload["public_call_issue"].endswith("/issues/19"):
        raise AssertionError("public reviewer call must point to the public call issue")
    expected_segments = {"technical_reviewer", "business_data_reviewer", "quick_demo_reviewer"}
    if {segment["id"] for segment in payload["reviewer_segments"]} != expected_segments:
        raise AssertionError("public reviewer call must define the expected reviewer segments")
    for segment in payload["reviewer_segments"]:
        if not segment["submit_to"].startswith("https://github.com/sunnnn2005/data-quality-agent/issues/new"):
            raise AssertionError("public reviewer call submissions must use public GitHub issue forms")
        if not segment["counts_toward"].endswith("_items"):
            raise AssertionError("public reviewer call segments must map to tracked outcome item metrics")
    for key, value in payload["current_counts"].items():
        if value != 0:
            raise AssertionError(f"{key} must remain zero until accepted public evidence exists")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("non-owner github evidence", "does not count private dms", "fake github engagement", "blocked while counts are zero"):
        if required not in joined:
            raise AssertionError(f"public reviewer call missing counting boundary: {required}")
    return {
        "public_reviewer_call_verified": True,
        "reviewer_segment_count": payload["reviewer_segment_count"],
        "linked_submission_paths": payload["linked_submission_paths"],
        "linked_outreach_tasks": payload["linked_outreach_tasks"],
        "required_public_evidence_fields": payload["required_public_evidence_fields"],
    }


def main() -> None:
    payload = build_public_reviewer_call()
    verify_public_reviewer_call(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
